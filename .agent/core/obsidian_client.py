"""
Obsidian Client - Direct access to Obsidian vault

This provides vault operations without requiring the Local REST API.
For simple file operations, just read/write to the vault path.

For more complex operations, consider using the Obsidian Local REST API
if running (http://localhost:27124).
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class ObsidianNote:
    """Represents an Obsidian note."""
    path: Path
    title: str
    content: str
    frontmatter: Dict
    tags: List[str]


def get_vault_path() -> Optional[Path]:
    """Get the configured vault path from mcp_config.json."""
    config_path = Path(".agent/config/mcp_config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            vault_path = config.get("obsidian", {}).get("vault_path")
            if vault_path:
                return Path(vault_path)
        except (json.JSONDecodeError, KeyError):
            pass
    return None


def create_note(
    folder: str,
    title: str,
    content: str,
    frontmatter: Optional[Dict] = None,
    vault_path: Optional[Path] = None
) -> Path:
    """
    Create a new note in the vault.
    
    Args:
        folder: Folder within vault (e.g., 'Sessions', 'Projects')
        title: Note title (used as filename)
        content: Note content (markdown)
        frontmatter: Optional YAML frontmatter dict
        vault_path: Override vault path
    
    Returns:
        Path to created note
    """
    vault = vault_path or get_vault_path()
    if not vault:
        raise ValueError("No vault path configured")
    
    # Build frontmatter
    fm_lines = ["---"]
    if frontmatter:
        for key, value in frontmatter.items():
            if isinstance(value, list):
                fm_lines.append(f"{key}: [{', '.join(str(v) for v in value)}]")
            else:
                fm_lines.append(f"{key}: {value}")
    else:
        fm_lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
    fm_lines.append("---")
    fm_lines.append("")
    
    full_content = "\n".join(fm_lines) + content
    
    # Create path
    note_path = vault / folder / f"{title}.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write
    note_path.write_text(full_content, encoding='utf-8')
    
    return note_path


def read_note(path: Path) -> Optional[ObsidianNote]:
    """
    Read a note from the vault.
    
    Args:
        path: Full path to the note
    
    Returns:
        ObsidianNote or None if not found
    """
    if not path.exists():
        return None
    
    content = path.read_text(encoding='utf-8')
    
    # Parse frontmatter
    frontmatter = {}
    tags = []
    body = content
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            import yaml
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                tags = frontmatter.get("tags", [])
            except:
                pass
            body = parts[2].strip()
    
    return ObsidianNote(
        path=path,
        title=path.stem,
        content=body,
        frontmatter=frontmatter,
        tags=tags if isinstance(tags, list) else [tags]
    )


def list_notes(folder: str, vault_path: Optional[Path] = None) -> List[Path]:
    """List all notes in a folder."""
    vault = vault_path or get_vault_path()
    if not vault:
        return []
    
    folder_path = vault / folder
    if not folder_path.exists():
        return []
    
    return list(folder_path.glob("*.md"))


def search_notes(query: str, vault_path: Optional[Path] = None) -> List[Path]:
    """Search notes by content."""
    vault = vault_path or get_vault_path()
    if not vault:
        return []
    
    results = []
    for note_path in vault.rglob("*.md"):
        try:
            content = note_path.read_text(encoding='utf-8')
            if query.lower() in content.lower():
                results.append(note_path)
        except:
            pass
    
    return results


# CLI
if __name__ == "__main__":
    import sys
    
    vault = get_vault_path()
    print(f"Vault path: {vault}")
    
    if vault:
        sessions = list_notes("Sessions", vault)
        print(f"Session logs: {len(sessions)}")
        
        reports = list_notes("Reports", vault)
        print(f"Reports: {len(reports)}")
