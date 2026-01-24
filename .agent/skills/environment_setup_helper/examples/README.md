# Environment Setup Helper - Examples

This directory contains example configurations and scripts for environment setup.

## Available Examples

### 1. Module-Specific Setup Scripts
- `setup_module_1.sh` - Docker & Terraform setup
- `setup_module_5.sh` - Spark & Java setup

### 2. Requirements Files
- `requirements_module_3.txt` - BigQuery & dbt packages
- `requirements_module_4.txt` - Analytics engineering stack

### 3. Configuration Templates
- `.env.example` - Environment variables template
- `gcp_config.example.yml` - GCP configuration

## Usage

Run environment validation:

```bash
python ../scripts/env_setup.py --validate
```

Setup for specific module:

```bash
python ../scripts/env_setup.py --module 1
```

Create virtual environment:

```bash
python ../scripts/env_setup.py --create-venv .venv
```

## Module Requirements

| Module | Required Tools |
|--------|---------------|
| 1 | Docker, Terraform, GCloud CLI |
| 2 | Python, Docker |
| 3 | Python, GCloud CLI, dbt |
| 4 | Python, dbt, Streamlit |
| 5 | Python, Java, Spark |
| 6 | Python, Docker, Kafka |
