---
title: Workflow Runner Spec
version: 0.1
---

# Workflow Runner Spec (v0.1)

## Goals

- Turn markdown workflows into repeatable executions
- Track step-level status, retries, and logs
- Support resume and single-step runs

## CLI

```
python .agent/core/workflow_runner.py --workflow wrap-session
python .agent/core/workflow_runner.py --workflow wrap-session --dry-run
python .agent/core/workflow_runner.py --workflow wrap-session --resume
python .agent/core/workflow_runner.py --workflow wrap-session --step sync_tasks
```

Flags:

- `--workflow <name|path>`
- `--dry-run`
- `--resume`
- `--step <step_id|step_title>`
- `--max-retries <n>`

## Workflow Parsing

- Workflow id comes from frontmatter `id` or file stem
- Steps are `###` headings under the `## Steps` section
- Executable blocks are fenced `powershell`, `bash`, or `sh`

Runner directives live in step text:

```
// runner
// id: sync_tasks
// retries: 2
// timeout_s: 120
// on_fail: stop
```

## Execution Model

- Steps run in order
- Default is to stop on first failure
- Retries use exponential backoff (1s, 2s, 4s)
- Timeout kills the process and marks the step failed

## Logging

JSONL logs written to:

- `.agent/logs/workflow_runs.jsonl`
- `.agent/logs/workflow_steps.jsonl`

Fields include:

- `workflow_id`, `workflow_run_id`
- `step_id`, `step_title`
- `status`, `duration_ms`, `attempts`

## State

Resume state stored in:

- `.agent/state/workflow_runs/<workflow_id>.json`

## Skill Output Contract (v0.1)

Skills should emit a final JSON object on stdout:

```json
{
  "skill": "obsidian_linear_sync",
  "success": true,
  "duration_ms": 1234,
  "error": null,
  "metrics": {
    "created": 3,
    "updated": 5,
    "skipped": 1
  },
  "artifacts": {
    "log_file": ".agent/logs/sync.jsonl",
    "note_path": "vault/Daily/2026-01-22.md"
  }
}
```

Required fields:

- `skill` (string)
- `success` (boolean)
- `duration_ms` (int)
- `error` (string or null)

Exit codes:

- `0` on success
- `1` on failure
- `2` on partial success (if supported)
