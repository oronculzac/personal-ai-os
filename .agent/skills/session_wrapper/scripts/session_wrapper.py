"""
Session Wrapper - Main entry point

This is the primary script for wrapping up a coding session.
It orchestrates: context collection → publish detection → output generation.
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Import sibling modules
from collect_context import get_config, get_git_info, get_linear_tickets, get_obsidian_focus
from publish_detector import analyze_session, format_decision, PublishDecision
from linear_client import LinearClient, format_issues_for_display


def collect_full_context() -> dict:
    """Collect all context data for the session."""
    config = get_config()
    
    context = {
        "timestamp": datetime.now().isoformat(),
        "git": get_git_info(),
        "linear": get_linear_tickets(config),
        "obsidian": get_obsidian_focus(config),
        "config": {
            "vault_path": config.get("obsidian", {}).get("vault_path"),
            "linear_workspace": config.get("linear", {}).get("workspace")
        }
    }
    
    return context


def generate_session_summary(context: dict, decision: PublishDecision) -> str:
    """Generate a human-readable session summary."""
    git = context.get("git", {})
    linear = context.get("linear", {})
    
    lines = [
        "=" * 60,
        "📊 SESSION SUMMARY",
        "=" * 60,
        f"⏰ Time: {context.get('timestamp', 'Unknown')}",
        "",
        "📁 Git Activity:",
        f"   Files Modified: {git.get('file_count', 0)}",
    ]
    
    # List modified files
    for f in git.get("modified_files", [])[:5]:
        lines.append(f"   • {f}")
    if git.get("file_count", 0) > 5:
        lines.append(f"   ... and {git.get('file_count', 0) - 5} more")
    
    lines.append("")
    lines.append("📋 Recent Commits:")
    for commit in git.get("recent_commits", "").split("\n")[:3]:
        if commit.strip():
            lines.append(f"   • {commit}")
    
    # Linear tickets
    tickets = linear.get("tickets", [])
    if tickets:
        lines.append("")
        lines.append("🎫 Linear Tickets:")
        for t in tickets[:3]:
            state = t.get("state", {}).get("name", "Unknown")
            lines.append(f"   [{state}] {t.get('identifier', '???')}: {t.get('title', 'Untitled')}")
    
    lines.append("")
    lines.append(format_decision(decision))
    
    return "\n".join(lines)


def save_session_log(context: dict, decision: PublishDecision, output_path: Path) -> bool:
    """Save the session log to Obsidian vault with synthesized content.
    Also creates a separate social drafts file.
    """
    try:
        # Import synthesizer
        from synthesizer import synthesize_session
        
        template_path = Path(__file__).parent.parent / "templates" / "session_note.md"
        
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        else:
            # Fallback template
            template = """---
date: {{date}}
type: session-log
publish_status: {{publish_status}}
target_repo: {{target_repo}}
---

# Session Log: {{date}}

## Summary
{{summary}}

## Git Activity
{{git_activity}}

## Publish Decision
{{publish_decision}}
"""
        
        # Synthesize content from context
        synth = synthesize_session(context)
        
        # Fill template
        git = context.get("git", {})
        
        content = template
        content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
        content = content.replace("{{time_range}}", datetime.now().strftime("%H:%M"))
        content = content.replace("{{focus_area}}", "Session Wrapper Development")
        content = content.replace("{{linear_tickets}}", str([t.get("identifier") for t in context.get("linear", {}).get("tickets", [])]))
        content = content.replace("{{title}}", f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        content = content.replace("{{publish_status}}", "pending" if decision.should_publish else "private")
        content = content.replace("{{target_repo}}", decision.target_repo.value if decision.target_repo else "none")
        content = content.replace("{{summary}}", f"Modified {git.get('file_count', 0)} files")
        content = content.replace("{{git_activity}}", git.get("diff_stat", "No changes"))
        content = content.replace("{{publish_decision}}", decision.reason)
        
        # Fill with SYNTHESIZED content (not placeholders!)
        content = content.replace("{{core_work_log}}", synth.core_work_log)
        content = content.replace("{{side_quest_log}}", synth.side_quest_log)
        content = content.replace("{{narrative_content}}", synth.narrative)
        
        # Add repo URL and social filename
        social_filename = output_path.stem + "_drafts.md"
        content = content.replace("{{repo_url}}", git.get("repo_url", "N/A"))
        content = content.replace("{{social_filename}}", social_filename)
        
        # Write article to Sessions folder
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Generate social drafts file
        social_template_path = Path(__file__).parent.parent / "templates" / "social_drafts.md"
        if social_template_path.exists():
            with open(social_template_path, 'r', encoding='utf-8') as f:
                social_template = f.read()
            
            # Fill social template
            social_content = social_template
            social_content = social_content.replace("{{title}}", f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            social_content = social_content.replace("{{focus_area}}", "Session Wrapper Development")
            social_content = social_content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
            social_content = social_content.replace("{{session_reference}}", f"Session {datetime.now().strftime('%Y-%m-%d')}")
            social_content = social_content.replace("{{twitter_draft}}", synth.twitter_draft)
            social_content = social_content.replace("{{linkedin_draft}}", synth.linkedin_draft)
            social_content = social_content.replace("{{suggested_tags}}", "dataengineering, learninginpublic, python")
            social_content = social_content.replace("{{suggested_series}}", "Learning in Public")
            social_content = social_content.replace("{{canonical_url}}", git.get("repo_url", ""))
            social_content = social_content.replace("{{filename}}", output_path.name)
            
            # Write to Social folder
            vault_path = context.get("config", {}).get("vault_path")
            if vault_path:
                social_path = Path(vault_path) / "Social" / social_filename
                social_path.parent.mkdir(parents=True, exist_ok=True)
                with open(social_path, 'w', encoding='utf-8') as f:
                    f.write(social_content)
                print(f"   📱 Social drafts: {social_path}")
        
        return True
    except Exception as e:
        print(f"Error saving session log: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Wrap up a coding session")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", type=str, help="Custom output path for session log")
    parser.add_argument("--force-publish", action="store_true", help="Force publish regardless of criteria")
    args = parser.parse_args()
    
    print("🔄 Collecting session context...")
    context = collect_full_context()
    
    if args.force_publish:
        context["force_publish"] = True
    
    print("🔍 Analyzing publish-worthiness...")
    decision = analyze_session(context)
    
    if args.json:
        output = {
            "context": context,
            "decision": {
                "should_publish": decision.should_publish,
                "content_type": decision.content_type.value if decision.content_type else None,
                "target_repo": decision.target_repo.value if decision.target_repo else None,
                "reason": decision.reason,
                "confidence": decision.confidence
            }
        }
        print(json.dumps(output, indent=2, default=str))
        return
    
    # Generate and display summary
    summary = generate_session_summary(context, decision)
    print(summary)
    
    if args.dry_run:
        print("\n🔸 DRY RUN - No files saved")
        return
    
    # Save session log
    if args.output:
        output_path = Path(args.output)
    else:
        vault_path = context.get("config", {}).get("vault_path")
        if vault_path:
            output_path = Path(vault_path) / "Journals" / "Sessions" / f"{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
        else:
            output_path = Path(f"session_{datetime.now().strftime('%Y-%m-%d_%H%M')}.md")
    
    print(f"\n💾 Saving session log to: {output_path}")
    if save_session_log(context, decision, output_path):
        print("✅ Session log saved!")
        
        if decision.should_publish:
            print(f"\n📢 This session is publish-worthy!")
            print(f"   Target: {decision.target_repo.value}")
            print(f"   Next step: Review and push to GitHub")
    else:
        print("❌ Failed to save session log")


if __name__ == "__main__":
    main()
