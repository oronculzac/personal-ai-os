"""
GitHub Publisher - Automated publishing to GitHub repositories

This module handles:
1. Repository routing based on content type
2. Smart commit message generation
3. Git operations (add, commit, push)
4. Dry-run mode for preview
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TargetRepo(Enum):
    PERSONAL_AI_OS = "personal-ai-os"
    DE_ZOOMCAMP = "de-zoomcamp-2026"
    LEARNING_LOGS = "learning-logs"


@dataclass
class PublishConfig:
    """Configuration for GitHub publishing."""
    username: str
    repos: Dict[str, str]  # repo_name -> local_path
    default_branch: str = "main"
    auto_push: bool = False


@dataclass
class PublishResult:
    success: bool
    repo: str
    files_committed: List[str]
    commit_message: str
    commit_hash: Optional[str]
    error: Optional[str]


def load_config(config_path: Path = None) -> Optional[PublishConfig]:
    """Load GitHub configuration from mcp_config.json."""
    if config_path is None:
        config_path = Path(".agent/config/mcp_config.json")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        github_config = config.get("github", {})
        if not github_config:
            return None
        
        return PublishConfig(
            username=github_config.get("username", ""),
            repos=github_config.get("repos", {}),
            default_branch=github_config.get("default_branch", "main"),
            auto_push=github_config.get("auto_push", False)
        )
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def generate_commit_message(content_type: str, description: str = None) -> str:
    """Generate a conventional commit message based on content type."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    prefixes = {
        "skill": "feat",
        "homework": "feat",
        "side_quest": "docs",
        "learning_log": "docs",
        "workflow": "feat",
        "manual": "chore"
    }
    
    prefix = prefixes.get(content_type, "chore")
    
    if content_type == "skill":
        return f"{prefix}: Add {description or 'new skill'}"
    elif content_type == "homework":
        return f"{prefix}: Complete {description or 'homework'}"
    elif content_type in ("side_quest", "learning_log"):
        return f"{prefix}: Session log {date_str} - {description or 'learning session'}"
    elif content_type == "workflow":
        return f"{prefix}: Add {description or 'workflow'}"
    else:
        return f"{prefix}: Update {description or 'files'}"


def get_git_status(repo_path: Path) -> Tuple[List[str], List[str], List[str]]:
    """
    Get git status for a repository.
    Returns: (staged, modified, untracked)
    """
    try:
        os.chdir(repo_path)
        
        # Staged files
        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip().split('\n')
        staged = [f for f in staged if f]
        
        # Modified files
        modified = subprocess.check_output(
            ["git", "diff", "--name-only"],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip().split('\n')
        modified = [f for f in modified if f]
        
        # Untracked files
        untracked = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip().split('\n')
        untracked = [f for f in untracked if f]
        
        return staged, modified, untracked
    except subprocess.CalledProcessError as e:
        return [], [], []


def copy_files_to_repo(
    source_files: List[Path],
    target_repo: Path,
    target_subdir: str = ""
) -> List[str]:
    """
    Copy files from source to target repository.
    Returns list of files copied (relative to repo root).
    """
    import shutil
    
    copied = []
    target_dir = target_repo / target_subdir if target_subdir else target_repo
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for source in source_files:
        if source.is_file():
            dest = target_dir / source.name
            shutil.copy2(source, dest)
            rel_path = str(dest.relative_to(target_repo))
            copied.append(rel_path)
        elif source.is_dir():
            dest = target_dir / source.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(source, dest)
            # Add all files in directory
            for f in dest.rglob("*"):
                if f.is_file():
                    copied.append(str(f.relative_to(target_repo)))
    
    return copied


def git_add_commit_push(
    repo_path: Path,
    files: List[str],
    commit_message: str,
    push: bool = False,
    branch: str = "main"
) -> PublishResult:
    """
    Stage, commit, and optionally push files.
    """
    original_dir = os.getcwd()
    
    try:
        os.chdir(repo_path)
        
        # Stage files
        for f in files:
            subprocess.run(["git", "add", f], check=True, capture_output=True)
        
        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                return PublishResult(
                    success=False,
                    repo=str(repo_path),
                    files_committed=[],
                    commit_message=commit_message,
                    commit_hash=None,
                    error="Nothing to commit - files may already be up to date"
                )
            return PublishResult(
                success=False,
                repo=str(repo_path),
                files_committed=files,
                commit_message=commit_message,
                commit_hash=None,
                error=result.stderr
            )
        
        # Get commit hash
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True
        ).strip()[:7]
        
        # Push if requested
        if push:
            push_result = subprocess.run(
                ["git", "push", "origin", branch],
                capture_output=True,
                text=True
            )
            if push_result.returncode != 0:
                return PublishResult(
                    success=False,
                    repo=str(repo_path),
                    files_committed=files,
                    commit_message=commit_message,
                    commit_hash=commit_hash,
                    error=f"Push failed: {push_result.stderr}"
                )
        
        return PublishResult(
            success=True,
            repo=str(repo_path),
            files_committed=files,
            commit_message=commit_message,
            commit_hash=commit_hash,
            error=None
        )
        
    except subprocess.CalledProcessError as e:
        return PublishResult(
            success=False,
            repo=str(repo_path),
            files_committed=[],
            commit_message=commit_message,
            commit_hash=None,
            error=str(e)
        )
    finally:
        os.chdir(original_dir)


def publish_to_github(
    target_repo: TargetRepo,
    files: List[Path],
    content_type: str,
    description: str = None,
    subdirectory: str = None,
    dry_run: bool = True,
    auto_push: bool = False
) -> PublishResult:
    """
    Main function to publish content to GitHub.
    
    Args:
        target_repo: Which repository to publish to
        files: List of file paths to publish
        content_type: Type of content (skill, homework, learning_log, etc.)
        description: Optional description for commit message
        subdirectory: Optional subdirectory within repo
        dry_run: If True, preview without making changes
        auto_push: If True, push to remote after commit
    
    Returns:
        PublishResult with details of the operation
    """
    config = load_config()
    
    if not config:
        return PublishResult(
            success=False,
            repo=target_repo.value,
            files_committed=[],
            commit_message="",
            commit_hash=None,
            error="No GitHub configuration found. Add 'github' section to mcp_config.json"
        )
    
    repo_path_str = config.repos.get(target_repo.value)
    if not repo_path_str:
        return PublishResult(
            success=False,
            repo=target_repo.value,
            files_committed=[],
            commit_message="",
            commit_hash=None,
            error=f"No local path configured for {target_repo.value}"
        )
    
    repo_path = Path(repo_path_str)
    if not repo_path.exists():
        return PublishResult(
            success=False,
            repo=target_repo.value,
            files_committed=[],
            commit_message="",
            commit_hash=None,
            error=f"Repository path does not exist: {repo_path}"
        )
    
    # Generate commit message
    commit_message = generate_commit_message(content_type, description)
    
    # Determine subdirectory based on content type
    if subdirectory is None:
        subdirectory_map = {
            "skill": ".agent/skills",
            "homework": "homework",
            "learning_log": "sessions",
            "side_quest": "sessions",
            "workflow": ".agent/workflows"
        }
        subdirectory = subdirectory_map.get(content_type, "")
    
    if dry_run:
        return PublishResult(
            success=True,
            repo=str(repo_path),
            files_committed=[str(f) for f in files],
            commit_message=commit_message,
            commit_hash="[DRY-RUN]",
            error=None
        )
    
    # Copy files to repo
    copied_files = copy_files_to_repo(files, repo_path, subdirectory)
    
    if not copied_files:
        return PublishResult(
            success=False,
            repo=str(repo_path),
            files_committed=[],
            commit_message=commit_message,
            commit_hash=None,
            error="No files were copied to the repository"
        )
    
    # Commit (and optionally push)
    return git_add_commit_push(
        repo_path,
        copied_files,
        commit_message,
        push=auto_push or config.auto_push,
        branch=config.default_branch
    )


def format_result(result: PublishResult) -> str:
    """Format publish result for display."""
    if result.success:
        lines = [
            "✅ PUBLISH SUCCESSFUL",
            "=" * 40,
            f"📁 Repository: {result.repo}",
            f"📝 Commit: {result.commit_hash}",
            f"💬 Message: {result.commit_message}",
            "",
            "📄 Files:"
        ]
        for f in result.files_committed[:10]:
            lines.append(f"   • {f}")
        if len(result.files_committed) > 10:
            lines.append(f"   ... and {len(result.files_committed) - 10} more")
    else:
        lines = [
            "❌ PUBLISH FAILED",
            "=" * 40,
            f"📁 Repository: {result.repo}",
            f"❗ Error: {result.error}"
        ]
    
    return "\n".join(lines)


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Publish content to GitHub")
    parser.add_argument("files", nargs="*", help="Files or directories to publish")
    parser.add_argument("--repo", choices=["personal-ai-os", "de-zoomcamp-2026", "learning-logs"],
                       default="learning-logs", help="Target repository")
    parser.add_argument("--type", choices=["skill", "homework", "learning_log", "workflow"],
                       default="learning_log", help="Content type")
    parser.add_argument("--description", "-d", help="Description for commit message")
    parser.add_argument("--subdir", help="Subdirectory within repo")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview without changes")
    parser.add_argument("--execute", action="store_true", help="Actually make changes (disables dry-run)")
    parser.add_argument("--push", action="store_true", help="Push to remote after commit")
    
    args = parser.parse_args()
    
    if not args.files:
        print("No files specified. Use --help for usage.")
        exit(1)
    
    files = [Path(f) for f in args.files]
    target = TargetRepo(args.repo)
    
    result = publish_to_github(
        target_repo=target,
        files=files,
        content_type=args.type,
        description=args.description,
        subdirectory=args.subdir,
        dry_run=not args.execute,
        auto_push=args.push
    )
    
    print(format_result(result))
