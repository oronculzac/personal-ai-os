---
name: Code Template Generator
description: Generate production-ready code templates for data engineering tasks including Spark, SQL, dbt, Terraform, Docker, and ETL scripts
version: 1.1.0
triggers:
  - generate code for
  - create script for
  - generate spark job
  - create dbt model
  - generate terraform config
  - create docker compose
  - generate sql query
  - create etl script
  - generate kafka code
examples:
  - "Generate a Spark ETL job for BigQuery"
  - "Create a dbt model for customer dimensions"
  - "Generate Terraform for GCS bucket"
  - "Create Docker Compose for local Spark cluster"
context_hints:
  - user needs boilerplate code for data engineering
  - user mentions Spark, SQL, dbt, Terraform, Docker
  - user asks for code generation or templates
  - user is doing DE Zoomcamp work
priority: 7
conflicts_with: []
capabilities:
  - spark_templates
  - sql_generation
  - dbt_models
  - terraform_configs
  - docker_configs
  - etl_scripts
  - kafka_code
  - python_pipelines
dependencies:
  - pyyaml>=6.0.0
auto_load: true
---

# Code Template Generator Skill

Generate production-ready code templates for data engineering tasks.

## 🎯 Purpose

Accelerate data engineering development by generating boilerplate code with best practices, error handling, logging, and documentation built-in.

## 🚀 Capabilities

### 1. **Spark Templates**
Generate PySpark scripts for:
- Data ingestion from various sources
- ETL transformations
- Batch processing jobs
- Data quality checks
- Delta Lake operations

**Example:**
```python
# Request: "Generate Spark job to read from CSV and write to Parquet"
# Output: Complete PySpark script with error handling, logging, config
```

### 2. **SQL Query Templates**
Generate SQL for:
- BigQuery queries
- PostgreSQL queries
- dbt models
- Window functions, CTEs
- Data quality checks

**Example:**
```sql
-- Request: "Generate BigQuery query with window functions"
-- Output: Optimized SQL with partitioning, clustering hints
```

### 3. **dbt Models**
Generate dbt files:
- Model SQL files
- Schema YAML files
- Tests
- Documentation

**Example:**
```yaml
# Request: "Create dbt model for customer dimensions"
# Output: Complete dbt model with tests and docs
```

### 4. **Terraform Configurations**
Generate Terraform code for:
- GCP resources (BigQuery, GCS, Compute)
- AWS resources (S3, Redshift, EC2)
- Networking, IAM
- Modules and variables

**Example:**
```hcl
# Request: "Generate Terraform for BigQuery dataset"
# Output: Complete .tf file with variables, outputs, best practices
```

### 5. **Docker Files**
Generate Docker configurations:
- Dockerfiles for Python/Spark apps
- Docker Compose for local development
- Multi-stage builds
- Health checks

**Example:**
```yaml
# Request: "Create Docker Compose for Spark and PostgreSQL"
# Output: Complete docker-compose.yml with volumes, networks
```

### 6. **ETL Scripts**
Generate Python ETL scripts:
- Data extraction from APIs
- Data transformation logic
- Data loading to warehouses
- Incremental processing
- Error handling and logging

### 7. **Kafka Code**
Generate Kafka configurations:
- Producer/Consumer code
- Topic configurations
- Avro schema definitions
- Stream processing with Kafka Streams

## 📋 Templates Included

### Data Engineering
- `spark_etl.py` - PySpark ETL template
- `incremental_load.py` - Incremental data loading pattern
- `data_quality.py` - Data quality checks
- `api_extractor.py` - API data extraction

### SQL & Analytics
- `bigquery_template.sql` - BigQuery query patterns
- `dbt_model.sql` - dbt model template
- `window_functions.sql` - Window function examples
- `cte_template.sql` - CTE patterns

### Infrastructure
- `main.tf` - Terraform main configuration
- `variables.tf` - Variable definitions
- `outputs.tf` - Output definitions
- `Dockerfile` - Multi-stage Python Dockerfile
- `docker-compose.yml` - Local development setup

### Orchestration
- `kestra_flow.yml` - Kestra workflow template
- `airflow_dag.py` - Airflow DAG template

## 🎨 Features

### Built-in Best Practices
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Configuration management
- ✅ Environment variable usage
- ✅ Type hints (Python)
- ✅ Documentation strings
- ✅ Data validation
- ✅ Performance optimization hints

### Customization
- Parameterized templates
- Context-aware generation
- Industry best practices
- Comments explaining key concepts

## 💡 Usage Examples

### Example 1: Spark ETL Job
**Request:** "Generate Spark job to read from GCS and write to BigQuery with partitioning"

**Output:**
- Complete PySpark script
- Configuration file
- README with setup instructions
- Sample data for testing

### Example 2: dbt Model
**Request:** "Create dbt model for sales aggregation with tests"

**Output:**
- SQL model file
- schema.yml with tests
- Documentation
- Sample test data

### Example 3: Terraform Infrastructure
**Request:** "Generate Terraform for data pipeline infrastructure on GCP"

**Output:**
- main.tf with all resources
- variables.tf
- outputs.tf
- README with deployment steps

## 🔧 How It Works

1. **Analyze Request:** Understand what code you need
2. **Select Template:** Choose appropriate template(s)
3. **Customize:** Fill in parameters, add context
4. **Generate:** Create code with best practices
5. **Document:** Add comments and setup instructions

## 📚 Learning Mode

Templates include:
- Inline comments explaining concepts
- Links to documentation
- Common pitfalls to avoid
- Performance optimization tips
- Security considerations

Perfect for learning while building!

## 🎯 Use Cases for Data Engineering Zoomcamp

### Module 1: Docker & Terraform
- Generate Dockerfiles for data apps
- Create Docker Compose for local dev
- Generate Terraform configs for GCP

### Module 2: Workflow Orchestration
- Generate Kestra workflow YAML
- Create pipeline scripts

### Module 3: Data Warehouse
- Generate BigQuery SQL queries
- Create partitioned table definitions

### Module 4: Analytics Engineering
- Generate dbt models
- Create tests and documentation

### Module 5: Batch Processing
- Generate PySpark scripts
- Create batch job templates

### Module 6: Streaming
- Generate Kafka producer/consumer
- Create schema definitions

## 🚀 Quick Start

```python
# Using the skill
"Generate Spark ETL script to read Parquet from S3 and write to BigQuery"

# Output includes:
# - spark_etl.py
# - config.yaml
# - requirements.txt
# - README.md
```

## 📖 Additional Resources

- Template library in `templates/`
- Example outputs in `examples/`
- Scripts for code generation in `scripts/`
