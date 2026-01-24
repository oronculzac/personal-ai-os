---
type: implementation_plan
source: C:\Users\Oron Culzac\.gemini\antigravity\brain\319157e1-c402-40b6-9daa-472a9c311ede\implementation_plan.md
synced: 2026-01-17T18:28:25.492653
topic: system review optimization plan
---

# System Review & Optimization Plan

Comprehensive improvements to Python environment handling, artifact naming, and Obsidian vault organization.

---

## User Review Required

> [!IMPORTANT]
> **Obsidian Folder Structure Change**: I'm proposing to reorganize your vault from 8 folders to a cleaner PARA-inspired structure. This affects where notes are stored. Please review the proposed structure below.

> [!WARNING]
> **Breaking Change**: Workflow commands will change from `python script.py` to `.agent\.venv\Scripts\python.exe script.py`. Existing muscle memory for direct Python calls will need adjustment.

---

## Proposed Changes

### Component 1: Python Virtual Environment Standardization

**Problem**: All 6 workflows and 22 scripts currently run Python globally, risking package conflicts.

**Solution**: Use the existing `.agent\.venv` virtual environment consistently.

---

#### [NEW] [run_python.ps1](file:///c:/Users/Oron Culzac/antigravity_general/.agent/scripts/run_python.ps1)

Wrapper script that automatically uses venv Python:
```powershell
# Runs Python script using .agent\.venv
$venvPython = "$PSScriptRoot\..\\.venv\\Scripts\\python.exe"
& $venvPython @args
```

---

#### [MODIFY] [wrap-session.md](file:///c:/Users/Oron Culzac/antigravity_general/.agent/workflows/wrap-session.md)

Update Python calls to use venv:
```diff
-python .agent\skills\session_wrapper\scripts\session_wrapper.py --dry-run
+.agent\.venv\Scripts\python.exe .agent\skills\session_wrapper\scripts\session_wrapper.py --dry-run
```

---

#### [MODIFY] [sync-obsidian-linear.md](file:///c:/Users/Oron Culzac/antigravity_general/.agent/workflows/sync-obsidian-linear.md)

Same pattern - use venv Python for all script calls.

---

#### [MODIFY] [morning-routine.md](file:///c:/Users/Oron Culzac/antigravity_general/.agent/workflows/morning-routine.md)

Update any Python script calls to use venv.

---

#### [MODIFY] [create-module-setup.md](file:///c:/Users/Oron Culzac/antigravity_general/.agent/workflows/create-module-setup.md)

Update Python calls to use venv.

---

#### [MODIFY] [onboard-project.md](file:///c:/Users/Oron Culzac/antigravity_general/.agent/workflows/onboard-project.md)

Update Python calls to use venv.

---

### Component 2: Intuitive Artifact Naming & Obsidian Integration

**Problem**: Artifacts like `task.md` and `implementation_plan.md` get created in the `.gemini/brain/<conversation-id>/` folder with generic names, making them hard to find later.

**Solution**: 
1. After creating artifacts, copy them to Obsidian with descriptive names
2. Use format: `{date}_{topic}_plan.md` or `{date}_{topic}_task.md`

---

#### [NEW] [artifact_sync.py](file:///c:/Users/Oron Culzac/antigravity_general/.agent/core/artifact_sync.py)

Script to copy artifacts to Obsidian with intuitive names:
- Detects artifact type (plan, task, walkthrough)
- Extracts topic from content
- Copies to appropriate Obsidian folder

---

#### Recommended Workflow Integration

When creating implementation plans:
1. Create in `.gemini/brain/<id>/implementation_plan.md` (as usual)
2. Copy to `vault/Plans/{date}_{topic}_plan.md`
3. Add backlink in daily note

---

### Component 3: Obsidian Vault Structure Optimization

**Current Structure** (8 folders):
```
vault/
├── Areas/          # AI, DataEngineering
├── Journals/       # Daily, Sessions  
├── Projects/       # Empty
├── Skills/         # Minimal content
├── Social/         # Empty
├── System/         # task.md, docs, images
├── Templates/      # 4 templates
└── .obsidian/      # Config
```

**Problems Identified**:
1. `Projects/`, `Social/`, `Skills/` are empty/underused
2. `System/` is a dumping ground (task.md, images, docs mixed)
3. No clear place for implementation plans/walkthroughs
4. `Areas/` has only 2 subfolders

---

#### Proposed Optimized Structure (PARA-inspired):

```
vault/
├── 00-Inbox/           # Quick capture, unsorted notes
├── 01-Projects/        # Active projects with deadlines
│   ├── DE-Zoomcamp/    # Data Engineering Zoomcamp
│   └── Personal-OS/    # This system development
├── 02-Areas/           # Ongoing areas of responsibility  
│   ├── Learning/       # Courses, tutorials
│   └── Career/         # Professional development
├── 03-Resources/       # Reference material
│   ├── Cheatsheets/    # Quick references
│   └── Guides/         # How-tos
├── 04-Archive/         # Completed/inactive items
├── Journals/           # Keep as-is (well-structured)
│   ├── Daily/
│   └── Sessions/
├── Plans/              # NEW: Implementation plans, tasks
├── Templates/          # Keep as-is
└── .obsidian/
```

**Key Changes**:
- **Numbered prefixes**: Ensures consistent ordering
- **`00-Inbox`**: Landing zone for quick capture
- **`Plans/`**: Dedicated home for implementation plans and task lists
- **Merged `Skills/` → `03-Resources/`**: Better context
- **Merged `Social/` → `01-Projects/` or delete**: If needed for content creation

---

## Verification Plan

### Automated Tests

None existing. Will verify manually.

### Manual Verification

**1. Venv Wrapper Test**
```powershell
# After creating run_python.ps1, test it works:
.agent\scripts\run_python.ps1 --version
# Expected: Python 3.x.x from venv

# Test a skill script:
.agent\scripts\run_python.ps1 .agent\skills\obsidian_linear_sync\scripts\sync.py --dry-run
# Expected: Script runs without import errors
```

**2. Workflow Test**
- Run `/wrap-session` with `--dry-run`
- Verify it uses venv Python (check for import errors)

**3. Obsidian Structure**
- After reorganization, verify:
  - Daily notes still work (path didn't change in Journals/)
  - Templates still accessible
  - Existing notes moved correctly

---

## Questions for You

1. **Obsidian structure**: Do you prefer the numbered prefix approach (`01-Projects/`) or plain names (`Projects/`)? The numbers keep folders sorted consistently.

2. **Artifact location in Obsidian**: Should plans go in:
   - `vault/Plans/` (dedicated folder)
   - `vault/01-Projects/{project-name}/plans/` (per-project)
   - Both (copy to both locations)

3. **Migration scope**: Should I migrate existing notes to new structure, or just set up the structure for new notes going forward?
