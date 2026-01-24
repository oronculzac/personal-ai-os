# Proactive Triggers - Installation Guide

## Overview

This folder contains scripts for proactive agent behavior that works outside of Antigravity conversations.

## Available Triggers

### 1. Git Post-Commit Hook
**File:** `post-commit`

Automatically suggests session wrap after significant commits (5+ files).

**Installation:**
```powershell
# Copy to your git hooks folder
Copy-Item ".agent\hooks\post-commit" ".git\hooks\post-commit"

# On Windows, the hook runs via Git Bash
# Make sure Git is installed with Unix tools
```

### 2. PowerShell Profile Greeting
**File:** `profile_greeting.ps1`

Shows time-based greetings and reminders when opening PowerShell.

**Installation:**
```powershell
# Open your profile
notepad $PROFILE

# Add this line (adjust path as needed):
. "C:\Users\Oron Culzac\antigravity_general\.agent\hooks\profile_greeting.ps1"

# Save and restart PowerShell
```

### 3. Windows Task Scheduler (Manual)

For true scheduled automation:

1. Open **Task Scheduler**
2. Create Basic Task
3. Trigger: Daily at 9:00 AM
4. Action: Start a program
   - Program: `python`
   - Arguments: `.agent\skills\session_wrapper\scripts\weekly_summary.py`
   - Start in: `C:\Users\Oron Culzac\antigravity_general`

## Testing

## Task Boundary Schema Validation

Schema: `task_boundary.schema.json`  
Example: `task_boundary.example.json`

Use any JSON Schema validator. Example with `ajv-cli`:

```powershell
ajv validate -s task_boundary.schema.json -d task_boundary.example.json
```

```powershell
# Test the profile greeting
. ".agent\hooks\profile_greeting.ps1"

# Test post-commit (after a commit)
git commit -m "test" --allow-empty
```

## Behavior Summary

| Trigger | When | Action |
|---------|------|--------|
| post-commit | After 5+ file commits | Suggest session wrap |
| profile_greeting | Terminal open (AM) | Suggest morning routine |
| profile_greeting | Terminal open (PM) | Suggest session wrap |
| Task Scheduler | 9 AM daily | Run weekly summary |
