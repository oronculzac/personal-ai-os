# Agent Personas - User Guide

## 🎭 What Are Agent Personas?

Agent Personas are **specialized AI identities** that give Antigravity focused expertise and curated skill sets. Each persona acts as a different professional role with domain-specific knowledge.

---

## 📋 Available Personas

### 1. SEO Specialist
**Focus**: Search engine optimization, keyword research, content strategy

**Skills Available**:
- Web Scraper (competitor analysis, SERP research)
- Excel Generator (ranking reports, keyword tracking)
- File Organizer (research materials)

**Best For**:
- Keyword research
- Competitor analysis
- SEO content optimization
- Traffic growth strategies
- SERP analysis

**Example Uses**:
```
"Scrape competitor meta tags from example.com"
"Create keyword opportunity report for 'AI automation'"
"Analyze top-ranking pages for 'content marketing'"
```

---

### 2. Data Analyst
**Focus**: Data analysis, visualization, business intelligence

**Skills Available**:
- Excel Generator (charts, pivot tables, formulas)
- Web Scraper (data collection)
- File Organizer (dataset management)

**Best For**:
- Data analysis and insights
- Creating charts and dashboards
- Trend analysis
- Statistical reporting
- Business intelligence

**Example Uses**:
```
"Analyze this sales data and find trends"
"Create Excel dashboard with monthly metrics"
"Scrape pricing data and compare competitors"
```

---

### 3. Content Writer
**Focus**: High-quality content creation, storytelling, engagement

**Skills Available**:
- Web Scraper (research and fact-checking)
- Excel Generator (content calendars, tracking)
- File Organizer (draft organization)

**Best For**:
- Blog posts and articles
- Content research
- Content planning
- Audience engagement
- Brand voice consistency

**Example Uses**:
```
"Research latest trends in AI for blog post"
"Create content calendar for January in Excel"
"Organize draft articles by topic"
```

---

## 🔀 Switching Personas

### Method 1: Command Line

**List available personas**:
```powershell
python .agent\core\persona_manager.py --list
```

**Activate a persona**:
```powershell
python .agent\core\persona_manager.py --activate seo_specialist
python .agent\core\persona_manager.py --activate data_analyst
python .agent\core\persona_manager.py --activate content_writer
```

**Check current persona**:
```powershell
python .agent\core\persona_manager.py --status
```

**Return to default mode** (all skills):
```powershell
python .agent\core\persona_manager.py --deactivate
```

### Method 2: Ask Antigravity

Simply ask:
- "Switch to SEO Specialist persona"
- "Activate Data Analyst mode"
- "Use Content Writer persona"
- "Return to default mode"

---

## 🎯 How Personas Change Behavior

### Same Task, Different Persona = Different Approach

**Task**: "Create a report about website performance"

**SEO Specialist**:
- Focuses on: rankings, organic traffic, keywords
- Creates: SEO performance report with SERP positions
- Includes: keyword opportunities, competitor gaps

**Data Analyst**:
- Focuses on: metrics, trends, statistical analysis
- Creates: Analytical dashboard with charts
- Includes: conversion rates, trend lines, forecasts

**Content Writer**:
- Focuses on: engagement, narrative, readability
- Creates: Written analysis with storytelling
- Includes: insights, recommendations, examples

---

## 💡 Best Practices

### When to Use Personas

✅ **Use a persona when**:
- You need specialized expertise
- Working on domain-specific tasks
- Want focused, role-appropriate responses
- Need consistent behavior across tasks

❌ **Use default mode when**:
- Doing general-purpose tasks
- Need access to all skills
- Exploring without specific focus

### Persona Workflows

**Typical Pattern**:
```
1. Activate persona: "Switch to SEO Specialist"
2. Work on related tasks for a session
3. Persona stays active across multiple requests
4. Switch when changing focus areas
```

---

## 🛠️ Creating Custom Personas

You can create your own specialized personas!

### Steps:
1. Create new JSON file in `.agent/personas/`
2. Define persona configuration (see examples)
3. Specify allowed skills
4. Write system prompt for behavior
5. Save and persona is auto-discovered

### Template:
```json
{
  "id": "your_persona_id",
  "name": "Your Persona Name",
  "version": "1.0.0",
  "description": "What this persona specializes in",
  "expertise": [
    "Skill area 1",
    "Skill area 2"
  ],
  "allowed_skills": [
    "skill_1",
    "skill_2" 
  ],
  "system_prompt": "Instructions for how to behave...",
  "behavioral_traits": {
    "writing_style": "professional",
    "focus_areas": ["area1", "area2"]
  }
}
```

---

## 📊 Persona + Skill Matrix

| Persona | Excel Gen | File Org | Web Scraper | Future Skills |
|---------|-----------|----------|-------------|---------------|
| SEO Specialist | ✅ Reports | ✅ Research | ✅ Analysis | Keyword Research, Blog Writer |
| Data Analyst | ✅ Dashboards | ✅ Datasets | ✅ Data Collection | Data Visualizer, Deck Creator |
| Content Writer | ✅ Calendars | ✅ Drafts | ✅ Research | Blog Writer, Grammar Checker |

---

## 🚀 Advanced Usage

### Multi-Persona Workflows

Complex projects can use multiple personas in sequence:

```
Example: "Launch new blog"

1. SEO Specialist persona:
   - Research keywords
   - Analyze competitors
   - Create keyword strategy

2. Content Writer persona:
   - Write blog posts
   - Optimize for readability
   - Create content calendar

3. Data Analyst persona:
   - Track performance
   - Analyze traffic
   - Create reports
```

### Persona Context

Each persona maintains its expertise throughout the session:
- Terminology stays consistent
- Approach remains focused
- Recommendations align with role

---

## 📁 Persona Files Location

```
.agent/personas/
├── seo_specialist.json
├── data_analyst.json
├── content_writer.json
└── your_custom_persona.json

.agent/config/
└── active_persona.json  # Tracks current persona
```

---

## 🆘 Troubleshooting

**Persona not found?**
```powershell
python .agent\core\persona_manager.py --list
```

**Can't activate persona?**
- Check persona ID matches filename (without .json)
- Ensure JSON is valid
- Verify personas directory exists

**Wrong skills showing?**
- Deactivate and reactivate persona
- Check allowed_skills list in persona JSON

---

## 🎉 Benefits

1. **Focused Expertise**: Get role-appropriate responses
2. **Reduced Noise**: Only see relevant skills
3. **Consistent Behavior**: Maintains professional persona
4. **Easy Switching**: Change roles as needs change
5. **Portable**: Personas are just JSON files

---

## Next Steps

1. Try each persona for different tasks
2. Notice how responses change based on role
3. Create custom persona for your specific needs
4. Build workflows combining multiple personas

**Personas transform Antigravity from generalist to specialist on demand!**
