---
description: Sync daily tasks between Obsidian and Linear
---

# Sync Obsidian ↔ Linear

Bidirectional sync of tasks between Obsidian daily notes and Linear issues.

## Usage

"Sync my tasks"
"Add today's tasks to Linear"

## What It Does

Scans Obsidian daily notes for unchecked tasks and creates corresponding Linear issues, maintaining links between both systems.

## Direction 1: Obsidian → Linear

### Steps

**1. Get Today's Daily Note**

Path: `Daily/{YYYY-MM-DD}.md`

**2. Extract Unchecked Tasks**

Find all lines matching:
```markdown
- [ ] Task description
```

Exclude tasks that already have Linear IDs:
```markdown
- [ ] Task [[LIN-123]]  ← Skip this
```

**3. For Each New Task:**

Create Linear issue:
- **Title:** Task text
- **Project:** From note frontmatter `linear_project` (if specified)
- **Labels:** `auto-created`, `daily`, `module-{n}` (if in module context)
- **Description:**
  ```
  Auto-created from Obsidian daily note
  Date: {date}
  Note: obsidian://vault/Daily/{date}
  ```

**4. Update Obsidian Note**

Replace task line with:
```markdown
- [ ] Task description [[LIN-{ID}]]
```

---

## Direction 2: Linear → Obsidian

### Steps

**1. Query Linear**

Get issues:
- Created today OR
- Updated today OR  
- Status changed today

Filter: `label: daily` OR `label: auto-created`

**2. For Each Issue:**

Check if already in today's note:
- Search for `[[LIN-{ID}]]`
- If found: Update status if needed
- If not found: Add to "From Linear" section

**3. Update Task Status**

If Linear issue completed:
```markdown
- [x] Task description [[LIN-123]] ✅
```

---

## Frontmatter Usage

Daily note can specify default Linear project:

```yaml
---
date: 2026-01-20
linear_project: "PRO-123"  ← All tasks go here by default
---
```

Inline override:
```markdown
- [ ] Study Spark #module-5  ← Project inferred from tag
```

---

## Conflict Resolution

**If task exists in both but status differs:**

Priority: **Linear wins** (source of truth for task status)

**If task deleted from Obsidian:**

Keep in Linear with note: "(Removed from daily note)"

**If task completed in Linear:**

Mark complete in Obsidian

---

## Example

**Before sync:**

Obsidian:
```markdown
# 2026-01-20

## Tasks
- [ ] Practice BigQuery partitioning
- [ ] Review dbt docs
- [x] Watch Module 3 videos [[LIN-45]]
```

Linear:
```
No matching tasks
```

**After sync:**

Obsidian:
```markdown
# 2026-01-20

## Tasks
- [ ] Practice BigQuery partitioning [[LIN-101]]
- [ ] Review dbt docs [[LIN-102]]
- [x] Watch Module 3 videos [[LIN-45]]
```

Linear:
```
LIN-101: Practice BigQuery partitioning (todo)
LIN-102: Review dbt docs (todo)
LIN-45: Watch Module 3 videos (done) ← Status synced
```

---

## Frequency

**Recommended:** 
- Morning: Pull from Linear → Obsidian
- Evening: Push from Obsidian → Linear

**Manual trigger:** "Sync my tasks"

**Auto:** Can run on schedule (optional)

---

## Success Criteria

- ✅ New Obsidian tasks create Linear issues
- ✅ Linear issue IDs added to Obsidian
- ✅ Status updates sync both ways
- ✅ No duplicate tasks created
- ✅ Links maintained between systems
