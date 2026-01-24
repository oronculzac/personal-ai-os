# 🚀 Skills & Cowork - Portable Setup Package

## What Is This?

This is a **complete, self-contained deployment package** for the Skills & Cowork system. Everything you need to set up on a new computer, profile, or workspace is in this folder.

---

## 📦 What's Included

```
portable_setup/
├── SETUP.md               ← You are here (deployment instructions)
├── agent/                 ← Complete Skills & Cowork system
│   ├── skills/           (Excel, File Organizer, Web Scraper, etc.)
│   ├── personas/         (SEO Specialist, Data Analyst, Content Writer)
│   ├── core/             (Helper scripts)
│   ├── workflows/        (Automation workflows)
│   └── config/           (Configuration files)
├── deploy.ps1            ← Automated deployment script
├── activate_skills.bat   ← Quick activation helper
└── requirements.txt      ← Python package requirements
```

---

## 🎯 Quick Deployment (3 Steps)

### Step 1: Copy This Folder
Copy the entire `portable_setup/` folder to your new location:
- USB drive
- Network share
- Cloud storage
- Email (zip it first)

### Step 2: Run Deployment Script
```powershell
cd portable_setup
.\deploy.ps1
```

The script will:
- ✅ Create virtual environment
- ✅ Install required packages (openpyxl, pandas, pyyaml)
- ✅ Verify all skills and personas
- ✅ Confirm everything works

### Step 3: Start Using
```powershell
.\activate_skills.bat
```

**That's it! You now have the complete Skills & Cowork system.**

---

## 🤖 For AI Agents Reading This

If you're an AI agent setting up this system, follow these steps:

**Deployment Commands**:
```powershell
# 1. Navigate to portable_setup folder
cd path/to/portable_setup

# 2. Create virtual environment
python -m venv agent\.venv

# 3. Activate virtual environment
agent\.venv\Scripts\Activate.ps1

# 4. Install packages
pip install -r requirements.txt

# 5. Copy agent folder to parent directory
Copy-Item -Recurse agent ..\agent

# 6. Verify installation
python ..\agent\core\skill_discovery.py
python ..\agent\core\persona_manager.py --list
```

**Success Criteria**:
- Skill discovery finds 4 skills
- Persona manager lists 3 personas  
- No import errors when running scripts

---

## 📋 What You Get

### Skills (4 Production-Ready)
1. **Excel Generator** - Create spreadsheets with formulas, charts, formatting
2. **File Organizer** - Autonomous file management with categorization
3. **Web Scraper** - Extract data from websites using browser automation
4. **Example Template** - Reference for creating custom skills

### Personas (3 Specialized Agents)
1. **SEO Specialist** - Keyword research, competitor analysis, content optimization
2. **Data Analyst** - Data analysis, visualization, business intelligence
3. **Content Writer** - High-quality content creation, research, engagement

### Infrastructure
- Auto-discovery skill system
- Persona management and switching
- Cowork autonomous file agent
- Folder permissions and safety controls
- Virtual environment for isolation

---

## 💻 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, Mac, or Linux
- **Disk Space**: ~100 MB (with virtual environment)
- **Internet**: For initial package installation

---

## 🔧 Manual Setup (If Script Fails)

```powershell
# 1. Create virtual environment
python -m venv agent\.venv

# 2. Activate (Windows)
agent\.venv\Scripts\Activate.ps1
# Or Mac/Linux: source agent/.venv/bin/activate

# 3. Install packages
pip install openpyxl==3.1.5 pandas==2.3.3 pyyaml==6.0.3

# 4. Move agent folder
Copy-Item -Recurse agent ..\agent

# 5. Test
cd ..
python agent\core\skill_discovery.py
```

---

## ✅ Verification

After deployment, confirm:

```powershell
# Skills discovered
python agent\core\skill_discovery.py
# Expected: ✓ Discovered 4 skills

# Personas available
python agent\core\persona_manager.py --list
# Expected: SEO Specialist, Data Analyst, Content Writer

# Excel generation works
python agent\skills\excel_generator\scripts\excel_builder.py --help
# Expected: Help text displayed
```

---

## 📚 Next Steps

1. **Read Documentation**: `agent\QUICKSTART.md`
2. **Activate Persona**: `python agent\core\persona_manager.py --activate seo_specialist`
3. **Test Skills**: Try creating an Excel file or organizing a folder
4. **Create Custom Persona**: Add your own specialized agent

---

## 🆘 Troubleshooting

**"python not found"**
- Install Python 3.8+ from python.org
- Add to PATH during installation

**"pip install fails"**
- Ensure virtual environment is activated (prompt shows `(.venv)`)
- Try: `python -m pip install openpyxl pandas pyyaml`

**"No module named 'openpyxl'"**
- Activate venv first: `agent\.venv\Scripts\Activate.ps1`
- Install packages: `pip install -r requirements.txt`

**"Skills not found"**
- Ensure `agent/` folder exists in parent directory
- Run: `python agent\core\skill_discovery.py`

---

## 🎉 What You Can Do Now

- **Create Excel Reports**: Spreadsheets with formulas and charts
- **Organize Files**: Autonomous file management by type/date/size
- **Scrape Websites**: Extract data using browser automation
- **Switch Personas**: Become SEO expert, data analyst, or content writer
- **Build Workflows**: Combine skills for complex automation

---

## 📞 Support

For detailed documentation:
- Quick Start: `agent\QUICKSTART.md`
- Deployment: `agent\DEPLOYMENT.md`
- Personas Guide: `agent\personas\README.md`

---

## ⚡ Quick Reference

**Activate environment**:
```powershell
.\activate_skills.bat
```

**List skills**:
```powershell
python agent\core\skill_discovery.py
```

**Activate persona**:
```powershell
python agent\core\persona_manager.py --activate data_analyst
```

**Create Excel file**:
```powershell
python agent\skills\excel_generator\scripts\excel_builder.py --template sales_report --output report.xlsx
```

---

**This package contains everything you need. Just copy, deploy, and use!** 🚀
