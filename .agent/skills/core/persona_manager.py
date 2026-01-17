#!/usr/bin/env python3
"""
Persona Manager - Manage specialized agent personas
Handles loading, switching, and filtering skills based on active persona
"""

import json
from pathlib import Path
from datetime import datetime


class PersonaManager:
    """Manage agent personas and skill restrictions"""
    
    def __init__(self, personas_dir='.agent/personas', config_dir='.agent/config'):
        self.personas_dir = Path(personas_dir)
        self.config_dir = Path(config_dir)
        self.active_persona_file = self.config_dir / 'active_persona.json'
        
        self.personas = {}
        self.active_persona = None
        
        self.load_all_personas()
        self.load_active_persona()
    
    def load_all_personas(self):
        """Load all persona configurations from personas directory"""
        if not self.personas_dir.exists():
            print(f"⚠️  Personas directory not found: {self.personas_dir}")
            return
        
        persona_count = 0
        for persona_file in self.personas_dir.glob('*.json'):
            try:
                with open(persona_file, 'r', encoding='utf-8') as f:
                    persona_data = json.load(f)
                
                persona_id = persona_data.get('id')
                if persona_id:
                    self.personas[persona_id] = persona_data
                    persona_count += 1
                    print(f"✓ Loaded persona: {persona_data.get('name', persona_id)}")
            except Exception as e:
                print(f"✗ Error loading {persona_file.name}: {e}")
        
        print(f"\n📋 Total personas loaded: {persona_count}")
    
    def load_active_persona(self):
        """Load the currently active persona from config"""
        if self.active_persona_file.exists():
            try:
                with open(self.active_persona_file, 'r', encoding='utf-8') as f:
                    active_data = json.load(f)
                
                persona_id = active_data.get('persona_id')
                if persona_id and persona_id in self.personas:
                    self.active_persona = self.personas[persona_id]
                    print(f"✓ Active persona: {self.active_persona['name']}")
                else:
                    print("⚠️  No valid active persona found")
            except Exception as e:
                print(f"✗ Error loading active persona: {e}")
        else:
            print("ℹ️  No active persona set (using default mode - all skills available)")
    
    def activate_persona(self, persona_id):
        """Switch to a specific persona"""
        if persona_id not in self.personas:
            print(f"✗ Persona not found: {persona_id}")
            print(f"Available personas: {', '.join(self.personas.keys())}")
            return False
        
        self.active_persona = self.personas[persona_id]
        
        # Save to config
        self.config_dir.mkdir(parents=True, exist_ok=True)
        active_data = {
            'persona_id': persona_id,
            'activated_at': datetime.now().isoformat(),
            'persona_name': self.active_persona['name']
        }
        
        with open(self.active_persona_file, 'w', encoding='utf-8') as f:
            json.dump(active_data, f, indent=2)
        
        print(f"\n🎭 Switched to: {self.active_persona['name']}")
        print(f"📝 Description: {self.active_persona['description']}")
        print(f"\n🛠️  Available skills:")
        for skill in self.active_persona.get('allowed_skills', []):
            print(f"   - {skill}")
        
        return True
    
    def deactivate_persona(self):
        """Return to default mode (all skills available)"""
        self.active_persona = None
        
        if self.active_persona_file.exists():
            self.active_persona_file.unlink()
        
        print("✓ Returned to default mode (all skills available)")
    
    def get_allowed_skills(self):
        """Get list of skills available to current persona"""
        if not self.active_persona:
            return None  # None means all skills are allowed
        
        return self.active_persona.get('allowed_skills', [])
    
    def get_system_prompt(self):
        """Get persona-specific system prompt"""
        if not self.active_persona:
            return ""
        
        return self.active_persona.get('system_prompt', '')
    
    def get_active_persona_info(self):
        """Get information about currently active persona"""
        if not self.active_persona:
            return {
                'active': False,
                'mode': 'default',
                'message': 'All skills available'
            }
        
        return {
            'active': True,
            'persona_id': self.active_persona['id'],
            'name': self.active_persona['name'],
            'description': self.active_persona['description'],
            'allowed_skills': self.active_persona.get('allowed_skills', []),
            'expertise': self.active_persona.get('expertise', [])
        }
    
    def list_personas(self):
        """List all available personas"""
        print("\n📋 Available Personas:\n")
        
        for persona_id, persona in self.personas.items():
            status = "🎭 ACTIVE" if (self.active_persona and self.active_persona['id'] == persona_id) else "  "
            print(f"{status} {persona['name']} ({persona_id})")
            print(f"      {persona['description']}")
            print(f"      Skills: {', '.join(persona.get('allowed_skills', []))}")
            print()
    
    def filter_skills(self, all_skills):
        """Filter skills based on active persona's allowed list"""
        if not self.active_persona:
            return all_skills  # No filtering in default mode
        
        allowed = set(self.active_persona.get('allowed_skills', []))
        filtered = [s for s in all_skills if s.get('id') in allowed]
        
        print(f"🔍 Filtered to {len(filtered)}/{len(all_skills)} skills for {self.active_persona['name']}")
        
        return filtered


def main():
    """CLI for persona management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Persona Manager")
    parser.add_argument("--list", "-l", action="store_true", help="List all personas")
    parser.add_argument("--activate", "-a", help="Activate a persona by ID")
    parser.add_argument("--deactivate", "-d", action="store_true", help="Deactivate current persona")
    parser.add_argument("--status", "-s", action="store_true", help="Show current persona status")
    
    args = parser.parse_args()
    
    pm = PersonaManager()
    
    if args.list:
        pm.list_personas()
    elif args.activate:
        pm.activate_persona(args.activate)
    elif args.deactivate:
        pm.deactivate_persona()
    elif args.status:
        info = pm.get_active_persona_info()
        print(json.dumps(info, indent=2))
    else:
        # Default: show status and list
        info = pm.get_active_persona_info()
        if info['active']:
            print(f"\n🎭 Active Persona: {info['name']}")
            print(f"📝 {info['description']}")
            print(f"\n🛠️  Available skills: {', '.join(info['allowed_skills'])}")
        else:
            print("\nℹ️  No active persona (default mode)")
        
        print("\n" + "="*50)
        pm.list_personas()


if __name__ == "__main__":
    main()
