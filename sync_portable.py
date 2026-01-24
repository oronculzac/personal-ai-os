#!/usr/bin/env python3
"""
Sync Script - Keep portable_setup folder up-to-date
Run this after making changes to skills, personas, or core files
"""

import shutil
from pathlib import Path
import json
from datetime import datetime

def sync_portable_setup():
    """Sync .agent folder to portable_setup/agent"""
    
    source = Path('.agent')
    dest = Path('portable_setup/agent')
    
    if not source.exists():
        print(f"✗ Source folder not found: {source}")
        return False
    
    # Exclusions - what NOT to copy
    exclude_dirs = {'.venv', '__pycache__', 'backups', 'test_folder'}
    exclude_files = {'active_persona.json', '.sync_info.json'}
    
    print("🔄 Syncing .agent folder to portable_setup/agent...")
    print(f"Source: {source.absolute()}")
    print(f"Destination: {dest.absolute()}\n")
    
    # Remove old destination
    if dest.exists():
        print("Removing old portable_setup/agent...")
        shutil.rmtree(dest)
    
    # Create new destination
    dest.mkdir(parents=True, exist_ok=True)
    print("✓ Created fresh portable_setup/agent\n")
    
    # Copy with exclusions
    copied_files = 0
    copied_dirs = 0
    skipped = 0
    
    def should_exclude(path):
        """Check if path should be excluded"""
        parts = path.parts
        # Check directory names
        if any(excl in parts for excl in exclude_dirs):
            return True
        # Check filename
        if path.name in exclude_files:
            return True
        # Check extensions
        if path.suffix == '.pyc':
            return True
        return False
    
    # Walk through source directory
    for item in source.rglob('*'):
        # Skip excluded items
        if should_exclude(item):
            skipped += 1
            continue
        
        # Calculate destination path
        rel_path = item.relative_to(source)
        dest_path = dest / rel_path
        
        try:
            if item.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
                copied_dirs += 1
            elif item.is_file():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)
                copied_files += 1
                # Print progress for important files
                if any(x in str(rel_path) for x in ['SKILL.md', '.json', '.py']):
                    print(f"  ✓ {rel_path}")
        except Exception as e:
            print(f"  ⚠ Could not copy {rel_path}: {e}")
    
    print(f"\n📊 Sync Summary:")
    print(f"  Files copied: {copied_files}")
    print(f"  Directories created: {copied_dirs}")
    print(f"  Items skipped: {skipped}")
    
    # Update sync metadata
    sync_info = {
        'last_sync': datetime.now().isoformat(),
        'files_copied': copied_files,
        'directories_copied': copied_dirs,
        'items_skipped': skipped,
        'source': str(source.absolute()),
        'destination': str(dest.absolute())
    }
    
    sync_file = Path('portable_setup/.sync_info.json')
    with open(sync_file, 'w') as f:
        json.dump(sync_info, f, indent=2)
    
    print(f"\n✅ Portable setup is now up-to-date!")
    print(f"   Last synced: {sync_info['last_sync']}")
    print(f"\n📦 Ready to copy portable_setup/ folder to new location")
    
    return True


if __name__ == "__main__":
    try:
        sync_portable_setup()
    except Exception as e:
        print(f"\n✗ Sync failed: {e}")
        exit(1)
