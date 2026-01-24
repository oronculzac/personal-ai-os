# Feature Status Report: Medium Priority Features

## 🎯 Overview

This report documents the current implementation status of the "Medium Priority" features from the system analysis.

---

## Feature 1: `/onboard-project` Workflow

### ✅ What's Implemented

**Workflow Documentation:** Fully documented at `.agent/workflows/onboard-project.md`

**Capabilities Defined:**
- Get project details (name, description)
- Create project folder structure (`projects/{name}/src`, `docs`, `notebooks`)
- Initialize git repository
- Create Obsidian folder and project note
- Create Linear project (optional)
- Display confirmation summary

**Workflow Triggers:**
- "onboard new project"
- "create new project"
- "add project"

### ❌ What's Missing

**Implementation Scripts:**
- No Python automation script exists
- Commands are documented but manual
- No Linear API integration for project creation

### 🔧 Implementation Status

**Status:** 🟡 **Partially Implemented**
- **Documentation:** ✅ Complete
- **Workflow Definition:** ✅ Complete
- **Automation Scripts:** ❌ Not implemented
- **Linear Integration:** ❌ Not implemented

### 📝 What Needs to Be Built

1. **Create automation script:** `.agent/workflows/scripts/onboard_project.py`
   ```python
   # Features needed:
   # - Parse project name and description
   # - Create folder structure
   # - Initialize git with .gitignore
   # - Create README.md with description
   # - Create Obsidian project note from template
   # - Optional: Create Linear project via API
   ```

2. **Linear API integration:**
   - Requires team admin permissions
   - Use existing `linear_client.py` from skills
   - Create project and return project ID

3. **Obsidian note template:**
   - Standard project overview template
   - Include frontmatter with Linear project ID

### 🚀 Usage (Current State)

**Current:** Semi-automated - User needs to manually run commands shown in workflow

**Example Current Flow:**
```
You: /onboard-project
AI: [Reads workflow, asks for details]
You: "portfolio-website"
AI: [Shows PowerShell commands to run]
You: [Manually execute commands]
```

**Desired:** Fully automated - AI executes everything

**Example Desired Flow:**
```
You: /onboard-project
AI: "Project name?"
You: "portfolio-website"
AI: "Description?"
You: "Personal portfolio site"
AI: [Automatically creates everything]
AI: "✅ Created! Location: projects/portfolio-website, Linear: PRO-45, Obsidian: Projects/Portfolio Website"
```

---

## Feature 2: `/sync-obsidian-linear` Workflow

### ✅ What's Implemented

**Workflow Documentation:** Fully documented at `.agent/workflows/sync-obsidian-linear.md`

**Capabilities Defined:**
- Bidirectional sync between Obsidian and Linear
- Extract unchecked tasks from Obsidian daily notes
- Create Linear issues for new tasks
- Add `[[LIN-XX]]` links back to Obsidian
- Sync task status (Linear wins conflicts)

**Workflow Triggers:**
- "Sync my tasks"
- "Add today's tasks to Linear"

### ❌ What's Missing

**Implementation Scripts:**
- No Python sync script exists
- All sync logic is documented but not automated
- No actual Obsidian file parsing
- No Linear issue creation automation

### 🔧 Implementation Status

**Status:** 🟡 **Partially Implemented**
- **Documentation:** ✅ Complete
- **Workflow Definition:** ✅ Complete (182 lines of detailed logic)
- **Automation Scripts:** ❌ Not implemented
- **Obsidian Integration:** ❌ Not implemented
- **Linear Integration:** ✅ Client exists (`linear_client.py`)

### 📝 What Needs to Be Built

1. **Create sync script:** `.agent/workflows/scripts/sync_obsidian_linear.py`
   ```python
   # Features needed:
   # - Parse Obsidian daily notes (vault/Daily/YYYY-MM-DD.md)
   # - Extract tasks: - [ ] Task description
   # - Check if task already has [[LIN-XX]]
   # - Create Linear issues for new tasks
   # - Update Obsidian with [[LIN-XX]] links
   # - Sync status from Linear back to Obsidian
   # - Handle conflicts (Linear wins)
   ```

2. **Obsidian file parsing:**
   - Read markdown files from `vault/Daily/`
   - Extract tasks with regex: `^- \[ \] (.+)$`
   - Detect existing Linear links: `\[\[LIN-\d+\]\]`
   - Update files with new links

3. **Bidirectional sync logic:**
   - Direction 1: Obsidian → Linear (create issues)
   - Direction 2: Linear → Obsidian (update status)
   - Conflict resolution (Linear status wins)

### 🚀 Usage (Current State)

**Current:** Manual - User needs to manually create Linear tasks

**Example Current Flow:**
```
You: /sync-obsidian-linear
AI: [Reads workflow documentation]
AI: "Here's how to sync... [explains manual process]"
You: [Manually create Linear tasks]
You: [Manually add [[LIN-XX]] to each task]
```

**Desired:** Fully automated - AI syncs everything

**Example Desired Flow:**
```
You: /sync-obsidian-linear
AI: [Scans vault/Daily/2026-01-17.md]
AI: "Found 3 unchecked tasks without Linear IDs"
AI: [Creates LIN-101, LIN-102, LIN-103]
AI: [Updates Obsidian file with links]
AI: "✅ Synced! 3 tasks created in Linear, Obsidian updated"
```

---

## Feature 3: Weekly Summaries

### ✅ What's Implemented

**Script Exists:** `.agent/skills/session_wrapper/scripts/weekly_summary.py`

**Status:** ✅ **Fully Implemented**

**Usage:**
```powershell
python .agent\skills\session_wrapper\scripts\weekly_summary.py
```

**Output:**
- Sessions logged this week
- Files modified
- Tasks completed
- Learning topics covered

---

## 📊 Summary Table

| Feature | Documentation | Scripts | Integration | Status |
|---------|---------------|---------|-------------|--------|
| `/onboard-project` | ✅ Complete | ❌ Missing | ❌ Missing | 🟡 30% |
| `/sync-obsidian-linear` | ✅ Complete | ❌ Missing | 🟡 Partial | 🟡 40% |
| Weekly Summaries | ✅ Complete | ✅ Exists | ✅ Works | ✅ 100% |

---

## 🎯 Recommendations

### Priority 1: Implement `/sync-obsidian-linear`

**Why:** High impact, frequently needed
- Daily task sync prevents manual work
- Keeps both systems aligned
- Most requested feature

**Effort:** Medium (2-3 hours)
- Obsidian file parsing
- Linear API calls (client already exists)
- File updating logic

### Priority 2: Implement `/onboard-project`

**Why:** Occasional use but high value
- Ensures consistent project structure
- One-time setup per project
- Prevents "forgot to initialize git" mistakes

**Effort:** Low (1-2 hours)
- Folder creation (simple)
- Git commands (straightforward)
- Linear project creation (API call)

---

## 🚀 Implementation Plan

### Phase 1: Sync Script (Highest Value)

**File:** `.agent/workflows/scripts/sync_obsidian_linear.py`

**Steps:**
1. Read today's daily note from `vault/Daily/`
2. Parse unchecked tasks: `- [ ] Task description`
3. Filter tasks without `[[LIN-XX]]`
4. Create Linear issues using `linear_client.py`
5. Update Obsidian file with `[[LIN-XX]]` links
6. Sync status from Linear back to Obsidian

**Dependencies:**
- `python-frontmatter` (already in session_wrapper)
- `linear_client.py` (already exists)
- Obsidian vault path from config

### Phase 2: Onboard Script (High Value)

**File:** `.agent/workflows/scripts/onboard_project.py`

**Steps:**
1. Prompt for project name (slug format)
2. Prompt for description
3. Create `projects/{name}/` with subdirectories
4. Initialize git with `.gitignore` and `README.md`
5. Create Obsidian project note
6. Optional: Create Linear project
7. Display summary with links

**Dependencies:**
- `gitpython` (already in github_publisher)
- `linear_client.py` (already exists)
- Project templates

---

## 💡 Current Workarounds

While scripts are being built, you can use these workflows manually:

### Manual `/onboard-project`:
1. Create folder: `New-Item -ItemType Directory projects/my-project`
2. Create subdirs: `src/`, `docs/`, `notebooks/`
3. Init git: `git init`, add `.gitignore`, commit
4. Create Obsidian note in `vault/Projects/`
5. Create Linear project manually

### Manual `/sync-obsidian-linear`:
1. Open daily note in Obsidian
2. For each unchecked task:
   - Create Linear issue
   - Add `[[LIN-XX]]` to task in Obsidian

---

## 📝 Bottom Line

**Status:** Both features are **documented** but **not automated**

**What works:**
- `/morning-routine` ✅
- `/wrap-session` ✅
- Weekly summaries ✅

**What needs scripts:**
- `/onboard-project` 🟡
- `/sync-obsidian-linear` 🟡

**Recommendation:** Build sync script first (highest daily value), then onboard script (occasional high value).
