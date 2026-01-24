# Quick Deployment Script
# Run this on NEW system after copying .agent folder

Write-Host "🚀 Skills & Cowork Deployment Starting..." -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".agent\.venv") {
    Write-Host "⚠ Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv .agent\.venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate venv
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .agent\.venv\Scripts\Activate.ps1

# Install packages
Write-Host "`nInstalling required packages..." -ForegroundColor Yellow
Write-Host "This may take a minute..." -ForegroundColor Gray
pip install --quiet openpyxl pandas pyyaml

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Package installation failed" -ForegroundColor Red
    exit 1
}

# Verify skills
Write-Host "`nVerifying skills..." -ForegroundColor Yellow
python .agent\core\skill_discovery.py

# Verify personas
Write-Host "`nVerifying personas..." -ForegroundColor Yellow
python .agent\core\persona_manager.py --list

# Success
Write-Host "`n" + "="*50 -ForegroundColor Green
Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "="*50 -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run: .\activate_skills.bat (to activate environment)"
Write-Host "  2. Test: python .agent\core\skill_discovery.py"
Write-Host "  3. Read: .agent\QUICKSTART.md"
Write-Host ""
Write-Host "Your Skills & Cowork system is ready to use! 🎉" -ForegroundColor Green
