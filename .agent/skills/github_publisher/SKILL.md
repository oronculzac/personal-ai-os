---
name: GitHub Publisher
description: Automatically publish session logs, skills, and learning content to appropriate GitHub repositories
version: 1.0.0
triggers:
  - publish to github
  - push session
  - commit learning
  - update github
capabilities:
  - git_operations
  - branch_management
  - commit_generation
  - repo_routing
dependencies:
  - gitpython>=3.1.0
auto_load: true
---

# GitHub Publisher Skill

Automate the "Learning-in-Public" GitHub publishing workflow.

## 🎯 Purpose

Seamlessly push publish-worthy content from your local workspace to the appropriate GitHub repository, maintaining consistent contribution activity and organized project structure.

## 🚀 Capabilities

### 1. **Repository Routing**
Routes content to the correct repo based on type:
- `personal-ai-os` — Skills, workflows, agent infrastructure
- `de-zoomcamp-2026` — Homework, module progress, cloud configs
- `learning-logs` — Session logs, side quests, daily learnings

### 2. **Smart Commit Messages**
Generates conventional commit messages:
- `feat: Add Session Wrapper skill with publish detection`
- `docs: Session log 2026-01-17 - BigQuery partitioning`
- `chore: Update DE Zoomcamp Module 3 progress`

### 3. **Branch Management**
- Auto-creates feature branches for new skills
- Commits directly to main for learning logs
- Supports PR-based workflow (optional)

### 4. **Dry-Run Mode**
Preview what would be published without making changes.

## 💡 Usage Examples

### Example 1: Publish Current Session
```
User: "Publish this session to GitHub"
Assistant: *Analyzes session, determines target repo, commits and pushes*
```

### Example 2: Push Specific Files
```
User: "Push my session wrapper skill to personal-ai-os"
Assistant: *Commits skill files and pushes to personal-ai-os repo*
```

### Example 3: Dry-Run Preview
```
User: "Show me what would be published"
Assistant: *Displays target repo, files, and commit message without pushing*
```

## 🔧 Configuration

Add GitHub configuration to `.agent/config/mcp_config.json`:
```json
{
  "github": {
    "username": "YOUR_GITHUB_USERNAME",
    "repos": {
      "personal-ai-os": "path/to/local/personal-ai-os",
      "de-zoomcamp-2026": "path/to/local/de-zoomcamp-2026", 
      "learning-logs": "path/to/local/learning-logs"
    },
    "default_branch": "main",
    "auto_push": false
  }
}
```

## 📋 Integration with Session Wrapper

The GitHub Publisher integrates with Session Wrapper's publish detection:

```
Session Wrapper → Publish Detector → GitHub Publisher
     ↓                  ↓                   ↓
  Collect           Determine          Commit & Push
  Context           Target Repo         to GitHub
```

## 🔒 Safety Features

- **Dry-run by default** — Preview before pushing
- **Confirmation prompts** — For destructive operations
- **Branch protection** — Won't force-push to main
- **Commit review** — Shows diff before committing
