---
description: Create setup (Obsidian notes + Linear project) for new DE Zoomcamp module
---

# Create Module Setup

Creates complete module setup with linked Obsidian notes and Linear project.

## Usage

"Create setup for Module 3: Data Warehousing"
"Setup Module 5"

## What It Does

1. Creates Obsidian note from module template
2. Creates Linear project  
3. Creates standard Linear tasks for module
4. Links them together (IDs in frontmatter)

## Steps

### 1. Create Obsidian Module Note

**Action:** Create note in `DataEngineering/Modules/`

**Template:** `module-template.md`

**Frontmatter:**
```yaml
module: {number}
title: {name}
status: not-started
linear_project_id: "{LINEAR_PROJECT_ID}"
start_date: {today}
```

**Filename:** `Module-{N:02d}-{slug}.md`

Example: `Module-03-Data-Warehousing.md`

---

### 2. Create Linear Project

**Action:** Create project via Linear MCP

**Name:** "Module {N}: {Title}"

**Description:**
```
Data Engineering Zoomcamp - Module {N}

📖 Notes: obsidian://vault/Areas/DataEngineering/Modules/Module-{N}
🎯 Goals: [list learning goals]
```

**Team:** Data Engineering

---

### 3. Create Standard Module Tasks

**Issues to create:**

1. **Watch lecture videos**
   - Title: `[Module {N}] Watch all lecture videos`
   - Labels: `module-{n}`, `learning`
   - Project: Link to module project

2. **Complete exercises**
   - Title: `[Module {N}] Complete practice exercises`
   - Labels: `module-{n}`, `practice`


3. **Homework assignment**
   - Title: `[Module {N}] Complete homework`
   - Labels: `module-{n}`, `homework`
   - Priority: High

4. **Review and reflect**
   - Title: `[Module {N}] Weekly reflection`
   - Labels: `module-{n}`, `reflection`

---

### 4. Link Everything

**Update Obsidian note frontmatter:**
```yaml
linear_project_id: "{PROJECT_ID}"
```

**Update Linear project description:**
```
📖 Obsidian Notes: obsidian://vault/DE/Modules/Module-{N}
```

---

## Example Result

**Obsidian:**
```
DataEngineering/Modules/Module-03-Data-Warehousing.md
```

**Linear:**
```
Project: Module 3: Data Warehousing
  ├── [Module 3] Watch all lecture videos
  ├── [Module 3] Complete practice exercises
  ├── [Module 3] Complete homework
  └── [Module 3] Weekly reflection
```

**Both linked bidirectionally** ✅

---

## Success Criteria

- ✅ Obsidian note created with template
- ✅ Linear project created
- ✅ 4 standard tasks created in Linear
- ✅ Frontmatter has Linear project ID
- ✅ Linear description has Obsidian link
