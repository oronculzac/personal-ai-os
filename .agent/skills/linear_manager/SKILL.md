---
name: Linear Manager
description: Manage Linear issues and projects - create tasks, track progress, sync with notes. Use when user says "create linear task", "track progress", or "setup module".
version: 2.1.0
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

Manage Linear project management with automatic fallback between Docker MCP and Python client.

## 🎯 Purpose

Create, update, and track Linear issues and projects.

## 🔧 Configuration Priority

> [!IMPORTANT]
> **Fallback Order** (use first available):
> 1. **Docker MCP** - If Docker Desktop is running, use `docker mcp tools call linear_*`
> 2. **Python Client** - If Docker unavailable, use `.agent/core/linear_client.py`

### Checking Docker Status
```powershell
docker info  # If fails, Docker isn't running
```

## 🚀 Method 1: Docker MCP (Primary)

When Docker Desktop is running:

```bash
docker mcp tools call create_issue '{"title":"...", "teamId":"...", "description":"..."}'
docker mcp tools call search_issues '{"query":"..."}'
```

**Note**: PowerShell JSON escaping often fails. If you get JSON parsing errors, switch to Method 2.

## 🚀 Method 2: Python Client (Fallback)

When Docker is unavailable or has issues, use the LinearClient:

```python
import sys
sys.path.insert(0, '.agent/core')
from linear_client import LinearClient

client = LinearClient()

# Test connection
result = client.test_connection()
print(f"Teams: {result['teams']}")

# Create issue
team_id = client.get_team_id()
result = client.create_issue(
    title="My task",
    description="Description here",
    team_id=team_id
)
print(f"Created: {result['identifier']}")

# Update state
client.update_state("LIN-123", "Done")
```

### Quick One-Liners

```powershell
# Test connection
python -c "import sys; sys.path.insert(0, '.agent/core'); from linear_client import LinearClient; print(LinearClient().test_connection())"

# Create issue
python -c "import sys; sys.path.insert(0, '.agent/core'); from linear_client import LinearClient; c = LinearClient(); print(c.create_issue('Title', 'Desc', c.get_team_id()))"
```

## 💡 Usage Examples

### Example 1: Create Issue
```
User: "Create Linear task to practice BigQuery partitioning"
Assistant: 
  1. Check if Docker is running
  2. If yes: docker mcp tools call create_issue
  3. If no: use Python client
```

### Example 2: Create Project with Issues
```python
# Use Python for complex operations
client = LinearClient()
team_id = client.get_team_id()

# Create project via GraphQL
mutation = """
mutation CreateProject($name: String!, $teamIds: [String!]!) {
    projectCreate(input: { name: $name, teamIds: $teamIds }) {
        success
        project { id name url }
    }
}
"""
result = client._execute_query(mutation, {"name": "My Project", "teamIds": [team_id]})
```

## 🔒 Security

- **Docker MCP**: Uses OAuth via `docker mcp oauth authorize linear`
- **Python Client**: Uses `LINEAR_API_KEY` from `.env` or environment

## 📁 Files

- `.agent/core/linear_client.py` - Python GraphQL client
- Team ID: `4737f1e3-bf95-4d04-9ff9-795727637507` (Linear-home-workspace)
