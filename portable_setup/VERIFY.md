# ✅ Portable Setup - Verification Checklist

Run this checklist to verify the portable_setup folder is complete and ready for deployment.

## Pre-Deployment Verification

### 1. Check Required Files

```powershell
cd portable_setup

# Core files
Test-Path SETUP.md           # Should be True
Test-Path deploy.ps1          # Should be True  
Test-Path requirements.txt    # Should be True
Test-Path activate_skills.bat # Should be True

# Agent folder
Test-Path agent              # Should be True
```

### 2. Check Agent Subdirectories

```powershell
# Skills
Test-Path agent\skills\excel_generator
Test-Path agent\skills\file_organizer
Test-Path agent\skills\web_scraper
Test-Path agent\skills\example_template

# Personas
Test-Path agent\personas\seo_specialist.json
Test-Path agent\personas\data_analyst.json
Test-Path agent\personas\content_writer.json

# Core scripts
Test-Path agent\core\skill_discovery.py
Test-Path agent\core\persona_manager.py
Test-Path agent\core\file_agent.py
Test-Path agent\core\folder_permissions.py

# Config
Test-Path agent\config\skill_registry.json
Test-Path agent\config\folder_permissions.json

# Documentation
Test-Path agent\QUICKSTART.md
```

All should return `True`.

### 3. Check No Excluded Files

```powershell
# These should NOT exist (environment-specific)
Test-Path agent\.venv         # Should be False
Test-Path agent\__pycache__   # Should be False  
Test-Path agent\backups       # Should be False
```

Should return `False` (good - they're excluded).

### 4. Test Deployment Script

```powershell
# Read the deploy script
Get-Content deploy.ps1 | Select-String "python -m venv"
# Should find venv creation command

Get-Content deploy.ps1 | Select-String "pip install"
# Should find package installation
```

### 5. Check Requirements.txt

```powershell
Get-Content requirements.txt
```

Should contain:
```
openpyxl==3.1.5
pandas==2.3.3
PyYAML==6.0.3
```

## Deployment Test

### Simulate Fresh Deployment

```powershell
# Copy to test location
Copy-Item -Recurse portable_setup C:\temp\test-deploy

# Run deployment
cd C:\temp\test-deploy
.\deploy.ps1

# Verify
python agent\core\skill_discovery.py
# Should discover 4 skills

python agent\core\persona_manager.py --list
# Should list 3 personas
```

## Size Check

```powershell
# Get total size
$size = (Get-ChildItem portable_setup -Recurse | Measure-Object -Property Length -Sum).Sum
$sizeMB = [math]::Round($size / 1MB, 2)
Write-Host "Total size: $sizeMB MB"
```

Should be < 5 MB (without .venv).

## Final Checklist

- [ ] All required files present
- [ ] All skills copied correctly
- [ ] All personas included
- [ ] Core scripts functional
- [ ] Configuration files present
- [ ] Documentation included
- [ ] No .venv or __pycache__ included
- [ ] deploy.ps1 works
- [ ] activate_skills.bat present
- [ ] requirements.txt correct
- [ ] Total size < 5 MB

If all checked ✅, package is ready for deployment!
