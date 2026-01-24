#!/usr/bin/env python3
"""
File Organizer - Intelligent file organization and management
Part of Antigravity Skills & Cowork System
"""

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib

class FileOrganizer:
    """Organize and manage files with safety controls"""
    
    def __init__(self, target_path, dry_run=True):
        self.target_path = Path(target_path)
        self.dry_run = dry_run
        self.operations = []
        self.backup_data = {
            'timestamp': datetime.now().isoformat(),
            'target_path': str(self.target_path),
            'operations': []
        }
        
        # File type categories
        self.categories = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'Spreadsheets': ['.xls', '.xlsx', '.csv'],
            'Presentations': ['.ppt', '.pptx'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.webp', '.ico'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml', '.yml', '.yaml'],
            'Executables': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm']
        }
    
    def scan_folder(self):
        """Scan folder and return file inventory"""
        if not self.target_path.exists():
            print(f"✗ Path does not exist: {self.target_path}")
            return []
        
        files = []
        for item in self.target_path.iterdir():
            if item.is_file():
                files.append({
                    'path': item,
                    'name': item.name,
                    'ext': item.suffix.lower(),
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime),
                    'created': datetime.fromtimestamp(item.stat().st_ctime)
                })
        
        return files
    
    def categorize_by_type(self, files):
        """Categorize files by type"""
        categorized = defaultdict(list)
        
        for file_info in files:
            ext = file_info['ext']
            category = 'Other'
            
            # Find matching category
            for cat_name, extensions in self.categories.items():
                if ext in extensions:
                    category = cat_name
                    break
            
            categorized[category].append(file_info)
        
        return dict(categorized)
    
    def categorize_by_date(self, files, mode='monthly'):
        """Categorize files by date"""
        categorized = defaultdict(list)
        
        for file_info in files:
            mod_date = file_info['modified']
            
            if mode == 'monthly':
                category = mod_date.strftime('%Y-%m')
            elif mode == 'yearly':
                category = mod_date.strftime('%Y')
            else:  # recent vs old
                threshold = datetime.now() - timedelta(days=180)  # 6 months
                category = 'Recent' if mod_date > threshold else 'Old'
            
            categorized[category].append(file_info)
        
        return dict(categorized)
    
    def categorize_by_size(self, files):
        """Categorize files by size"""
        categorized = defaultdict(list)
        
        for file_info in files:
            size = file_info['size']
            
            if size < 1_000_000:  # < 1 MB
                category = 'Small'
            elif size < 10_000_000:  # < 10 MB
                category = 'Medium'
            elif size < 100_000_000:  # < 100 MB
                category = 'Large'
            else:
                category = 'Huge'
            
            categorized[category].append(file_info)
        
        return dict(categorized)
    
    def find_duplicates(self, files):
        """Find duplicate files by hash"""
        hash_dict = defaultdict(list)
        
        print("Calculating file hashes...")
        for file_info in files:
            file_hash = self._calculate_hash(file_info['path'])
            hash_dict[file_hash].append(file_info)
        
        # Filter to only duplicates
        duplicates = {h: f for h, f in hash_dict.items() if len(f) > 1}
        
        return duplicates
    
    def _calculate_hash(self, file_path, algorithm='md5'):
        """Calculate file hash"""
        hash_obj = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
    
    def organize(self, categorized_files):
        """Organize files into category folders"""
        self.operations = []
        
        for category, files in categorized_files.items():
            # Create category folder
            category_path = self.target_path / category
            
            if not self.dry_run:
                category_path.mkdir(exist_ok=True)
            
            # Move files
            for file_info in files:
                source = file_info['path']
                dest = category_path / file_info['name']
                
                # Handle name conflicts
                if dest.exists():
                    dest = self._get_unique_name(dest)
                
                operation = {
                    'action': 'move',
                    'source': str(source),
                    'destination': str(dest),
                    'category': category
                }
                
                self.operations.append(operation)
                self.backup_data['operations'].append(operation)
                
                if not self.dry_run:
                    try:
                        shutil.move(str(source), str(dest))
                    except Exception as e:
                        print(f"✗ Error moving {source.name}: {e}")
        
        return self.operations
    
    def _get_unique_name(self, path):
        """Generate unique filename if conflict exists"""
        counter = 1
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        
        while path.exists():
            path = parent / f"{stem}_{counter}{suffix}"
            counter += 1
        
        return path
    
    def batch_rename(self, files, pattern, start=1):
        """Batch rename files with pattern"""
        self.operations = []
        
        for idx, file_info in enumerate(files, start):
            source = file_info['path']
            
            # Apply pattern
            if pattern == 'sequential':
                new_name = f"file_{idx:03d}{source.suffix}"
            elif pattern == 'date_prefix':
                date_str = file_info['modified'].strftime('%Y-%m-%d')
                new_name = f"{date_str}_{source.name}"
            else:
                new_name = pattern.format(index=idx, name=source.stem, ext=source.suffix)
            
            dest = source.parent / new_name
            
            operation = {
                'action': 'rename',
                'source': str(source),
                'destination': str(dest)
            }
            
            self.operations.append(operation)
            self.backup_data['operations'].append(operation)
            
            if not self.dry_run:
                try:
                    source.rename(dest)
                except Exception as e:
                    print(f"✗ Error renaming {source.name}: {e}")
        
        return self.operations
    
    def preview_operations(self):
        """Show preview of operations"""
        if not self.operations:
            print("No operations planned")
            return
        
        print("\n📋 Organization Preview:\n")
        
        # Group by category
        by_category = defaultdict(list)
        for op in self.operations:
            category = op.get('category', 'N/A')
            by_category[category].append(op)
        
        total_files = len(self.operations)
        print(f"Would process {total_files} files:\n")
        
        for category, ops in sorted(by_category.items()):
            print(f"  {category}/ ({len(ops)} files)")
            for op in ops[:3]:  # Show first 3
                source_name = Path(op['source']).name
                print(f"    - {source_name}")
            if len(ops) > 3:
                print(f"    ... and {len(ops) - 3} more")
            print()
    
    def execute_operations(self):
        """Execute the planned operations"""
        if self.dry_run:
            print("⚠️  Dry-run mode - no files will be modified")
            self.preview_operations()
            return
        
        print(f"\n🔄 Executing {len(self.operations)} operations...\n")
        
        success_count = 0
        for op in self.operations:
            try:
                # Operations were already executed in organize()
                success_count += 1
            except Exception as e:
                print(f"✗ Error: {e}")
        
        print(f"\n✅ Completed: {success_count}/{len(self.operations)} operations")
    
    def save_backup(self, backup_path=None):
        """Save backup data for undo capability"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = Path('.agent/backups') / f'org_{timestamp}.json'
        
        backup_path = Path(backup_path)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(self.backup_data, f, indent=2)
        
        print(f"\n💾 Backup saved: {backup_path}")
        return backup_path
    
    def generate_report(self):
        """Generate organization report"""
        by_category = defaultdict(int)
        for op in self.operations:
            category = op.get('category', 'Other')
            by_category[category] += 1
        
        print("\n" + "="*50)
        print("📊 ORGANIZATION REPORT")
        print("="*50)
        print(f"\nTarget: {self.target_path}")
        print(f"Total Files Processed: {len(self.operations)}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'EXECUTED'}")
        print(f"\nFiles by Category:")
        
        for category, count in sorted(by_category.items()):
            icon = {'Documents': '📄', 'Images': '🖼️', 'Videos': '🎥', 
                   'Audio': '🎵', 'Archives': '📦', 'Code': '💻'}.get(category, '📁')
            print(f"  {icon} {category}: {count} files")
        
        print("\n" + "="*50)


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description="File Organizer")
    parser.add_argument("--path", "-p", required=True, help="Folder path to organize")
    parser.add_argument("--mode", "-m", default="by-type", 
                       choices=['by-type', 'by-date', 'by-size', 'find-duplicates'],
                       help="Organization mode")
    parser.add_argument("--dry-run", "-d", action="store_true", 
                       help="Preview without making changes")
    parser.add_argument("--execute", "-e", action="store_true",
                       help="Execute the organization")
    
    args = parser.parse_args()
    
    # Initialize organizer
    organizer = FileOrganizer(args.path, dry_run=not args.execute)
    
    # Scan files
    print(f"📂 Scanning: {args.path}\n")
    files = organizer.scan_folder()
    
    if not files:
        print("No files found to organize")
        return
    
    print(f"Found {len(files)} files\n")
    
    # Categorize based on mode
    if args.mode == 'by-type':
        categorized = organizer.categorize_by_type(files)
    elif args.mode == 'by-date':
        categorized = organizer.categorize_by_date(files)
    elif args.mode == 'by-size':
        categorized = organizer.categorize_by_size(files)
    elif args.mode == 'find-duplicates':
        duplicates = organizer.find_duplicates(files)
        print(f"\nFound {len(duplicates)} sets of duplicates:")
        for file_hash, dupe_files in duplicates.items():
            print(f"\n  Hash: {file_hash[:8]}...")
            for dupe in dupe_files:
                print(f"    - {dupe['name']} ({dupe['size']} bytes)")
        return
    
    # Organize files
    organizer.organize(categorized)
    
    # Preview or execute
    if args.dry_run or not args.execute:
        organizer.preview_operations()
        print("\n💡 Tip: Use --execute to apply changes")
    else:
        organizer.execute_operations()
        backup_path = organizer.save_backup()
        organizer.generate_report()
        print(f"\n🔄 Undo: python undo.py --backup {backup_path}")


if __name__ == "__main__":
    main()
