#!/usr/bin/env python3
"""
Workflow Runner

Executes markdown workflows with step-level status, retries, and logging.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import uuid4

try:
    from .logger import get_logger, get_logs_dir
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from logger import get_logger, get_logs_dir


RUN_STATE_DIR = Path(".agent") / "state" / "workflow_runs"
WORKFLOW_GLOB = Path(".agent") / "workflows" / "*.md"


@dataclass
class StepConfig:
    retries: int = 0
    timeout_s: Optional[int] = None
    on_fail: str = "stop"


@dataclass
class Step:
    title: str
    step_id: str
    commands: List[Dict[str, str]] = field(default_factory=list)
    config: StepConfig = field(default_factory=StepConfig)


@dataclass
class Workflow:
    workflow_id: str
    description: Optional[str]
    path: Path
    steps: List[Step]


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "step"


def _parse_frontmatter(lines: List[str]) -> Dict[str, str]:
    if not lines or lines[0].strip() != "---":
        return {}
    frontmatter = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def _parse_step_config(lines: List[str]) -> Dict[str, Any]:
    config = StepConfig()
    override_id = None
    config_lines = []
    in_runner_block = False
    for line in lines:
        stripped = line.strip()
        if stripped == "// runner":
            in_runner_block = True
            continue
        if in_runner_block:
            if not stripped.startswith("//"):
                break
            config_lines.append(stripped.lstrip("//").strip())
    for entry in config_lines:
        if not entry:
            continue
        if ":" not in entry:
            continue
        key, value = [part.strip() for part in entry.split(":", 1)]
        if key == "id":
            if value:
                override_id = _slugify(value)
        elif key == "retries":
            try:
                config.retries = max(0, int(value))
            except ValueError:
                pass
        elif key == "timeout_s":
            try:
                config.timeout_s = max(1, int(value))
            except ValueError:
                pass
        elif key == "on_fail":
            if value in {"stop", "continue"}:
                config.on_fail = value
    return {"config": config, "override_id": override_id}


def _parse_workflow(path: Path) -> Workflow:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    frontmatter = _parse_frontmatter(lines)
    workflow_id = frontmatter.get("id", path.stem)
    description = frontmatter.get("description")

    steps: List[Step] = []
    in_steps = False
    current_step: Optional[Step] = None
    step_buffer: List[str] = []
    in_code_block = False
    code_lang = ""
    code_lines: List[str] = []

    for line in lines:
        if line.startswith("## ") and line.strip().lower() == "## steps":
            in_steps = True
            continue
        if line.startswith("## ") and line.strip().lower() != "## steps":
            in_steps = False
            continue

        if not in_steps:
            continue

        if line.startswith("### "):
            if current_step:
                parsed = _parse_step_config(step_buffer)
                current_step.config = parsed["config"]
                if parsed["override_id"]:
                    current_step.step_id = parsed["override_id"]
                steps.append(current_step)
            title = line[4:].strip()
            current_step = Step(title=title, step_id=_slugify(title))
            step_buffer = []
            continue

        if current_step is None:
            continue

        step_buffer.append(line)

        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = line.strip("`").strip().lower()
                code_lines = []
            else:
                in_code_block = False
                if code_lang in {"powershell", "bash", "sh"}:
                    current_step.commands.append({
                        "language": code_lang,
                        "command": "\n".join(code_lines).strip(),
                    })
                code_lang = ""
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)

    if current_step:
        parsed = _parse_step_config(step_buffer)
        current_step.config = parsed["config"]
        if parsed["override_id"]:
            current_step.step_id = parsed["override_id"]
        steps.append(current_step)

    return Workflow(workflow_id=workflow_id, description=description, path=path, steps=steps)


def _write_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _load_state(workflow_id: str) -> Dict[str, Any]:
    state_path = RUN_STATE_DIR / f"{workflow_id}.json"
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _save_state(workflow_id: str, state: Dict[str, Any]) -> None:
    RUN_STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path = RUN_STATE_DIR / f"{workflow_id}.json"
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _run_command(command: str, language: str, timeout_s: Optional[int]) -> Dict[str, Any]:
    if language == "powershell":
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command]
    else:
        cmd = ["bash", "-lc", command]

    start = time.time()
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        duration_ms = int((time.time() - start) * 1000)
        return {
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_ms": duration_ms,
        }
    except subprocess.TimeoutExpired as exc:
        duration_ms = int((time.time() - start) * 1000)
        return {
            "exit_code": 124,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "duration_ms": duration_ms,
            "timeout": True,
        }


def _find_workflow(path_or_name: str) -> Path:
    candidate = Path(path_or_name)
    if candidate.exists():
        return candidate
    matches = list(WORKFLOW_GLOB.parent.glob(f"{path_or_name}.md"))
    if matches:
        return matches[0]
    raise FileNotFoundError(f"Workflow not found: {path_or_name}")


def _resolve_step_index(workflow: Workflow, step_selector: str) -> Optional[int]:
    selector_norm = step_selector.strip().lower()
    for idx, step in enumerate(workflow.steps):
        if step.step_id == selector_norm or step.title.lower() == selector_norm:
            return idx
    return None


def run_workflow(
    workflow: Workflow,
    dry_run: bool,
    resume: bool,
    step_selector: Optional[str],
    max_retries: Optional[int],
) -> int:
    logger = get_logger("workflow_runner")
    workflow_run_id = f"{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:6]}"
    logs_dir = get_logs_dir()
    runs_log = logs_dir / "workflow_runs.jsonl"
    steps_log = logs_dir / "workflow_steps.jsonl"

    state = _load_state(workflow.workflow_id)
    start_index = 0
    if resume and state.get("last_completed_index") is not None:
        start_index = int(state["last_completed_index"]) + 1

    if step_selector:
        step_index = _resolve_step_index(workflow, step_selector)
        if step_index is None:
            raise ValueError(f"Unknown step: {step_selector}")
        start_index = step_index

    logger.info(
        "Starting workflow",
        extra={
            "workflow_id": workflow.workflow_id,
            "workflow_run_id": workflow_run_id,
            "step_start_index": start_index,
            "dry_run": dry_run,
        },
    )

    run_summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "workflow_id": workflow.workflow_id,
        "workflow_run_id": workflow_run_id,
        "success": True,
        "steps_total": len(workflow.steps),
        "steps_completed": 0,
    }

    for idx, step in enumerate(workflow.steps):
        if idx < start_index:
            continue
        if step_selector and idx != start_index:
            break

        step_status = "skipped"
        step_start = time.time()
        retries = step.config.retries
        if max_retries is not None:
            retries = max_retries
        attempt = 0

        if dry_run:
            step_status = "skipped"
        else:
            while attempt <= retries:
                attempt += 1
                step_error = None
                for command in step.commands:
                    result = _run_command(
                        command["command"],
                        command["language"],
                        step.config.timeout_s,
                    )
                    if result["exit_code"] != 0:
                        step_error = result.get("stderr") or "Command failed"
                        break
                if step_error is None:
                    step_status = "success"
                    break
                if attempt <= retries:
                    time.sleep(2 ** (attempt - 1))
                else:
                    step_status = "failed"

        duration_ms = int((time.time() - step_start) * 1000)
        step_payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "workflow_id": workflow.workflow_id,
            "workflow_run_id": workflow_run_id,
            "step_id": step.step_id,
            "step_title": step.title,
            "status": step_status,
            "duration_ms": duration_ms,
            "attempts": 0 if dry_run else attempt,
        }
        _write_jsonl(steps_log, step_payload)

        if step_status == "success":
            run_summary["steps_completed"] += 1
            state.update({
                "last_run_id": workflow_run_id,
                "last_completed_index": idx,
                "last_completed_step": step.step_id,
                "updated_at": datetime.utcnow().isoformat() + "Z",
            })
            _save_state(workflow.workflow_id, state)
        elif step_status == "failed" and step.config.on_fail != "continue":
            run_summary["success"] = False
            break

    _write_jsonl(runs_log, run_summary)
    return 0 if run_summary["success"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run markdown workflows")
    parser.add_argument("--workflow", required=True, help="Workflow name or path")
    parser.add_argument("--dry-run", action="store_true", help="List steps only")
    parser.add_argument("--resume", action="store_true", help="Resume last run")
    parser.add_argument("--step", help="Run a single step by id or title")
    parser.add_argument("--max-retries", type=int, help="Override step retries")
    args = parser.parse_args()

    workflow_path = _find_workflow(args.workflow)
    workflow = _parse_workflow(workflow_path)

    if not workflow.steps:
        raise ValueError("No steps found in workflow")

    return run_workflow(
        workflow=workflow,
        dry_run=args.dry_run,
        resume=args.resume,
        step_selector=args.step,
        max_retries=args.max_retries,
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
