#!/usr/bin/env python3
"""
Folder Permission Manager
Handles safe folder access for Cowork functionality
"""

import json
from pathlib import Path
from datetime import datetime

class FolderPermissionManager:
    def __init__(self, config_path='.agent/config/folder_permissions.json'):
        self.config_path = Path(config_path)
        self.load_config()
    
    def load_config(self):
        """Load permissions configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'version': '1.0',
                'permissions': [],
                'audit_log': []
            }
    
    def save_config(self):
        """Save permissions configuration"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def request_access(self, path, reason, access_level='read'):
        """Request access to a folder"""
        path = str(Path(path).resolve())
        
        # Check if already granted
        for perm in self.config['permissions']:
            if perm['path'] == path:
                print(f"✓ Access already granted to: {path}")
                return True
        
        print(f"\n📁 Folder Access Request:")
        print(f"   Path: {path}")
        print(f"   Reason: {reason}")
        print(f"   Access Level: {access_level}")
        
        # In production, this would prompt user
        # For now, return True for demo
        return True
    
    def grant_access(self, path, access_level='read_write'):
        """Grant access to a folder"""
        permission = {
            'path': str(Path(path).resolve()),
            'granted_at': datetime.now().isoformat(),
            'access_level': access_level,
            'auto_approve_operations': False
        }
        
        self.config['permissions'].append(permission)
        self.save_config()
        print(f"✓ Access granted to: {path}")
    
    def has_access(self, path):
        """Check if access is granted to path"""
        path = str(Path(path).resolve())
        
        for perm in self.config['permissions']:
            if path.startswith(perm['path']):
                return True
        return False
    
    def log_operation(self, operation, path, success=True):
        """Log file operation to audit log"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'path': str(path),
            'success': success
        }
        
        self.config['audit_log'].append(log_entry)
        self.save_config()

if __name__ == '__main__':
    pm = FolderPermissionManager()
    print("Folder Permission Manager initialized")
    print(f"Current permissions: {len(pm.config['permissions'])}")
