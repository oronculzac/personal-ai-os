"""
Linear API Client - Direct access to Linear for task management

This module provides a standalone client for the Linear GraphQL API,
used by Session Wrapper and other skills for task management.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class LinearIssue:
    identifier: str
    title: str
    url: str
    description: Optional[str]
    state: str
    project: Optional[str]
    cycle: Optional[int]
    labels: List[str]


class LinearClient:
    """Client for Linear GraphQL API."""
    
    API_URL = "https://api.linear.app/graphql"
    
    def __init__(self, api_key: Optional[str] = None, config_path: Optional[Path] = None):
        """
        Initialize the Linear client.
        
        Args:
            api_key: Direct API key (takes precedence)
            config_path: Path to mcp_config.json (fallback)
        """
        self.api_key = api_key
        
        if not self.api_key and config_path:
            self.api_key = self._load_api_key(config_path)
        
        if not self.api_key:
            # Try default config location
            default_config = Path(".agent/config/mcp_config.json")
            if default_config.exists():
                self.api_key = self._load_api_key(default_config)
    
    def _load_api_key(self, config_path: Path) -> Optional[str]:
        """Load API key from config file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get("linear", {}).get("api_key")
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def _execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a GraphQL query against Linear API."""
        if not self.api_key:
            raise ValueError("No Linear API key configured")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(self.API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Linear API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
        
        return data.get("data", {})
    
    def get_in_progress_issues(self) -> List[LinearIssue]:
        """Get all issues currently in progress."""
        query = """
        query InProgressIssues {
            issues(filter: { state: { name: { eq: "In Progress" } } }) {
                nodes {
                    identifier
                    title
                    url
                    description
                    state { name }
                    project { name }
                    cycle { number }
                    labels { nodes { name } }
                }
            }
        }
        """
        
        data = self._execute_query(query)
        return self._parse_issues(data.get("issues", {}).get("nodes", []))
    
    def get_recently_completed(self, hours: int = 24) -> List[LinearIssue]:
        """Get issues completed within the specified hours."""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        query = """
        query RecentlyCompleted($since: DateTime!) {
            issues(filter: { completedAt: { gt: $since } }) {
                nodes {
                    identifier
                    title
                    url
                    description
                    state { name }
                    project { name }
                    cycle { number }
                    labels { nodes { name } }
                }
            }
        }
        """
        
        data = self._execute_query(query, {"since": since})
        return self._parse_issues(data.get("issues", {}).get("nodes", []))
    
    def get_session_tickets(self, hours: int = 24) -> List[LinearIssue]:
        """Get all tickets relevant to a session (in progress + recently done)."""
        in_progress = self.get_in_progress_issues()
        completed = self.get_recently_completed(hours)
        
        # Deduplicate by identifier
        seen = set()
        result = []
        for issue in in_progress + completed:
            if issue.identifier not in seen:
                seen.add(issue.identifier)
                result.append(issue)
        
        return result
    
    def get_issue_by_id(self, identifier: str) -> Optional[LinearIssue]:
        """Get a specific issue by its identifier (e.g., 'DEZ-123')."""
        query = """
        query GetIssue($id: String!) {
            issue(id: $id) {
                identifier
                title
                url
                description
                state { name }
                project { name }
                cycle { number }
                labels { nodes { name } }
            }
        }
        """
        
        try:
            data = self._execute_query(query, {"id": identifier})
            issue_data = data.get("issue")
            if issue_data:
                return self._parse_issue(issue_data)
        except Exception:
            pass
        return None
    
    def search_issues(self, query_text: str) -> List[LinearIssue]:
        """Search for issues by text."""
        query = """
        query SearchIssues($query: String!) {
            issueSearch(query: $query, first: 10) {
                nodes {
                    identifier
                    title
                    url
                    description
                    state { name }
                    project { name }
                    cycle { number }
                    labels { nodes { name } }
                }
            }
        }
        """
        
        data = self._execute_query(query, {"query": query_text})
        return self._parse_issues(data.get("issueSearch", {}).get("nodes", []))
    
    def _parse_issues(self, nodes: List[Dict]) -> List[LinearIssue]:
        """Parse a list of issue nodes into LinearIssue objects."""
        return [self._parse_issue(node) for node in nodes]
    
    def _parse_issue(self, node: Dict) -> LinearIssue:
        """Parse a single issue node into a LinearIssue object."""
        return LinearIssue(
            identifier=node.get("identifier", ""),
            title=node.get("title", ""),
            url=node.get("url", ""),
            description=node.get("description"),
            state=node.get("state", {}).get("name", "Unknown"),
            project=node.get("project", {}).get("name") if node.get("project") else None,
            cycle=node.get("cycle", {}).get("number") if node.get("cycle") else None,
            labels=[label.get("name") for label in node.get("labels", {}).get("nodes", [])]
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the API connection and return workspace info."""
        query = """
        query TestConnection {
            viewer {
                id
                name
                email
            }
            teams {
                nodes {
                    name
                    key
                }
            }
        }
        """
        
        try:
            data = self._execute_query(query)
            return {
                "success": True,
                "user": data.get("viewer", {}),
                "teams": [t.get("name") for t in data.get("teams", {}).get("nodes", [])]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def format_issues_for_display(issues: List[LinearIssue]) -> str:
    """Format issues for human-readable display."""
    if not issues:
        return "No issues found."
    
    lines = ["Linear Issues", "=" * 40]
    for issue in issues:
        status_icon = "🔄" if issue.state == "In Progress" else "✅" if issue.state == "Done" else "📋"
        lines.append(f"{status_icon} [{issue.identifier}] {issue.title}")
        if issue.project:
            lines.append(f"   📁 Project: {issue.project}")
        if issue.labels:
            lines.append(f"   🏷️ Labels: {', '.join(issue.labels)}")
        lines.append(f"   🔗 {issue.url}")
        lines.append("")
    
    return "\n".join(lines)


# CLI interface
if __name__ == "__main__":
    import sys
    
    client = LinearClient()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--test":
            result = client.test_connection()
            if result["success"]:
                print("✅ Connection successful!")
                print(f"   User: {result['user'].get('name', 'Unknown')}")
                print(f"   Teams: {', '.join(result['teams'])}")
            else:
                print(f"❌ Connection failed: {result['error']}")
        
        elif command == "--in-progress":
            issues = client.get_in_progress_issues()
            print(format_issues_for_display(issues))
        
        elif command == "--session":
            issues = client.get_session_tickets()
            print(format_issues_for_display(issues))
            
            # Also output as JSON for piping
            print("\n--- JSON Output ---")
            print(json.dumps([{
                "identifier": i.identifier,
                "title": i.title,
                "state": i.state,
                "project": i.project
            } for i in issues], indent=2))
        
        elif command == "--search" and len(sys.argv) > 2:
            query_text = " ".join(sys.argv[2:])
            issues = client.search_issues(query_text)
            print(format_issues_for_display(issues))
        
        else:
            print("Usage:")
            print("  python linear_client.py --test         # Test connection")
            print("  python linear_client.py --in-progress  # Get in-progress issues")
            print("  python linear_client.py --session      # Get session-relevant issues")
            print("  python linear_client.py --search <query>  # Search issues")
    else:
        # Default: show session tickets
        issues = client.get_session_tickets()
        print(format_issues_for_display(issues))
