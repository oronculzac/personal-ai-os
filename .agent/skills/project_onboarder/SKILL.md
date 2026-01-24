---
name: Project Onboarder
description: Automates new project setup - creates folder structure, git repo, Obsidian note, and Linear project
version: 1.1.0
triggers:
  - onboard project
  - new project
  - create project
  - start project
  - initialize project
examples:
  - "Create a new project for my side quest"
  - "Onboard the data pipeline project"
  - "Set up a new project called ML Experiments"
  - "Start a new project"
context_hints:
  - user mentions starting or creating a new project
  - user wants consistent project structure
  - user mentions project scaffolding or setup
priority: 7
conflicts_with: []
capabilities:
  - project_structure_creation
  - git_initialization
  - linear_project_creation
  - obsidian_project_note
dependencies:
  - gitpython>=3.1.0
  - requests>=2.31.0
auto_load: true
---

# Project Onboarder Skill

Automates the entire setup process for a new project in your Personal AI OS.

## 🎯 Purpose

Ensures every project starts with a consistent structure and is correctly linked across your tools (Git, Obsidian, Linear).

## 🚀 Usage

### Via Workflow
```
/onboard-project
```

### Via Natural Language
```
"Start a new project called portfolio-site"
"Onboard a data-analysis project"
```

### Via Script
```powershell
# Interactive mode
python .agent\skills\project_onboarder\scripts\onboard.py

# Direct mode
python .agent\skills\project_onboarder\scripts\onboard.py --name "portfolio-site" --description "My new personal site"
```

## 📋 What It Does

1. **Creates Directories**
   - `projects/{name}/`
   - `projects/{name}/src/`
   - `projects/{name}/docs/`
   - `projects/{name}/notebooks/`

2. **Initializes Git**
   - Runs `git init`
   - Creates `.gitignore` (Python/Node default)
   - Creates `README.md` and commits it

3. **Sets up Linear**
   - Creates a new Project in your default Team
   - Returns the Project ID (e.g., "PRO-123")

4. **Sets up Obsidian**
   - Creates a project note in `vault/Projects/{Name}.md`
   - Links to Local Folder and Linear Project
   - Uses a standard template

## 🔧 Configuration

Uses keys from `.agent/config/mcp_config.json`.

## 📦 Project Structure Template

```
projects/
  └── my-project/
      ├── .git/
      ├── docs/
      ├── notebooks/
      ├── src/
      ├── .gitignore
      └── README.md
```

## 📝 Obsidian Note Template

```markdown
---
type: project
status: active
linear_id: PRO-123
git_path: projects/my-project
created: 2026-01-17
---

# My Project

[Description]

## 🔗 Links
- [[Local Folder]]: `projects/my-project`
- [Linear Project](https://linear.app/team/project/PRO-123)

## 📝 Notes
...
```
