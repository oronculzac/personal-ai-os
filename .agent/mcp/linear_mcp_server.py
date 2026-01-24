"""
Linear MCP Server - Model Context Protocol wrapper for Linear API

This is a proof-of-concept MCP server that wraps our Linear client,
following the MCP specification for AI-tool integration.

Usage:
    This server can be registered with MCP-compatible hosts (like Claude Desktop)
    to provide Linear issue management capabilities.
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
from linear_client import LinearClient


@dataclass
class Tool:
    """MCP Tool definition."""
    name: str
    description: str
    input_schema: Dict[str, Any]


class LinearMCPServer:
    """
    MCP Server wrapper for Linear API.
    
    Implements the core MCP patterns:
    - Tool registration
    - Tool discovery
    - Tool invocation
    """
    
    def __init__(self):
        self.name = "linear"
        self.version = "1.0.0"
        self.client = LinearClient()
        self.tools = self._register_tools()
    
    def _register_tools(self) -> List[Tool]:
        """Register available tools."""
        return [
            Tool(
                name="create_issue",
                description="Create a new Linear issue/task",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Issue title"},
                        "description": {"type": "string", "description": "Issue description (markdown)"},
                    },
                    "required": ["title"]
                }
            ),
            Tool(
                name="list_issues",
                description="List all Linear issues",
                input_schema={
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Max issues to return", "default": 20}
                    }
                }
            ),
            Tool(
                name="update_issue_state",
                description="Update an issue's state (e.g., In Progress, Done)",
                input_schema={
                    "type": "object",
                    "properties": {
                        "issue_id": {"type": "string", "description": "Issue ID (e.g., LIN-14)"},
                        "state": {"type": "string", "description": "New state name"}
                    },
                    "required": ["issue_id", "state"]
                }
            ),
            Tool(
                name="get_in_progress",
                description="Get all issues currently in progress",
                input_schema={"type": "object", "properties": {}}
            ),
        ]
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """Return tool definitions for discovery."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in self.tools
        ]
    
    def invoke_tool(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a tool by name with given parameters.
        
        This is the core MCP pattern - tools are invoked via a standard interface.
        """
        if name == "create_issue":
            team_id = self.client.get_team_id()
            if not team_id:
                return {"error": "No team found"}
            return self.client.create_issue(
                title=params.get("title", "Untitled"),
                description=params.get("description", ""),
                team_id=team_id
            )
        
        elif name == "list_issues":
            limit = params.get("limit", 20)
            issues = self.client.list_all_issues(limit)
            return {
                "count": len(issues),
                "issues": [
                    {
                        "id": i.identifier,
                        "title": i.title,
                        "state": i.state,
                        "url": i.url
                    }
                    for i in issues
                ]
            }
        
        elif name == "update_issue_state":
            return self.client.update_state(
                issue_id=params.get("issue_id"),
                state_name=params.get("state")
            )
        
        elif name == "get_in_progress":
            issues = self.client.get_in_progress_issues()
            return {
                "count": len(issues),
                "issues": [
                    {"id": i.identifier, "title": i.title}
                    for i in issues
                ]
            }
        
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Return server metadata."""
        return {
            "name": self.name,
            "version": self.version,
            "protocol": "mcp",
            "tools_count": len(self.tools)
        }


def main():
    """CLI for testing the MCP server."""
    server = LinearMCPServer()
    
    print("=== Linear MCP Server ===")
    print(f"Name: {server.name}")
    print(f"Version: {server.version}")
    print()
    
    print("Available Tools:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    
    # Test tool invocation
    print("Testing get_in_progress:")
    result = server.invoke_tool("get_in_progress", {})
    print(f"  Result: {result.get('count', 0)} in-progress issues")
    print()
    
    print("Testing list_issues (limit=5):")
    result = server.invoke_tool("list_issues", {"limit": 5})
    print(f"  Result: {result.get('count', 0)} issues")
    for issue in result.get("issues", [])[:5]:
        print(f"    [{issue['id']}] {issue['title'][:40]}")


if __name__ == "__main__":
    main()
