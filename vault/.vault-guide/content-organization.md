# Content Organization System

## 📁 Structure

```
vault/
├── Journals/
│   └── Sessions/          # Article-quality session logs
│       └── YYYY-MM-DD_Topic.md
├── Social/                # NEW: Platform-specific drafts
│   └── YYYY-MM-DD_Topic_drafts.md
└── 02-Areas/
    └── DataEngineering/
        └── Modules/       # Course notes
```

## 📝 File Purposes

### Session Logs (`vault/Journals/Sessions/`)
**Purpose:** Publication-ready articles for Dev.to, personal blog, etc.

**Content:**
- Learning narrative
- Technical details
- Code examples
- Troubleshooting journey
- NO social media drafts

**Example:** `2026-01-18_DE-Zoomcamp-Docker.md`

---

### Social Drafts (`vault/Social/`)
**Purpose:** Platform-specific copy for Twitter, LinkedIn, etc.

**Content:**
- Twitter/X thread
- LinkedIn post
- Dev.to metadata (tags, series, etc.)
- Links back to session article

**Example:** `2026-01-18_DE-Zoomcamp-Docker_drafts.md`

---

### Module Notes (`vault/02-Areas/DataEngineering/Modules/`)
**Purpose:** Reference documentation for course content

**Content:**
- Lecture notes
- Code snippets
- Troubleshooting guides
- Key concepts
- Questions/clarifications

**Example:** `Module-01-Docker-Terraform.md`

## 🔄 Workflow

### When Wrapping a Session

1. **Session Wrapper generates TWO files:**
   - `vault/Journals/Sessions/[date]_[topic].md` → Article
   - `vault/Social/[date]_[topic]_drafts.md` → Social

2. **Article is Dev.to ready:**
   - No social drafts section
   - GitHub URLs (not file:// links)
   - Engaging title
   - Clean frontmatter

3. **Social drafts are separate:**
   - Twitter thread
   - LinkedIn post
   - Platform metadata

### Publishing Flow

```
Session Work
    ↓
Session Wrapper generates
    ↓
├─→ Sessions/article.md → Dev.to (publish as draft)
└─→ Social/drafts.md → Copy/paste to Twitter/LinkedIn
```

## 🎯 Benefits

1. **Clean separation** - Articles don't contain social drafts
2. **Single source** - Social folder = all platform content
3. **Reusable** - Can create different drafts for same session
4. **Organized** - Easy to find what you need

## 📋 TODO: Skill Updates

- [ ] Update `session_wrapper` to generate separate files
- [ ] Update `devto_publisher` to only read session articles
- [ ] Create template for social drafts file
- [ ] Update `/wrap-session` workflow documentation

---

*Created: 2026-01-18*  
*Last updated: 2026-01-18*
