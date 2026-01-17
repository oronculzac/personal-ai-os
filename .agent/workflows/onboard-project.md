---
description: Onboard a new project with proper setup including git, Linear project, and Obsidian folder
---

# Onboard New Project Workflow

Use this workflow to add a new project to the Personal AI OS with all integrations set up.

## Triggers
- "onboard new project"
- "create new project"
- "add project"

## Steps

### 1. Get Project Details
Ask user for:
- Project name (slug format, e.g., `my-new-project`)
- Project description
- Whether to create git repo (default: yes)
- Whether to create Linear project (default: yes)
- Whether to create Obsidian folder (default: yes)

### 2. Create Project Structure
```powershell
# Create project folder
New-Item -ItemType Directory -Path "projects/{project_name}"

# Create standard subdirectories
New-Item -ItemType Directory -Path "projects/{project_name}/src"
New-Item -ItemType Directory -Path "projects/{project_name}/docs"
New-Item -ItemType Directory -Path "projects/{project_name}/notebooks"
```

### 3. Initialize Git Repository
```powershell
cd projects/{project_name}
git init
# Create README.md with project description
# Create .gitignore from template
git add .
git commit -m "Initial project setup"
```

### 4. Create Obsidian Folder
```powershell
New-Item -ItemType Directory -Path "vault/Projects/{ProjectName}"
# Create project note from template
```

### 5. Create Linear Project (Optional)
// turbo
```python
# Use LinearClient to create project
from linear_client import LinearClient
client = LinearClient()
# Note: Linear API for project creation requires team admin permissions
```

### 6. Update Configuration
Add project to `mcp_config.json` or `.env` if needed.

### 7. Confirmation
Display summary:
- Project location
- Git status
- Obsidian folder link
- Linear project link (if created)

## Notes
- Projects live in `projects/` directory
- Each project uses the global `.agent/` (no nested agents)
- Project-specific configs can use `.env` in project folder
