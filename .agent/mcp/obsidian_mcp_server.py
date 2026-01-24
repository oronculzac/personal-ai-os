"""
Obsidian MCP Server - Model Context Protocol wrapper for Obsidian vault

Provides MCP-compatible access to the Obsidian vault for:
- Creating notes
- Reading notes
- Searching notes
- Listing folders
"""

import json
import sys
from typing import Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
from obsidian_client import (
    create_note, read_note, list_notes, search_notes, get_vault_path
)


@dataclass
class Tool:
    """MCP Tool definition."""
    name: str
    description: str
    input_schema: Dict[str, Any]


class ObsidianMCPServer:
    """
    MCP Server wrapper for Obsidian vault operations.
    """
    
    def __init__(self):
        self.name = "obsidian"
        self.version = "1.0.0"
        self.vault_path = get_vault_path()
        self.tools = self._register_tools()
    
    def _register_tools(self) -> List[Tool]:
        """Register available tools."""
        return [
            Tool(
                name="create_note",
                description="Create a new note in the Obsidian vault",
                input_schema={
                    "type": "object",
                    "properties": {
                        "folder": {"type": "string", "description": "Folder path (e.g., 'Sessions', 'Reports')"},
                        "title": {"type": "string", "description": "Note title (filename without .md)"},
                        "content": {"type": "string", "description": "Note content in markdown"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for the note"}
                    },
                    "required": ["folder", "title", "content"]
                }
            ),
            Tool(
                name="read_note",
                description="Read a note's content from the vault",
                input_schema={
                    "type": "object",
                    "properties": {
                        "folder": {"type": "string", "description": "Folder containing the note"},
                        "title": {"type": "string", "description": "Note title (without .md)"}
                    },
                    "required": ["folder", "title"]
                }
            ),
            Tool(
                name="list_notes",
                description="List all notes in a folder",
                input_schema={
                    "type": "object",
                    "properties": {
                        "folder": {"type": "string", "description": "Folder to list"}
                    },
                    "required": ["folder"]
                }
            ),
            Tool(
                name="search_notes",
                description="Search for notes containing specific text",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="get_vault_info",
                description="Get vault path and folder structure",
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
        """Invoke a tool by name."""
        
        if name == "create_note":
            try:
                frontmatter = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                }
                if params.get("tags"):
                    frontmatter["tags"] = params["tags"]
                
                path = create_note(
                    folder=params["folder"],
                    title=params["title"],
                    content=params["content"],
                    frontmatter=frontmatter,
                    vault_path=self.vault_path
                )
                return {
                    "success": True,
                    "path": str(path),
                    "title": params["title"]
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif name == "read_note":
            try:
                note_path = self.vault_path / params["folder"] / f"{params['title']}.md"
                note = read_note(note_path)
                if note:
                    return {
                        "success": True,
                        "title": note.title,
                        "content": note.content[:500],  # Truncate for response
                        "tags": note.tags,
                        "frontmatter": note.frontmatter
                    }
                return {"success": False, "error": "Note not found"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif name == "list_notes":
            try:
                notes = list_notes(params["folder"], self.vault_path)
                return {
                    "success": True,
                    "count": len(notes),
                    "notes": [n.stem for n in notes]
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif name == "search_notes":
            try:
                results = search_notes(params["query"], self.vault_path)
                return {
                    "success": True,
                    "count": len(results),
                    "matches": [str(r.relative_to(self.vault_path)) for r in results[:10]]
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif name == "get_vault_info":
            folders = []
            if self.vault_path and self.vault_path.exists():
                folders = [d.name for d in self.vault_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            return {
                "success": True,
                "vault_path": str(self.vault_path) if self.vault_path else None,
                "folders": folders
            }
        
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Return server metadata."""
        return {
            "name": self.name,
            "version": self.version,
            "protocol": "mcp",
            "vault_path": str(self.vault_path) if self.vault_path else None,
            "tools_count": len(self.tools)
        }


def main():
    """CLI for testing the MCP server."""
    server = ObsidianMCPServer()
    
    print("=== Obsidian MCP Server ===")
    print(f"Name: {server.name}")
    print(f"Version: {server.version}")
    print(f"Vault: {server.vault_path}")
    print()
    
    print("Available Tools:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    
    # Test vault info
    print("Testing get_vault_info:")
    result = server.invoke_tool("get_vault_info", {})
    print(f"  Folders: {result.get('folders', [])}")
    print()
    
    # Test list notes
    print("Testing list_notes (Sessions):")
    result = server.invoke_tool("list_notes", {"folder": "Sessions"})
    print(f"  Found: {result.get('count', 0)} notes")
    for note in result.get("notes", [])[:3]:
        print(f"    - {note}")


if __name__ == "__main__":
    main()
