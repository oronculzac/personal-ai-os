import os
import json
import subprocess
import requests
import datetime
from pathlib import Path

# Configuration Paths
MCP_CONFIG_PATH = Path(".agent/config/mcp_config.json")

def get_config():
    if MCP_CONFIG_PATH.exists():
        try:
            with open(MCP_CONFIG_PATH, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def get_git_info():
    try:
        # Get changed files
        diff = subprocess.check_output(["git", "diff", "--stat"], stderr=subprocess.STDOUT).decode('utf-8')
        # Get recent commits (last 24 hours to be safe)
        log = subprocess.check_output(["git", "log", "--since=24.hours", "--oneline"], stderr=subprocess.STDOUT).decode('utf-8')
        
        # Extract list of modified files for publish detection
        modified_files = []
        for line in diff.split('\n'):
            # Match lines like: " path/to/file.py | 10 +++---"
            import re
            match = re.match(r'^\s*(.+?)\s*\|', line)
            if match:
                modified_files.append(match.group(1).strip())
        
        return {
            "diff_stat": diff.strip(),
            "recent_commits": log.strip(),
            "modified_files": modified_files,
            "file_count": len(modified_files)
        }
    except subprocess.CalledProcessError:
        return {"error": "Not a git repository or git error", "modified_files": [], "file_count": 0}
    except FileNotFoundError:
        return {"error": "Git not installed", "modified_files": [], "file_count": 0}

def get_linear_tickets(config):
    api_key = config.get("linear", {}).get("api_key")
    if not api_key:
        return {"tickets": [], "error": "No Linear API key found in config"}

    url = "https://api.linear.app/graphql"
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    
    # Query for In Progress tickets, recently done, AND Active Cycle tickets
    query = """
    query {
      issues(filter: { 
        or: [
          { state: { name: { eq: "In Progress" } } },
          { completedAt: { gt: "%s" } }
        ]
      }) {
        nodes {
          identifier
          title
          url
          description
          state { name }
          project { name }
          cycle { number }
        }
      }
    }
    """ % (datetime.datetime.now() - datetime.timedelta(hours=24)).isoformat()

    try:
        response = requests.post(url, headers=headers, json={"query": query})
        if response.status_code == 200:
            data = response.json()
            return {"tickets": data.get("data", {}).get("issues", {}).get("nodes", [])}
        else:
            return {"error": f"Linear API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_obsidian_focus(config):
    vault_path = config.get("obsidian", {}).get("vault_path")
    if not vault_path or not os.path.exists(vault_path):
        return {"error": "Obsidian vault path not found"}
    
    # Check for a specific 'Current Focus' note or recently modified
    # 1. Try to read a standard 'System/Focus.md' or similar if it existed
    # 2. For now, let's just return the last modified non-daily note
    
    try:
        # Find all .md files, sort by modification time
        files = []
        for root, _, filenames in os.walk(vault_path):
            if ".obsidian" in root: continue
            for f in filenames:
                if f.endswith(".md"):
                    full_path = os.path.join(root, f)
                    files.append((full_path, os.path.getmtime(full_path)))
        
        # Sort by time desc
        files.sort(key=lambda x: x[1], reverse=True)
        
        # Get top 3 recently modified
        recent_notes = []
        for fpath, _ in files[:3]:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read(500) # First 500 chars
                recent_notes.append({
                    "path": fpath,
                    "preview": content
                })
            except:
                continue
                
        return {"recent_notes": recent_notes}
    except Exception as e:
        return {"error": str(e)}

def main():
    config = get_config()
    git_data = get_git_info()
    linear_data = get_linear_tickets(config)
    obsidian_data = get_obsidian_focus(config)
    
    context = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git": git_data,
        "linear": linear_data,
        "obsidian": obsidian_data,
        "obsidian_vault_path": config.get("obsidian", {}).get("vault_path")
    }
    
    print(json.dumps(context, indent=2))

if __name__ == "__main__":
    main()
