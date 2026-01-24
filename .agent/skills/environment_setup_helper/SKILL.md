---
name: Environment Setup Helper
description: Automate environment setup, dependency management, and validation for data engineering projects
version: 1.1.0
triggers:
  - setup environment
  - check dependencies
  - validate setup
  - create virtual environment
  - install requirements
  - setup docker
  - configure gcp
  - initialize terraform
examples:
  - "Setup my environment for Module 1"
  - "Check if Docker is running"
  - "Create a virtual environment for this project"
  - "Validate my GCP configuration"
context_hints:
  - user mentions environment setup or dependencies
  - user has installation or configuration issues
  - user mentions Docker, Terraform, or GCP setup
  - user starting a new module
priority: 7
conflicts_with: []
capabilities:
  - environment_creation
  - dependency_validation
  - docker_setup
  - cloud_configuration
  - tool_installation
  - health_checks
dependencies: []
auto_load: true
---

# Environment Setup Helper Skill

Automate environment setup and validation for data engineering projects.

## 🎯 Purpose

Streamline the setup process for data engineering environments, ensuring all tools, dependencies, and configurations are properly installed and validated.

## 🚀 Capabilities

### 1. **Virtual Environment Management**
- Create Python virtual environments
- Activate/deactivate environments
- Generate requirements.txt
- Validate installed packages
- Manage multiple Python versions

### 2. **Docker Setup**
- Check Docker installation
- Validate Docker Compose
- Test container connectivity
- Setup Docker networks
- Manage Docker volumes

### 3. **Cloud Platform Configuration**
- GCP authentication setup
- AWS credentials configuration
- Azure CLI setup
- Service account management
- Permission validation

### 4. **Terraform Initialization**
- Initialize Terraform projects
- Validate Terraform configs
- Setup backend configuration
- Check provider versions

### 5. **Database Connectivity**
- Test PostgreSQL connections
- Validate BigQuery access
- Check database credentials
- Create test databases

### 6. **Tool Validation**
- Check Python version
- Validate Java installation (for Spark)
- Check Git configuration
- Verify IDE setup

## 📋 Pre-flight Checks

Run comprehensive environment validation:

```bash
✓ Python 3.9+ installed
✓ pip available
✓ Docker running
✓ Docker Compose installed
✓ GCP CLI configured
✓ Terraform installed
✓ Git configured
⚠ Spark not found (optional)
```

## 💡 Usage Examples

### Example 1: Setup for Module 1 (Docker & Terraform)
```bash
# Check prerequisites
python env_setup.py --check-module 1

# Setup Docker
python env_setup.py --setup-docker

# Initialize Terraform
python env_setup.py --init-terraform
```

### Example 2: Setup Python Environment
```bash
# Create virtual environment
python env_setup.py --create-venv my_project

# Install requirements
python env_setup.py --install-requirements requirements.txt

# Validate installation
python env_setup.py --validate-packages
```

### Example 3: GCP Configuration
```bash
# Setup GCP credentials
python env_setup.py --setup-gcp --project-id my-project

# Test BigQuery access
python env_setup.py --test-bigquery

# Validate permissions
python env_setup.py --check-gcp-permissions
```

## 🔧 Module-Specific Setup

### Module 1: Containerization & IaC
- Install Docker Desktop
- Setup Terraform
- Configure GCP CLI
- Test PostgreSQL container

### Module 2: Workflow Orchestration
- Setup Kestra
- Configure Python environment
- Validate API access

### Module 3: Data Warehouse
- Configure BigQuery access
- Setup dbt environment
- Test query execution

### Module 4: Analytics Engineering
- Install dbt-core and dbt-bigquery
- Setup Streamlit
- Configure Looker Studio access

### Module 5: Batch Processing
- Install PySpark
- Setup Java JDK
- Configure Spark settings

### Module 6: Streaming
- Setup Kafka environment
- Install Kafka tools
- Configure Avro schemas

## 🎯 Features

### Automated Detection
- Detect OS (Windows/Mac/Linux)
- Find installed tools
- Check versions
- Identify missing dependencies

### Guided Setup
- Step-by-step instructions
- Error messages with solutions
- Links to documentation
- Troubleshooting tips

### Validation Reports
- Generate setup status reports
- Export to Markdown
- Track setup progress
- Identify blockers

### Rollback Support
- Undo environment changes
- Reset to clean state
- Backup configurations

## 🚀 Quick Start

```python
from environment_setup_helper import EnvironmentSetup

# Initialize
setup = EnvironmentSetup()

# Run full validation
report = setup.validate_all()
print(report)

# Setup specific module
setup.setup_for_module(1)  # Docker & Terraform

# Fix issues
setup.fix_issues(auto=True)
```

## 📊 Health Check Dashboard

Visual status of your environment:

```
Environment Health Check
━━━━━━━━━━━━━━━━━━━━━━━━
✓ Python: 3.11.0 
✓ Docker: 24.0.6
✓ Terraform: 1.6.0
✓ GCP CLI: 450.0.0
⚠ Java: Not found (needed for Spark)
✗ Kafka: Not installed

Overall Status: 80% Ready
```

## 🎓 Use Cases for Data Engineering Zoomcamp

- **Week 0:** Initial environment setup
- **Module Start:** Validate module prerequisites
- **Troubleshooting:** Diagnose environment issues
- **Fresh Install:** Setup on new machine
- **Collaboration:** Ensure team has identical setup

## 📖 Common Issues & Solutions

### Docker Not Running
```
Issue: Cannot connect to Docker daemon
Solution: Start Docker Desktop
Command: setup.start_docker()
```

### GCP Auth Failed
```
Issue: Application Default Credentials not found
Solution: Run gcloud auth application-default login
Command: setup.configure_gcp_auth()
```

### Missing Python Packages
```
Issue: ModuleNotFoundError
Solution: Install from requirements.txt
Command: setup.install_requirements()
```

## 🔒 Security Features

- Never store credentials in code
- Use environment variables
- Support for secret managers
- Audit logging of setup actions

## 📦 What's Included

- `scripts/env_setup.py` - Main setup automation
- `scripts/validators.py` - Validation functions
- `scripts/installers.py` - Installation helpers
- `examples/` - Setup configuration examples
