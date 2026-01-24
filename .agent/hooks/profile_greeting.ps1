# PowerShell Profile Script for Proactive Agent Behavior
# Add this to your $PROFILE to get morning greetings and reminders
#
# Installation:
#   1. Open PowerShell
#   2. Run: notepad $PROFILE
#   3. Add: . "C:\Users\Oron Culzac\antigravity_general\.agent\hooks\profile_greeting.ps1"
#   4. Save and restart PowerShell

$currentHour = (Get-Date).Hour
$workspacePath = "C:\Users\Oron Culzac\antigravity_general"

# Only show in the main workspace
if ((Get-Location).Path -like "*antigravity*") {
    Write-Host ""
    
    # Morning greeting (6 AM - 11 AM)
    if ($currentHour -ge 6 -and $currentHour -lt 11) {
        Write-Host "Good morning! Ready for your daily standup?" -ForegroundColor Cyan
        Write-Host "   Say: /morning-routine" -ForegroundColor Gray
        Write-Host ""
    }
    # Afternoon check (2 PM - 5 PM)
    elseif ($currentHour -ge 14 -and $currentHour -lt 17) {
        Write-Host "Afternoon check: How is the session going?" -ForegroundColor Yellow
        Write-Host "   Consider: /wrap-session when done" -ForegroundColor Gray
        Write-Host ""
    }
    # Evening wrap reminder (5 PM - 8 PM)
    elseif ($currentHour -ge 17 -and $currentHour -lt 20) {
        Write-Host "Wrapping up for the day?" -ForegroundColor Magenta
        Write-Host "   Do not forget to log your session!" -ForegroundColor Gray
        Write-Host "   Say: wrap up" -ForegroundColor Gray
        Write-Host ""
    }
    
    # Show quick stats
    try {
        $sessionCount = (Get-ChildItem "$workspacePath\vault\Sessions\*.md" -ErrorAction SilentlyContinue).Count
        $lastCommit = git log -1 --format="%s" 2>$null
        if ($lastCommit) {
            Write-Host "Sessions logged: $sessionCount | Last commit: $lastCommit" -ForegroundColor DarkGray
        }
    }
    catch {
        # Silently ignore errors
    }
}
