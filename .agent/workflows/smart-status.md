---
description: Check automation status and trigger smart sync
---

# Smart Status Check

Uses Time and Obsidian State to determine the best next action.

## Usage

```
/smart-status
"Check status"
"What should I do?"
```

## Workflow

**1. Call Smart Sync**

Triggers the `obsidian_linear_sync` skill in smart mode:

- **Check Time**: Uses `time` MCP.
- **Check Logs**: Reads `System/sync_log.md`.

**2. Decision Tree**

- **If > 4 hours since last sync**:
  - Agent: "It's been 4 hours. Syncing tasks..."
  - Action: Execute Sync.

- **If > 5 PM and not wrapped**:
  - Agent: "It's end of day. Ready to wrap up?"
  - Action: Propose `/wrap-session`.

- **Else**:
  - Agent: "All systems nominal. Last sync: {time}"
