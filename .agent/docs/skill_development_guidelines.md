# Skill Development Guidelines

## 🎯 Core Principle: Skills First

**All automation scripts should be organized as skills, not standalone scripts.**

### Why Skills?
1. **Discoverable** — AI auto-loads skills from SKILL.md
2. **Composable** — Other skills can import them
3. **Documented** — SKILL.md provides usage instructions
4. **Maintainable** — Standard structure for all automations
5. **Triggerable** — Natural language commands work automatically

---

## 📁 Skill Structure

Every skill must follow this structure:

```
.agent/skills/{skill_name}/
├── SKILL.md          # Required: Skill documentation
├── scripts/          # Required: Python scripts
│   ├── __init__.py   # Optional: For imports
│   └── main.py       # Main script(s)
├── examples/         # Optional: Usage examples
├── templates/        # Optional: Templates
└── resources/        # Optional: Additional files
```

### SKILL.md Template

```yaml
---
name: Skill Name
description: One-line description
version: 1.0.0
triggers:
  - natural language trigger 1
  - natural language trigger 2
capabilities:
  - capability_1
  - capability_2
dependencies:
  - requests>=2.31.0
auto_load: true
---

# Skill Name

## 🎯 Purpose

What this skill does and why.

## 🚀 Usage

### Via Natural Language
```
"Say this to trigger"
```

### Via Script
```powershell
python .agent\skills\{skill_name}\scripts\main.py [args]
```

## 🔧 Configuration

Configuration details...

## 📋 Examples

Usage examples...
```

---

## 🚫 Never Do This

### ❌ Standalone scripts at root
```
antigravity_general/
├── my_script.py          # BAD - not discoverable
└── some_automation.py    # BAD - no documentation
```

### ❌ Scripts in workflow folder without skill
```
.agent/workflows/scripts/
└── orphan_script.py      # BAD - belongs in a skill
```

### ❌ Undocumented scripts
```
.agent/skills/some_skill/
└── scripts/
    └── magic.py          # BAD - no SKILL.md
```

---

## ✅ Always Do This

### ✅ Create proper skill structure
```
.agent/skills/my_new_feature/
├── SKILL.md              # GOOD - documented
└── scripts/
    └── feature.py        # GOOD - organized
```

### ✅ Include triggers in SKILL.md
```yaml
triggers:
  - my new feature
  - do the feature thing
  - run feature
```

### ✅ Import from other skills
```python
# GOOD - import from sister skill
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'linear_manager' / 'scripts'))
from linear_client import LinearClient
```

---

## 📝 Workflow-Skill Relationship

**Workflows** = High-level human processes (documented in `.agent/workflows/`)
**Skills** = Reusable automation modules (scripts in `.agent/skills/`)

**Pattern:**
- Workflows **call** skills
- Skills **provide** automation
- Workflows **orchestrate** skills

**Example:**
```
/wrap-session (workflow)
  ↓ calls
session_wrapper skill
  ↓ imports
linear_manager skill
  ↓ uses
linear_client.py
```

---

## 🔄 Converting Standalone Scripts

If you have a standalone script, convert it:

1. **Create skill folder:**
   ```powershell
   mkdir .agent\skills\{skill_name}\scripts
   ```

2. **Move script:**
   ```powershell
   mv standalone_script.py .agent\skills\{skill_name}\scripts\main.py
   ```

3. **Create SKILL.md:**
   - Document purpose
   - Add triggers
   - List dependencies

4. **Update imports:**
   - Use relative paths from skill location
   - Import from sister skills

---

## 🎯 Decision Tree: Script or Skill?

```
Is this automation reusable?
├── YES → Create a skill
│   └── Will it be triggered by natural language?
│       ├── YES → Add triggers to SKILL.md
│       └── NO  → Still create skill (for organization)
└── NO  → Is it a one-off utility?
    ├── YES → Put in core/ or as temporary script
    └── NO  → Probably should be a skill
```

---

## 📊 Current Skill Inventory

| Skill | Purpose | Status |
|-------|---------|--------|
| session_wrapper | Auto-document sessions | ✅ Complete |
| github_publisher | Publish to GitHub | ✅ Complete |
| linear_manager | Linear API client | ✅ Complete |
| obsidian_manager | Obsidian API client | ✅ Complete |
| obsidian_linear_sync | Sync tasks | ✅ New |
| devto_publisher | Blog publishing | ✅ Complete |
| code_template_generator | DE templates | ✅ Complete |
| environment_setup_helper | Deps management | ✅ Complete |
| file_organizer | File management | ✅ Complete |
| excel_generator | Spreadsheets | ✅ Complete |
| notebook_manager | Jupyter notebooks | ✅ Complete |
| web_scraper | Data extraction | ✅ Complete |
| example_template | Skill template | 📝 Template |

---

## 🚀 Creating a New Skill (Checklist)

- [ ] Create folder: `.agent/skills/{skill_name}/`
- [ ] Create `scripts/` subfolder
- [ ] Add main script to `scripts/`
- [ ] Create `SKILL.md` with frontmatter
- [ ] Add natural language triggers
- [ ] Document usage examples
- [ ] List dependencies
- [ ] Test script execution
- [ ] Verify AI can discover skill
