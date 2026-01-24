---
module: 1
title: Docker & Terraform
status: in-progress
linear_project_id: "1a4900dd-b7c4-4030-b259-9bd446e30ed2"
linear_project_url: https://linear.app/linear-home-workspace/project/module-1-docker-terraform-a9858e512f38
start_date: 2026-01-17
tags:
  - de-zoomcamp
  - module-1
  - docker
  - terraform
---

# Module 1: Docker & Terraform

## 📚 Overview

Introduction to containerization with Docker and Infrastructure as Code with Terraform.

**Duration:** ~1 week  
**Status:** 🔄 In Progress

## 🎯 Learning Goals

- [x] Understand Docker fundamentals and containerization
- [x] Run PostgreSQL in Docker container
- [x] Learn Docker Compose for multi-container apps
- [x] Build data ingestion pipeline with Docker
- [ ] Introduction to Terraform basics
- [ ] Deploy infrastructure to GCP with Terraform
- [ ] Complete homework

## 📋 Linear Tasks

[View in Linear](https://linear.app/linear-home-workspace/project/module-1-docker-terraform-a9858e512f38)

## 📖 Course Notes

### Lecture 1: Introduction to Docker

**Key Discovery: `uv` Package Manager**
- Modern Python package manager - never heard of it before!
- Usage: `uv run <command>` or `uv add <package>`
- **IDE Integration Note:** Remember to change the interpreter in the IDE if using `uv` (command-line method not explained in course - need to research later)

**Dockerfile Best Practice with `uv`:**
```dockerfile
# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"
```

**Jupyter in Cloud Shell:**
Working on Google Cloud Shell required special configuration:

```python
# ~/.jupyter/jupyter_notebook_config.py
c = get_config()

# Allow connections from Cloud Shell URL
c.NotebookApp.ip = '*'
c.NotebookApp.allow_remote_access = True
c.NotebookApp.allow_origin = '*'

# ⚠️ INSECURE - for testing only!
c.NotebookApp.token = ''
c.NotebookApp.password = ''
c.NotebookApp.disable_check_xsrf = True

# For production: Use hashed password
# from IPython.lib import passwd
# c.NotebookApp.password = passwd('your_secret_password')
```

---

### Lecture 2: Docker Compose & PostgreSQL

✅ **Completed:** Docker and Docker Compose sections  
🚧 **Still To Go:** PostgreSQL deep dive

**Built a Complete Data Ingestion Pipeline:**

#### Project Structure
```
pipeline/
├── ingest_data.py     # Main ETL script
├── Dockerfile         # Container definition
├── pyproject.toml     # uv dependencies
├── uv.lock           # Locked versions
└── notebook.ipynb    # Exploratory work
```

#### Key Components

**1. Data Ingestion Script (`ingest_data.py`)**
- Downloads NYC Taxi CSV data from GitHub
- Uses **chunking** for memory efficiency (100k rows/chunk)
- Leverages `sqlalchemy` + `pandas` for PostgreSQL writes
- CLI with `click` for parameterization

```python
# Core pattern: Chunked ingestion
df_iter = pd.read_csv(url, iterator=True, chunksize=100000)

first_chunk = next(df_iter)
first_chunk.head(0).to_sql(name=table, con=engine, if_exists="replace")

for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name=table, con=engine, if_exists="append")
```

**2. Docker Compose Multi-Service Stack**

```yaml
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "ny_taxi_postgres_data:/var/lib/postgresql/data"
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8085:80"

  taxi-ingest:
    build:
      context: ./pipeline
    command: >
      --pg_host=pgdatabase 
      --pg_user=root 
      --year=2021 
      --month=1
    depends_on:
      - pgdatabase

volumes:
  ny_taxi_postgres_data:
  pgadmin_data:
```

---

## 🐛 Troubleshooting Guide

### 1. Git & File Permissions

**Error:** `warning: could not open directory '.../ny_taxi_postgres_data/': Permission denied`

**Cause:** Docker volumes are owned by `root`. Database files should never be in Git.

**Solution:**
```gitignore
# .gitignore
ny_taxi_postgres_data/
pgadmin_data/
__pycache__/
*.pyc
```

---

### 2. Python Dependencies with `uv`

**Error:** `ModuleNotFoundError: No module named 'tqdm'`

**Cause:** Dependencies in `pyproject.toml` but not installed.

**Solution:**
```bash
uv pip install .
# or in notebook:
!uv add tqdm
```

---

### 3. Docker Compose V1 vs V2

**Error:** `client version 1.30 is too old`

**Cause:** Using legacy `docker-compose` (hyphen).

**Solution:** Use modern V2 command:
```bash
docker compose up -d  # ← Space, not hyphen!
```

---

### 4. YAML Indentation

**Error:** `Unsupported config option for services: 'pgadmin'`

**Cause:** YAML indentation破坏了hierarchy.

**Solution:** Ensure all services are nested under `services:`, remove `version:` tag.

---

### 5. Postgres Volume Corruption

**Error:** `pg-taxi-db exited with code 1`

**Root Cause:**
1. Used `postgres:18` (dev version) instead of stable `postgres:13`
2. Corrupted volume from failed start

**Solution:**
```bash
# -v flag is CRITICAL - it deletes volumes
docker compose down -v

# Update docker-compose.yml
image: postgres:13

# Restart clean
docker compose up -d
```

---

### 6. Docker Networking

**Key Concept:** Containers use **service names** as hostnames, not `localhost`.

**Connecting pgAdmin → Postgres:**
- Host: `pgdatabase` (service name)
- Port: `5432`
- User: `root`
- Database: `ny_taxi`

**Connecting External Script:**
```bash
# Find network
docker network ls

# Run on same network
docker run -it \
  --network=module-1-docker-terraform_default \
  taxi_ingest:v001 \
  --pg_host=pgdatabase \
  --pg_user=root
```

---

### Lecture 3: Terraform Basics

*Not started yet*

### Lecture 4: GCP with Terraform

*Not started yet*

---

## 💻 Code Examples

### Docker Commands Reference

```bash
# Modern Docker Compose
docker compose up -d
docker compose down -v  # -v removes volumes

# Network debugging
docker network ls
docker network inspect <network_name>

# Container logs
docker logs <container_name>
docker logs -f pgdatabase  # follow

# Exec into running container
docker exec -it pgdatabase psql -U root -d ny_taxi
```

### Data Ingestion CLI

```bash
# Build image
docker build -t taxi_ingest:v001 .

# Run locally (needs network)
docker run -it \
  --network=module-1-docker-terraform_default \
  taxi_ingest:v001 \
  --pg_host=pgdatabase \
  --pg_user=root \
  --pg_pass=root \
  --pg_db=ny_taxi \
  --year=2021 \
  --month=1
```

### Dockerfile with `uv`

```dockerfile
FROM python:3.13.11-slim

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

# CRITICAL: Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
RUN uv sync --locked

# Copy application code
COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]
```

---

## 🔑 Key Concepts

### Docker
- **Containers vs VMs:** Lightweight processes vs full OS virtualization
- **Images and Layers:** Immutable layers, cacheable builds
- **Docker Compose:** Multi-container orchestration with YAML
- **Networking:** Service discovery via service names
- **Volumes:** Persistent data storage

### Data Engineering Pipeline
- **Chunked Processing:** Memory-efficient large file handling
- **Schema Enforcement:** Explicit `dtype` mapping for Pandas
- **Idempotent Operations:** `if_exists='replace'` for table creation
- **Progress Monitoring:** `tqdm` for ETL visibility

### Terraform
*To be documented after Lecture 3*

---

## ❓ Questions & Clarifications

- [ ] How to set `uv` Python interpreter via command line (not just IDE)?
- [ ] Best practices for Jupyter security in Cloud Shell for production?
- [ ] When to use Docker volumes vs bind mounts?

---

## 🔗 Resources

- [Course Materials](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform)
- [Docker Documentation](https://docs.docker.com/)
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

---

## ✅ Homework

### Questions
1. Docker version
2. Running container
3. PostgreSQL setup
4. Docker Compose
5. Terraform basics

### Submission
- [ ] Complete all questions
- [ ] Test locally
- [ ] Submit to GitHub
- [ ] Verify submission

---

## 📝 Weekly Reflection

### What went well:
- Successfully built complete data ingestion pipeline
- Learned troubleshooting through actual errors (great learning!)
- Docker Compose multi-service setup working perfectly

### What was challenging:
- Postgres version incompatibility (18 → 13)
- Corrupted Docker volumes requiring hard reset
- Jupyter configuration for Cloud Shell environment

### Key takeaways:
- `docker compose down -v` is critical when volumes get corrupted
- Service names are hostnames in Docker networks
- Modern `uv` package manager is impressive for Python dependency management
- Chunked data processing is essential for large datasets

---

*Created: 2026-01-17*  
*Last updated: 2026-01-18*
