---
name: AI Researcher
description: Automated skill to gather and summarize AI news and trends from various sources (Google Trends, RSS).
version: 1.1.0
triggers:
  - research AI news
  - get AI trends
  - summarize AI developments
  - AI newsletter
  - what's new in AI
examples:
  - "What's happening in AI this week?"
  - "Research the latest AI developments"
  - "Create an AI news summary"
  - "Find trending AI topics"
context_hints:
  - user asks about AI news or trends
  - user wants industry updates
  - user mentions research or monitoring AI landscape
priority: 5
conflicts_with: []
capabilities:
  - trend_analysis
  - news_aggregation
  - community_monitoring
  - report_generation
dependencies:
  - pytrends>=4.9.0
  - feedparser>=6.0.0
  - requests>=2.31.0
  - beautifulsoup4>=4.12.0
auto_load: true
---

# AI Researcher Skill

This skill automates the process of researching the latest developments in Artificial Intelligence. It fetches data from social media, news feeds, and search trends to provide a daily snapshot of the AI landscape.

## Capabilities

- **Trend Analysis**: Fetches current trending searches related to AI from Google Trends.
- **News Aggregation**: Crawls RSS feeds from top tech news sites (TechCrunch, VentureBeat).
- **Community Pulse**: Monitors key Subreddits (r/ArtificialIntelligence, r/LocalLLaMA) for top discussions.
- **Report Generation**: Compiles all gathered information into a clean, readable Markdown report in `vault/Areas/AI/Reports/`.

## Usage

Run the main research script:

```powershell
python .agent/skills/ai_researcher/scripts/research.py
```

## Configuration

The skill uses a standard set of feeds and keywords defined in `scripts/research.py`. You can modify the `CONFIG` dictionary in that file to add more sources or change search terms.

## Dependencies

- `pytrends`
- `feedparser`
- `requests`
- `beautifulsoup4`

Make sure to install these in your environment:
```powershell
pip install -r .agent/skills/ai_researcher/scripts/requirements.txt
```
