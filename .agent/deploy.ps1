# deploy.ps1 - Personal AI OS Deployment Script
# Run this on a new system to set up the agent

param(
    [switch]$Full,
    [switch]$SkipVenv,
    [switch]$Verify
)

Write-Host "==================================" -ForegroundColor Cyan
Write-Host " Personal AI OS Deployment Script" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$agentDir = ".agent"

# Check we're in the right directory
if (-not (Test-Path $agentDir)) {
    Write-Host "ERROR: .agent folder not found. Run from workspace root." -ForegroundColor Red
    exit 1
}

# Step 1: Create virtual environment
if (-not $SkipVenv) {
    Write-Host "[1/4] Creating virtual environment..." -ForegroundColor Yellow
    
    if (Test-Path "$agentDir\.venv") {
        Write-Host "   Virtual environment already exists" -ForegroundColor Gray
    }
    else {
        python -m venv "$agentDir\.venv"
        Write-Host "   Created $agentDir\.venv" -ForegroundColor Green
    }
    
    # Activate
    Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
    & "$agentDir\.venv\Scripts\Activate.ps1"
    Write-Host "   Activated" -ForegroundColor Green
}
else {
    Write-Host "[1-2/4] Skipping virtual environment" -ForegroundColor Gray
}

# Step 3: Install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
if (Test-Path "$agentDir\requirements.txt") {
    pip install -r "$agentDir\requirements.txt" -q
    Write-Host "   Dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "   No requirements.txt found, installing core deps" -ForegroundColor Gray
    pip install pyyaml requests python-frontmatter pandas openpyxl -q
}

# Step 4: Discover skills
Write-Host "[4/4] Discovering skills..." -ForegroundColor Yellow
python "$agentDir\core\skill_discovery.py"

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host " Deployment Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan

# Verification
if ($Verify) {
    Write-Host ""
    Write-Host "Running verification..." -ForegroundColor Yellow
    
    # Check venv
    $venvExists = Test-Path "$agentDir\.venv"
    Write-Host "  [$(if($venvExists){'✓'}else{'✗'})] Virtual environment" -ForegroundColor $(if ($venvExists) { 'Green' }else { 'Red' })
    
    # Check skills
    $skillCount = (Get-ChildItem "$agentDir\skills" -Directory).Count
    Write-Host "  [✓] Skills discovered: $skillCount" -ForegroundColor Green
    
    # Check personas
    $personaCount = (Get-ChildItem "$agentDir\personas" -Filter "*.json").Count
    Write-Host "  [✓] Personas available: $personaCount" -ForegroundColor Green
    
    # Check config
    $configExists = Test-Path "$agentDir\config\mcp_config.json"
    Write-Host "  [$(if($configExists){'✓'}else{'!'})] Config file $(if(-not $configExists){'(create from .env)'})" -ForegroundColor $(if ($configExists) { 'Green' }else { 'Yellow' })
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Copy .env.example to .env and add your API keys"
Write-Host "  2. Activate: .agent\.venv\Scripts\Activate.ps1"
Write-Host "  3. Start using skills in Antigravity!"
Write-Host ""
