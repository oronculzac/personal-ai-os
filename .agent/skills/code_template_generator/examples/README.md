# Code Template Generator - Examples

This directory contains example outputs from the Code Template Generator skill.

## Available Examples

### 1. Spark ETL Script
See `spark_etl_example.py` for a complete PySpark ETL job template.

### 2. dbt Model
See `dbt_model_example/` for dbt model with schema and tests.

### 3. Terraform Configuration
See `terraform_bigquery_example.tf` for BigQuery dataset setup.

### 4. Docker Compose
See `docker-compose-example.yml` for data engineering stack.

## Usage

Generate your own templates using:

```bash
python ../scripts/template_generator.py --type spark --output my_script.py
python ../scripts/template_generator.py --type dbt
python ../scripts/template_generator.py --type terraform
python ../scripts/template_generator.py --type docker
```

## Customization

All templates are fully customizable. Edit the generated code to match your specific needs.
