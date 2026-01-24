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

# Load .env from workspace root
try:
    from dotenv import load_dotenv
    # Find workspace root (directory containing .agent/)
    _current = Path(__file__).parent
    while _current != _current.parent:
        if (_current.parent / ".env").exists():
            load_dotenv(_current.parent / ".env")
            break
        _current = _current.parent
except ImportError:
    pass  # dotenv not installed, rely on system env vars


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
            config_path: Path to mcp_config.json (legacy fallback)
        
        Priority order:
        1. api_key parameter
        2. LINEAR_API_KEY environment variable
        3. mcp_config.json (legacy, deprecated)
        """
        self.api_key = api_key
        
        # Try environment variable first
        if not self.api_key:
            self.api_key = os.getenv("LINEAR_API_KEY")
        
        # Legacy fallback to config file (deprecated)
        if not self.api_key and config_path:
            self.api_key = self._load_api_key(config_path)
        
        if not self.api_key:
            # Try default config location (legacy)
            default_config = Path(".agent/config/mcp_config.json")
            if default_config.exists():
                self.api_key = self._load_api_key(default_config)
    
    def _load_api_key(self, config_path: Path) -> Optional[str]:
        """Load API key from config file (legacy, deprecated)."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get("linear", {}).get("api_key")
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    
    def _execute_query(self, query: str, variables: Optional[Dict] = None, 
                       max_retries: int = 3) -> Dict[str, Any]:
        """Execute a GraphQL query against Linear API with retry logic."""
        if not self.api_key:
            raise ValueError("No Linear API key configured")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        last_exception = None
        for attempt in range(max_retries):
            try:
                response = requests.post(self.API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 429:  # Rate limited
                    wait_time = min(2 ** attempt, 8)  # 1, 2, 4, max 8 seconds
                    import time
                    time.sleep(wait_time)
                    continue
                
                if response.status_code >= 500:  # Server error, retry
                    wait_time = min(2 ** attempt, 8)
                    import time
                    time.sleep(wait_time)
                    continue
                
                if response.status_code != 200:
                    raise Exception(f"Linear API error: {response.status_code} - {response.text}")
                
                data = response.json()
                
                if "errors" in data:
                    raise Exception(f"GraphQL errors: {data['errors']}")
                
                return data.get("data", {})
                
            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = min(2 ** attempt, 8)
                    import time
                    time.sleep(wait_time)
                    continue
                raise Exception(f"Linear API request failed after {max_retries} retries: {e}")
        
        if last_exception:
            raise Exception(f"Linear API request failed after {max_retries} retries: {last_exception}")
        raise Exception("Linear API request failed unexpectedly")
    
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
                    id
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
                "teams": data.get("teams", {}).get("nodes", [])
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_team_id(self) -> Optional[str]:
        """Get the first team's ID for issue creation."""
        result = self.test_connection()
        if result["success"] and result["teams"]:
            return result["teams"][0].get("id")
        return None
    
    def create_issue(self, title: str, description: str, team_id: str, 
                     labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new issue in Linear.
        
        Args:
            title: Issue title
            description: Issue description (markdown)
            team_id: Team ID to create issue in
            labels: Optional list of label names
        
        Returns:
            Dict with success status and issue details
        """
        mutation = """
        mutation CreateIssue($title: String!, $description: String!, $teamId: String!) {
            issueCreate(input: {
                title: $title
                description: $description
                teamId: $teamId
            }) {
                success
                issue {
                    identifier
                    title
                    url
                }
            }
        }
        """
        
        try:
            data = self._execute_query(mutation, {
                "title": title,
                "description": description,
                "teamId": team_id
            })
            
            result = data.get("issueCreate", {})
            if result.get("success"):
                issue = result.get("issue", {})
                return {
                    "success": True,
                    "identifier": issue.get("identifier"),
                    "title": issue.get("title"),
                    "url": issue.get("url")
                }
            else:
                return {"success": False, "error": "Issue creation failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_session_ticket(self, session_summary: str, files_modified: int, 
                               commits: List[str]) -> Dict[str, Any]:
        """
        Create a session completion ticket.
        
        Args:
            session_summary: Brief summary of what was done
            files_modified: Number of files changed
            commits: List of commit messages
        
        Returns:
            Dict with creation result
        """
        team_id = self.get_team_id()
        if not team_id:
            return {"success": False, "error": "No team found"}
        
        today = datetime.now().strftime("%Y-%m-%d")
        title = f"📔 Session Log: {today}"
        
        description = f"""## Session Summary
{session_summary}

## Stats
- **Files Modified:** {files_modified}
- **Commits:** {len(commits)}

## Commits
{chr(10).join('- ' + c for c in commits[:10])}

---
*Auto-created by Session Wrapper*
"""
        
        return self.create_issue(title, description, team_id)
    
    def update_issue(self, issue_id: str, title: Optional[str] = None, 
                     description: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing issue.
        
        Args:
            issue_id: The issue's internal ID or identifier (e.g., LIN-14)
            title: New title (optional)
            description: New description (optional)
        
        Returns:
            Dict with update result
        """
        # First get the issue's internal ID if we have an identifier like LIN-14
        if "-" in issue_id and not issue_id.startswith("lin_"):
            # Extract the number from identifier like LIN-14
            parts = issue_id.split("-")
            if len(parts) == 2:
                team_key = parts[0]
                issue_number = int(parts[1])
                
                # Query to find issue by team key and number
                query = """
                query GetIssueByNumber($teamKey: String!, $number: Float!) {
                    issues(filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }, first: 1) {
                        nodes { id identifier }
                    }
                }
                """
                try:
                    data = self._execute_query(query, {
                        "teamKey": team_key,
                        "number": issue_number
                    })
                    nodes = data.get("issues", {}).get("nodes", [])
                    if nodes:
                        issue_id = nodes[0].get("id")
                    else:
                        return {"success": False, "error": f"Issue {issue_id} not found"}
                except Exception as e:
                    return {"success": False, "error": str(e)}
        
        # Build the update input
        update_input = {}
        if title:
            update_input["title"] = title
        if description:
            update_input["description"] = description
        
        if not update_input:
            return {"success": False, "error": "No updates provided"}
        
        mutation = """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
            issueUpdate(id: $id, input: $input) {
                success
                issue { identifier title }
            }
        }
        """
        
        try:
            data = self._execute_query(mutation, {
                "id": issue_id,
                "input": update_input
            })
            
            result = data.get("issueUpdate", {})
            if result.get("success"):
                return {
                    "success": True,
                    "identifier": result.get("issue", {}).get("identifier"),
                    "title": result.get("issue", {}).get("title")
                }
            else:
                return {"success": False, "error": "Update failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_all_issues(self, limit: int = 50) -> List[LinearIssue]:
        """Get all issues in the workspace."""
        query = """
        query AllIssues($first: Int!) {
            issues(first: $first, orderBy: createdAt) {
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
        
        data = self._execute_query(query, {"first": limit})
        return self._parse_issues(data.get("issues", {}).get("nodes", []))
    
    def update_state(self, issue_id: str, state_name: str) -> Dict[str, Any]:
        """
        Update an issue's state/status.
        
        Args:
            issue_id: Issue identifier (e.g., LIN-14)
            state_name: State name (e.g., 'In Progress', 'Done', 'Canceled')
        """
        # First get the issue's internal ID
        if "-" in issue_id and not issue_id.startswith("lin_"):
            parts = issue_id.split("-")
            if len(parts) == 2:
                team_key = parts[0]
                issue_number = int(parts[1])
                
                query = """
                query GetIssueAndStates($teamKey: String!, $number: Float!) {
                    issues(filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }, first: 1) {
                        nodes { id identifier team { id states { nodes { id name } } } }
                    }
                }
                """
                try:
                    data = self._execute_query(query, {
                        "teamKey": team_key,
                        "number": issue_number
                    })
                    nodes = data.get("issues", {}).get("nodes", [])
                    if not nodes:
                        return {"success": False, "error": f"Issue {issue_id} not found"}
                    
                    issue_uuid = nodes[0].get("id")
                    states = nodes[0].get("team", {}).get("states", {}).get("nodes", [])
                    
                    # Find the target state
                    state_id = None
                    for s in states:
                        if s.get("name", "").lower() == state_name.lower():
                            state_id = s.get("id")
                            break
                    
                    if not state_id:
                        available = [s.get("name") for s in states]
                        return {"success": False, "error": f"State '{state_name}' not found. Available: {available}"}
                    
                    # Update the issue
                    mutation = """
                    mutation UpdateIssueState($id: String!, $stateId: String!) {
                        issueUpdate(id: $id, input: { stateId: $stateId }) {
                            success
                            issue { identifier state { name } }
                        }
                    }
                    """
                    data = self._execute_query(mutation, {
                        "id": issue_uuid,
                        "stateId": state_id
                    })
                    result = data.get("issueUpdate", {})
                    if result.get("success"):
                        return {
                            "success": True,
                            "identifier": result.get("issue", {}).get("identifier"),
                            "state": result.get("issue", {}).get("state", {}).get("name")
                        }
                    return {"success": False, "error": "State update failed"}
                except Exception as e:
                    return {"success": False, "error": str(e)}
        return {"success": False, "error": "Invalid issue ID format"}
    
    def archive_issue(self, issue_id: str) -> Dict[str, Any]:
        """Archive (soft delete) an issue."""
        # Get internal ID first
        if "-" in issue_id:
            parts = issue_id.split("-")
            if len(parts) == 2:
                team_key = parts[0]
                issue_number = int(parts[1])
                
                query = """
                query GetIssueId($teamKey: String!, $number: Float!) {
                    issues(filter: { team: { key: { eq: $teamKey } }, number: { eq: $number } }, first: 1) {
                        nodes { id identifier }
                    }
                }
                """
                try:
                    data = self._execute_query(query, {
                        "teamKey": team_key,
                        "number": issue_number
                    })
                    nodes = data.get("issues", {}).get("nodes", [])
                    if not nodes:
                        return {"success": False, "error": f"Issue {issue_id} not found"}
                    
                    issue_uuid = nodes[0].get("id")
                    
                    mutation = """
                    mutation ArchiveIssue($id: String!) {
                        issueArchive(id: $id) {
                            success
                        }
                    }
                    """
                    data = self._execute_query(mutation, {"id": issue_uuid})
                    if data.get("issueArchive", {}).get("success"):
                        return {"success": True, "identifier": issue_id}
                    return {"success": False, "error": "Archive failed"}
                except Exception as e:
                    return {"success": False, "error": str(e)}
        return {"success": False, "error": "Invalid issue ID format"}


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
                print(f"   Teams: {', '.join(t.get('name', t.get('key', 'Unknown')) for t in result['teams'])}")
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
