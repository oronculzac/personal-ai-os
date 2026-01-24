# Quick Reference Card
## Personal AI OS - Essential Commands

---

## 🎯 Core Workflows

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| **`/morning-routine`** ⭐ | Start of every day | Pulls Linear tasks, reviews yesterday, sets priorities |
| **`/wrap-session`** ⭐ | End of every session | Creates log, publishes to GitHub, generates social posts |
| **`/onboard-project`** | New project/course | Sets up git + Linear + Obsidian structure |
| **`/sync-obsidian-linear`** | Manual sync needed | Bidirectional task sync between systems |
| **`/create-module-setup`** | New course module | Creates module notes + Linear project |
| **`/setup-skills-cowork`** | New workspace | Deploys Skills & Cowork system |

---

## 💬 Natural Language Commands

| Say This | AI Does |
|----------|---------|
| "Continue with LIN-45" | Loads task context from Linear + Obsidian + Git |
| "Show my tasks" | Displays current Linear tasks |
| "Create note for Module 3" | Creates structured Obsidian note |
| "Publish to GitHub" | Routes & publishes current work |
| "What did I work on yesterday?" | Reviews last session log |
| "Create task for homework" | Creates Linear issue |

---

## ⚡ Automatic Triggers

### Morning Routine (`/morning-routine`)
1. ✅ Fetches "In Progress" Linear tasks
2. ✅ Reads yesterday's session log
3. ✅ Shows weekly stats
4. ✅ Suggests top 3 priorities
5. ✅ Optional: Latest tech trend research

### Wrap Session (`/wrap-session`)
1. ✅ Analyzes `git log` and `git diff`
2. ✅ Links Linear tasks worked on
3. ✅ Detects "side quests" (drift from ticket)
4. ✅ Recommends publish target with confidence
5. ✅ Creates session log in Obsidian
6. ✅ Generates Twitter thread + LinkedIn post
7. ✅ Publishes to GitHub (with approval)

---

## 📊 System Integration Points

```
┌──────────────┐      ┌──────────────┐
│   Obsidian   │◄────►│    Linear    │
│  (Knowledge) │      │   (Tasks)    │
└──────┬───────┘      └──────┬───────┘
       │                     │
       │   ┌────────────┐    │
       └──►│  Session   │◄───┘
           │  Wrapper   │
           └─────┬──────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
  ┌──────────┐      ┌──────────┐
  │  GitHub  │      │ Dev.to   │
  │  (Code)  │      │  (Blog)  │
  └──────────┘      └──────────┘
```

---

## 📁 Publishing Routes

| Content Type | Confidence | Target Repo |
|--------------|------------|-------------|
| New skill (SKILL.md + scripts) | 90% | `personal-ai-os` |
| Homework completed | 85% | `de-zoomcamp-2026` |
| Side quest detected | 70% | `learning-logs` |
| ≥3 files modified | 60% | `learning-logs` |

---

## 🗓️ Recommended Daily Cadence

### 🌅 Morning (09:00)
```bash
/morning-routine
# Review priorities
# Start with top task
```

### ⚙️ During Work
- Reference Linear tasks: "Work on LIN-45"
- AI maintains context automatically
- Create Obsidian notes as needed

### 🌙 Evening (17:00)
```bash
/wrap-session
# Review publish recommendation
# Approve → Auto-publish
# Optional: Publish to Dev.to
```

### 📅 Weekly (Friday)
```powershell
python .agent\skills\session_wrapper\scripts\weekly_summary.py
```

---

## 🔑 Key Rules for Seamless Flow

### ✅ DO's
- ✅ Always start day with `/morning-routine`
- ✅ Always end session with `/wrap-session`
- ✅ Reference Linear task IDs in conversations
- ✅ Trust auto-publish detection (90%+ accuracy)
- ✅ Use `/onboard-project` for new initiatives
- ✅ Sync Obsidian ↔ Linear daily

### ❌ DON'Ts
- ❌ Don't manually commit to GitHub (let `/wrap-session` handle it)
- ❌ Don't skip morning routine (loses context)
- ❌ Don't forget to wrap sessions (breaks learning log)
- ❌ Don't manually create Linear tasks for daily notes (use sync)

---

## 🎯 Context Loading

When you say:
```
"Continue with LIN-45"
```

AI automatically:
1. Fetches task details from Linear
2. Finds linked Obsidian notes
3. Reviews recent git commits
4. Provides context summary
5. Suggests next steps

---

## 📝 Obsidian ↔ Linear Sync

**Before:**
```markdown
# Daily/2026-01-17.md
- [ ] Practice BigQuery partitioning
- [ ] Review dbt docs
```

**After `/sync-obsidian-linear`:**
```markdown
# Daily/2026-01-17.md
- [ ] Practice BigQuery partitioning [[LIN-101]]
- [ ] Review dbt docs [[LIN-102]]
```

**Status sync:**
- ✅ Check in Obsidian → Marks done in Linear
- ✅ Complete in Linear → Updates Obsidian
- 🔄 Bidirectional, Linear wins conflicts

---

## 🚀 Project Structure Created by `/onboard-project`

```
antigravity_general/
├── projects/
│   └── {project-name}/
│       ├── src/
│       ├── docs/
│       ├── notebooks/
│       ├── README.md
│       ├── .gitignore
│       └── .git/
│
├── vault/
│   └── Projects/
│       └── {ProjectName}/
│           └── {ProjectName}.md
│
└── Linear:
    └── "{ProjectName}" project
```

---

## 📊 Session Log Output

Created at: `vault/Sessions/YYYY-MM-DD_HHMM.md`

Contains:
- 📋 What I Did (technical summary)
- 💡 What I Learned (conceptual insights)
- 🔗 Linear Tasks worked on
- 📁 Files modified
- 🐦 Twitter thread (auto-generated)
- 💼 LinkedIn post (auto-generated)

---

## 🎓 Skills Available (Use Naturally)

- **Session Wrapper** — Auto-document sessions
- **GitHub Publisher** — Route & publish content
- **Linear Manager** — Manage Linear tasks via MCP
- **Obsidian Manager** — Manage notes via MCP
- **Dev.to Publisher** — Publish blog posts
- **Code Template Generator** — Generate DE templates
- **Environment Setup Helper** — Automate dependencies
- **File Organizer** — Intelligent file management
- **Web Scraper** — Extract website data

Just mention what you need: "Generate a Spark template" or "Search my vault for BigQuery notes"

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Tasks not syncing | Run `/sync-obsidian-linear` |
| Context lost | Say "Continue with LIN-XX" |
| Forgot to wrap session | Run `/wrap-session` anytime |
| Need to review yesterday | Check `vault/Sessions/` |
| Missing priorities | Run `/morning-routine` |

---

## 💾 File Locations

- **Skills:** `.agent/skills/`
- **Workflows:** `.agent/workflows/`
- **Session Logs:** `vault/Sessions/`
- **Projects:** `projects/`
- **Obsidian Notes:** `vault/`
- **Config:** `.agent/config/mcp_config.json`

---

## ⚡ Power Tips

1. **Consistent habits** — Morning routine + Wrap session = Success
2. **Trust automation** — 90%+ accuracy on publish detection
3. **Linear task IDs** — Always reference for auto-context
4. **Side quests are OK** — System tracks drift automatically
5. **Publish often** — Maintains GitHub streak + learning visibility

---

> **Remember:** The system works best with **consistent workflow execution**. Trust the automation, use the workflows, maintain the rhythm.

**Morning → Work → Evening → Repeat** 🔄
