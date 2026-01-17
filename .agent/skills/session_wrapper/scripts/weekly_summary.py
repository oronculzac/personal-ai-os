"""
Weekly Summary Generator - Aggregate daily session logs into weekly review

This module:
1. Reads session logs from the past week
2. Aggregates statistics (files modified, commits, tickets completed)
3. Generates a weekly summary for reflection and sharing
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class WeeklySummary:
    """Container for weekly summary data."""
    week_start: str
    week_end: str
    total_sessions: int
    total_files_modified: int
    total_commits: int
    tickets_completed: List[str]
    side_quests: List[str]
    highlights: List[str]
    linkedin_post: str
    twitter_thread: str


def get_session_files(vault_path: Path, days: int = 7) -> List[Path]:
    """Get session log files from the past N days."""
    sessions_dir = vault_path / "Sessions"
    if not sessions_dir.exists():
        return []
    
    cutoff = datetime.now() - timedelta(days=days)
    session_files = []
    
    for f in sessions_dir.glob("*.md"):
        try:
            # Parse date from filename (format: YYYY-MM-DD_HHMM.md)
            date_str = f.stem.split("_")[0]
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date >= cutoff:
                session_files.append(f)
        except (ValueError, IndexError):
            continue
    
    return sorted(session_files)


def parse_session_log(file_path: Path) -> Dict[str, Any]:
    """Parse a session log file and extract key metrics."""
    content = file_path.read_text(encoding="utf-8")
    
    # Extract frontmatter
    frontmatter = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm_content = content[3:end]
            for line in fm_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
    
    # Count files mentioned (look for backticks with file paths)
    files_mentioned = len(re.findall(r'`[^`]+\.(py|md|json|yaml|yml|js|ts)`', content))
    
    # Extract commits (look for commit patterns)
    commits = re.findall(r'[a-f0-9]{7}\s+\w+:', content)
    
    # Look for side quest section
    has_side_quest = "Side Quest" in content and "No side quests" not in content
    
    return {
        "date": frontmatter.get("date", file_path.stem),
        "files_mentioned": files_mentioned,
        "commits": len(commits),
        "has_side_quest": has_side_quest,
        "linear_tickets": frontmatter.get("linear_tickets", "[]"),
        "focus": frontmatter.get("focus_area", "Unknown")
    }


def generate_weekly_summary(vault_path: Path) -> WeeklySummary:
    """Generate a weekly summary from session logs."""
    session_files = get_session_files(vault_path)
    
    if not session_files:
        return WeeklySummary(
            week_start=datetime.now().strftime("%Y-%m-%d"),
            week_end=datetime.now().strftime("%Y-%m-%d"),
            total_sessions=0,
            total_files_modified=0,
            total_commits=0,
            tickets_completed=[],
            side_quests=[],
            highlights=["No sessions logged this week."],
            linkedin_post="",
            twitter_thread=""
        )
    
    # Aggregate data
    total_files = 0
    total_commits = 0
    side_quests = []
    dates = []
    
    for f in session_files:
        data = parse_session_log(f)
        total_files += data["files_mentioned"]
        total_commits += data["commits"]
        dates.append(data["date"])
        if data["has_side_quest"]:
            side_quests.append(data["date"])
    
    week_start = min(dates) if dates else datetime.now().strftime("%Y-%m-%d")
    week_end = max(dates) if dates else datetime.now().strftime("%Y-%m-%d")
    
    # Generate highlights
    highlights = [
        f"Logged {len(session_files)} coding sessions",
        f"Modified approximately {total_files} files",
        f"Made {total_commits} commits"
    ]
    if side_quests:
        highlights.append(f"Explored {len(side_quests)} side quests")
    
    # Generate social posts
    linkedin = f"""📊 Weekly Learning Recap ({week_start} to {week_end})

This week in my Data Engineering journey:

✅ {len(session_files)} coding sessions logged
📁 ~{total_files} files modified
🔄 {total_commits} commits pushed
{'🔍 ' + str(len(side_quests)) + ' side quests explored' if side_quests else ''}

Key learnings:
• [Highlight 1]
• [Highlight 2]
• [Highlight 3]

I'm building a Personal AI OS that automates this entire documentation process.

Check my progress: github.com/oronculzac

#LearningInPublic #DataEngineering #WeeklyReview"""

    twitter = f"""🧵 Weekly Learning Recap

1/ This week's stats:
📊 {len(session_files)} sessions
📁 {total_files} files modified
🔄 {total_commits} commits

2/ Biggest win: [What was the highlight?]

3/ Biggest challenge: [What was hard?]

4/ Next week focus: [What's planned?]

5/ All documented at github.com/oronculzac/learning-logs

#LearningInPublic #DataEngineering"""

    return WeeklySummary(
        week_start=week_start,
        week_end=week_end,
        total_sessions=len(session_files),
        total_files_modified=total_files,
        total_commits=total_commits,
        tickets_completed=[],
        side_quests=side_quests,
        highlights=highlights,
        linkedin_post=linkedin,
        twitter_thread=twitter
    )


def format_weekly_summary(summary: WeeklySummary) -> str:
    """Format weekly summary as markdown."""
    return f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
type: weekly-summary
week: {summary.week_start} to {summary.week_end}
---

# Weekly Summary: {summary.week_start} to {summary.week_end}

## 📊 Stats

| Metric | Value |
|--------|-------|
| Sessions Logged | {summary.total_sessions} |
| Files Modified | ~{summary.total_files_modified} |
| Commits | {summary.total_commits} |
| Side Quests | {len(summary.side_quests)} |

## 🌟 Highlights

{chr(10).join('- ' + h for h in summary.highlights)}

## 📣 Social Drafts

### LinkedIn Post

{summary.linkedin_post}

### Twitter Thread

{summary.twitter_thread}
"""


# CLI
if __name__ == "__main__":
    import sys
    import json
    
    # Default vault path
    config_path = Path(".agent/config/mcp_config.json")
    vault_path = Path("vault")
    
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            vault_path = Path(config.get("obsidian", {}).get("vault_path", "vault"))
    
    print(f"Generating weekly summary from: {vault_path}")
    summary = generate_weekly_summary(vault_path)
    print(format_weekly_summary(summary))
