---
date: 2026-01-17
type: research-note
tags: [mcp, ai-agents, architecture, research]
status: phase-2-complete
---

# MCP Integration Research & Roadmap

## What is MCP?

**Model Context Protocol (MCP)** is an open standard by Anthropic for connecting AI agents to external tools and data sources via a standardized JSON-RPC interface.

### Key Benefits
- **Universal Interface**: Like USB-C for AI tools
- **Dynamic Discovery**: Tools advertise capabilities automatically
- **Scalability**: Connect to many tools without custom integration
- **Security**: Built-in access control and schema enforcement

## Official MCP Servers (Don't Reinvent!)

| Service | Official Package | Status |
|---------|-----------------|--------|
| Linear | `@linear/mcp-server` (npm) | ✅ Available |
| GitHub | `@github/mcp-server` (npm) | ✅ Available |
| Obsidian | `@mcp/obsidian` (community) | ✅ Available |
| Filesystem | `@mcp/filesystem` (official) | ✅ Available |

**For production use, prefer official npm packages.**

**Issues:**
- Direct API calls mean custom code per service
- No standardized interface
- Tool discovery is manual (SKILL.md files)

## MCP Architecture

```
          ┌─────────────┐
          │   MCP Host  │  (Antigravity AI)
          │  (Agent)    │
          └──────┬──────┘
                 │ JSON-RPC
          ┌──────┴──────┐
          │ MCP Client  │
          └──────┬──────┘
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
  ┌────────┐ ┌────────┐ ┌────────┐
  │Linear  │ │Obsidian│ │GitHub  │
  │Server  │ │Server  │ │Server  │
  └────────┘ └────────┘ └────────┘
```

## Implementation Roadmap

### Phase 1: Proof of Concept (2-4 hours)
- [ ] Create MCP server wrapper for Linear client
- [ ] Test with local MCP host
- [ ] Document learnings

### Phase 2: Core Integration (1-2 days)
- [ ] Create MCP server for Obsidian vault
- [ ] Create MCP server for GitHub operations
- [ ] Update session_wrapper to use MCP

### Phase 3: Production Ready (1 week)
- [ ] Add error handling and retry logic
- [ ] Implement access control
- [ ] Create deployment documentation
- [ ] Update DEPLOYMENT.md

## MCP Server Template

```python
# mcp_linear_server.py
from mcp import Server, Tool

class LinearMCPServer(Server):
    def __init__(self):
        super().__init__("linear")
        self.register_tool(
            Tool(
                name="create_issue",
                description="Create a Linear issue",
                input_schema={...},
                handler=self.create_issue
            )
        )
    
    async def create_issue(self, params):
        # Use existing linear_client.py
        from .agent.core.linear_client import LinearClient
        client = LinearClient()
        return client.create_issue(...)
```

## Resources

- https://modelcontextprotocol.io
- Anthropic MCP GitHub repository
- Example MCP servers

## Decision: When to Implement

**Recommended**: Start with Phase 1 when adding new integrations.
**Current priority**: Medium (system works well with direct API calls)

---

*Research completed: 2026-01-17*
