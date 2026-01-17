---
description: Wrap up a coding session with auto-detection and publish to GitHub
---

# Wrap Session Workflow

Automatically analyze, document, and optionally publish your coding session.

## Triggers

Say any of these:
- "wrap up"
- "wrap session"
- "end session"
- "log session"
- "publish to github"

## Steps

**1. Collect Session Context**
// turbo
```powershell
python .agent\skills\session_wrapper\scripts\session_wrapper.py --dry-run
```

Review the output to see:
- Files modified
- Linear tickets worked on
- Publish recommendation (repo + confidence)

**2. Save Session Log to Obsidian**

If user approves, save the session log:
// turbo
```powershell
python .agent\skills\session_wrapper\scripts\session_wrapper.py
```

This creates a note in `vault/Sessions/YYYY-MM-DD_HHMM.md`

**3. Publish to GitHub (if recommended)**

If publish detector says "Should Publish: Yes", offer to publish:

For **skills** → push to `personal-ai-os`:
```powershell
python .agent\skills\github_publisher\scripts\publisher.py .agent\skills\<skill_name> --repo personal-ai-os --type skill --execute
```

For **homework** → push to `de-zoomcamp-2026`:
```powershell
python .agent\skills\github_publisher\scripts\publisher.py <homework_files> --repo de-zoomcamp-2026 --type homework --execute
```

For **session logs** → push to `learning-logs`:
```powershell
python .agent\skills\github_publisher\scripts\publisher.py vault\Sessions\<log_file>.md --repo learning-logs --type learning_log --execute
```

## Auto-Detection Criteria

The system recommends publishing when:
| Criterion | Confidence | Target Repo |
|-----------|------------|-------------|
| New skill created (SKILL.md + scripts) | 90% | personal-ai-os |
| Homework completed | 85% | de-zoomcamp-2026 |
| Side quest (drift from ticket) | 70% | learning-logs |
| ≥3 files modified | 60% | learning-logs |

## Example Flow

```
User: "wrap up"

Agent: 
1. Runs session_wrapper.py --dry-run
2. Shows: "5 files modified, skill detected, recommend publish to personal-ai-os (90%)"
3. Asks: "Save session log and publish to GitHub?"
4. If yes: Saves log, publishes to repo
5. Reports: "Session logged! Pushed to personal-ai-os (commit abc123)"
```
