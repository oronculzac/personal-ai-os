#!/usr/bin/env python3
"""
Project Onboarder
Automates new project setup: Folders, Git, Linear, Obsidian.

Usage:
    python onboard.py [--name "project-name"] [--description "Description"] [--dry-run]
"""

import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add paths for imports
agent_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(agent_root / 'skills' / 'linear_manager' / 'scripts'))
sys.path.insert(0, str(agent_root / 'core'))

from linear_client import LinearClient
from obsidian_client import create_note, get_vault_path

class ProjectOnboarder:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.workspace_root = agent_root.parent
        self.projects_root = self.workspace_root / 'projects'
        self.linear = LinearClient()
        self.vault_path = get_vault_path()

    def create_structure(self, project_name: str) -> Path:
        """Create project directory structure"""
        project_path = self.projects_root / project_name
        
        folders = ['src', 'docs', 'notebooks']
        
        print(f"📂 Creating folders in {project_path}...")
        
        if self.dry_run:
            return project_path

        project_path.mkdir(parents=True, exist_ok=True)
        for folder in folders:
            (project_path / folder).mkdir(exist_ok=True)
            
        return project_path

    def init_git(self, project_path: Path, description: str):
        """Initialize git repository"""
        print("🐙 Initializing Git...")
        
        if self.dry_run:
            return

        # git init
        subprocess.run(['git', 'init'], cwd=project_path, check=True, capture_output=True)
        
        # .gitignore
        gitignore = """
__pycache__/
*.pyc
.env
.ipynb_checkpoints/
node_modules/
.DS_Store
"""
        (project_path / '.gitignore').write_text(gitignore.strip())
        
        # README.md
        readme = f"# {project_path.name}\n\n{description}\n"
        (project_path / 'README.md').write_text(readme)
        
        # Initial commit
        subprocess.run(['git', 'add', '.'], cwd=project_path, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', ':tada: Initial commit'], cwd=project_path, check=True, capture_output=True)

    def create_linear_project(self, name: str, description: str) -> Optional[str]:
        """Create Linear project and return ID"""
        print("⚡ Creating Linear project...")
        
        if self.dry_run:
            return "DRY-RUN-ID"

        try:
            # Create project (LinearClient needs create_project method)
            # Checking LinearClient capabilities... existing client has create_project
            project = self.linear.create_project(name=name, description=description)
            return project['id']
            # Note: The returned object might act differently depending on implementation
            # Checking the code I saw earlier: return result['data']['projectCreate']['project'] which has 'id'
        except Exception as e:
            print(f"⚠️ Failed to create Linear project: {e}")
            return None

    def create_obsidian_note(self, name: str, description: str, linear_id: Optional[str], project_path: Path):
        """Create Obsidian project note"""
        print("📓 Creating Obsidian note...")
        
        if self.dry_run:
            return

        if not self.vault_path:
            print("⚠️ No Obsidian vault configured. Skipping note creation.")
            return
            
        # Prepare frontmatter
        relative_path = project_path.relative_to(self.workspace_root).as_posix()
        linear_link = f"https://linear.app/project/{linear_id}" if linear_id else "N/A"
        frontmatter = {
            "type": "project",
            "status": "active",
            "linear_id": linear_id or "N/A",
            "git_path": relative_path,
            "created": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Prepare content
        template_path = self.vault_path / "Templates" / "project-template.md"
        if template_path.exists():
            content = template_path.read_text(encoding='utf-8')
            # Replace placeholders
            content = content.replace("{PROJECT_NAME}", name.replace("-", " ").title())
            content = content.replace("{DESCRIPTION}", description)
            content = content.replace("{LINEAR_ID}", linear_id or "N/A")
            content = content.replace("{LINEAR_URL}", linear_link)
            content = content.replace("{LOCA_PATH}", relative_path)
            content = content.replace("{GIT_PATH}", relative_path)
            content = content.replace("{DATE}", datetime.now().strftime("%Y-%m-%d"))
        else:
            # Fallback if template missing
            content = f"""
{description}

## 🔗 Links
- [[Local Folder]]: `{relative_path}`
- [Linear Project]({linear_link})

## 📝 Notes
- [ ] Initial planning
"""
        
        # Create note
        try:
            create_note(
                folder="Projects",  # Assuming Projects folder exists or will be created
                title=name.replace("-", " ").title(),
                content=content,
                frontmatter=frontmatter,
                vault_path=self.vault_path
            )
        except Exception as e:
            print(f"⚠️ Failed to create Obsidian note: {e}")

    def run(self, name: str, description: str):
        print(f"🚀 Onboarding Project: {name}")
        print("=" * 30)
        
        # 1. Create Folder Structure
        project_path = self.create_structure(name)
        
        # 2. Init Git
        self.init_git(project_path, description)
        
        # 3. Linear Project
        linear_id = self.create_linear_project(name, description)
        if linear_id:
            print(f"✅ Linear Project Created: {linear_id}")
            
        # 4. Obsidian Note
        self.create_obsidian_note(name, description, linear_id, project_path)
        
        print("=" * 30)
        print("✅ Onboarding Complete!")
        print(f"📍 Location: {project_path}")

def main():
    parser = argparse.ArgumentParser(description='Onboard new project')
    parser.add_argument('--name', help='Project name (slug)')
    parser.add_argument('--description', help='Project description')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    args = parser.parse_args()
    
    # Interactive mode if args missing
    name = args.name
    if not name:
        name = input("Project Name (slug, e.g. my-cool-app): ").strip()
    
    description = args.description
    if not description:
        description = input("Description: ").strip()
        
    onboarder = ProjectOnboarder(dry_run=args.dry_run)
    onboarder.run(name, description)

if __name__ == "__main__":
    main()
