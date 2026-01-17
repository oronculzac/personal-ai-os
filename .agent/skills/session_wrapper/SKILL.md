---
name: Session Wrapper
description: Automates the creation of "Learning-in-Public" session logs by aggregating Git activity, Linear tasks, and generating social-ready content.
version: 1.1.0
triggers:
  - wrap session
  - create session log
  - log session
  - end session
capabilities:
  - git_analysis
  - task_aggregation
  - content_synthesis
  - social_drafting
  - publish_detection
  - github_routing
dependencies:
  - requests>=2.31.0
  - gitpython>=3.1.0
  - python-frontmatter>=1.0.0
auto_load: true
---

# Session Wrapper Skill

Automate the "Learning-in-Public" workflow by turning work into content.

## 🎯 Purpose

Eliminate the friction of documenting your learning. This skill analyzes your recent work (Git commits, Linear tickets) and uses the `content_writer` persona to generate a structured session log with ready-to-post social media drafts.

## 🚀 Capabilities

### 1. **Context Collection**
- **Git Analysis**: Scans your current repository for recent changes (`git diff`, `git log`).
- **Linear Integration**: Fetches "In Progress" or recently "Done" tickets to identify what you worked on.
- **Session Notes**: Incorporates any scratchpad notes you've made.

### 2. **Core Intelligence: Smart Alignment**
- **Drift Detection**: Compares your `git diff` against the `linear_ticket.scope`.
    - *Example*: If you edited `automation.py` but the ticket is "Study SQL", it flags this as a **Side Quest**.
- **Attribution**:
    - **Core Work**: properly logged under the main project.
    - **Side Quests**: logged separately, with auto-suggestions to create new Linear tickets.

### 3. **Content Engine**
Synthesizes the raw data into a narrative:
- **The Struggle**: identifying technical blockers.
- **The Win**: explaining the solution.
- **The Lesson**: extracting the core concept.

### 4. **Output Generation**
Creates a comprehensive Markdown file in your Obsidian Vault:
- **Core Project Work**: Work matching the main ticket.
- **Side Quests & Tooling**: Work that is supportive but tangential.
- **Twitter Thread**: A hook-driven thread optimized for engagement.
- **LinkedIn Post**: A professional summary of the session.

## 💡 Usage Examples

### Example 1: Wrap Up a Coding Session
```
User: "Wrap up this session. I was working on the BigQuery setup."
Assistant: *Runs analysis, finds modified config files, fetches the 'BigQuery Setup' ticket from Linear, and creates a session log in Obsidian.*
```

### Example 2: Log Specific Learning
```
User: "Create a session log for my work on dbt models."
Assistant: *Focuses the summary on dbt transformation logic and creates a relevant Twitter thread about data modeling.*
```

## 🔧 Configuration

Ensures `mcp_config.json` contains:
```json
{
  "linear": { "api_key": "..." },
  "obsidian": { "vault_path": "..." }
}
```

## 📝 Template Structure

The generated note follows this structure:
1.  **Metadata**: Date, Time, Tags.
2.  **What I Did**: Technical summary.
3.  **What I Learned**: Conceptual summary.
4.  **Social Drafts**: Twitter & LinkedIn.
