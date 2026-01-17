# Personal AI OS 🤖

A modular, portable AI agent framework with specialized skills and personas for productivity automation.

## 🎯 Vision

Transform learning into content, code into documentation, and tasks into public accountability — all automated via AI-agent orchestration.

## 🚀 Features

- **Modular Skills** — Plug-and-play capabilities (Excel, Web Scraping, Session Wrapper)
- **Personas** — Role-based expertise (Data Engineer, Content Writer, DevOps)
- **Publish Detection** — Auto-identify GitHub-worthy content
- **Learning-in-Public** — Automated session logs and social drafts

## 📦 Structure

```
.agent/
├── skills/              # Modular capabilities
│   ├── session_wrapper/ # Learning-in-Public automation
│   ├── github_publisher/# Auto-commit to repos
│   └── ...
├── personas/            # Role-based configurations
├── workflows/           # Automation scripts
├── core/                # Helper utilities
└── config/              # Configuration files
```

## 🔧 Quick Start

1. Clone this repo
2. Create virtual environment:
   ```powershell
   python -m venv .agent\.venv
   .agent\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Configure `.agent/config/mcp_config.json`
4. Start using skills!

## 💡 Key Skills

### Session Wrapper
Wraps up coding sessions into structured logs with:
- Git activity tracking
- Linear ticket aggregation
- Publish-worthiness detection
- Social media draft generation

### GitHub Publisher
Auto-commits content to appropriate repos:
- Skills → `personal-ai-os`
- Homework → `de-zoomcamp-2026`
- Session logs → `learning-logs`

## 📚 Documentation

- [Quick Start Guide](.agent/QUICKSTART.md)
- [Deployment Guide](.agent/DEPLOYMENT.md)
- [Skill Authoring](docs/SKILL_AUTHORING.md)

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

*Built with ❤️ for the Learning-in-Public community*
