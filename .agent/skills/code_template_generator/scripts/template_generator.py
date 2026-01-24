#!/usr/bin/env python3
"""
Code Template Generator
Generate production-ready code templates for data engineering tasks
"""

import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class CodeTemplateGenerator:
    """Generate code templates for data engineering tasks"""
    
    def __init__(self, templates_dir='templates'):
        self.templates_dir = Path(__file__).parent.parent / templates_dir
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load all available templates"""
        templates = {}
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob('*.template'):
                name = template_file.stem
                with open(template_file, 'r', encoding='utf-8') as f:
                    templates[name] = f.read()
        return templates
    
    def generate_spark_etl(self, 
                          source_type: str = 'csv',
                          target_type: str = 'parquet',
                          source_path: str = 'gs://bucket/data',
                          target_path: str = 'gs://bucket/output') -> str:
        """Generate PySpark ETL script"""
        
        template = f'''#!/usr/bin/env python3
"""
Spark ETL Job
Generated: {datetime.now().isoformat()}

Purpose: Extract data from {source_type}, transform, and load to {target_type}
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SparkETLJob:
    """Spark ETL Job for data processing"""
    
    def __init__(self, app_name="etl_job"):
        self.spark = SparkSession.builder \\
            .appName(app_name) \\
            .config("spark.sql.adaptive.enabled", "true") \\
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \\
            .getOrCreate()
        
        # Set log level
        self.spark.sparkContext.setLogLevel("WARN")
        logger.info(f"Spark session initialized: {{app_name}}")
    
    def extract(self, source_path: str) -> "DataFrame":
        """
        Extract data from source
        
        Args:
            source_path: Path to source data
            
        Returns:
            DataFrame with source data
        """
        logger.info(f"Reading data from {{source_path}}")
        
        try:
            df = self.spark.read \\
                .format("{source_type}") \\
                .option("header", "true") \\
                .option("inferSchema", "true") \\
                .load(source_path)
            
            record_count = df.count()
            logger.info(f"Successfully read {{record_count}} records")
            
            return df
            
        except Exception as e:
            logger.error(f"Error reading data: {{e}}")
            raise
    
    def transform(self, df: "DataFrame") -> "DataFrame":
        """
        Transform data
        
        Args:
            df: Input DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Starting data transformation")
        
        try:
            # Add processing timestamp
            df = df.withColumn("processed_at", F.current_timestamp())
            
            # TODO: Add your transformation logic here
            # Example transformations:
            # - Data type conversions
            # - Column renaming
            # - Filtering
            # - Aggregations
            # - Joins
            
            # Data quality checks
            null_counts = df.select(
                [F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df.columns]
            ).collect()[0].asDict()
            
            logger.info(f"Null counts: {{null_counts}}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error in transformation: {{e}}")
            raise
    
    def load(self, df: "DataFrame", target_path: str, partition_cols: List[str] = None):
        """
        Load data to target
        
        Args:
            df: DataFrame to write
            target_path: Target path
            partition_cols: Columns to partition by
        """
        logger.info(f"Writing data to {{target_path}}")
        
        try:
            writer = df.write \\
                .mode("overwrite") \\
                .format("{target_type}")
            
            if partition_cols:
                writer = writer.partitionBy(*partition_cols)
                logger.info(f"Partitioning by: {{partition_cols}}")
            
            writer.save(target_path)
            
            output_count = df.count()
            logger.info(f"Successfully wrote {{output_count}} records")
            
        except Exception as e:
            logger.error(f"Error writing data: {{e}}")
            raise
    
    def run(self, source_path: str = "{source_path}", 
            target_path: str = "{target_path}",
            partition_cols: List[str] = None):
        """
        Run the full ETL pipeline
        
        Args:
            source_path: Source data path
            target_path: Target data path
            partition_cols: Columns to partition by
        """
        logger.info("Starting ETL job")
        start_time = datetime.now()
        
        try:
            # Extract
            df = self.extract(source_path)
            
            # Transform
            df_transformed = self.transform(df)
            
            # Load
            self.load(df_transformed, target_path, partition_cols)
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"ETL job completed successfully in {{duration:.2f}} seconds")
            
        except Exception as e:
            logger.error(f"ETL job failed: {{e}}")
            raise
        finally:
            self.spark.stop()
            logger.info("Spark session stopped")


if __name__ == "__main__":
    # Run the ETL job
    job = SparkETLJob(app_name="data_pipeline")
    
    # Configure your paths
    SOURCE_PATH = "{source_path}"
    TARGET_PATH = "{target_path}"
    PARTITION_COLS = ["year", "month"]  # Adjust as needed
    
    # Execute
    job.run(
        source_path=SOURCE_PATH,
        target_path=TARGET_PATH,
        partition_cols=PARTITION_COLS
    )
'''
        return template
    
    def generate_dbt_model(self, model_name: str, source_table: str) -> Dict[str, str]:
        """Generate dbt model with schema and tests"""
        
        model_sql = f'''{{{{
  config(
    materialized='table',
    partition_by={{
      'field': 'created_date',
      'data_type': 'date',
      'granularity': 'day'
    }},
    cluster_by=['user_id']
  )
}}}}

-- {model_name} model
-- Generated: {datetime.now().isoformat()}

WITH source_data AS (
  SELECT *
  FROM {{{{ source('raw', '{source_table}') }}}}
  WHERE _loaded_at >= CURRENT_DATE() - 7
),

transformed AS (
  SELECT
    id,
    user_id,
    DATE(created_at) AS created_date,
    -- Add your transformations here
    created_at,
    updated_at
  FROM source_data
)

SELECT * FROM transformed
'''
        
        schema_yml = f'''version: 2

models:
  - name: {model_name}
    description: "TODO: Add model description"
    columns:
      - name: id
        description: "Primary key"
        tests:
          - unique
          - not_null
      
      - name: user_id
        description: "User identifier"
        tests:
          - not_null
          - relationships:
              to: ref('users')
              field: id
      
      - name: created_date
        description: "Date when record was created"
        tests:
          - not_null
      
      - name: created_at
        description: "Timestamp when record was created"
      
      - name: updated_at
        description: "Timestamp when record was last updated"
'''
        
        return {
            'model.sql': model_sql,
            'schema.yml': schema_yml
        }
    
    def generate_terraform_bigquery(self, dataset_name: str, project_id: str) -> str:
        """Generate Terraform configuration for BigQuery dataset"""
        
        template = f'''# BigQuery Dataset Configuration
# Generated: {datetime.now().isoformat()}

terraform {{
  required_version = ">= 1.0"
  
  required_providers {{
    google = {{
      source  = "hashicorp/google"
      version = "~> 5.0"
    }}
  }}
}}

# Variables
variable "project_id" {{
  description = "GCP Project ID"
  type        = string
  default     = "{project_id}"
}}

variable "region" {{
  description = "GCP region"
  type        = string
  default     = "us-central1"
}}

variable "dataset_name" {{
  description = "BigQuery dataset name"
  type        = string
  default     = "{dataset_name}"
}}

# BigQuery Dataset
resource "google_bigquery_dataset" "main" {{
  dataset_id    = var.dataset_name
  friendly_name = var.dataset_name
  description   = "Data warehouse dataset for {dataset_name}"
  location      = var.region
  project       = var.project_id

  # Data retention
  default_table_expiration_ms = 0  # Never expire (adjust as needed)

  # Access control
  access {{
    role          = "OWNER"
    user_by_email = "terraform@${{var.project_id}}.iam.gserviceaccount.com"
  }}

  access {{
    role          = "READER"
    special_group = "projectReaders"
  }}

  # Labels for organization
  labels = {{
    environment = "dev"
    managed_by  = "terraform"
    dataset     = var.dataset_name
  }}
}}

# Example Table
resource "google_bigquery_table" "example" {{
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "example_table"
  project    = var.project_id

  # Partitioning
  time_partitioning {{
    type  = "DAY"
    field = "created_date"
  }}

  # Clustering
  clustering = ["user_id", "status"]

  # Schema
  schema = jsonencode([
    {{
      name        = "id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Record ID"
    }},
    {{
      name        = "user_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "User identifier"
    }},
    {{
      name        = "created_date"
      type        = "DATE"
      mode        = "REQUIRED"
      description = "Creation date"
    }},
    {{
      name        = "status"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Record status"
    }}
  ])

  # Deletion protection
  deletion_protection = true
}}

# Outputs
output "dataset_id" {{
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.main.dataset_id
}}

output "dataset_location" {{
  description = "BigQuery dataset location"
  value       = google_bigquery_dataset.main.location
}}
'''
        return template
    
    def generate_docker_compose(self, services: List[str] = ['postgres', 'spark']) -> str:
        """Generate Docker Compose configuration"""
        
        template = f'''# Docker Compose for Data Engineering
# Generated: {datetime.now().isoformat()}

version: '3.8'

services:
'''
        
        if 'postgres' in services:
            template += '''
  postgres:
    image: postgres:15-alpine
    container_name: de_postgres
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
      POSTGRES_DB: dataeng
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - de_network
'''
        
        if 'spark' in services:
            template += '''
  spark-master:
    image: bitnami/spark:3.5
    container_name: spark_master
    environment:
      - SPARK_MODE=master
      - SPARK_MASTER_PORT=7077
      - SPARK_MASTER_WEBUI_PORT=8080
    ports:
      - "8080:8080"
      - "7077:7077"
    volumes:
      - ./jobs:/opt/spark/jobs
      - ./data:/opt/spark/data
    networks:
      - de_network

  spark-worker:
    image: bitnami/spark:3.5
    container_name: spark_worker
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_CORES=2
      - SPARK_WORKER_MEMORY=2g
    depends_on:
      - spark-master
    volumes:
      - ./jobs:/opt/spark/jobs
      - ./data:/opt/spark/data
    networks:
      - de_network
'''
        
        template += '''
volumes:
  postgres_data:
    driver: local

networks:
  de_network:
    driver: bridge
'''
        
        return template


# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Code Template Generator")
    parser.add_argument("--type", choices=['spark', 'dbt', 'terraform', 'docker'], 
                       required=True, help="Template type")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    generator = CodeTemplateGenerator()
    
    if args.type == 'spark':
        code = generator.generate_spark_etl()
        print(code)
    elif args.type == 'dbt':
        code = generator.generate_dbt_model('my_model', 'source_table')
        print("Model SQL:")
        print(code['model.sql'])
        print("\nSchema YAML:")
        print(code['schema.yml'])
    elif args.type == 'terraform':
        code = generator.generate_terraform_bigquery('my_dataset', 'my-project')
        print(code)
    elif args.type == 'docker':
        code = generator.generate_docker_compose()
        print(code)
