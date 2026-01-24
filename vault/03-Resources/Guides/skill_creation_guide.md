# Skill Creation Best Practices

Guidelines for creating MCP-aligned skills in Antigravity.

---

## 🎯 Core Principles (From MCP Standard)

### 1. **Schema Precision = Agency**
The more precisely you define inputs, the more reliably the AI uses the tool.

### 2. **Docstrings Drive Selection**
The LLM reads function docstrings to decide when to use a tool. Quality descriptions = smart tool selection.

### 3. **Fail Gracefully**
Always handle errors and provide actionable feedback.

---

## 📋 SKILL.md Frontmatter (Required)

```yaml
---
name: Skill Name                    # Human-readable name
description: One-line description   # LLM reads this for skill selection
version: 1.0.0                      # Semantic versioning
triggers:                           # Natural language phrases
  - trigger phrase one
  - trigger phrase two
capabilities:                       # What the skill can do
  - capability_one
  - capability_two
dependencies:                       # Python packages required
  - requests>=2.31.0
inputs:                             # NEW: Define expected inputs
  required:
    - name: input_name
      type: string
      description: What this input is for
  optional:
    - name: dry_run
      type: boolean
      default: false
      description: Preview without changes
outputs:                            # NEW: Define expected outputs
  - name: result_path
    type: path
    description: Path to created file
auto_load: true                     # Auto-discover this skill
---
```

---

## 🐍 Script Best Practices

### Function Docstrings (Critical!)

```python
def create_report(data: dict, output_path: str, format: str = "xlsx") -> Path:
    """
    Create a formatted report from data.
    
    Use this tool when the user asks to:
    - Generate a report
    - Export data to Excel
    - Create a spreadsheet summary
    
    Args:
        data: Dictionary with report data (keys become columns)
        output_path: Where to save the file (absolute path)
        format: Output format - 'xlsx', 'csv', or 'json'
    
    Returns:
        Path to the created report file
    
    Raises:
        ValueError: If data is empty or format is invalid
    """
```

### Error Handling Pattern

```python
def execute_tool(params: dict) -> dict:
    """Execute with proper error handling"""
    try:
        # Validate inputs
        if not params.get('required_field'):
            return {"success": False, "error": "Missing required field"}
        
        # Execute
        result = do_the_work(params)
        
        # Return structured response
        return {
            "success": True,
            "result": result,
            "message": f"Completed successfully"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Check input format and try again"
        }
```

### Structured Returns (MCP-Aligned)

Always return structured data the LLM can interpret:

```python
# Good - structured response
return {
    "success": True,
    "files_created": ["path1.md", "path2.md"],
    "count": 2,
    "next_steps": ["Review files", "Commit to git"]
}

# Bad - unstructured string
return "Created 2 files successfully"
```

---

## 📁 Skill Folder Structure

```
.agent/skills/my_skill/
├── SKILL.md              # Required: Instructions + frontmatter
├── scripts/
│   ├── __init__.py       # Make importable
│   └── main.py           # Core logic with docstrings
├── resources/            # Optional: Templates, configs
│   └── template.json
└── tests/                # Optional but recommended
    └── test_main.py
```

---

## ✅ Skill Checklist

Before shipping a skill, verify:

- [ ] **SKILL.md** has complete frontmatter
- [ ] **Description** clearly explains when to use this skill
- [ ] **Triggers** cover natural language variations
- [ ] **Dependencies** are listed
- [ ] **Scripts** have comprehensive docstrings
- [ ] **Errors** are caught and return helpful messages
- [ ] **Returns** are structured (dict with success/error)
- [ ] **Venv** path used: `.agent\.venv\Scripts\python.exe`

---

## 🔄 Comparison: Antigravity vs MCP

| Aspect | Antigravity Current | MCP Standard | Alignment Action |
|--------|---------------------|--------------|------------------|
| Skill Definition | YAML frontmatter | JSON Schema | Add `inputs`/`outputs` to frontmatter |
| Tool Description | `description` field | `description` in schema | ✅ Already aligned |
| Input Schema | Implicit in code | Explicit `inputSchema` | Document in frontmatter |
| Invocation | Direct Python | JSON-RPC 2.0 | Keep direct, add structured returns |
| Error Handling | Various | Structured response | Standardize return format |

---

## 🎭 Future: Persona Drift Prevention

When creating personas, add **axioms** to prevent drift:

```json
{
  "axioms": [
    "Always validate before executing destructive operations",
    "Maintain technical precision over conversational style",
    "Prefer explicit error messages over silent failures"
  ],
  "refresh_interval": 8,
  "tone_protocol": "Echo"
}
```

---

*Updated: 2026-01-17 | Based on MCP Specification Analysis*
