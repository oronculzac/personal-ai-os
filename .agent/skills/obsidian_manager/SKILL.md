---
name: Obsidian Manager
description: Manage Obsidian vault notes via MCP - create, read, search notes and manage knowledge base
version: 1.1.0
triggers:
  - create obsidian note
  - search vault
  - read note
  - update knowledge base
  - find in notes
examples:
  - "Create a note about Spark partitioning"
  - "Search my vault for BigQuery notes"
  - "Show my Module 3 notes"
  - "Create today's daily note"
context_hints:
  - user mentions Obsidian or note-taking
  - user wants to search their knowledge base
  - user asks to create or find notes
  - user references their vault
priority: 7
conflicts_with: []
capabilities:
  - note_creation
  - vault_search
  - note_reading
  - metadata_management
  - template_application
dependencies:
  - requests>=2.31.0
  - python-frontmatter>=1.0.0
auto_load: true
---

# Obsidian Manager Skill

Manage your Obsidian knowledge base via MCP (Model Context Protocol).

## 🎯 Purpose

Seamlessly create, read, and search Obsidian notes during conversations with Antigravity, enabling knowledge management automation.

## 🚀 Capabilities

### 1. **Note Creation**
- Create notes from templates
- Add frontmatter metadata
- Auto-link related notes
- Organize in folder structure

### 2. **Vault Search**
- Search by content
- Search by tags
- Search by metadata
- Find backlinks

### 3. **Note Management**
- Read existing notes
- Update note content
- Update metadata
- Move/rename notes

### 4. **Template System**
- Daily note templates
- Module note templates
- Homework templates
- Custom templates

## 💡 Usage Examples

### Example 1: Create Daily Note
```
User: "Create today's daily note"
Assistant: *Creates note in Daily/ with template*
```

### Example 2: Search Vault
```
User: "Find all notes about Spark"
Assistant: *Searches vault and returns matching notes*
```

### Example 3: Create Module Note
```
User: "Create note for Module 3: Data Warehousing"
Assistant: *Creates structured note from template*
```

## 📋 Templates

### Daily Note Template
```markdown
---
date: {{date}}
type: daily
linear_tasks: []
---

# {{date}}

## 📝 Learning Today

## ✅ Tasks
- [ ] 

## 💡 Insights

## 🔗 Links
```

### Module Note Template  
```markdown
---
module: {{module_number}}
title: {{title}}
status: not-started
linear_project_id: ""
start_date: {{date}}
---

# Module {{module_number}}: {{title}}

## Overview

## Learning Goals
- [ ] 

## Notes

## Resources
```

## 🔧 Configuration

MCP configuration at `.agent/config/mcp_config.json`:
```json
{
  "obsidian": {
    "vault_path": "C:\\Users\\Oron Culzac\\ObsidianVault",
    "api_url": "http://localhost:27124",
    "api_key": "YOUR_KEY"
  }
}
```

## 🎓 Use Cases for DE Zoomcamp

- **Daily Learning Journal**: Auto-create daily notes
- **Module Documentation**: Structure learning by module
- **Code Snippets**: Save and organize code examples
- **Concept Maps**: Link related DataEngineering concepts
- **Weekly Reviews**: Generate summaries

## 📖 Common Commands

Via conversation:
- "Create daily note"
- "Search vault for BigQuery"
- "Show me my Module 3 notes"
- "Create note about dbt best practices"

## 🔒 Security

- API key stored securely in config
- Local vault access only
- No external data transmission
