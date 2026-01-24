# Social Media Drafts - DE Zoomcamp Docker Session

**Topic:** Building First Containerized Data Pipeline  
**Date:** 2026-01-18  
**Session:** Module 1 - Docker & Data Ingestion

---

## 🐦 Twitter/X Thread

🧵 Day 1 of #DataEngineeringZoomcamp 🚀

Built my first containerized data pipeline with Docker!

Here's what I learned deploying a PostgreSQL + pgAdmin stack and ingesting 1.3M NYC taxi records 👇

1/ 🎯 **Challenge:** Load 1.3M taxi trip records into PostgreSQL without crashing my laptop.

**Solution:** Chunked processing with Pandas!
- Read CSV in 100k row chunks
- Stream to DB incrementally
- Memory stays constant 📉

2/ 🔧 **New Tool Alert:** `uv` package manager

This Rust-based Python tool is FAST:
- Replaces pip + venv
- Integrates beautifully with Docker
- Auto-locks dependencies

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
```

3/ 🐛 **Bug Hunt:** Postgres container kept crashing (exit code 1)

**Culprit:** Corrupted Docker volume from failed init

**Fix:**
```bash
docker compose down -v  # ← -v is critical!
```

Learned: Volumes persist EVERYTHING, including broken state!

4/ 🌐 **Docker Networking 101:**

Containers don't use `localhost` - they use service names!

❌ `--pg_host=localhost`  
✅ `--pg_host=pgdatabase`

Auto DNS resolution within the same Docker network 🎯

5/ 📊 **Stats:**
- 20 files created
- 6 bugs squashed
- 1.3M records ingested
- ∞ Docker knowledge gained

6/ 💡 **Key Takeaway:**

Data engineering isn't just about code - it's about:
- Reliable infrastructure (Docker)
- Memory-efficient patterns (chunking)
- Debugging persistence layers (volumes)

Building systems that SCALE matters!

7/ Next up: Terraform + GCP for cloud deployment ☁️

Following along? Check out @DataTalksClub's free course:
https://github.com/DataTalksClub/data-engineering-zoomcamp

#DataEngineering #Docker #LearningInPublic #100DaysOfCode

---

## 💼 LinkedIn Post

**📚 Data Engineering Zoomcamp - Day 1: Docker Deep Dive**

Today I completed the containerization module of DataTalksClub's Data Engineering Zoomcamp, and I'm excited about what I built!

**🎯 What I Built:**
A production-ready data ingestion pipeline using Docker Compose to orchestrate:
- PostgreSQL 13 database
- pgAdmin for management
- Custom Python ETL service

**📖 Key Technical Learnings:**

1️⃣ **Modern Python Tooling:** Discovered `uv` - a Rust-based package manager that's revolutionizing Python dependency management. The speed difference vs pip is remarkable!

2️⃣ **Memory-Efficient ETL:** Implemented chunked data processing to ingest 1.3M+ NYC taxi records without overwhelming system resources. This pattern is foundational for enterprise-scale data engineering.

3️⃣ **Docker Networking:** Learned that containerized services communicate via service names (e.g., `pgdatabase`), not `localhost`. This mental model shift is crucial for microservices architecture.

**🐛 Real-World Debugging:**
- Solved Postgres volume corruption by understanding Docker's persistence layer
- Navigated YAML syntax gotchas in Docker Compose
- Configured Jupyter for secure Cloud Shell environments

**💡 The Bigger Picture:**

What struck me most wasn't just *writing code* - it was understanding how to build **reliable, reproducible infrastructure**. Docker transforms "works on my machine" into "works everywhere."

This is the foundation modern data platforms are built on, and I'm grateful to be learning it hands-on.

**📊 Session Stats:**
- ⏱️ 9 hours (including productive debugging time!)
- 📁 20 files created
- 💾 1.3M records successfully ingested

Next up: Terraform for Infrastructure as Code + GCP deployment.

Building in public and documenting every step. If you're interested in data engineering, I highly recommend checking out the free course from DataTalksClub.

What's your experience with Docker in data workflows? Would love to hear insights! 👇

#DataEngineering #Docker #LearningInPublic #ProfessionalDevelopment #DataTalksClub

---

## 📝 Dev.to Options

**Tags:** `dataengineering` `docker` `learninginpublic` `tutorial`  
**Series:** "Data Engineering Zoomcamp Journey"  
**Canonical URL:** https://github.com/oronculzac/de-zoomcamp-2026

---

*Generated from session: 2026-01-18*  
*Article: [vault/Journals/Sessions/2026-01-18_DE-Zoomcamp-Docker.md](../Journals/Sessions/2026-01-18_DE-Zoomcamp-Docker.md)*
