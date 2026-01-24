---
name: Dev.to Publisher
description: Publish blog posts to Dev.to from session logs and weekly summaries
version: 1.1.0
triggers:
  - publish to devto
  - create blog post
  - share on devto
  - write article
examples:
  - "Publish this session to Dev.to"
  - "Create a blog post from my learning today"
  - "Share this summary on Dev.to"
  - "Write an article about BigQuery partitioning"
context_hints:
  - user mentions Dev.to or blogging
  - user wants to share their learning publicly
  - user mentions creating articles or posts
  - learning-in-public sharing request
priority: 6
conflicts_with: []
capabilities:
  - article_creation
  - session_conversion
  - weekly_summaries
dependencies:
  - requests>=2.31.0
auto_load: true
---

# Dev.to Publisher Skill

Publish your learning journey to Dev.to automatically.

## 🎯 Purpose

Convert session logs and weekly summaries into Dev.to blog posts, expanding your "Learning in Public" reach beyond GitHub.

## 🚀 Capabilities

### 1. **Session Log → Blog Post**
Converts daily session logs into formatted Dev.to articles:
- Adds proper frontmatter
- Applies consistent tags
- Creates as draft for review

### 2. **Weekly Summary → Blog Post**
Transforms weekly summaries into recap posts:
- Stats and highlights
- Series: "Weekly Recaps"

### 3. **Draft Management**
- Creates as draft by default (safety first!)
- Review before publishing
- Bulk publish ready drafts

## 💡 Usage Examples

### Example 1: Publish Session Log
```
User: "Publish today's session to Dev.to"
Agent: *Converts session log to article, creates as draft*
```

### Example 2: Check Connection
```powershell
python .agent\skills\devto_publisher\scripts\devto_publisher.py --test
```

### Example 3: Preview Article
```powershell
python .agent\skills\devto_publisher\scripts\devto_publisher.py --publish vault\Sessions\2026-01-17_0627.md
```

## 🔒 Safety Features

- **Draft by default** — Never auto-publishes
- **Secrets check** — Scans for API keys before publishing
- **Preview mode** — Review content before creating

## 📋 Configuration

Add Dev.to API key to `.agent/config/mcp_config.json`:
```json
{
  "devto": {
    "api_key": "YOUR_DEVTO_API_KEY",
    "username": "your_username"
  }
}
```

Get your API key: https://dev.to/settings/extensions
