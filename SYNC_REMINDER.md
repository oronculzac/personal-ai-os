# 📝 IMPORTANT: Keeping portable_setup Up-to-Date

## Auto-Sync After Changes

**CRITICAL**: After making ANY changes to the Skills & Cowork system, run the sync script to update the portable_setup folder:

```powershell
python sync_portable.py
```

This ensures `portable_setup/` always contains the latest version.

---

## What Changes Require Syncing?

Run `python sync_portable.py` after:

✅ **Adding new skills**
- Created new skill folder in `.agent/skills/`
- Updated skill SKILL.md or scripts

✅ **Modifying personas**
- Changed persona configurations in `.agent/personas/`
- Added new personas

✅ **Updating core scripts**
- Modified `skill_discovery.py`, `persona_manager.py`, `file_agent.py`
- Changed `folder_permissions.py`

✅ **Changing configurations**
- Updated `skill_registry.json`
- Modified `folder_permissions.json`
- Changed any workflow files

✅ **Documentation updates**
- Modified QUICKSTART.md, README.md, or other docs

---

## The Sync Script

**What it does**:
- Copies `.agent/` → `portable_setup/agent/`
- Excludes: `.venv`, `__pycache__`, `backups`, temporary files
- Preserves: All skills, personas, configs, scripts, docs
- Tracks: Last sync time in `.sync_info.json`

**Safety**:
- Only syncs essential files
- Skips environment-specific data
- Non-destructive (cleans and rebuilds)

---

## Workflow

**After making changes**:
```powershell
# 1. Make your changes to .agent/
# (add skill, update persona, modify script, etc.)

# 2. Sync to portable_setup
python sync_portable.py

# 3. portable_setup/ is now ready to deploy
```

**Result**: Your deployment package is always current!

---

## Automation Idea (Future)

Consider adding to the end of skill/persona creation scripts:
```python
# Auto-sync portable_setup
import subprocess
subprocess.run(["python", "sync_portable.py"])
```

Or create a Git pre-commit hook:
```bash
#!/bin/bash
python sync_portable.py
git add portable_setup/
```

---

## Quick Check

**Is portable_setup up-to-date?**
```powershell
Get-Content portable_setup\.sync_info.json
```

Shows last sync time and file count.

---

**Remember**: `portable_setup/` is your deployment package. Keep it synced! 🔄
