"""
Unified Configuration Loader

Provides a single source of truth for all configuration values.
Priority order:
1. Environment variables (from .env)
2. mcp_config.json (for paths only, no secrets)
3. Default values

Usage:
    from core.config import config
    api_key = config.linear_api_key
    vault_path = config.obsidian_vault_path
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from dotenv import load_dotenv


@dataclass
class Config:
    """Unified configuration with validation."""
    
    # Paths
    workspace_root: Path = field(default_factory=lambda: Path.cwd())
    agent_dir: Path = field(init=False)
    config_dir: Path = field(init=False)
    logs_dir: Path = field(init=False)
    skills_dir: Path = field(init=False)
    
    # Obsidian
    obsidian_vault_path: Optional[Path] = None
    obsidian_api_url: str = "http://localhost:27124"
    obsidian_api_key: Optional[str] = None
    
    # Linear
    linear_api_key: Optional[str] = None
    linear_workspace: Optional[str] = None
    
    # GitHub
    github_username: Optional[str] = None
    github_token: Optional[str] = None
    github_default_branch: str = "main"
    github_repos: Dict[str, Path] = field(default_factory=dict)
    
    # Dev.to
    devto_api_key: Optional[str] = None
    devto_username: Optional[str] = None
    
    def __post_init__(self):
        """Initialize derived paths and load configuration."""
        self.agent_dir = self.workspace_root / ".agent"
        self.config_dir = self.agent_dir / "config"
        self.logs_dir = self.agent_dir / "logs"
        self.skills_dir = self.agent_dir / "skills"
        
        # Ensure logs directory exists
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self._load_env()
        self._load_mcp_config()
        self._validate()
    
    def _load_env(self):
        """Load environment variables from .env file."""
        env_file = self.workspace_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
        
        # Obsidian
        self.obsidian_api_key = os.getenv("OBSIDIAN_API_KEY", self.obsidian_api_key)
        self.obsidian_api_url = os.getenv("OBSIDIAN_API_URL", self.obsidian_api_url)
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
        if vault_path:
            self.obsidian_vault_path = Path(vault_path)
        
        # Linear
        self.linear_api_key = os.getenv("LINEAR_API_KEY", self.linear_api_key)
        self.linear_workspace = os.getenv("LINEAR_WORKSPACE", self.linear_workspace)
        
        # GitHub
        self.github_username = os.getenv("GITHUB_USERNAME", self.github_username)
        self.github_token = os.getenv("GITHUB_TOKEN", self.github_token)
        self.github_default_branch = os.getenv("GITHUB_DEFAULT_BRANCH", self.github_default_branch)
        
        # Dev.to
        self.devto_api_key = os.getenv("DEVTO_API_KEY", self.devto_api_key)
        self.devto_username = os.getenv("DEVTO_USERNAME", self.devto_username)
    
    def _load_mcp_config(self):
        """Load paths from mcp_config.json (no secrets)."""
        config_file = self.config_dir / "mcp_config.json"
        if not config_file.exists():
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                mcp_config = json.load(f)
            
            # Obsidian path (fallback if not in env)
            if not self.obsidian_vault_path:
                vault_path = mcp_config.get("obsidian", {}).get("vault_path")
                if vault_path:
                    self.obsidian_vault_path = Path(vault_path)
            
            # GitHub repos (paths only, not secrets)
            repos = mcp_config.get("github", {}).get("repos", {})
            for name, path in repos.items():
                self.github_repos[name] = Path(path)
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not load mcp_config.json: {e}")
    
    def _validate(self):
        """Validate required configuration is present."""
        self.errors = []
        self.warnings = []
        
        if not self.linear_api_key:
            self.warnings.append("LINEAR_API_KEY not set - Linear integration disabled")
        
        if not self.obsidian_vault_path:
            self.warnings.append("OBSIDIAN_VAULT_PATH not set - Obsidian integration disabled")
        elif not self.obsidian_vault_path.exists():
            self.warnings.append(f"Obsidian vault path does not exist: {self.obsidian_vault_path}")
    
    def is_valid(self) -> bool:
        """Check if configuration is valid (no errors)."""
        return len(self.errors) == 0
    
    def print_status(self):
        """Print configuration status."""
        print("=" * 50)
        print("Personal AI OS Configuration")
        print("=" * 50)
        print(f"Workspace: {self.workspace_root}")
        print(f"Vault: {self.obsidian_vault_path or 'Not configured'}")
        print(f"Linear: {'Configured' if self.linear_api_key else 'Not configured'}")
        print(f"GitHub: {'Configured' if self.github_token else 'Not configured'}")
        print(f"Dev.to: {'Configured' if self.devto_api_key else 'Not configured'}")
        
        if self.warnings:
            print("\nWarnings:")
            for w in self.warnings:
                print(f"  ⚠️ {w}")
        
        if self.errors:
            print("\nErrors:")
            for e in self.errors:
                print(f"  ❌ {e}")


def get_config(workspace_root: Optional[Path] = None) -> Config:
    """Get configuration instance."""
    if workspace_root is None:
        # Try to find workspace root by looking for .agent folder
        cwd = Path.cwd()
        if (cwd / ".agent").exists():
            workspace_root = cwd
        else:
            # Walk up directory tree
            for parent in cwd.parents:
                if (parent / ".agent").exists():
                    workspace_root = parent
                    break
            else:
                workspace_root = cwd
    
    return Config(workspace_root=workspace_root)


# Singleton instance
_config: Optional[Config] = None


def config() -> Config:
    """Get or create the global config instance."""
    global _config
    if _config is None:
        _config = get_config()
    return _config


if __name__ == "__main__":
    # Test configuration loading
    cfg = get_config()
    cfg.print_status()
