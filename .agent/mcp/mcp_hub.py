"""
MCP Hub - Unified interface to MCP servers

This module provides a registry of available MCP servers and a unified
way to invoke tools across them.

Rather than building custom MCP servers from scratch, we can:
1. Use official MCP servers where they exist
2. Wrap our existing clients for local use
3. Document integration approach

Official MCP Servers Available:
- linear: npm @linear/mcp-server (official)
- obsidian: npm @mcp/obsidian (community)
- github: npm @github/mcp-server (official)
- filesystem: npm @mcp/filesystem (official)

Our Custom Servers (for reference):
- linear_mcp_server.py - wraps our LinearClient
- obsidian_mcp_server.py - wraps our obsidian_client
- github_mcp_server.py - wraps git CLI

The custom servers follow MCP patterns and work locally,
but for production use, prefer the official npm packages.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import our custom servers
sys.path.insert(0, str(Path(__file__).parent))
from linear_mcp_server import LinearMCPServer
from obsidian_mcp_server import ObsidianMCPServer
from github_mcp_server import GitHubMCPServer


class MCPHub:
    """
    Unified interface to multiple MCP servers.
    
    Provides:
    - Server discovery
    - Tool aggregation
    - Unified invocation
    """
    
    def __init__(self):
        self.servers = {
            "linear": LinearMCPServer(),
            "obsidian": ObsidianMCPServer(),
            "github": GitHubMCPServer(),
        }
    
    def list_servers(self) -> List[Dict[str, Any]]:
        """List all registered servers."""
        return [
            {
                "name": name,
                "version": server.version,
                "tools_count": len(server.tools)
            }
            for name, server in self.servers.items()
        ]
    
    def list_all_tools(self) -> List[Dict[str, Any]]:
        """List all tools across all servers."""
        tools = []
        for server_name, server in self.servers.items():
            for tool in server.list_tools():
                tools.append({
                    "server": server_name,
                    "name": tool["name"],
                    "full_name": f"{server_name}.{tool['name']}",
                    "description": tool["description"]
                })
        return tools
    
    def invoke(self, full_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a tool using full_name format: server.tool_name
        
        Example: hub.invoke("linear.create_issue", {"title": "New task"})
        """
        parts = full_name.split(".", 1)
        if len(parts) != 2:
            return {"error": f"Invalid tool name format. Use: server.tool_name"}
        
        server_name, tool_name = parts
        
        if server_name not in self.servers:
            return {"error": f"Server '{server_name}' not found. Available: {list(self.servers.keys())}"}
        
        return self.servers[server_name].invoke_tool(tool_name, params)
    
    def get_server(self, name: str):
        """Get a specific server instance."""
        return self.servers.get(name)


def main():
    """CLI demo of the MCP Hub."""
    hub = MCPHub()
    
    print("=" * 60)
    print("MCP Hub - Unified MCP Server Interface")
    print("=" * 60)
    print()
    
    print("Registered Servers:")
    for server in hub.list_servers():
        print(f"  - {server['name']} v{server['version']} ({server['tools_count']} tools)")
    print()
    
    print(f"Total Tools Available: {len(hub.list_all_tools())}")
    print()
    
    print("Sample Tools:")
    for tool in hub.list_all_tools()[:8]:
        print(f"  - {tool['full_name']}: {tool['description'][:50]}...")
    print()
    
    # Demo invocation
    print("Demo: Invoking linear.get_in_progress")
    result = hub.invoke("linear.get_in_progress", {})
    print(f"  Result: {result.get('count', 0)} in-progress issues")
    print()
    
    print("Demo: Invoking obsidian.get_vault_info")
    result = hub.invoke("obsidian.get_vault_info", {})
    print(f"  Vault folders: {result.get('folders', [])[:5]}")
    print()
    
    print("Demo: Invoking github.get_branch")
    result = hub.invoke("github.get_branch", {})
    print(f"  Current branch: {result.get('branch', 'unknown')}")


if __name__ == "__main__":
    main()
