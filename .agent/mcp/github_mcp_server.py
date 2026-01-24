"""
GitHub MCP Server - Model Context Protocol wrapper for GitHub operations

Provides MCP-compatible access to GitHub for:
- Commit info
- Push operations
- Repo status
- Branch management
"""

import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Tool:
    """MCP Tool definition."""
    name: str
    description: str
    input_schema: Dict[str, Any]


class GitHubMCPServer:
    """
    MCP Server wrapper for GitHub/Git operations.
    
    Uses git CLI for operations (no API token required for local ops).
    """
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.name = "github"
        self.version = "1.0.0"
        self.repo_path = repo_path or Path.cwd()
        self.tools = self._register_tools()
    
    def _run_git(self, *args) -> tuple[bool, str]:
        """Run a git command and return (success, output)."""
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            return False, result.stderr.strip()
        except Exception as e:
            return False, str(e)
    
    def _register_tools(self) -> List[Tool]:
        """Register available tools."""
        return [
            Tool(
                name="get_status",
                description="Get git status (modified/staged files)",
                input_schema={"type": "object", "properties": {}}
            ),
            Tool(
                name="get_log",
                description="Get recent commit history",
                input_schema={
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Number of commits", "default": 5}
                    }
                }
            ),
            Tool(
                name="get_diff",
                description="Get diff of changed files",
                input_schema={
                    "type": "object",
                    "properties": {
                        "staged": {"type": "boolean", "description": "Show staged changes only", "default": False}
                    }
                }
            ),
            Tool(
                name="stage_files",
                description="Stage files for commit",
                input_schema={
                    "type": "object",
                    "properties": {
                        "files": {"type": "array", "items": {"type": "string"}, "description": "Files to stage (use '.' for all)"}
                    },
                    "required": ["files"]
                }
            ),
            Tool(
                name="commit",
                description="Create a commit with message",
                input_schema={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "Commit message"}
                    },
                    "required": ["message"]
                }
            ),
            Tool(
                name="push",
                description="Push to remote repository",
                input_schema={
                    "type": "object",
                    "properties": {
                        "remote": {"type": "string", "default": "origin"},
                        "branch": {"type": "string", "description": "Branch to push (default: current)"}
                    }
                }
            ),
            Tool(
                name="get_branch",
                description="Get current branch name",
                input_schema={"type": "object", "properties": {}}
            ),
            Tool(
                name="get_remotes",
                description="List remote repositories",
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
        
        if name == "get_status":
            success, output = self._run_git("status", "--short")
            if success:
                lines = output.split('\n') if output else []
                return {
                    "success": True,
                    "modified": len([l for l in lines if l.startswith(' M') or l.startswith('M ')]),
                    "staged": len([l for l in lines if l.startswith('A ') or l.startswith('M ')]),
                    "untracked": len([l for l in lines if l.startswith('??')]),
                    "files": lines[:10]
                }
            return {"success": False, "error": output}
        
        elif name == "get_log":
            limit = params.get("limit", 5)
            success, output = self._run_git("log", f"-{limit}", "--oneline")
            if success:
                commits = []
                for line in output.split('\n'):
                    if line:
                        parts = line.split(' ', 1)
                        commits.append({"hash": parts[0], "message": parts[1] if len(parts) > 1 else ""})
                return {"success": True, "commits": commits}
            return {"success": False, "error": output}
        
        elif name == "get_diff":
            args = ["diff", "--stat"]
            if params.get("staged"):
                args.append("--cached")
            success, output = self._run_git(*args)
            return {"success": success, "diff": output[:500] if success else None, "error": output if not success else None}
        
        elif name == "stage_files":
            files = params.get("files", ["."])
            success, output = self._run_git("add", *files)
            return {"success": success, "staged": files, "error": output if not success else None}
        
        elif name == "commit":
            message = params.get("message", "Update")
            success, output = self._run_git("commit", "-m", message)
            if success:
                # Get the commit hash
                _, hash_output = self._run_git("rev-parse", "--short", "HEAD")
                return {"success": True, "commit_hash": hash_output, "message": message}
            return {"success": False, "error": output}
        
        elif name == "push":
            remote = params.get("remote", "origin")
            branch = params.get("branch")
            args = ["push", remote]
            if branch:
                args.append(branch)
            success, output = self._run_git(*args)
            return {"success": success, "remote": remote, "output": output}
        
        elif name == "get_branch":
            success, output = self._run_git("symbolic-ref", "--short", "HEAD")
            return {"success": success, "branch": output if success else None}
        
        elif name == "get_remotes":
            success, output = self._run_git("remote", "-v")
            if success:
                remotes = {}
                for line in output.split('\n'):
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            remotes[parts[0]] = parts[1]
                return {"success": True, "remotes": remotes}
            return {"success": False, "error": output}
        
        else:
            return {"error": f"Unknown tool: {name}"}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Return server metadata."""
        _, branch = self._run_git("symbolic-ref", "--short", "HEAD")
        return {
            "name": self.name,
            "version": self.version,
            "protocol": "mcp",
            "repo_path": str(self.repo_path),
            "current_branch": branch,
            "tools_count": len(self.tools)
        }


def main():
    """CLI for testing the MCP server."""
    server = GitHubMCPServer()
    
    print("=== GitHub MCP Server ===")
    info = server.get_server_info()
    print(f"Name: {info['name']}")
    print(f"Version: {info['version']}")
    print(f"Branch: {info['current_branch']}")
    print()
    
    print("Available Tools:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    
    # Test status
    print("Testing get_status:")
    result = server.invoke_tool("get_status", {})
    print(f"  Modified: {result.get('modified', 0)}, Staged: {result.get('staged', 0)}")
    print()
    
    # Test log
    print("Testing get_log:")
    result = server.invoke_tool("get_log", {"limit": 3})
    for commit in result.get("commits", []):
        print(f"  {commit['hash']}: {commit['message'][:50]}")


if __name__ == "__main__":
    main()
