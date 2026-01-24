# Quick Deployment Script for Portable Setup
# Run this after copying portable_setup folder to new location

param(
    [string]$TargetDir = ".."
)

Write-Host "🚀 Skills & Cowork Deployment Starting..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in portable_setup folder
if (!(Test-Path "agent")) {
    Write-Host "✗ Error: 'agent' folder not found!" -ForegroundColor Red
    Write-Host "  Make sure you're running this from inside the portable_setup folder" -ForegroundColor Yellow
    exit 1
}

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "agent\.venv") {
    Write-Host "⚠ Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Recreate it? (y/n)"
    if ($response -eq "y") {
        Remove-Item -Recurse -Force "agent\.venv"
        python -m venv agent\.venv
        Write-Host "✓ Virtual environment recreated" -ForegroundColor Green
    }
} else {
    python -m venv agent\.venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate and install
Write-Host "`nInstalling packages in virtual environment..." -ForegroundColor Yellow
& agent\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
& agent\.venv\Scripts\python.exe -m pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Package installation failed" -ForegroundColor Red
    exit 1
}

# Copy to target directory
Write-Host "`nCopying agent folder to: $TargetDir" -ForegroundColor Yellow
if (Test-Path "$TargetDir\.agent") {
    Write-Host "⚠ .agent folder already exists in target" -ForegroundColor Yellow
    $response = Read-Host "Overwrite? (y/n)"
    if ($response -ne "y") {
        Write-Host "Skipping copy. Using existing .agent folder." -ForegroundColor Yellow
        $skipCopy = $true
    } else {
        Remove-Item -Recurse -Force "$TargetDir\.agent"
        Copy-Item -Recurse "agent" "$TargetDir\.agent"
        Write-Host "✓ Agent folder copied" -ForegroundColor Green
    }
} else {
    Copy-Item -Recurse "agent" "$TargetDir\.agent"
    Write-Host "✓ Agent folder copied" -ForegroundColor Green
}

# Verify installation
Write-Host "`nVerifying installation..." -ForegroundColor Yellow
Write-Host "Discovering skills..." -ForegroundColor Gray
& agent\.venv\Scripts\python.exe "$TargetDir\.agent\core\skill_discovery.py"

Write-Host "`nDiscovering personas..." -ForegroundColor Gray  
& agent\.venv\Scripts\python.exe "$TargetDir\.agent\core\persona_manager.py" --list

# Create activation helper in target
$activateScript = @"
@echo off
echo Activating Skills ^& Cowork environment...
call .agent\.venv\Scripts\activate.bat
echo.
echo ✓ Environment activated!
echo.
echo Quick commands:
echo   python .agent\core\skill_discovery.py
echo   python .agent\core\persona_manager.py --list
echo.
"@

$activateScript | Out-File -FilePath "$TargetDir\activate_skills.bat" -Encoding ASCII
Write-Host "✓ Created activation script in target directory" -ForegroundColor Green

# Success message
Write-Host "`n" + ("="*60) -ForegroundColor Green
Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green  
Write-Host ("="*60) -ForegroundColor Green
Write-Host ""
Write-Host "Skills & Cowork system is now installed at:" -ForegroundColor Cyan
Write-Host "  $((Resolve-Path $TargetDir).Path)\.agent" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. cd $TargetDir" -ForegroundColor White
Write-Host "  2. .\activate_skills.bat" -ForegroundColor White
Write-Host "  3. Read: .agent\QUICKSTART.md" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Your system is ready to use!" -ForegroundColor Green
