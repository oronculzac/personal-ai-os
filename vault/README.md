# Obsidian Vault Structure

This vault follows a **PARA-inspired** organization system for optimal knowledge management.

## 📁 Folder Structure

| Folder | Purpose | Examples |
|--------|---------|----------|
| **00-Inbox** | Quick capture, unsorted notes | Ideas, snippets, quick thoughts |
| **01-Projects** | Active projects with deadlines | DE-Zoomcamp, Personal-OS |
| **02-Areas** | Ongoing responsibilities | Learning, Career, Health |
| **03-Resources** | Reference material | Cheatsheets, Guides, Reports |
| **04-Archive** | Completed/inactive items | Old docs, finished projects |
| **Journals** | Time-based entries | Daily notes, Session logs |
| **Plans** | Implementation plans & tasks | Synced from AI artifacts |
| **Templates** | Note templates | Daily note, Project, Module |

## 🔄 Workflows

### Daily Notes
- Location: `Journals/Daily/YYYY-MM-DD.md`
- Auto-synced with Linear via `/sync-obsidian-linear`

### Session Logs
- Location: `Journals/Sessions/YYYY-MM-DD_HHMM.md`
- Created by `/wrap-session` workflow

### Implementation Plans
- Location: `Plans/{date}_{topic}_plan.md`
- Synced from `.gemini/brain/` via artifact_sync skill

## 🎯 Quick Reference

- **New idea?** → `00-Inbox`
- **Starting a project?** → `01-Projects/{project-name}/`
- **Learning something?** → `02-Areas/Learning/` or project folder
- **Need to reference later?** → `03-Resources/`
- **Done with something?** → `04-Archive/`

## 🔗 Integration

This vault integrates with:
- **Linear** for task management
- **AI Agent** for artifact syncing
- **GitHub** for publishing session logs
