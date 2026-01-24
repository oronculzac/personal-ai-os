---
name: Obsidian Linear Sync
description: Sync tasks between Obsidian notes and Linear issues. Currently Obsidian→Linear. Use when user says "sync tasks", "add to linear", or "sync obsidian".
version: 2.1.0
triggers:
  - sync obsidian linear
  - sync my tasks
  - sync tasks to linear
  - add tasks to linear
  - push tasks to linear
  - update linear from notes
  - smart sync
  - check status
examples:
  - "Sync my daily tasks to Linear"
  - "Add today's tasks to Linear"
  - "Smart check if I need to sync"
  - "What should I do?"
context_hints:
  - user mentions Obsidian and Linear together
  - user has tasks in daily notes that need tracking
  - user mentions syncing or pushing tasks
  - user asks for status or next steps
  - user wants automated checks
priority: 8
conflicts_with:
  - linear_manager
capabilities:
  - task_extraction
  - linear_issue_creation
  - obsidian_file_update
  - linear_to_obsidian_sync
  - smart_state_management
dependencies: []
inputs:
  optional:
    - name: date
      type: string
      description: Specific date to sync (YYYY-MM-DD format)
    - name: note
      type: path
      description: Specific note path to sync instead of daily note
    - name: smart_mode
      type: boolean
      description: If true, checks last_sync time before execution
outputs:
  - name: created
    type: array
    description: List of created Linear issues with identifiers
auto_load: true
---

# Obsidian Linear Sync Skill

Automatically sync tasks between Obsidian notes and Linear issues using pure MCP tool calls.

## 🎯 Purpose

Eliminate manual task duplication. When you create tasks in Obsidian daily notes:
1. **READ**: You read the daily note content.
2. **PARSE**: You identify unchecked tasks `- [ ] Task` without links.
3. **CREATE**: You create Linear issues for them.
4. **UPDATE**: You append the Linear ID `[[LIN-XXX]]` to the task in Obsidian.
5. **LOG**: You update `System/sync_log.md` with the new timestamp.

## 🚀 Usage Workflow

### Smart Sync (Status Check)
Trigger: "Smart sync" or "Check status"
1. **Get Time**: Call `time` server (`get_current_time`).
2. **Read State**: Call `obsidian_read_file` on `System/sync_log.md`.
3. **Logic**:
   - If `Now - last_sync > 4 hours`: **Proceed to Sync**.
   - If `Now > 17:00` (5 PM) AND `last_wrap < Today`: **Suggest Wrap Up**.
   - Else: Report "All up to date".

### Standard Sync (Execution)
1. **Determine Context Date**
   - **Action**: Use `time` server to get current local date.

- **Goal**: Resolve "today" accurately to `YYYY-MM-DD` string.

### 2. Read Note
- Path: `Daily/{YYYY-MM-DD}.md`
- Action: Call `obsidian_read_file` (or `batch_get`).

### 3. Process Content
- Look for lines like `- [ ] Some task description`.
- Ignore lines that already have `[[LIN-Link]]`.

### 4. Loop & CreateIssues
For each new task:
- Call `linear_create_issue(title="Some task description")`.
- Get the `identifier` from the result (e.g., "LIN-123").

### 5. Patch Note
- Call `obsidian_patch_content` or `obsidian_append_content` (if patch not available, read-modify-write with `obsidian_write_file` if safe).
- **Preferred**: Use `obsidian_patch_content` to replace `- [ ] Some task description` with `- [ ] Some task description [[LIN-123]]`.

## 🔧 Configuration

Server is configured in Docker MCP Toolkit.
Ensure `linear`, `obsidian` and `time` servers are enabled.

## 📁 Daily Notes

Daily notes should be in `Daily/YYYY-MM-DD.md` (or your configured path).

## 🔄 Integration

**Morning Routine:**
- Ask: "Sync my daily note tasks to Linear".

**Wrap Session:**
- Ask: "Sync any new tasks I added to Linear".
