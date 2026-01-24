#!/usr/bin/env python3
"""
Skill Discovery and Management Helper
Scans .agent/skills/ and registers available skills
"""

import json
import os
from pathlib import Path
import yaml

def discover_skills(skills_dir='.agent/skills'):
    """Scan skills directory and build registry"""
    skills = []
    skills_path = Path(skills_dir)
    
    if not skills_path.exists():
        print(f"Skills directory not found: {skills_dir}")
        return skills
    
    for skill_folder in skills_path.iterdir():
        if not skill_folder.is_dir():
            continue
            
        skill_md = skill_folder / 'SKILL.md'
        if not skill_md.exists():
            continue
        
        # Parse SKILL.md frontmatter
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    
                    skill_info = {
                        'id': skill_folder.name,
                        'name': frontmatter.get('name', skill_folder.name),
                        'description': frontmatter.get('description', ''),
                        'version': frontmatter.get('version', '1.0.0'),
                        'path': str(skill_folder),
                        'triggers': frontmatter.get('triggers', []),
                        'capabilities': frontmatter.get('capabilities', []),
                        'dependencies': frontmatter.get('dependencies', []),
                        'enabled': True,
                        'auto_load': frontmatter.get('auto_load', True)
                    }
                    
                    skills.append(skill_info)
                    print(f"✓ Discovered skill: {skill_info['name']}")
        except Exception as e:
            print(f"✗ Error parsing {skill_folder.name}: {e}")
    
    return skills

def update_registry(skills):
    """Update skill_registry.json with discovered skills"""
    registry_path = Path('.agent/config/skill_registry.json')
    
    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    else:
        registry = {'version': '1.0', 'skills': []}
    
    registry['skills'] = skills
    
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    
    print(f"\n✓ Registry updated: {len(skills)} skills registered")

if __name__ == '__main__':
    print("Scanning for skills...")
    skills = discover_skills()
    update_registry(skills)
    print(f"\nTotal skills found: {len(skills)}")
    
    for skill in skills:
        print(f"  - {skill['name']} (v{skill['version']})")
