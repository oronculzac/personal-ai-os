---
name: Notebook Manager
description: Create, organize, and manage Jupyter notebooks with templates for data engineering tasks
version: 1.1.0
triggers:
  - create notebook
  - generate jupyter notebook
  - make notebook for
  - setup notebook
  - organize notebooks
examples:
  - "Create a Spark development notebook"
  - "Generate a data exploration notebook"
  - "Setup notebook for BigQuery queries"
  - "Organize my notebooks by module"
context_hints:
  - user mentions Jupyter or notebooks
  - user wants to explore or analyze data
  - user needs structured notebook templates
  - user is doing data engineering development
priority: 6
conflicts_with: []
capabilities:
  - notebook_creation
  - template_application
  - notebook_organization
  - cell_templates
  - markdown_generation
dependencies:
  - jupyter>=1.0.0
  - nbformat>=5.0.0
auto_load: true
---

# Notebook Manager Skill

Create and manage Jupyter notebooks with templates for data engineering workflows.

## 🎯 Purpose

Accelerate notebook-based development with pre-configured templates, common cell patterns, and organizational tools for data engineering tasks.

## 🚀 Capabilities

### 1. **Template-Based Notebook Creation**
Create notebooks from templates:
- Data exploration notebooks
- ETL development notebooks
- Spark job notebooks
- SQL query notebooks
- Data quality notebooks
- ML experiment notebooks

### 2. **Common Cell Patterns**
Pre-configured cells for:
- Import statements (pandas, pyspark, etc.)
- Connection setup (databases, cloud storage)
- Configuration loading
- Logging setup
- Helper functions
- Visualization setup

### 3. **Module-Specific Templates**

**Module 1: Docker & Terraform**
- Docker testing notebook
- Terraform validation notebook

**Module 2: Workflow Orchestration**
- Pipeline development notebook
- Kestra testing notebook

**Module 3: Data Warehouse**
- BigQuery exploration notebook
- Query optimization notebook

**Module 4: Analytics Engineering**
- dbt development notebook
- Data visualization notebook

**Module 5: Batch Processing**
- Spark development notebook
- Data processing notebook

**Module 6: Streaming**
- Kafka testing notebook
- Stream processing notebook

### 4. **Organization Tools**
- Auto-naming with timestamps
- Folder structuring
- Notebook indexing
- Tag management

### 5. **Code Extraction**
- Extract code cells to .py files
- Generate scripts from notebooks
- Create modules from functions

## 📋 Notebook Templates

### 1. **Data Exploration Template**
```
# Data Exploration: [Dataset Name]

## Setup
- Imports
- Configuration
- Data loading

## Overview
- Dataset shape
- Column types
- Missing values
- Basic statistics

## Analysis
- Distributions
- Correlations
- Outliers

## Insights
- Key findings
- Next steps
```

### 2. **ETL Development Template**
```
# ETL Development: [Pipeline Name]

## Configuration
- Source connection
- Target connection
- Parameters

## Extract
- Load source data
- Validate schema

## Transform
- Data cleaning
- Business logic
- Aggregations

## Load
- Write to target
- Data quality checks

## Testing
- Unit tests
- Integration tests
```

### 3. **Spark Job Template**
```
# Spark Job: [Job Name]

## Setup
- SparkSession creation
- Configuration
- UDF definitions

## Data Loading
- Read sources
- Schema validation

## Transformations
- Data processing
- Aggregations
- Joins

## Output
- Write results
- Partitioning
- Performance metrics
```

## 💡 Usage Examples

### Example 1: Create Data Exploration Notebook
```python
from notebook_manager import NotebookManager

nm = NotebookManager()

# Create from template
nb = nm.create_notebook(
    template='data_exploration',
    title='NYC Taxi Data Analysis',
    output_dir='notebooks/module3'
)
```

### Example 2: Create Spark Development Notebook
```python
nb = nm.create_notebook(
    template='spark_job',
    title='User Event Processing',
    params={
        'source_path': 'gs://bucket/events',
        'target_path': 'gs://bucket/processed'
    }
)
```

### Example 3: Organize Existing Notebooks
```python
# Auto-organize by date and topic
nm.organize_notebooks(
    source_dir='notebooks',
    strategy='by_date_and_topic'
)
```

## 🎨 Features

### Smart Defaults
- Auto-import common libraries
- Pre-configured plotting style
- Standard helper functions
- Logging setup

### Markdown Templates
- Section headers
- TODO lists
- Documentation blocks
- Code explanations

### Code Cells
- Import blocks
- Configuration cells
- Helper function cells
- Testing cells

## 📊 Notebook Structure

Standard notebook organization:
```
1. Title & Overview
2. Imports & Setup
3. Configuration
4. Helper Functions
5. Main Logic (numbered sections)
6. Visualization
7. Summary & Next Steps
```

## 🔧 Cell Templates

### Import Cell
```python
# Standard data engineering imports
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Spark Setup Cell
```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Create Spark session
spark = SparkSession.builder \\
    .appName("notebook_session") \\
    .config("spark.sql.adaptive.enabled", "true") \\
    .getOrCreate()

print(f"Spark version: {spark.version}")
```

### BigQuery Connection Cell
```python
from google.cloud import bigquery

# Initialize BigQuery client
project_id = 'your-project-id'
client = bigquery.Client(project=project_id)

print(f"Connected to project: {project_id}")
```

## 🎯 Use Cases for Data Engineering Zoomcamp

### Module  1: Docker & Terraform
- Test Docker containers
- Validate Terraform outputs
- Debug infrastructure issues

### Module 3: Data Warehouse
- Explore BigQuery datasets
- Develop and test SQL queries
- Analyze query performance

### Module 4: Analytics Engineering
- Develop dbt transformations
- Create visualizations
- Test analytics logic

### Module 5: Batch Processing
- Develop Spark jobs
- Test transformations
- Optimize performance

### Module 6: Streaming
- Test Kafka connections
- Develop stream processors
- Debug data flows

## 📦 Included Templates

- `data_exploration.ipynb` - General data exploration
- `spark_development.ipynb` - Spark job development
- `sql_queries.ipynb` - SQL query development
- `etl_pipeline.ipynb` - ETL pipeline development
- `data_quality.ipynb` - Data quality checks
- `streaming_dev.ipynb` - Stream processing development

## 🚀 Quick Start

```python
from notebook_manager import NotebookManager

# Create manager
nm = NotebookManager()

# Create notebook for Module 3
nb = nm.create_from_module(
    module_number=3,
    task='bigquery_exploration'
)

# Open in Jupyter
nm.open_notebook(nb)
```

## 📖 Best Practices

### Notebook Organization
- One topic per notebook
- Clear naming convention
- Date prefixes for chronological order
- Organize in module folders

### Code Quality
- Use cells for logical sections
- Add markdown documentation
- Include data validation
- Clear variable names

### Version Control
- Commit notebooks regularly
- Clear output before committing
- Use .gitignore for large outputs
- Add meaningful commit messages

## 🔒 Security

- Never commit credentials in notebooks
- Use environment variables
- Clear sensitive outputs
- Use .gitignore for data files
