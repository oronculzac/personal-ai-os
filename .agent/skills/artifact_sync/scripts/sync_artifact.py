#!/usr/bin/env python3
"""
Artifact Sync - Copy AI artifacts to Obsidian with intuitive naming.

Usage:
    python sync_artifact.py --source <path>  # Sync specific artifact
    python sync_artifact.py --recent         # Sync recent artifacts
    python sync_artifact.py --dry-run        # Preview without changes
"""

import re
import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'core'))


class ArtifactSync:
    """Sync AI-generated artifacts to Obsidian with intuitive naming"""
    
    # Artifact type patterns
    TYPE_PATTERNS = {
        'implementation_plan': ['implementation_plan', 'plan'],
        'task': ['task'],
        'walkthrough': ['walkthrough'],
    }
    
    # Target folders by type
    TARGET_FOLDERS = {
        'implementation_plan': 'Plans',
        'task': 'Plans',
        'walkthrough': 'Journals/Sessions',
        'other': 'Plans',
    }
    
    def __init__(self, vault_path: str = None, dry_run: bool = False):
        """Initialize with vault path"""
        if vault_path is None:
            # Default vault path relative to workspace root
            workspace_root = Path(__file__).parent.parent.parent.parent.parent
            vault_path = workspace_root / 'vault'
        else:
            vault_path = Path(vault_path)
        
        self.vault_path = vault_path
        self.dry_run = dry_run
        
        # Ensure target folders exist
        for folder in set(self.TARGET_FOLDERS.values()):
            target = self.vault_path / folder
            if not self.dry_run:
                target.mkdir(parents=True, exist_ok=True)
    
    def detect_type(self, filepath: Path) -> str:
        """Detect artifact type from filename"""
        filename = filepath.stem.lower()
        
        for artifact_type, patterns in self.TYPE_PATTERNS.items():
            for pattern in patterns:
                if pattern in filename:
                    return artifact_type
        
        return 'other'
    
    def extract_topic(self, content: str) -> str:
        """Extract topic from artifact content"""
        # Try to get H1 heading
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            topic = h1_match.group(1)
            # Clean up the topic
            topic = re.sub(r'[^\w\s-]', '', topic)
            topic = topic.lower().strip()
            # Convert to slug
            topic = re.sub(r'\s+', '_', topic)
            # Limit length
            words = topic.split('_')[:4]
            return '_'.join(words)
        
        # Fallback: use first meaningful line
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('---')]
        if lines:
            first_line = lines[0][:50]
            first_line = re.sub(r'[^\w\s-]', '', first_line)
            return re.sub(r'\s+', '_', first_line.lower().strip())
        
        return 'untitled'
    
    def generate_filename(self, source_path: Path, content: str) -> Tuple[str, str]:
        """Generate intuitive filename from artifact"""
        artifact_type = self.detect_type(source_path)
        topic = self.extract_topic(content)
        date = datetime.now().strftime('%Y-%m-%d')
        
        # Map type to suffix
        type_suffix = {
            'implementation_plan': 'plan',
            'task': 'task',
            'walkthrough': 'walkthrough',
            'other': 'note',
        }
        
        suffix = type_suffix.get(artifact_type, 'note')
        filename = f"{date}_{topic}_{suffix}.md"
        
        return filename, artifact_type
    
    def add_frontmatter(self, content: str, source_path: Path, topic: str, artifact_type: str) -> str:
        """Add or update frontmatter with sync metadata"""
        now = datetime.now().isoformat()
        
        new_frontmatter = f"""---
type: {artifact_type}
source: {source_path}
synced: {now}
topic: {topic.replace('_', ' ')}
---

"""
        
        # Check if content already has frontmatter
        if content.startswith('---'):
            # Find end of frontmatter
            parts = content.split('---', 2)
            if len(parts) >= 3:
                # Keep original frontmatter and add sync info
                original_fm = parts[1].strip()
                rest = parts[2]
                
                # Add sync metadata to existing frontmatter
                updated_fm = f"""---
{original_fm}
sync_source: {source_path}
sync_time: {now}
---
"""
                return updated_fm + rest
        
        # No existing frontmatter, add new
        return new_frontmatter + content
    
    def sync_artifact(self, source_path: Path) -> Optional[Path]:
        """Sync a single artifact to Obsidian"""
        if not source_path.exists():
            print(f"❌ Source not found: {source_path}")
            return None
        
        # Read content
        content = source_path.read_text(encoding='utf-8')
        
        # Generate filename and detect type
        filename, artifact_type = self.generate_filename(source_path, content)
        topic = self.extract_topic(content)
        
        # Determine target folder
        target_folder = self.TARGET_FOLDERS.get(artifact_type, 'Plans')
        target_path = self.vault_path / target_folder / filename
        
        # Add frontmatter
        synced_content = self.add_frontmatter(content, source_path, topic, artifact_type)
        
        if self.dry_run:
            print(f"[DRY RUN] Would sync:")
            print(f"  Source: {source_path}")
            print(f"  Target: {target_path}")
            print(f"  Type: {artifact_type}")
            print(f"  Topic: {topic}")
            return target_path
        
        # Write to target
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(synced_content, encoding='utf-8')
        
        print(f"✅ Synced: {source_path.name}")
        print(f"   → {target_path}")
        
        return target_path
    
    def sync_recent(self, hours: int = 24) -> list:
        """Sync all recent artifacts from .gemini/brain/"""
        # Find .gemini/brain directory
        workspace_root = Path(__file__).parent.parent.parent.parent.parent
        brain_dir = workspace_root.parent / '.gemini' / 'antigravity' / 'brain'
        
        if not brain_dir.exists():
            print(f"❌ Brain directory not found: {brain_dir}")
            return []
        
        results = []
        cutoff = datetime.now().timestamp() - (hours * 3600)
        
        # Find artifact files
        artifact_patterns = ['implementation_plan.md', 'task.md', 'walkthrough.md']
        
        for conv_dir in brain_dir.iterdir():
            if not conv_dir.is_dir():
                continue
            
            for pattern in artifact_patterns:
                artifact = conv_dir / pattern
                if artifact.exists():
                    # Check if recent
                    if artifact.stat().st_mtime > cutoff:
                        result = self.sync_artifact(artifact)
                        if result:
                            results.append(result)
        
        return results


def main():
    parser = argparse.ArgumentParser(description='Sync AI artifacts to Obsidian')
    parser.add_argument('--source', type=str, help='Path to specific artifact to sync')
    parser.add_argument('--recent', action='store_true', help='Sync all recent artifacts')
    parser.add_argument('--hours', type=int, default=24, help='Hours to look back for --recent')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--vault', type=str, help='Path to Obsidian vault')
    args = parser.parse_args()
    
    sync = ArtifactSync(vault_path=args.vault, dry_run=args.dry_run)
    
    print("🔄 Artifact Sync")
    print("=" * 40)
    
    if args.source:
        source = Path(args.source)
        if not source.is_absolute():
            source = Path.cwd() / source
        sync.sync_artifact(source)
    elif args.recent:
        results = sync.sync_recent(hours=args.hours)
        print(f"\n📊 Synced {len(results)} artifact(s)")
    else:
        print("Usage: Specify --source <path> or --recent")
        print("       Add --dry-run to preview changes")


if __name__ == "__main__":
    main()
