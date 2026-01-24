# Quick Reference: Data Engineering Skills & Personas

## 🎭 Activate Personas

```powershell
# Data engineering work (most modules)
python .agent\core\persona_manager.py --activate data_engineer

# Infrastructure/Docker/Terraform work
python .agent\core\persona_manager.py --activate devops_engineer

# Check current persona
python .agent\core\persona_manager.py --status

# Return to default
python .agent\core\persona_manager.py --deactivate
```

## 🛠️ Use Skills via CLI

### Environment Setup Helper
```powershell
# Validate full environment
python .agent\skills\environment_setup_helper\scripts\env_setup.py --validate

# Check module requirements
python .agent\skills\environment_setup_helper\scripts\env_setup.py --module 1

# Create venv
python .agent\skills\environment_setup_helper\scripts\env_setup.py --create-venv .venv
```

### Code Template Generator
```powershell
# Generate Spark job
python .agent\skills\code_template_generator\scripts\template_generator.py --type spark

# Generate dbt model
python .agent\skills\code_template_generator\scripts\template_generator.py --type dbt

# Generate Terraform
python .agent\skills\code_template_generator\scripts\template_generator.py --type terraform

# Generate Docker Compose
python .agent\skills\code_template_generator\scripts\template_generator.py --type docker
```

### Notebook Manager
```powershell
# Create data exploration notebook
python .agent\skills\notebook_manager\scripts\notebook_manager.py \
    --template exploration \
    --title "My Analysis" \
    --output ./notebooks

# Create Spark notebook
python .agent\skills\notebook_manager\scripts\notebook_manager.py \
    --template spark \
    --title "Spark Job" \
    --output ./notebooks
```

## 📋 Module-Specific Workflows

### Module 1: Docker & Terraform
```powershell
# 1. Activate persona
python .agent\core\persona_manager.py --activate devops_engineer

# 2. Check environment
python .agent\skills\environment_setup_helper\scripts\env_setup.py --module 1

# 3. Generate Docker Compose (via conversation)
# "Create Docker Compose for PostgreSQL and pgAdmin"

# 4. Generate Terraform (via conversation)
# "Generate Terraform for GCP BigQuery dataset"
```

### Module 3: Data Warehouse
```powershell
# 1. Activate persona
python .agent\core\persona_manager.py --activate data_engineer

# 2. Create exploration notebook
python .agent\skills\notebook_manager\scripts\notebook_manager.py \
    --template exploration \
    --title "BigQuery Exploration" \
    --output ./notebooks/module3
```

### Module 5: Batch Processing
```powershell
# 1. Check Spark environment
python .agent\skills\environment_setup_helper\scripts\env_setup.py --module 5

# 2. Create Spark notebook
python .agent\skills\notebook_manager\scripts\notebook_manager.py \
    --template spark \
    --title "Batch Processing" \
    --output ./notebooks/module5

# 3. Generate Spark job (via conversation)
# "Generate Spark ETL script for processing events"
```

## 🔍 System Status

```powershell
# List all personas
python .agent\core\persona_manager.py --list

# Discover skills
python .agent\core\skill_discovery.py

# Check folder permissions
python .agent\core\folder_permissions.py
```

## 💡 Common Tasks

### Setup new module workspace
```powershell
# Create folder structure
mkdir -p modules\module-X\{homework,notes,code}

# Activate Data Engineer persona
python .agent\core\persona_manager.py --activate data_engineer

# Validate environment
python .agent\skills\environment_setup_helper\scripts\env_setup.py --module X
```

### Start homework assignment
```powershell
# Create notebook
python .agent\skills\notebook_manager\scripts\notebook_manager.py \
    --template exploration \
    --title "Module X Homework" \
    --output ./homework/module-X
```

### Generate pipeline code
Via conversation after activating Data Engineer persona:
- "Generate Spark job for processing data from GCS to BigQuery"
- "Create dbt model for user aggregations"
- "Generate Kafka consumer for streaming events"
