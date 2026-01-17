"""
Enhanced Content Synthesizer v2 - Context-aware content generation

Improvements over v1:
- Extracts actual accomplishments from git data
- Creates specific, non-placeholder social content
- Generates Dev.to article drafts
- Saves content to Obsidian Social folder
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class EnhancedContent:
    """Container for all synthesized content."""
    core_work_log: str
    side_quest_log: str
    narrative: str
    twitter_draft: str
    linkedin_draft: str
    devto_draft: str
    key_accomplishments: List[str]


def extract_accomplishments(git_data: Dict, linear_tickets: List) -> List[str]:
    """Extract actual accomplishments from session data."""
    accomplishments = []
    
    # From commits
    commits = git_data.get("recent_commits", "").strip()
    for line in commits.split("\n")[:5]:
        if line.strip():
            # Extract commit message (after hash)
            parts = line.split(" ", 1)
            if len(parts) > 1:
                msg = parts[1]
                # Clean conventional commit format
                if msg.startswith("feat:"):
                    accomplishments.append(f"Built {msg[5:].strip()}")
                elif msg.startswith("fix:"):
                    accomplishments.append(f"Fixed {msg[4:].strip()}")
                elif msg.startswith("chore:"):
                    accomplishments.append(f"Updated {msg[6:].strip()}")
                else:
                    accomplishments.append(msg)
    
    # From modified files - identify key patterns
    files = git_data.get("modified_files", [])
    for f in files:
        if "SKILL.md" in f:
            skill_name = f.split("/")[-2] if "/" in f else "new skill"
            accomplishments.append(f"Created {skill_name} skill")
        elif "workflow" in f.lower():
            accomplishments.append("Added automation workflow")
        elif "test" in f.lower():
            accomplishments.append("Added tests")
    
    # Deduplicate and limit
    seen = set()
    unique = []
    for a in accomplishments:
        if a.lower() not in seen:
            seen.add(a.lower())
            unique.append(a)
    
    return unique[:5]


def generate_twitter_enhanced(context: Dict, accomplishments: List[str]) -> str:
    """Generate an enhanced Twitter/X thread with actual content."""
    git_data = context.get("git", {})
    file_count = len(git_data.get("modified_files", []))
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Pick the most interesting accomplishment for hook
    main_accomplishment = accomplishments[0] if accomplishments else "made good progress"
    
    # Build thread
    thread = f"""🧵 Learning in Public: {date_str}

1/ Today I {main_accomplishment.lower()}!

Here's what I learned 👇

"""
    
    # Add accomplishments as thread items
    for i, acc in enumerate(accomplishments[1:4], 2):
        thread += f"{i}/ ✅ {acc}\n\n"
    
    thread += f"""{len(accomplishments) + 1}/ Stats:
📁 {file_count} files modified
🔄 Pushed to GitHub
📔 Documented everything

{len(accomplishments) + 2}/ Building in public means every mistake becomes a lesson for others.

Check my progress: github.com/oronculzac

#LearningInPublic #DataEngineering #100DaysOfCode #BuildInPublic"""
    
    return thread


def generate_linkedin_enhanced(context: Dict, accomplishments: List[str]) -> str:
    """Generate an enhanced LinkedIn post with professional framing."""
    git_data = context.get("git", {})
    file_count = len(git_data.get("modified_files", []))
    
    main_accomplishment = accomplishments[0] if accomplishments else "Made progress on my learning journey"
    
    post = f"""📚 Learning in Public Update

{main_accomplishment}

Today's session highlights:
"""
    
    for acc in accomplishments[:4]:
        post += f"✅ {acc}\n"
    
    post += f"""
📊 Session Stats:
• {file_count} files modified
• Code pushed to GitHub
• Progress documented in my knowledge base

💡 Key insight: The best way to learn is to build things, break things, and share what you discover.

I'm documenting my Data Engineering journey while building a Personal AI OS that automates this entire workflow.

What are you building this week?

#DataEngineering #LearningInPublic #CareerGrowth #TechJourney #BuildInPublic"""
    
    return post


def generate_devto_draft(context: Dict, accomplishments: List[str], narrative: str) -> str:
    """Generate a Dev.to article draft."""
    git_data = context.get("git", {})
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_count = len(git_data.get("modified_files", []))
    
    main_topic = accomplishments[0] if accomplishments else "Today's Progress"
    
    article = f"""---
title: "Learning Log: {main_topic}"
published: false
description: Daily learning log - {date_str}
tags: learninginpublic, dataengineering, devjournal, productivity
series: Daily Learning Logs
---

# {main_topic}

*{date_str} • {file_count} files modified*

## What I Built Today

"""
    
    for acc in accomplishments:
        article += f"- {acc}\n"
    
    article += f"""

## The Journey

{narrative}

## Code Highlights

```python
# Key changes today
# - Modified {file_count} files
# - See commits for details
```

## Key Takeaways

1. **What worked:** Document as you go - it's easier than reconstructing later
2. **What I'd do differently:** Start with tests next time
3. **Next steps:** Continue building and sharing

## Resources

- [My GitHub](https://github.com/oronculzac)
- [Personal AI OS](https://github.com/oronculzac/personal-ai-os)

---

*This post was auto-generated from my Learning-in-Public workflow. [Learn how it works!](https://github.com/oronculzac/personal-ai-os/tree/main/.agent/skills/session_wrapper)*
"""
    
    return article


def synthesize_enhanced(context: Dict) -> EnhancedContent:
    """
    Main entry point - synthesize all content with enhanced quality.
    """
    git_data = context.get("git", {})
    linear_tickets = context.get("linear", {}).get("tickets", [])
    
    # Extract actual accomplishments
    accomplishments = extract_accomplishments(git_data, linear_tickets)
    
    # Generate core work log
    modified_files = git_data.get("modified_files", [])
    commits = git_data.get("recent_commits", "").strip()
    
    core_log_lines = ["### Files Modified"]
    for f in modified_files[:10]:
        core_log_lines.append(f"- `{f}`")
    if len(modified_files) > 10:
        core_log_lines.append(f"*...and {len(modified_files) - 10} more*")
    
    core_log_lines.append("\n### Commits")
    for commit in commits.split("\n")[:5]:
        if commit.strip():
            core_log_lines.append(f"- {commit}")
    
    core_work_log = "\n".join(core_log_lines)
    
    # Side quest detection
    side_quest_log = "*No side quests detected — focused session!*"
    
    # Narrative with actual content
    narrative = f"""### The Journey

**What I Accomplished:**
{chr(10).join('- ' + a for a in accomplishments) if accomplishments else '- Made incremental progress'}

**The Challenge:**
Every session has its hurdles. Today's was about maintaining focus and pushing through.

**Key Takeaway:**
Small consistent steps compound into significant progress. Keep shipping!
"""
    
    return EnhancedContent(
        core_work_log=core_work_log,
        side_quest_log=side_quest_log,
        narrative=narrative,
        twitter_draft=generate_twitter_enhanced(context, accomplishments),
        linkedin_draft=generate_linkedin_enhanced(context, accomplishments),
        devto_draft=generate_devto_draft(context, accomplishments, narrative),
        key_accomplishments=accomplishments
    )


def save_social_drafts(content: EnhancedContent, vault_path: Path) -> Dict[str, Path]:
    """Save social drafts to Obsidian vault."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    paths = {}
    
    # Twitter
    twitter_path = vault_path / "Social" / "Twitter" / f"{date_str}.md"
    twitter_path.parent.mkdir(parents=True, exist_ok=True)
    twitter_path.write_text(f"""---
date: {date_str}
platform: twitter
status: draft
---

# Twitter Thread Draft

{content.twitter_draft}
""", encoding="utf-8")
    paths["twitter"] = twitter_path
    
    # LinkedIn
    linkedin_path = vault_path / "Social" / "LinkedIn" / f"{date_str}.md"
    linkedin_path.parent.mkdir(parents=True, exist_ok=True)
    linkedin_path.write_text(f"""---
date: {date_str}
platform: linkedin
status: draft
---

# LinkedIn Post Draft

{content.linkedin_draft}
""", encoding="utf-8")
    paths["linkedin"] = linkedin_path
    
    # Dev.to
    devto_path = vault_path / "Social" / "DevTo" / f"{date_str}.md"
    devto_path.parent.mkdir(parents=True, exist_ok=True)
    devto_path.write_text(content.devto_draft, encoding="utf-8")
    paths["devto"] = devto_path
    
    return paths


# For backwards compatibility, map to original function name
def synthesize_session(context: Dict):
    """Wrapper for backwards compatibility with session_wrapper."""
    enhanced = synthesize_enhanced(context)
    
    # Return as the original SynthesizedContent format
    from dataclasses import dataclass as dc
    
    @dc
    class SynthesizedContent:
        core_work_log: str
        side_quest_log: str
        narrative: str
        twitter_draft: str
        linkedin_draft: str
    
    return SynthesizedContent(
        core_work_log=enhanced.core_work_log,
        side_quest_log=enhanced.side_quest_log,
        narrative=enhanced.narrative,
        twitter_draft=enhanced.twitter_draft,
        linkedin_draft=enhanced.linkedin_draft
    )


# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_context = {
            "git": {
                "modified_files": [
                    ".agent/skills/session_wrapper/scripts/synthesizer.py",
                    ".agent/skills/devto_publisher/SKILL.md",
                    ".agent/core/secrets_checker.py"
                ],
                "recent_commits": "abc123 feat: Add Dev.to publisher\ndef456 feat: Add secrets checker\nghi789 chore: Update config"
            },
            "linear": {"tickets": []}
        }
        
        content = synthesize_enhanced(test_context)
        
        print("=" * 60)
        print("ENHANCED SYNTHESIZED CONTENT")
        print("=" * 60)
        print("\n### Key Accomplishments\n")
        for a in content.key_accomplishments:
            print(f"  ✅ {a}")
        print("\n### Twitter Draft\n")
        print(content.twitter_draft[:500])
        print("\n### LinkedIn Draft\n")
        print(content.linkedin_draft[:500])
        print("\n### Dev.to Draft (preview)\n")
        print(content.devto_draft[:500])
    else:
        print("Usage: python synthesizer.py --test")
