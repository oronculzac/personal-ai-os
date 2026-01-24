#!/usr/bin/env python3
"""
Notebook Manager
Create and manage Jupyter notebooks with templates
"""

import json
import nbformat as nbf
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class NotebookManager:
    """Manage Jupyter notebooks with templates"""
    
    def __init__(self, templates_dir='templates'):
        self.templates_dir = Path(__file__).parent.parent / templates_dir
        self.nb_version = 4  # Jupyter notebook format version
    
    def create_cell(self, cell_type: str, source: str, metadata: Dict = None) -> nbf.NotebookNode:
        """Create a notebook cell"""
        if cell_type == 'markdown':
            cell = nbf.v4.new_markdown_cell(source)
        elif cell_type == 'code':
            cell = nbf.v4.new_code_cell(source)
        else:
            raise ValueError(f"Invalid cell type: {cell_type}")
        
        if metadata:
            cell.metadata.update(metadata)
        
        return cell
    
    def create_data_exploration_notebook(self, title: str, dataset_name: str = "dataset") -> nbf.NotebookNode:
        """Create a data exploration notebook"""
        
        cells = []
        
        # Title
        cells.append(self.create_cell('markdown', f"# Data Exploration: {title}\\n\\n**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n## Objective\\n\\nExplore and analyze {dataset_name} to understand its structure, quality, and characteristics."))
        
        # Imports
        cells.append(self.create_cell('markdown', "## 1. Setup & Imports"))
        cells.append(self.create_cell('code', """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

# Configure display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
warnings.filterwarnings('ignore')

# Set plot style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("✓ Imports complete")"""))
        
        # Load Data
        cells.append(self.create_cell('markdown', "## 2. Load Data"))
        cells.append(self.create_cell('code', f"""# Load dataset
# TODO: Update path to your data file
file_path = 'data/{dataset_name}.csv'

try:
    df = pd.read_csv(file_path)
    print(f"✓ Loaded {{len(df):,}} rows and {{len(df.columns)}} columns")
except FileNotFoundError:
    print(f"✗ File not found: {{file_path}}")
    df = None"""))
        
        # Overview
        cells.append(self.create_cell('markdown', "## 3. Dataset Overview"))
        cells.append(self.create_cell('code', """# Display first few rows
df.head()"""))
        
        cells.append(self.create_cell('code', """# Dataset info
print("Dataset Information:")
print("-" * 50)
print(f"Shape: {df.shape}")
print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print("\\nColumn Types:")
print(df.dtypes.value_counts())"""))
        
        # Missing Values
        cells.append(self.create_cell('markdown', "## 4. Data Quality Checks"))
        cells.append(self.create_cell('code', """# Check for missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100

missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_pct
}).sort_values('Percentage', ascending=False)

print("Missing Values:")
print(missing_df[missing_df['Missing Count'] > 0])"""))
        
        cells.append(self.create_cell('code', """# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates:,} ({(duplicates/len(df)*100):.2f}%)")"""))
        
        # Statistics
        cells.append(self.create_cell('markdown', "## 5. Statistical Summary"))
        cells.append(self.create_cell('code', """# Numerical columns summary
df.describe()"""))
        
        cells.append(self.create_cell('code', """# Categorical columns summary
categorical_cols = df.select_dtypes(include=['object']).columns
if len(categorical_cols) > 0:
    print("Categorical Columns:")
    for col in categorical_cols:
        unique_count = df[col].nunique()
        print(f"\\n{col}:")
        print(f"  Unique values: {unique_count}")
        if unique_count < 20:
            print(f"  Value counts:\\n{df[col].value_counts().head(10)}")"""))
        
        # Visualizations
        cells.append(self.create_cell('markdown', "## 6. Visualizations"))
        cells.append(self.create_cell('code', """# Distribution of numerical columns
numerical_cols = df.select_dtypes(include=[np.number]).columns

if len(numerical_cols) > 0:
    n_cols = min(len(numerical_cols), 4)
    fig, axes = plt.subplots(
        nrows=(len(numerical_cols) + n_cols - 1) // n_cols,
        ncols=n_cols,
        figsize=(16, 4 * ((len(numerical_cols) + n_cols - 1) // n_cols))
    )
    axes = axes.flatten() if len(numerical_cols) > 1 else [axes]
    
    for idx, col in enumerate(numerical_cols):
        df[col].hist(bins=30, ax=axes[idx], edgecolor='black')
        axes[idx].set_title(f'Distribution of {col}')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Frequency')
    
    # Hide empty subplots
    for idx in range(len(numerical_cols), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()"""))
        
        cells.append(self.create_cell('code', """# Correlation heatmap
if len(numerical_cols) > 1:
    plt.figure(figsize=(12, 8))
    correlation = df[numerical_cols].corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.show()"""))
        
        # Insights
        cells.append(self.create_cell('markdown', "## 7. Key Insights\\n\\n### Observations\\n- TODO: Add your observations\\n\\n### Data Quality Issues\\n- TODO: Note any data quality problems\\n\\n### Next Steps\\n- TODO: List next steps for analysis"))
        
        # Create notebook
        nb = nbf.v4.new_notebook(cells=cells)
        
        # Add metadata
        nb.metadata = {
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            },
            'language_info': {
                'name': 'python',
                'version': '3.9.0'
            }
        }
        
        return nb
    
    def create_spark_notebook(self, title: str, app_name: str = "spark_app") -> nbf.NotebookNode:
        """Create a Spark development notebook"""
        
        cells = []
        
        # Title
        cells.append(self.create_cell('markdown', f"# Spark Job Development: {title}\\n\\n**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}"))
        
        # Setup
        cells.append(self.create_cell('markdown', "## 1. Spark Session Setup"))
        cells.append(self.create_cell('code', f"""from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Spark session
spark = SparkSession.builder \\
    .appName("{app_name}") \\
    .config("spark.sql.adaptive.enabled", "true") \\
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \\
    .config("spark.sql.shuffle.partitions", "200") \\
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print(f"✓ Spark {{spark.version}} session created")
print(f"✓ Application: {app_name}")"""))
        
        # Load Data
        cells.append(self.create_cell('markdown', "## 2. Load Data"))
        cells.append(self.create_cell('code', """# Load source data
source_path = "path/to/data"  # TODO: Update path

df = spark.read \\
    .format("parquet") \\
    .load(source_path)

print(f"✓ Loaded {df.count():,} records")
df.printSchema()"""))
        
        # Explore
        cells.append(self.create_cell('markdown', "## 3. Data Exploration"))
        cells.append(self.create_cell('code', """# Show sample data
df.show(10, truncate=False)"""))
        
        # Transform
        cells.append(self.create_cell('markdown', "## 4. Transformations"))
        cells.append(self.create_cell('code', """# Apply transformations
df_transformed = df \\
    .withColumn("processing_date", F.current_date()) \\
    .withColumn("processing_timestamp", F.current_timestamp())

# TODO: Add your transformation logic here

df_transformed.show(5)"""))
        
        # Data Quality
        cells.append(self.create_cell('markdown', "## 5. Data Quality Checks"))
        cells.append(self.create_cell('code', """# Check null counts
null_counts = df_transformed.select(
    [F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df_transformed.columns]
)

print("Null counts:")
null_counts.show()"""))
        
        # Save
        cells.append(self.create_cell('markdown', "## 6. Save Results"))
        cells.append(self.create_cell('code', """# Write to target
target_path = "path/to/output"  # TODO: Update path

# df_transformed.write \\
#     .mode("overwrite") \\
#     .format("parquet") \\
#     .partitionBy("processing_date") \\
#     .save(target_path)

print(f"✓ Data would be written to {target_path}")"""))
        
        cells.append(self.create_cell('markdown', "## 7. Cleanup"))
        cells.append(self.create_cell('code', """# Stop Spark session
# spark.stop()
print("Spark session still running for development")"""))
        
        # Create notebook
        nb = nbf.v4.new_notebook(cells=cells)
        nb.metadata = {
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            }
        }
        
        return nb
    
    def save_notebook(self, notebook: nbf.NotebookNode, filename: str, output_dir: str = "."):
        """Save notebook to file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            nbf.write(notebook, f)
        
        print(f"✓ Notebook saved: {filepath}")
        return filepath


# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Notebook Manager")
    parser.add_argument("--template", choices=['exploration', 'spark'], 
                       required=True, help="Notebook template")
    parser.add_argument("--title", required=True, help="Notebook title")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--filename", help="Output filename (auto-generated if not provided)")
    
    args = parser.parse_args()
    
    nm = NotebookManager()
    
    # Generate filename if not provided
    if not args.filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        safe_title = args.title.lower().replace(' ', '_')
        args.filename = f"{timestamp}_{safe_title}.ipynb"
    
    # Create notebook
    if args.template == 'exploration':
        nb = nm.create_data_exploration_notebook(args.title)
    elif args.template == 'spark':
        nb = nm.create_spark_notebook(args.title)
    
    # Save
    nm.save_notebook(nb, args.filename, args.output)
