---
description: Morning routine with daily standup pulling Linear tasks and setting priorities
---

# Morning Routine Workflow

Start your day with an automated standup that pulls your tasks and helps prioritize.

## Triggers
- "morning routine"
- "daily standup"
- "what's on for today"
- "start my day"

## Steps

### 1. Greeting
```
Good morning! Let me pull together your standup...
```

### 2. Pull Linear Tasks
// turbo
```powershell
.agent\.venv\Scripts\python.exe -c "
import sys
sys.path.insert(0, '.agent/skills/session_wrapper/scripts')
from linear_client import LinearClient
from datetime import datetime

client = LinearClient()
issues = client.get_in_progress_issues()
print(f'📋 In Progress ({len(issues)} items):')
for i in issues:
    print(f'  [{i.identifier}] {i.title}')
"
```

### 3. Check Yesterday's Session
Review the most recent session log in `vault/Journals/Sessions/` for continuity.

### 4. Sync Obsidian Tasks
// turbo
```powershell
.agent\.venv\Scripts\python.exe .agent\skills\obsidian_linear_sync\scripts\sync.py
```

### 5. Show Weekly Stats
// turbo
```powershell
.agent\.venv\Scripts\python.exe .agent\skills\session_wrapper\scripts\weekly_summary.py
```

### 6. Priority Suggestions
Based on:
- Tickets in progress
- Yesterday's work
- Any deadlines

Suggest top 3 priorities for today.

### 7. Optional: Trend Research
If user agrees, run the AI Researcher skill:
// turbo
```powershell
.agent\.venv\Scripts\python.exe .agent\skills\ai_researcher\scripts\research.py
```

### 8. Create Today's Plan
Optionally create a daily note in Obsidian with:
- Top priorities
- Scheduled tasks
- Notes from yesterday

## Output Format
```
📅 Morning Standup - {date}

📋 In Progress:
- [LIN-XX] Task 1
- [LIN-YY] Task 2

📊 This Week:
- X sessions logged
- Y files modified

🎯 Suggested Priorities:
1. [High] Complete LIN-XX
2. [Medium] Review PR
3. [Low] Documentation update

Ready to start?
```
