# run_python.ps1 - Wrapper script to run Python using the .agent venv
# Usage: .agent\scripts\run_python.ps1 <script.py> [args...]
#
# This ensures all Python scripts in the Personal AI OS use the virtual
# environment instead of the global Python installation.

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Get the .agent directory (parent of scripts folder)
$agentDir = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $agentDir ".venv\Scripts\python.exe"

# Check if venv exists
if (-not (Test-Path $venvPython)) {
    Write-Host "❌ Virtual environment not found at: $venvPython" -ForegroundColor Red
    Write-Host "   Run: python -m venv .agent\.venv" -ForegroundColor Yellow
    Write-Host "   Then: .agent\.venv\Scripts\pip install -r .agent\requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Run Python with all passed arguments
& $venvPython @Arguments
