"""
Publish Detector - Determines if session content is GitHub-worthy

This module analyzes session context and determines:
1. Whether the content should be published
2. Which repository it should go to
3. The content type (skill, homework, learning-log)
"""

import re
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ContentType(Enum):
    SKILL = "skill"
    HOMEWORK = "homework"
    SIDE_QUEST = "side_quest"
    LEARNING_LOG = "learning_log"
    WORKFLOW = "workflow"
    MANUAL = "manual"


class TargetRepo(Enum):
    PERSONAL_AI_OS = "personal-ai-os"
    DE_ZOOMCAMP = "de-zoomcamp-2026"
    LEARNING_LOGS = "learning-logs"


@dataclass
class PublishDecision:
    should_publish: bool
    content_type: Optional[ContentType]
    target_repo: Optional[TargetRepo]
    reason: str
    confidence: float  # 0.0 to 1.0


# Keywords that indicate different content types
SKILL_INDICATORS = ["skill.md", "skills/", "__init__.py", "scripts/"]
HOMEWORK_INDICATORS = ["homework", "exercise", "solution", "answer", "submission"]
DE_ZOOMCAMP_INDICATORS = ["zoomcamp", "module-", "bigquery", "spark", "dbt", "terraform", "docker", "airflow"]
SIDE_QUEST_KEYWORDS = ["config", "setup", "tool", "automation", "script", "util"]


def extract_modified_files(git_diff_stat: str) -> List[str]:
    """Extract list of modified files from git diff --stat output."""
    files = []
    for line in git_diff_stat.split('\n'):
        # Match lines like: " path/to/file.py | 10 +++---"
        match = re.match(r'^\s*(.+?)\s*\|', line)
        if match:
            files.append(match.group(1).strip())
    return files


def count_modified_files(git_diff_stat: str) -> int:
    """Count number of files modified from git diff --stat output."""
    return len(extract_modified_files(git_diff_stat))


def extract_ticket_keywords(tickets: List[Dict]) -> List[str]:
    """Extract keywords from Linear ticket titles."""
    keywords = []
    for ticket in tickets:
        title = ticket.get("title", "").lower()
        # Split on common separators and filter short words
        words = re.split(r'[\s\-_:,]+', title)
        keywords.extend([w for w in words if len(w) > 3])
    return list(set(keywords))


def detect_side_quest(modified_files: List[str], ticket_keywords: List[str]) -> Tuple[bool, str]:
    """
    Detect if work drifted from the main Linear ticket scope.
    
    Returns: (is_side_quest, reason)
    """
    if not ticket_keywords:
        return False, "No tickets to compare against"
    
    unrelated_files = []
    for file in modified_files:
        file_lower = file.lower()
        # Check if any ticket keyword appears in the file path
        if not any(kw in file_lower for kw in ticket_keywords):
            # Check if it's not a common config/meta file
            if not any(meta in file_lower for meta in ['.gitignore', 'readme', 'license', '.env']):
                unrelated_files.append(file)
    
    # If more than 30% of files are unrelated, it's a side quest
    if len(unrelated_files) > 0 and len(unrelated_files) / len(modified_files) > 0.3:
        return True, f"Files unrelated to ticket: {', '.join(unrelated_files[:3])}"
    
    return False, "Work aligned with ticket scope"


def detect_skill_creation(modified_files: List[str]) -> Tuple[bool, str]:
    """Detect if a new skill was created."""
    skill_files = [f for f in modified_files if "skill" in f.lower() and f.endswith(".md")]
    script_files = [f for f in modified_files if "/scripts/" in f.lower() and f.endswith(".py")]
    
    if skill_files and script_files:
        return True, f"New skill detected: {skill_files[0]}"
    return False, ""


def detect_homework(modified_files: List[str], commit_messages: str) -> Tuple[bool, str]:
    """Detect if homework was completed."""
    # Check file paths
    for file in modified_files:
        if any(hw in file.lower() for hw in HOMEWORK_INDICATORS):
            return True, f"Homework file modified: {file}"
    
    # Check commit messages
    if any(hw in commit_messages.lower() for hw in HOMEWORK_INDICATORS):
        return True, "Homework mentioned in commit"
    
    return False, ""


def detect_de_zoomcamp_content(modified_files: List[str], commit_messages: str) -> bool:
    """Check if content is related to DE Zoomcamp."""
    all_text = " ".join(modified_files).lower() + " " + commit_messages.lower()
    return any(indicator in all_text for indicator in DE_ZOOMCAMP_INDICATORS)


def analyze_session(context: Dict[str, Any]) -> PublishDecision:
    """
    Main function to analyze session context and determine publish-worthiness.
    
    Args:
        context: Dict containing 'git', 'linear', and optional 'force_publish' keys
    
    Returns:
        PublishDecision with recommendation
    """
    git_data = context.get("git", {})
    linear_data = context.get("linear", {})
    force_publish = context.get("force_publish", False)
    force_target = context.get("target_repo")
    
    # Handle errors
    if "error" in git_data:
        return PublishDecision(
            should_publish=False,
            content_type=None,
            target_repo=None,
            reason=f"Git error: {git_data['error']}",
            confidence=1.0
        )
    
    # Extract data
    diff_stat = git_data.get("diff_stat", "")
    commit_log = git_data.get("recent_commits", "")
    tickets = linear_data.get("tickets", [])
    
    modified_files = extract_modified_files(diff_stat)
    file_count = len(modified_files)
    ticket_keywords = extract_ticket_keywords(tickets)
    
    # Rule 0: Forced publish
    if force_publish and force_target:
        return PublishDecision(
            should_publish=True,
            content_type=ContentType.MANUAL,
            target_repo=TargetRepo(force_target) if force_target in [r.value for r in TargetRepo] else TargetRepo.LEARNING_LOGS,
            reason="Manually flagged for publish",
            confidence=1.0
        )
    
    # Rule 1: New skill created → personal-ai-os
    is_skill, skill_reason = detect_skill_creation(modified_files)
    if is_skill:
        return PublishDecision(
            should_publish=True,
            content_type=ContentType.SKILL,
            target_repo=TargetRepo.PERSONAL_AI_OS,
            reason=skill_reason,
            confidence=0.9
        )
    
    # Rule 2: Homework completed → de-zoomcamp-2026
    is_homework, homework_reason = detect_homework(modified_files, commit_log)
    if is_homework:
        return PublishDecision(
            should_publish=True,
            content_type=ContentType.HOMEWORK,
            target_repo=TargetRepo.DE_ZOOMCAMP,
            reason=homework_reason,
            confidence=0.85
        )
    
    # Rule 3: Side Quest detected → learning-logs
    is_side_quest, sq_reason = detect_side_quest(modified_files, ticket_keywords)
    if is_side_quest:
        return PublishDecision(
            should_publish=True,
            content_type=ContentType.SIDE_QUEST,
            target_repo=TargetRepo.LEARNING_LOGS,
            reason=sq_reason,
            confidence=0.7
        )
    
    # Rule 4: Significant code changes (≥3 files) → learning-logs
    if file_count >= 3:
        # Determine if it's DE Zoomcamp related
        is_de = detect_de_zoomcamp_content(modified_files, commit_log)
        return PublishDecision(
            should_publish=True,
            content_type=ContentType.LEARNING_LOG,
            target_repo=TargetRepo.DE_ZOOMCAMP if is_de else TargetRepo.LEARNING_LOGS,
            reason=f"Significant session: {file_count} files modified",
            confidence=0.6
        )
    
    # Default: Don't publish
    return PublishDecision(
        should_publish=False,
        content_type=None,
        target_repo=None,
        reason=f"Session not significant enough ({file_count} files modified)",
        confidence=0.8
    )


def format_decision(decision: PublishDecision) -> str:
    """Format the decision for display."""
    if decision.should_publish:
        return f"""
📢 PUBLISH RECOMMENDATION
========================
✅ Should Publish: Yes
📁 Target Repo: {decision.target_repo.value if decision.target_repo else 'N/A'}
📝 Content Type: {decision.content_type.value if decision.content_type else 'N/A'}
💡 Reason: {decision.reason}
🎯 Confidence: {decision.confidence:.0%}
"""
    else:
        return f"""
📢 PUBLISH RECOMMENDATION
========================
❌ Should Publish: No
💡 Reason: {decision.reason}
🎯 Confidence: {decision.confidence:.0%}
"""


# CLI interface
if __name__ == "__main__":
    import sys
    import json
    
    # Example usage - can be called standalone or imported
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test with sample data
        test_context = {
            "git": {
                "diff_stat": """
 .agent/skills/session_wrapper/scripts/collect_context.py | 10 ++++---
 .agent/skills/session_wrapper/scripts/publish_detector.py | 150 ++++++++++++
 .agent/skills/session_wrapper/SKILL.md | 5 ++--
 README.md | 2 ++
""",
                "recent_commits": "abc123 Add publish detector\ndef456 Update session wrapper"
            },
            "linear": {
                "tickets": [
                    {"title": "Implement Session Wrapper skill", "state": {"name": "In Progress"}}
                ]
            }
        }
        
        decision = analyze_session(test_context)
        print(format_decision(decision))
    else:
        # Read context from stdin (piped from collect_context.py)
        try:
            context = json.load(sys.stdin)
            decision = analyze_session(context)
            print(format_decision(decision))
            
            # Also output as JSON for piping
            print("\n--- JSON Output ---")
            print(json.dumps({
                "should_publish": decision.should_publish,
                "content_type": decision.content_type.value if decision.content_type else None,
                "target_repo": decision.target_repo.value if decision.target_repo else None,
                "reason": decision.reason,
                "confidence": decision.confidence
            }, indent=2))
        except json.JSONDecodeError:
            print("Error: No valid JSON input. Run with --test for demo.")
