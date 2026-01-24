#!/usr/bin/env python3
"""
Environment Setup Helper
Automate environment setup and validation for data engineering projects
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import platform


class EnvironmentSetup:
    """Manage data engineering environment setup and validation"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.python_version = sys.version_info
        self.checks = {}
        
    def check_python(self) -> Tuple[bool, str]:
        """Check Python version"""
        version = f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}"
        
        if self.python_version >= (3, 8):
            return True, f"✓ Python {version} (supported)"
        else:
            return False, f"✗ Python {version} (need 3.8+)"
    
    def check_docker(self) -> Tuple[bool, str]:
        """Check if Docker is installed and running"""
        try:
            result = subprocess.run(
                ['docker', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                # Test if Docker daemon is running
                test_result = subprocess.run(
                    ['docker', 'ps'],
                    capture_output=True,
                    timeout=5
                )
                
                if test_result.returncode == 0:
                    return True, f"✓ {version} (running)"
                else:
                    return False, f"⚠ Docker installed but daemon not running"
            else:
                return False, "✗ Docker not found"
                
        except FileNotFoundError:
            return False, "✗ Docker not installed"
        except subprocess.TimeoutExpired:
            return False, "⚠ Docker not responding"
        except Exception as e:
            return False, f"✗ Error checking Docker: {e}"
    
    def check_docker_compose(self) -> Tuple[bool, str]:
        """Check Docker Compose installation"""
        try:
            result = subprocess.run(
                ['docker', 'compose', 'version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, f"✓ {version}"
            else:
                return False, "✗ Docker Compose not found"
                
        except Exception as e:
            return False, f"✗ Docker Compose: {e}"
    
    def check_terraform(self) -> Tuple[bool, str]:
        """Check Terraform installation"""
        try:
            result = subprocess.run(
                ['terraform', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.split('\\n')[0]
                return True, f"✓ {version}"
            else:
                return False, "✗ Terraform not found"
                
        except FileNotFoundError:
            return False, "✗ Terraform not installed"
        except Exception as e:
            return False, f"✗ Error: {e}"
    
    def check_gcloud(self) -> Tuple[bool, str]:
        """Check Google Cloud SDK"""
        try:
            result = subprocess.run(
                ['gcloud', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version_line = result.stdout.split('\\n')[0]
                return True, f"✓ {version_line}"
            else:
                return False, "✗ GCloud CLI not found"
                
        except FileNotFoundError:
            return False, "✗ GCloud CLI not installed"
        except Exception as e:
            return False, f"✗ Error: {e}"
    
    def check_git(self) -> Tuple[bool, str]:
        """Check Git installation"""
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, f"✓ {version}"
            else:
                return False, "✗ Git not found"
                
        except FileNotFoundError:
            return False, "✗ Git not installed"
        except Exception as e:
            return False, f"✗ Error: {e}"
    
    def check_java(self) -> Tuple[bool, str]:
        """Check Java installation (needed for Spark)"""
        try:
            result = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Java outputs to stderr
            output = result.stderr if result.stderr else result.stdout
            
            if 'version' in output.lower():
                version_line = output.split('\\n')[0]
                return True, f"✓ {version_line}"
            else:
                return False, "✗ Java not found"
                
        except FileNotFoundError:
            return False, "⚠ Java not installed (needed for Spark)"
        except Exception as e:
            return False, f"⚠ Error: {e}"
    
    def check_virtualenv(self, venv_path: str = ".venv") -> Tuple[bool, str]:
        """Check if virtual environment exists"""
        venv_dir = Path(venv_path)
        
        if venv_dir.exists():
            python_path = venv_dir / "Scripts" / "python.exe" if self.os_type == "Windows" else venv_dir / "bin" / "python"
            
            if python_path.exists():
                return True, f"✓ Virtual environment found at {venv_path}"
            else:
                return False, f"⚠ Directory exists but not a valid venv: {venv_path}"
        else:
            return False, f"✗ No virtual environment at {venv_path}"
    
    def create_virtualenv(self, venv_path: str = ".venv") -> Tuple[bool, str]:
        """Create a new virtual environment"""
        try:
            print(f"Creating virtual environment at {venv_path}...")
            
            result = subprocess.run(
                [sys.executable, '-m', 'venv', venv_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, f"✓ Created virtual environment at {venv_path}"
            else:
                return False, f"✗ Failed to create venv: {result.stderr}"
                
        except Exception as e:
            return False, f"✗ Error creating venv: {e}"
    
    def install_requirements(self, requirements_file: str = "requirements.txt") -> Tuple[bool, str]:
        """Install packages from requirements.txt"""
        req_path = Path(requirements_file)
        
        if not req_path.exists():
            return False, f"✗ Requirements file not found: {requirements_file}"
        
        try:
            print(f"Installing requirements from {requirements_file}...")
            
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', requirements_file],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return True, f"✓ Installed packages from {requirements_file}"
            else:
                return False, f"✗ Installation failed: {result.stderr}"
                
        except Exception as e:
            return False, f"✗ Error: {e}"
    
    def validate_all(self) -> Dict[str, Tuple[bool, str]]:
        """Run all validation checks"""
        checks = {
            'Python': self.check_python(),
            'Docker': self.check_docker(),
            'Docker Compose': self.check_docker_compose(),
            'Terraform': self.check_terraform(),
            'GCloud CLI': self.check_gcloud(),
            'Git': self.check_git(),
            'Java': self.check_java(),
            'Virtual Env': self.check_virtualenv()
        }
        
        self.checks = checks
        return checks
    
    def print_report(self):
        """Print validation report"""
        print("\\n" + "="*50)
        print("Environment Setup Validation Report")
        print("="*50 + "\\n")
        
        if not self.checks:
            self.validate_all()
        
        passed = 0
        total = len(self.checks)
        
        for tool, (status, message) in self.checks.items():
            print(f"{tool:20} {message}")
            if status:
                passed += 1
        
        print("\\n" + "-"*50)
        percentage = int((passed / total) * 100)
        print(f"Status: {passed}/{total} checks passed ({percentage}%)")
        print("-"*50 + "\\n")
        
        if percentage < 100:
            print("⚠ Some tools are missing or not configured properly.")
            print("Run with --help to see setup instructions.\\n")
        else:
            print("✅ All checks passed! Environment is ready.\\n")
    
    def setup_for_module(self, module_num: int):
        """Setup environment for specific course module"""
        print(f"\\nSetting up environment for Module {module_num}...\\n")
        
        module_requirements = {
            1: ['Python', 'Docker', 'Docker Compose', 'Terraform', 'GCloud CLI'],
            2: ['Python', 'Docker', 'Virtual Env'],
            3: ['Python', 'GCloud CLI', 'Virtual Env'],
            4: ['Python', 'Virtual Env'],
            5: ['Python', 'Java', 'Virtual Env'],
            6: ['Python', 'Docker', 'Virtual Env']
        }
        
        required = module_requirements.get(module_num, [])
        
        if not required:
            print(f"Unknown module: {module_num}")
            return
        
        print(f"Required tools for Module {module_num}: {', '.join(required)}\\n")
        
        if not self.checks:
            self.validate_all()
        
        missing = []
        for tool in required:
            if tool in self.checks:
                status, message = self.checks[tool]
                if not status:
                    missing.append(tool)
        
        if missing:
            print(f"⚠ Missing tools: {', '.join(missing)}")
            print("\\nPlease install the missing tools before proceeding.\\n")
        else:
            print(f"✅ All required tools for Module {module_num} are installed!\\n")


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Environment Setup Helper")
    parser.add_argument('--validate', action='store_true', help='Run all validation checks')
    parser.add_argument('--module', type=int, help='Check setup for specific module (1-6)')
    parser.add_argument('--create-venv', metavar='PATH', help='Create virtual environment')
    parser.add_argument('--install-req', metavar='FILE', help='Install from requirements.txt')
    
    args = parser.parse_args()
    
    setup = EnvironmentSetup()
    
    if args.validate or (not any(vars(args).values())):
        setup.validate_all()
        setup.print_report()
    
    if args.module:
        setup.setup_for_module(args.module)
    
    if args.create_venv:
        success, message = setup.create_virtualenv(args.create_venv)
        print(message)
    
    if args.install_req:
        success, message = setup.install_requirements(args.install_req)
        print(message)


if __name__ == "__main__":
    main()
