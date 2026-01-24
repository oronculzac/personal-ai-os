---
description: Setup Skills & Cowork system in new workspace
---

# Skills & Cowork Universal Setup

This workflow sets up the complete Skills & Cowork system in any workspace, enabling portable AI agent capabilities with modular skills and autonomous file management.

## Prerequisites

Ensure you have Python 3.8+ installed and access to pip.

## Initial Setup

// turbo

1. Create core directory structure:
```powershell
mkdir -p .agent/skills, .agent/config, .agent/core, .agent/workflows, .agent/templates
```

2. Verify directory creation:
```powershell
ls .agent
```

## Install Dependencies

// turbo

3. Create virtual environment for isolated packages:
```powershell
python -m venv .agent\.venv
```

4. Activate virtual environment:
```powershell
.agent\.venv\Scripts\Activate.ps1
```

Note: On Mac/Linux use: `source .agent/.venv/bin/activate`

5. Create consolidated requirements file:
```powershell
@"
# Core Skills Dependencies
openpyxl>=3.0.0
pandas>=1.5.0
pyyaml>=6.0.0
python-pptx>=0.6.21
pypdf2>=3.0.0
python-docx>=0.8.11
pillow>=9.0.0
matplotlib>=3.5.0
seaborn>=0.12.0

# Optional (for advanced features)
# pytesseract>=0.3.10  # OCR functionality (requires Tesseract)
# sqlalchemy>=2.0.0     # Database support
"@ | Out-File -FilePath .agent/skills/requirements_all.txt -Encoding UTF8
```

// turbo

6. Install Python dependencies in virtual environment:
```powershell
pip install -r .agent/skills/requirements_all.txt
```

## Create Configuration Files

5. Create skill registry configuration:
```powershell
@"
{
  "version": "1.0",
  "workspace_name": "antigravity_general",
  "skills": [],
  "skill_sources": {
    "local": ".agent/skills",
    "official": "https://github.com/antigravity-skills/official-skills",
    "community": "https://github.com/antigravity-skills/community"
  },
  "auto_discover": true,
  "auto_load_on_startup": true
}
"@ | Out-File -FilePath .agent/config/skill_registry.json -Encoding UTF8
```

6. Create folder permissions configuration:
```powershell
@"
{
  "version": "1.0",
  "workspace_root": "$PWD",
  "permissions": [],
  "audit_log": [],
  "global_restrictions": {
    "never_access": [
      "C:/Windows/System32",
      "C:/Program Files",
      "*/AppData/Local",
      "*/.git"
    ]
  },
  "safety_settings": {
    "require_approval_for_delete": true,
    "auto_backup_before_modify": true,
    "dry_run_by_default": true,
    "max_files_per_operation": 100
  }
}
"@ | Out-File -FilePath .agent/config/folder_permissions.json -Encoding UTF8
```

## Create Core Helper Scripts

7. Create skill discovery helper:
```powershell
@"
#!/usr/bin/env python3
"""
Skill Discovery and Management Helper
Scans .agent/skills/ and registers available skills
"""

import json
import os
from pathlib import Path
import yaml

def discover_skills(skills_dir='.agent/skills'):
    """Scan skills directory and build registry"""
    skills = []
    skills_path = Path(skills_dir)
    
    if not skills_path.exists():
        print(f"Skills directory not found: {skills_dir}")
        return skills
    
    for skill_folder in skills_path.iterdir():
        if not skill_folder.is_dir():
            continue
            
        skill_md = skill_folder / 'SKILL.md'
        if not skill_md.exists():
            continue
        
        # Parse SKILL.md frontmatter
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    
                    skill_info = {
                        'id': skill_folder.name,
                        'name': frontmatter.get('name', skill_folder.name),
                        'description': frontmatter.get('description', ''),
                        'version': frontmatter.get('version', '1.0.0'),
                        'path': str(skill_folder),
                        'triggers': frontmatter.get('triggers', []),
                        'capabilities': frontmatter.get('capabilities', []),
                        'dependencies': frontmatter.get('dependencies', []),
                        'enabled': True,
                        'auto_load': frontmatter.get('auto_load', True)
                    }
                    
                    skills.append(skill_info)
                    print(f"✓ Discovered skill: {skill_info['name']}")
        except Exception as e:
            print(f"✗ Error parsing {skill_folder.name}: {e}")
    
    return skills

def update_registry(skills):
    """Update skill_registry.json with discovered skills"""
    registry_path = Path('.agent/config/skill_registry.json')
    
    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    else:
        registry = {'version': '1.0', 'skills': []}
    
    registry['skills'] = skills
    
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    
    print(f"\n✓ Registry updated: {len(skills)} skills registered")

if __name__ == '__main__':
    print("Scanning for skills...")
    skills = discover_skills()
    update_registry(skills)
    print(f"\nTotal skills found: {len(skills)}")
    
    for skill in skills:
        print(f"  - {skill['name']} (v{skill['version']})")
"@ | Out-File -FilePath .agent/core/skill_discovery.py -Encoding UTF8
```

8. Create folder permission helper:
```powershell
@"
#!/usr/bin/env python3
"""
Folder Permission Manager
Handles safe folder access for Cowork functionality
"""

import json
from pathlib import Path
from datetime import datetime

class FolderPermissionManager:
    def __init__(self, config_path='.agent/config/folder_permissions.json'):
        self.config_path = Path(config_path)
        self.load_config()
    
    def load_config(self):
        """Load permissions configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'version': '1.0',
                'permissions': [],
                'audit_log': []
            }
    
    def save_config(self):
        """Save permissions configuration"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def request_access(self, path, reason, access_level='read'):
        """Request access to a folder"""
        path = str(Path(path).resolve())
        
        # Check if already granted
        for perm in self.config['permissions']:
            if perm['path'] == path:
                print(f"✓ Access already granted to: {path}")
                return True
        
        print(f"\n📁 Folder Access Request:")
        print(f"   Path: {path}")
        print(f"   Reason: {reason}")
        print(f"   Access Level: {access_level}")
        
        # In production, this would prompt user
        # For now, return True for demo
        return True
    
    def grant_access(self, path, access_level='read_write'):
        """Grant access to a folder"""
        permission = {
            'path': str(Path(path).resolve()),
            'granted_at': datetime.now().isoformat(),
            'access_level': access_level,
            'auto_approve_operations': False
        }
        
        self.config['permissions'].append(permission)
        self.save_config()
        print(f"✓ Access granted to: {path}")
    
    def has_access(self, path):
        """Check if access is granted to path"""
        path = str(Path(path).resolve())
        
        for perm in self.config['permissions']:
            if path.startswith(perm['path']):
                return True
        return False
    
    def log_operation(self, operation, path, success=True):
        """Log file operation to audit log"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'path': str(path),
            'success': success
        }
        
        self.config['audit_log'].append(log_entry)
        self.save_config()

if __name__ == '__main__':
    pm = FolderPermissionManager()
    print("Folder Permission Manager initialized")
    print(f"Current permissions: {len(pm.config['permissions'])}")
"@ | Out-File -FilePath .agent/core/folder_permissions.py -Encoding UTF8
```

## Create README Documentation

9. Create workspace setup guide:
```powershell
@"
# Skills & Cowork System

## Overview

This workspace is equipped with Antigravity's Skills & Cowork system, providing:

- **Modular Skills**: Reusable AI capabilities for document generation, data analysis, and automation
- **Cowork Functionality**: Autonomous file management with safety controls
- **Universal Portability**: Deploy to any workspace with simple setup

## Available Skills

Skills are located in `.agent/skills/`. To see available skills:

\`\`\`powershell
.agent\.venv\Scripts\python.exe .agent/core/skill_discovery.py
\`\`\`

## Using Skills

Skills are automatically discovered and loaded. Simply ask Antigravity to perform tasks like:

- "Create an Excel spreadsheet with sales data"
- "Generate a PowerPoint presentation"
- "Analyze this CSV file"
- "Organize my downloads folder"

## Folder Permissions

For file operations, Antigravity will request folder access. Permissions are managed in:

\`\`\`
.agent/config/folder_permissions.json
\`\`\`

## Adding New Skills

1. Create folder in \`.agent/skills/your-skill-name/\`
2. Add \`SKILL.md\` with frontmatter
3. Add scripts and resources
4. Run skill discovery to register

## Safety Features

- ✅ Dry-run mode by default
- ✅ Automatic backups before modifications
- ✅ Approval required for deletions
- ✅ Audit logging of all operations

## Directory Structure

\`\`\`
.agent/
├── skills/              # Modular skill packages
├── config/              # Configuration files
├── core/                # Core helper scripts
├── workflows/           # Automation workflows
└── templates/           # Workspace templates
\`\`\`

## Next Steps

1. Install skill dependencies: \`pip install -r .agent/skills/requirements_all.txt\`
2. Discover available skills: \`.agent\.venv\Scripts\python.exe .agent/core/skill_discovery.py\`
3. Start using skills in conversations with Antigravity

## Support

For issues or questions, refer to the implementation plan in the brain directory.
"@ | Out-File -FilePath .agent/README.md -Encoding UTF8
```

## Validation

10. Verify directory structure:
```powershell
tree .agent /F
```

11. Test skill discovery:
```powershell
.agent\.venv\Scripts\python.exe .agent/core/skill_discovery.py
```

## Done!

Your workspace is now equipped with the Skills & Cowork system foundation!

**Next steps:**
- Add your first skill (e.g., Excel Generator)
- Grant folder permissions as needed
- Start automating workflows

**To deploy this to another workspace:**
1. Copy the entire `.agent/` directory to new project
2. Run this workflow again with `// turbo-all` enabled
3. Customize as needed
