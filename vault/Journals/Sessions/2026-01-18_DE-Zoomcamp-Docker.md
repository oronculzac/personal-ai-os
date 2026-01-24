---
date: 2026-01-18
type: session-log
tags: [learning-in-public, de-zoomcamp, docker, data-engineering]
module: module-1-docker-terraform
---

# Building My First Containerized Data Pipeline: Docker + PostgreSQL for 1.3M Records

**Journey:** Data Engineering Zoomcamp - Module 1  
**Time Invested:** ~9 hours  
**Focus:** Docker, Data Ingestion, and Real-World Troubleshooting

---

## 🎯 The Challenge

As part of the Data Engineering Zoomcamp, I set out to build a production-ready data pipeline for ingesting and analyzing 1.3 million NYC taxi trip records. The catch? Everything needed to run in Docker containers for portability and reproducibility.

This was my first deep dive into containerized data infrastructure, and the journey was filled with valuable lessons.

---

## 💻 What I Built

### Multi-Container Data Stack

I created a complete local data environment using Docker Compose with three services:

- **PostgreSQL 13** - Database for storing taxi trip data
- **pgAdmin** - Web-based database management interface
- **Custom Ingestion Service** - Automated ETL pipeline

**Architecture:**
```
┌─────────────────┐
│  taxi-ingest    │ ──┐
│  (Python/uv)    │   │
└─────────────────┘   │
                      ▼
┌─────────────────┐   ┌──────────────┐
│    pgadmin      │──▶│  pgdatabase  │
│  (Web UI:8085)  │   │  (PG:5432)   │
└─────────────────┘   └──────────────┘
                            │
                      [Docker Volume]
                      ny_taxi_postgres_data
```

### Production-Ready ETL Pipeline

The ingestion pipeline features:
- **Chunked processing** (100k rows/chunk) for memory efficiency
- **CLI interface** using `click` for parameterization
- **Schema enforcement** with explicit Pandas dtypes
- **Progress tracking** using `tqdm`
- **Full Dockerization** with modern `uv` package manager

**Tech Stack:**
- Python 3.13 with `uv` for dependency management
- `pandas` for data manipulation
- `sqlalchemy` + `psycopg2` for PostgreSQL connectivity
- `click` for CLI framework

---

## 📖 Key Technical Learnings

### Discovery: `uv` Package Manager

This was my first exposure to `uv` - a Rust-based Python package manager that's revolutionizing dependency management.

**Why it's impressive:**
- Lightning-fast dependency resolution
- Automatic virtual environment management
- Seamless Docker integration

**Critical Dockerfile pattern:**
```dockerfile
# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# This is essential - add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Install locked dependencies
RUN uv sync --locked
```

### Docker Compose Modernization

I learned the hard way about Docker versioning:
- ❌ `docker-compose` (V1 - deprecated, throws version errors)
- ✅ `docker compose` (V2 - integrated into Docker CLI)

The space vs. hyphen makes all the difference!

### Docker Networking Fundamentals

One of the biggest "aha!" moments: containers communicate via **service names**, not `localhost`.

For connecting to the database from the ingestion script:
- ❌ `--pg_host=localhost`
- ✅ `--pg_host=pgdatabase`

Docker's internal DNS automatically resolves service names to container IPs within the same network.

### Memory-Efficient Data Processing

Essential pattern for handling large datasets:

```python
# Create iterator with chunk size
df_iter = pd.read_csv(url, iterator=True, chunksize=100000)

# Create table schema from first chunk
first_chunk = next(df_iter)
first_chunk.head(0).to_sql(name=table, if_exists="replace")

# Stream remaining chunks
for chunk in tqdm(df_iter):
    chunk.to_sql(name=table, if_exists="append")
```

This approach kept memory usage constant while processing 1.3M+ records.

---

## 🐛 Real-World Debugging Journey

### Problem 1: Postgres Container Crash

**Error:** `pg-taxi-db exited with code 1`

**Root Cause:**
- Used `postgres:18` (unstable development version)
- Corrupted volume from failed initialization

**Solution:**
```bash
docker compose down -v  # Critical: -v removes volumes!
# Update to postgres:13 in docker-compose.yml
docker compose up -d
```

**Lesson:** Always use stable versions and understand that volumes persist *everything*, including broken state.

---

### Problem 2: Git Permission Denied

**Error:** `warning: could not open directory 'ny_taxi_postgres_data/': Permission denied`

**Root Cause:** Docker volumes are owned by `root`, causing Git to choke when scanning directories.

**Solution:**
```gitignore
ny_taxi_postgres_data/
pgadmin_data/
__pycache__/
*.pyc
```

**Lesson:** Database volumes should NEVER be committed to version control.

---

### Problem 3: YAML Indentation Issues

**Error:** `Unsupported config option for services: 'pgadmin'`

**Root Cause:** YAML is whitespace-sensitive - services weren't properly nested.

**Solution:**
```yaml
services:  # ← Must be top level
  pgdatabase:  # ← 2 spaces indentation
    image: postgres:13
    ...
  pgadmin:  # ← Same level as pgdatabase
    image: dpage/pgadmin4
    ...
```

---

### Problem 4: Jupyter Security in Cloud Shell

Working on Google Cloud Shell required special Jupyter configuration. For development environments:

```python
c.NotebookApp.ip = '*'
c.NotebookApp.allow_origin = '*'
c.NotebookApp.token = ''  # INSECURE - dev only!
```

**Note:** This is insecure and only for testing. Production environments should use proper authentication.

---

## 📊 Session Outcomes

- ⏱️ **Time:** 9 hours (including productive debugging!)
- 📁 **Files Created:** 20 (pipeline code, Docker configs, notebooks)
- 🐛 **Bugs Solved:** 6 major issues
- 💾 **Data Ingested:** 1,369,765 taxi trip records
- 📚 **New Tools:** `uv`, modern Docker Compose, chunked ETL patterns

---

## 💡 The Bigger Picture

What struck me most wasn't just writing code - it was understanding how to build **reliable, reproducible infrastructure**.

Docker transforms the infamous "works on my machine" problem into "works everywhere." For data engineering, this is foundational. When you're orchestrating complex data pipelines across teams and environments, containerization isn't optional - it's essential.

Key principles I internalized:

1. **Infrastructure as Code** - Docker Compose files are reproducible blueprints
2. **Memory Efficiency** - Chunking is non-negotiable for large datasets
3. **Failure Modes Matter** - Understanding volume persistence, networking, and cleanup is as important as the happy path

---

## 🔗 Code & Resources

**Repository:** [de-zoomcamp-2026](https://github.com/oronculzac/de-zoomcamp-2026/tree/main/modules/module-1-docker-terraform)

**Key Files:**
- `pipeline/ingest_data.py` - Production ETL script
- `pipeline/Dockerfile` - Container definition with uv
- `docker-compose.yml` - Multi-service orchestration
- `pipeline/notebook.ipynb` - Exploratory analysis

**Course:** [DataTalksClub Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) (Free!)

---

## 🚀 Next Steps

- Complete PostgreSQL deep dive
- Terraform for Infrastructure as Code
- Deploy to Google Cloud Platform
- Production hardening and security

---

**Building in public!** Follow my journey as I document learning data engineering from the ground up. Every win, every bug, every lesson.

*What's your experience with containerized data workflows? Drop your insights in the comments!*
