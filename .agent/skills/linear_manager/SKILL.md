---
name: Linear Manager
description: Manage Linear issues and projects - create tasks, track progress, sync with notes. Use when user says "create linear task", "track progress", or "setup module".
version: 2.0.0
triggers:
  - create linear issue
  - create linear task
  - update linear
  - track progress
  - create module
  - setup module
  - show my tasks
examples:
  - "Create a Linear task for the BigQuery homework"
  - "Show my in-progress tasks"
  - "Setup Module 4 in Linear"
  - "What tasks do I have this week?"
  - "Create an issue for fixing the sync bug"
context_hints:
  - user mentions Linear or project management
  - user wants to create or track tasks
  - user asks about their todo list or backlog
  - user mentions modules or homework tracking
priority: 8
conflicts_with:
  - obsidian_linear_sync
capabilities:
  - issue_creation
  - project_management
  - task_tracking
  - progress_monitoring
inputs:
  required:
    - name: title
      type: string
      description: Issue title
  optional:
    - name: description
      type: string
      description: Issue description
    - name: project_id
      type: string
      description: Linear project ID to link issue
    - name: labels
      type: array
      description: Labels to apply to the issue
outputs:
  - name: identifier
    type: string
    description: Linear issue ID (e.g., LIN-123)
  - name: url
    type: string
    description: URL to the created issue
auto_load: true
---

# Linear Manager Skill

Manage Linear project management via MCP (Model Context Protocol).

## 🎯 Purpose

Create, update, and track Linear issues and projects directly using the Linear MCP server.

## 🚀 Capabilities

### 1. **Issue Management**
- **Create Issue**: Use `linear_create_issue`
- **Update Issue**: Use `linear_update_issue`
- **Search**: Use `linear_search_issues`

### 2. **Project Management**
- **List Projects**: Use `linear_list_projects`

## 💡 Usage Examples

### Example 1: Create Issue
```
User: "Create Linear task to practice BigQuery partitioning"
Assistant: calls linear_create_issue(title="Practice BigQuery partitioning", teamId="...", labelIds=[...])
```

### Example 2: Track Progress
```
User: "Show my Module 3 tasks"
Assistant: calls linear_search_issues(query="Module 3", filter={...})
```

## 🔧 Configuration

Server is configured in Docker MCP Toolkit.
Ensure you have authorized the connection via `docker mcp oauth authorize linear` if prompted by the tool.

## 🎓 Use Cases for DE Zoomcamp

- **Homework Tracking**: Create issues for each homework question.
- **Module Setup**: Manually create a project and populate it with issues.

## 📖 Common Commands

- "Create task for Spark homework"
- "Show my tasks for this week"
- "Setup Module 5" -> Create a project and add tasks using multiple tool calls.

## 🔒 Security

- Authentication handled by Docker MCP securely.
