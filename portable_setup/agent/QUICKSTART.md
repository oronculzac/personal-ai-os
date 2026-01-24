# Skills & Cowork Quick Reference

## 🚀 Quick Start

### New Workspace Setup
```powershell
# Option 1: Use the workflow (recommended)
# In Antigravity, just say: "Run the setup-skills-cowork workflow"

# Option 2: Manual setup
cd your-new-project
mkdir .agent
# Copy .agent/ folder from existing workspace
```

### Verify Installation
```powershell
# Check directory structure
tree .agent /F

# Discover skills
python .agent/core/skill_discovery.py
```

---

## 📚 Skills System

### Using Skills
Just ask Antigravity naturally:
- "Create an Excel spreadsheet with Q1 sales data"
- "Generate a PowerPoint about project updates"
- "Analyze this CSV file and create visualizations"
- "Convert this PDF to Word"

### Available Built-in Skills
- **example_template**: Template for creating new skills

### Creating Custom Skills

1. **Create folder structure:**
```powershell
.agent/skills/your-skill-name/
├── SKILL.md              # Instructions
├── scripts/              # Python/PowerShell scripts
│   └── your_script.py
├── resources/            # Templates, data
│   └── template.xlsx
└── examples/             # Sample outputs
```

2. **Write SKILL.md with frontmatter:**
```yaml
---
name: Your Skill Name
description: What this skill does
version: 1.0.0
triggers:
  - keyword1
  - keyword phrase
dependencies:
  - python-package>=1.0.0
capabilities:
  - capability_name
---

# Your Skill Name

## Purpose
Describe what this skill does

## Instructions
Step-by-step instructions for Antigravity to follow
```

3. **Register the skill:**
```powershell
python .agent/core/skill_discovery.py
```

---

## 📁 Cowork (File Management)

### Request Folder Access
Antigravity will ask for permission when needing file access:
```
"I need to access C:/Users/You/Documents for organizing files. 
Permission will be recorded in folder_permissions.json."
```

### Folder Operations
- **Organize folders**: "Organize my Downloads by file type"
- **Batch rename**: "Rename all PDFs in this folder with date prefix"
- **Find duplicates**: "Find duplicate files in Documents"
- **Archive old files**: "Archive files older than 1 year"

### Safety Features
✅ Dry-run mode by default (preview before execution)
✅ Automatic backups before modifications
✅ Approval required for deletions
✅ Full audit logging

### Check Permissions
```powershell
# View current permissions
cat .agent/config/folder_permissions.json

# View audit log
python .agent/core/folder_permissions.py
```

---

## 🔧 Configuration Files

### skill_registry.json
```json
{
  "skills": [...],          // Auto-populated
  "auto_discover": true,    // Scan on startup
  "auto_load_on_startup": true
}
```

### folder_permissions.json
```json
{
  "permissions": [...],     // Granted folder access
  "audit_log": [...],       // Operation history
  "safety_settings": {
    "require_approval_for_delete": true,
    "dry_run_by_default": true
  }
}
```

---

## 🛠️ Common Tasks

### Deploy to New Workspace
```powershell
# Copy entire .agent/ folder
Copy-Item -Recurse C:/path/to/existing/.agent C:/path/to/new-workspace/.agent

# Run setup workflow
cd C:/path/to/new-workspace
# Ask Antigravity: "Run setup-skills-cowork workflow"
```

### Add New Skill Package
```powershell
# Copy skill folder
Copy-Item -Recurse .agent/skills/new-skill .agent/skills/

# Discover and register
python .agent/core/skill_discovery.py
```

### Update Dependencies
```powershell
# Install all skill dependencies
pip install -r .agent/skills/requirements_all.txt

# Install specific skill dependencies
pip install -r .agent/skills/excel_generator/requirements.txt
```

---

## 📦 Directory Structure

```
your-workspace/
├── .agent/
│   ├── skills/              # Modular skill packages
│   │   ├── example_template/
│   │   ├── excel_generator/
│   │   └── requirements_all.txt
│   ├── config/              # Configuration files
│   │   ├── skill_registry.json
│   │   └── folder_permissions.json
│   ├── core/                # Helper scripts
│   │   ├── skill_discovery.py
│   │   └── folder_permissions.py
│   ├── workflows/           # Automation workflows
│   │   └── setup-skills-cowork.md
│   └── README.md            # Documentation
└── your-project-files/
```

---

## 🎯 Workflow Examples

### Example 1: Process Receipts
```
User: "Scan my Receipts folder, extract data, and create expense report"

Antigravity will:
1. Request access to Receipts folder
2. Use document_transformer skill (OCR)
3. Use data_analyzer skill (extract amounts, dates)
4. Use excel_generator skill (create report)
5. Save to specified location
```

### Example 2: Generate Report
```
User: "Create quarterly sales presentation from sales_data.csv"

Antigravity will:
1. Use data_analyzer skill (analyze CSV)
2. Generate visualizations
3. Use powerpoint_generator skill (create slides)
4. Export as PPTX
```

---

## 🆘 Troubleshooting

**Skill not recognized?**
```powershell
python .agent/core/skill_discovery.py
```

**Permission denied for folder?**
- Check `.agent/config/folder_permissions.json`
- Grant access when prompted

**Missing dependencies?**
```powershell
pip install -r .agent/skills/requirements_all.txt
```

**Skills not loading?**
- Verify SKILL.md has proper frontmatter (starts with `---`)
- Check for YAML syntax errors
- Ensure skill is enabled in registry

---

## 📖 Next Steps

1. ✅ Run setup workflow in your workspace
2. ✅ Create your first custom skill
3. ✅ Test file operations with Cowork
4. ✅ Deploy to another workspace to test portability

**Pro Tip**: Use `/setup-skills-cowork` as a workflow command for instant setup!
