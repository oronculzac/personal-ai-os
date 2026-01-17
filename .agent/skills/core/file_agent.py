#!/usr/bin/env python3
"""
Cowork File Agent - Autonomous file management
Coordinates file operations with safety controls
"""

import sys
import os
from pathlib import Path
import json

# Add workspace root to path
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

# Now import our modules
from folder_permissions import FolderPermissionManager

# Import organizer directly
sys.path.insert(0, str(Path(__file__).parent.parent / 'skills' / 'file_organizer' / 'scripts'))
from organizer import FileOrganizer


class CoworkFileAgent:
    """Autonomous file management agent"""
    
    def __init__(self):
        self.permission_manager = FolderPermissionManager()
        self.current_task = None
        self.task_history = []
    
    def organize_folder(self, folder_path, mode='by-type', dry_run=True):
        """
        Organize a folder with automatic permission handling
        
        Args:
            folder_path: Path to folder to organize
            mode: Organization mode (by-type, by-date, by-size)
            dry_run: Preview changes without executing
        
        Returns:
            dict with task results
        """
        folder_path = Path(folder_path).resolve()
        
        # Step 1: Request folder access
        print(f"\n🤖 Cowork File Agent")
        print(f"Task: Organize {folder_path}")
        print(f"Mode: {mode}")
        print(f"Dry Run: {dry_run}\n")
        
        has_access = self.permission_manager.request_access(
            path=str(folder_path),
            reason=f"Organize files using '{mode}' mode"
        )
        
        if not has_access:
            return {
                'success': False,
                'error': 'Folder access denied'
            }
        
        # Grant access if not already granted
        if not self.permission_manager.has_access(str(folder_path)):
            self.permission_manager.grant_access(str(folder_path))
        
        # Step 2: Initialize organizer
        organizer = FileOrganizer(folder_path, dry_run=dry_run)
        
        # Step 3: Scan files
        print(f"📂 Scanning folder...\n")
        files = organizer.scan_folder()
        
        if not files:
            return {
                'success': True,
                'message': 'No files found to organize',
                'files_processed': 0
            }
        
        print(f"Found {len(files)} files")
        
        # Step 4: Categorize
        if mode == 'by-type':
            categorized = organizer.categorize_by_type(files)
        elif mode == 'by-date':
            categorized = organizer.categorize_by_date(files)
        elif mode == 'by-size':
            categorized = organizer.categorize_by_size(files)
        else:
            return {
                'success': False,
                'error': f'Unknown mode: {mode}'
            }
        
        # Step 5: Create organization plan
        organizer.organize(categorized)
        
        # Step 6: Preview or execute
        if dry_run:
            organizer.preview_operations()
            result = {
                'success': True,
                'dry_run': True,
                'operations': organizer.operations,
                'files_processed': len(organizer.operations),
                'categories': list(categorized.keys())
            }
        else:
            organizer.execute_operations()
            backup_path = organizer.save_backup()
            organizer.generate_report()
            
            # Log to audit
            self.permission_manager.log_operation(
                operation='organize_folder',
                path=str(folder_path),
                success=True
            )
            
            result = {
                'success': True,
                'dry_run': False,
                'operations': organizer.operations,
                'files_processed': len(organizer.operations),
                'categories': list(categorized.keys()),
                'backup_path': str(backup_path)
            }
        
        # Save to task history
        self.task_history.append({
            'task': 'organize_folder',
            'path': str(folder_path),
            'mode': mode,
            'dry_run': dry_run,
            'result': result
        })
        
        return result
    
    def find_duplicates(self, folder_path):
        """Find duplicate files in folder"""
        folder_path = Path(folder_path).resolve()
        
        # Request access
        has_access = self.permission_manager.request_access(
            path=str(folder_path),
            reason="Find duplicate files"
        )
        
        if not has_access:
            return {'success': False, 'error': 'Access denied'}
        
        # Grant if needed
        if not self.permission_manager.has_access(str(folder_path)):
            self.permission_manager.grant_access(str(folder_path), access_level='read')
        
        # Scan and find duplicates
        organizer = FileOrganizer(folder_path, dry_run=True)
        files = organizer.scan_folder()
        duplicates = organizer.find_duplicates(files)
        
        # Calculate space that could be saved
        space_saved = 0
        for dupe_group in duplicates.values():
            # Keep one, save space from others
            space_saved += sum(f['size'] for f in dupe_group[1:])
        
        return {
            'success': True,
            'duplicate_groups': len(duplicates),
            'total_duplicates': sum(len(g) - 1 for g in duplicates.values()),
            'space_saved_bytes': space_saved,
            'space_saved_mb': round(space_saved / 1_000_000, 2),
            'duplicates': duplicates
        }
    
    def batch_rename(self, folder_path, pattern, dry_run=True):
        """Batch rename files in folder"""
        folder_path = Path(folder_path).resolve()
        
        # Request access
        has_access = self.permission_manager.request_access(
            path=str(folder_path),
            reason=f"Batch rename files with pattern: {pattern}"
        )
        
        if not has_access:
            return {'success': False, 'error': 'Access denied'}
        
        # Grant if needed
        if not self.permission_manager.has_access(str(folder_path)):
            self.permission_manager.grant_access(str(folder_path))
        
        # Rename files
        organizer = FileOrganizer(folder_path, dry_run=dry_run)
        files = organizer.scan_folder()
        operations = organizer.batch_rename(files, pattern)
        
        if dry_run:
            organizer.preview_operations()
        else:
            organizer.execute_operations()
            self.permission_manager.log_operation(
                operation='batch_rename',
                path=str(folder_path),
                success=True
            )
        
        return {
            'success': True,
            'dry_run': dry_run,
            'files_renamed': len(operations),
            'operations': operations
        }


def main():
    """CLI for Cowork File Agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cowork File Agent")
    parser.add_argument("--path", "-p", required=True, help="Folder path")
    parser.add_argument("--action", "-a", default="organize",
                       choices=['organize', 'duplicates', 'rename'],
                       help="Action to perform")
    parser.add_argument("--mode", "-m", default="by-type",
                       help="Organization mode (for organize action)")
    parser.add_argument("--pattern", help="Rename pattern (for rename action)")
    parser.add_argument("--execute", "-e", action="store_true",
                       help="Execute (not dry-run)")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = CoworkFileAgent()
    
    # Perform action
    if args.action == 'organize':
        result = agent.organize_folder(
            args.path,
            mode=args.mode,
            dry_run=not args.execute
        )
    elif args.action == 'duplicates':
        result = agent.find_duplicates(args.path)
    elif args.action == 'rename':
        if not args.pattern:
            print("Error: --pattern required for rename action")
            return
        result = agent.batch_rename(
            args.path,
            pattern=args.pattern,
            dry_run=not args.execute
        )
    
    # Print result
    print(f"\n📊 Result: {json.dumps(result, indent=2, default=str)}")


if __name__ == "__main__":
    main()
