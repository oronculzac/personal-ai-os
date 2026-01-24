---
name: Artifact Sync
description: Sync AI-generated artifacts (plans, tasks, walkthroughs) to Obsidian with intuitive naming. Use when user says "sync artifact", "save plan", or "copy to vault".
version: 1.2.0
triggers:
  - sync artifact
  - save plan to obsidian
  - copy task to notes
  - sync to vault
  - save walkthrough
examples:
  - "Save this implementation plan to my notes"
  - "Sync the walkthrough to Obsidian"
  - "Copy this task list to my vault"
  - "Archive this plan"
context_hints:
  - user mentions saving or syncing AI-generated content
  - user references plans, tasks, or walkthroughs
  - user wants to preserve conversation artifacts
  - user mentions Obsidian vault
priority: 7
conflicts_with: []
capabilities:
  - artifact_detection
  - topic_extraction
  - obsidian_sync
  - intuitive_naming
dependencies:
  - pyyaml>=6.0
inputs:
  required:
    - name: source
      type: path
      description: Path to the artifact file to sync
  optional:
    - name: dry_run
      type: boolean
      default: false
      description: Preview sync without making changes
    - name: recent
      type: boolean
      default: false
      description: Sync all recent artifacts from last 24 hours
outputs:
  - name: target_path
    type: path
    description: Path where artifact was synced in vault
  - name: artifact_type
    type: string
    description: Detected type (plan, task, walkthrough)
auto_load: true
---

# Artifact Sync Skill

Automatically copy AI-generated artifacts to Obsidian with descriptive, searchable names.

## 🎯 Purpose

When you create implementation plans, task lists, or walkthroughs with the AI, they get saved in `.gemini/brain/<conversation-id>/` with generic names like `implementation_plan.md`. This skill copies them to your Obsidian vault with intuitive names like `2026-01-17_system_review_plan.md`.

## 📦 Supported Artifact Types

| Type | Source Filename | Destination Folder | Output Example |
|------|----------------|-------------------|----------------|
| Implementation Plan | `implementation_plan.md` | `vault/Plans/` | `2026-01-17_auth_system_plan.md` |
| Task List | `task.md` | `vault/Plans/` | `2026-01-17_bugfix_task.md` |
| Walkthrough | `walkthrough.md` | `vault/Journals/Sessions/` | `2026-01-17_api_refactor_walkthrough.md` |
| Other | `*.md` | `vault/Plans/` | `2026-01-17_topic_note.md` |

## 🚀 How It Works

### Artifact Detection
- Monitors `.gemini/brain/` for new/updated artifacts
- Detects type: `implementation_plan`, `task`, `walkthrough`, `other`

### Topic Extraction
- Parses the artifact's H1 heading or frontmatter
- Extracts key topic words
- Generates slug: `{date}_{topic}_{type}.md`

### Obsidian Integration
- Copies to appropriate vault folder:
  - Plans → `vault/Plans/`
  - Tasks → `vault/Plans/`
  - Walkthroughs → `vault/Journals/Sessions/`
- Adds frontmatter with source link

## 💡 Usage

### Via Natural Language
```
"Sync this plan to Obsidian"
"Save the implementation plan to my notes"
"Copy today's artifacts to vault"
```

### Via Script
```powershell
# Sync specific artifact
.agent\.venv\Scripts\python.exe .agent\skills\artifact_sync\scripts\sync_artifact.py --source "path/to/artifact.md"

# Sync all recent artifacts
.agent\.venv\Scripts\python.exe .agent\skills\artifact_sync\scripts\sync_artifact.py --recent

# Dry run
.agent\.venv\Scripts\python.exe .agent\skills\artifact_sync\scripts\sync_artifact.py --dry-run
```

## 📁 Output Structure

**Input:** `.gemini/brain/abc123/implementation_plan.md`

**Output:** `vault/Plans/2026-01-17_system_review_plan.md`

With frontmatter:
```yaml
---
type: plan
source: .gemini/brain/abc123/implementation_plan.md
synced: 2026-01-17T18:00:00
topic: system review
---
```

## 🔧 Configuration

Uses vault path from `.agent/config/mcp_config.json`:
```json
{
  "obsidian": {
    "vault_path": "vault/"
  }
}
```

## 📋 Naming Convention

| Artifact Type | Format | Example |
|---------------|--------|---------|
| Plan | `{date}_{topic}_plan.md` | `2026-01-17_auth_system_plan.md` |
| Task | `{date}_{topic}_task.md` | `2026-01-17_bugfix_task.md` |
| Walkthrough | `{date}_{topic}_walkthrough.md` | `2026-01-17_api_refactor_walkthrough.md` |

## 🎯 Integration

Designed to work with:
- `/wrap-session` workflow (auto-sync walkthroughs)
- Any planning session (manual or auto sync)
