# Deployment Guide - Porting Skills & Cowork to New Systems

## 🚀 Quick Overview

The Skills & Cowork system is **100% portable**. Everything you need is in the `.agent/` folder.

**What transfers**:
- ✅ All skills (Excel, File Organizer, Web Scraper, etc.)
- ✅ All personas (SEO Specialist, Data Analyst, Content Writer)
- ✅ Configuration files
- ✅ Helper scripts (skill_discovery, persona_manager, file_agent)
- ✅ Workflows and documentation

**What doesn't transfer** (recreated on new system):
- ❌ Virtual environment (`.venv`) - too large, system-specific
- ❌ Active persona state - user preference
- ❌ Cached Python files (`__pycache__`)

---

## 📋 Deployment Methods

### Method 1: New Workspace on Same Computer (Easiest)

**Time**: < 2 minutes

**Steps**:
```powershell
# 1. Copy .agent folder to new workspace
Copy-Item -Recurse C:\old-workspace\.agent C:\new-workspace\.agent

# 2. Navigate to new workspace
cd C:\new-workspace

# 3. Create virtual environment
python -m venv .agent\.venv

# 4. Activate venv
.agent\.venv\Scripts\Activate.ps1

# 5. Install packages
pip install openpyxl pandas pyyaml

# 6. Test
python .agent\core\skill_discovery.py
```

**Done!** All skills and personas are immediately available.

---

### Method 2: New Computer / New User Profile

**Time**: 5-10 minutes

**Prerequisites on New System**:
- Python 3.8+ installed
- Git (optional, for version control)

**Steps**:

#### Option A: Using USB Drive / Network Share

```powershell
# On OLD computer
# 1. Copy .agent folder to USB/network drive
Copy-Item -Recurse .agent E:\transfer\.agent

# On NEW computer
# 2. Create workspace directory
mkdir C:\Users\NewUser\my-workspace
cd C:\Users\NewUser\my-workspace

# 3. Copy .agent from USB
Copy-Item -Recurse E:\transfer\.agent .agent

# 4. Set up virtual environment
python -m venv .agent\.venv
.agent\.venv\Scripts\Activate.ps1
pip install openpyxl pandas pyyaml

# 5. Verify
python .agent\core\skill_discovery.py
python .agent\core\persona_manager.py --list
```

#### Option B: Using Git (Recommended for Teams)

```powershell
# On OLD computer (one-time setup)
cd your-workspace
git init
git add .agent/
git commit -m "Add Skills & Cowork system"
git remote add origin https://github.com/yourusername/skills-cowork.git
git push -u origin main

# On NEW computer
git clone https://github.com/yourusername/skills-cowork.git
cd skills-cowork

# Set up environment
python -m venv .agent\.venv
.agent\.venv\Scripts\Activate.ps1
pip install openpyxl pandas pyyaml

# Done!
```

#### Option C: Manual File Transfer

```powershell
# Compress on OLD system
Compress-Archive -Path .agent -DestinationPath skills-cowork.zip

# Transfer skills-cowork.zip (email, cloud storage, etc.)

# Extract on NEW system
Expand-Archive -Path skills-cowork.zip -DestinationPath C:\new-workspace\
cd C:\new-workspace

# Set up
python -m venv .agent\.venv
.agent\.venv\Scripts\Activate.ps1
pip install openpyxl pandas pyyaml
```

---

### Method 3: Team Deployment (Multiple Users)

**Scenario**: Share Skills & Cowork with team members

**Recommended Approach**: Git Repository

**Setup (Team Lead - One Time)**:

```powershell
# 1. Create GitHub/GitLab repository
git init
git add .agent/
git add .gitignore
git commit -m "Initial Skills & Cowork setup"
git push origin main

# 2. Add README for team
# (see Team README template below)
```

**Setup (Team Members)**:

```powershell
# 1. Clone repository
git clone https://your-repo-url.git
cd project-name

# 2. Run setup script (or manual steps)
python -m venv .agent\.venv
.agent\.venv\Scripts\Activate.ps1
pip install -r .agent/skills/requirements_all.txt

# 3. Optionally activate a persona
python .agent\core\persona_manager.py --activate data_analyst

# Ready to use!
```

---

## 📦 What Gets Transferred

### Directory Structure

```
.agent/
├── skills/                    ✅ TRANSFER (all skill logic)
│   ├── excel_generator/
│   ├── file_organizer/
│   ├── web_scraper/
│   └── example_template/
│
├── personas/                  ✅ TRANSFER (all personas)
│   ├── seo_specialist.json
│   ├── data_analyst.json
│   └── content_writer.json
│
├── core/                      ✅ TRANSFER (helper scripts)
│   ├── skill_discovery.py
│   ├── persona_manager.py
│   ├── folder_permissions.py
│   └── file_agent.py
│
├── workflows/                 ✅ TRANSFER (automation)
│   └── setup-skills-cowork.md
│
├── config/                    ✅ TRANSFER (configs)
│   ├── skill_registry.json
│   └── folder_permissions.json
│
├── .venv/                     ❌ DON'T TRANSFER (recreate)
└── QUICKSTART.md             ✅ TRANSFER (docs)
```

### File Sizes (Approximate)

- `.agent/` folder (without .venv): **~500 KB**
- `.agent/.venv/` (if included): **~50-100 MB** ⚠️ Don't transfer!
- Total transfer size: **< 1 MB** 🎉

---

## 🔧 Platform-Specific Notes

### Windows → Windows
✅ **Direct copy works perfectly**
- Same paths (.agent\.venv\Scripts\)
- Same activation (Activate.ps1)

### Windows → Mac/Linux
⚠️ **Minor adjustments needed**

**Activation command changes**:
```bash
# Instead of: .agent\.venv\Scripts\Activate.ps1
source .agent/.venv/bin/activate

# Path separators
# Windows: .agent\core\skill_discovery.py
# Mac/Linux: .agent/core/skill_discovery.py
```

**Update activate_skills.bat → activate_skills.sh**:
```bash
#!/bin/bash
source .agent/.venv/bin/activate
echo "Skills & Cowork environment activated!"
```

### Mac/Linux → Windows
⚠️ **Same adjustments in reverse**

---

## ✅ Verification Checklist

After deploying to new system, verify:

```powershell
# 1. Virtual environment exists
Test-Path .agent\.venv
# Should return: True

# 2. Packages installed
.agent\.venv\Scripts\python.exe -m pip list
# Should show: openpyxl, pandas, pyyaml

# 3. Skills discovered
python .agent\core\skill_discovery.py
# Should show: 4 skills found

# 4. Personas available
python .agent\core\persona_manager.py --list
# Should show: 3 personas

# 5. Test a skill
python .agent\skills\excel_generator\scripts\excel_builder.py --help
# Should show: Excel builder help

# 6. Test persona switching
python .agent\core\persona_manager.py --activate seo_specialist
# Should activate SEO Specialist
```

All passing? **System is ready!** ✅

---

## 🎯 Common Scenarios

### Scenario 1: Developer Moving to New Laptop

```powershell
# OLD laptop: Push to GitHub
git add .agent/
git commit -m "Update skills"
git push

# NEW laptop: Pull and setup
git clone your-repo
cd project
python -m venv .agent\.venv
.agent\.venv\Scripts\Activate.ps1
pip install -r .agent/skills/requirements_all.txt
```

**Time**: 5 minutes

---

### Scenario 2: Sharing with Colleague

**Best Method**: Zip and email

```powershell
# Create package
Compress-Archive -Path .agent -DestinationPath skills-cowork.zip

# Email skills-cowork.zip to colleague

# Colleague: Extract and setup
Expand-Archive skills-cowork.zip
cd extracted-location
python -m venv .agent\.venv
# ... (standard setup)
```

**Time**: 2 minutes setup for recipient

---

### Scenario 3: Multiple Projects on Same Machine

```
C:\
├── project-a\
│   └── .agent\        ← Independent setup
│       └── .venv\     ← Project A packages
│
├── project-b\
│   └── .agent\        ← Independent setup
│       └── .venv\     ← Project B packages (same versions)
│
└── project-c\
    └── .agent\        ← Independent setup
        └── .venv\     ← Project C packages
```

**Each project is completely isolated!** ✅

---

## 🚀 Automation Script

Create **deploy.ps1** for one-command deployment:

```powershell
# deploy.ps1
Write-Host "Deploying Skills & Cowork system..." -ForegroundColor Green

# Create venv
Write-Host "Creating virtual environment..."
python -m venv .agent\.venv

# Activate
Write-Host "Activating environment..."
& .agent\.venv\Scripts\Activate.ps1

# Install packages
Write-Host "Installing packages..."
pip install openpyxl pandas pyyaml

# Verify
Write-Host "`nVerifying installation..."
python .agent\core\skill_discovery.py

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "Run: .\activate_skills.bat to start using the system"
```

**Usage**:
```powershell
.\deploy.ps1
```

---

## 📝 Team README Template

Create this in your repository root:

```markdown
# Skills & Cowork System

AI agent capabilities with specialized personas and modular skills.

## Quick Start

1. Clone this repository
2. Run deployment:
   ```powershell
   python -m venv .agent\.venv
   .agent\.venv\Scripts\Activate.ps1
   pip install -r .agent/skills/requirements_all.txt
   ```
3. Activate environment: `.\activate_skills.bat`
4. Discover skills: `python .agent\core\skill_discovery.py`

## Available Skills
- Excel Generator
- File Organizer
- Web Scraper

## Available Personas
- SEO Specialist
- Data Analyst
- Content Writer

## Documentation
See `.agent/QUICKSTART.md` for detailed usage.
```

---

## 🔐 What NOT to Transfer

**Don't include in transfers**:
- `.venv/` - Virtual environment (too large, system-specific)
- `__pycache__/` - Python cache (regenerated)
- `.agent/backups/` - Old backups (workspace-specific)
- `.agent/test_folder/` - Test data
- `.agent/config/active_persona.json` - User preference

**Already excluded by .gitignore** ✅

---

## 💡 Best Practices

### For Personal Use
1. **Keep .agent/ in version control** (Git)
2. **Use .gitignore** to exclude .venv
3. **Update across machines** via git pull
4. **Recreate venv** on each machine

### For Teams
1. **Central Git repository**
2. **Document setup in README**
3. **Pin package versions** in requirements.txt
4. **Create setup scripts** for new members
5. **Share custom personas** via repository

### For Production
1. **Use virtual environments** (already set up!)
2. **Lock dependencies** (requirements.txt with ==)
3. **Test on fresh system** before deploying
4. **Document deployment** process

---

## ⚡ Quick Reference

**Copy to new workspace**:
```powershell
Copy-Item -Recurse .agent C:\new-workspace\.agent
```

**Setup venv**:
```powershell
python -m venv .agent\.venv
.agent\.venv\Scripts\Activate.ps1
pip install openpyxl pandas pyyaml
```

**Verify**:
```powershell
python .agent\core\skill_discovery.py
```

**That's it!** 3 commands, < 2 minutes. 🚀

---

## 🆘 Troubleshooting

**Issue**: "python not found"
- Install Python 3.8+ first
- Add to PATH

**Issue**: "pip install fails"
- Ensure venv is activated (prompt shows `.venv`)
- Try: `python -m pip install...`

**Issue**: "No module named 'openpyxl'"
- Activate venv first: `.agent\.venv\Scripts\Activate.ps1`
- Reinstall: `pip install openpyxl pandas pyyaml`

**Issue**: "Skills not found"
- Check `.agent/skills/` directory exists
- Run skill discovery: `python .agent\core\skill_discovery.py`

---

## ✅ Success Criteria

Your deployment is successful when:
- ✅ Skill discovery finds all 4 skills
- ✅ Persona manager lists 3 personas
- ✅ File agent runs without errors
- ✅ Excel generator can create files
- ✅ Virtual environment is isolated

**You're now portable across any system!** 🎉
