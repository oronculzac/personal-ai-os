---
type: implementation_plan
source: C:\Users\Oron Culzac\.gemini\antigravity\brain\319157e1-c402-40b6-9daa-472a9c311ede\implementation_plan.md
synced: 2026-01-17T18:57:13.869746
topic: skills cowork personas research
---

# Skills, Cowork & Personas Research Plan

Research to validate and improve Antigravity's skill/persona implementation against industry standards.

**Decisions (Optimal Route):**
- ✅ Focus: Skill alignment first (foundation before personas)
- ✅ Approach: MCP-aligned patterns (not full MCP server compatibility)
- ✅ Priority skills: session_wrapper, artifact_sync, linear_manager, obsidian_linear_sync

---

## Phase 0: Antigravity Current State ✅ COMPLETE

### Skills Architecture
- **16 skills** with SKILL.md frontmatter pattern
- **Structure**: `name`, `description`, `version`, `triggers`, `capabilities`, `dependencies`, `auto_load`
- **Scripts**: Python files in `scripts/` subfolder
- **Discovery**: `skill_discovery.py` scans and registers skills

### Personas Architecture  
- **5 personas**: data_engineer, devops_engineer, data_analyst, content_writer, seo_specialist
- **Format**: JSON with `system_prompt`, `allowed_skills`, `behavioral_traits`, `expertise`
- **Manager**: `persona_manager.py` activates/deactivates personas
- **Mechanism**: Restricts skill access + injects system prompt

### Key Observations
| Component | Antigravity | MCP Standard |
|-----------|-------------|--------------|
| Skill definition | YAML frontmatter | JSON Schema with inputSchema |
| Tool invocation | Direct Python execution | JSON-RPC 2.0 protocol |
| Persona structure | JSON with system_prompt | MCP Prompts primitive |
| Drift prevention | None explicit | Axioms, Echo protocols |

---

## Phase 1: Framework Analysis

### 1.1 MCP Specification Review
- [ ] Tool schema requirements (name, description, inputSchema)
- [ ] JSON-RPC 2.0 communication patterns
- [ ] Resource vs Tool vs Prompt primitives
- [ ] Best practices: docstring quality, ACLs, schema precision

### 1.2 Claude Cowork Architecture
- [ ] Agentic loop pattern (Plan → Act → Observe → Correct)
- [ ] Sandboxing/virtualization approach
- [ ] Folder permission model
- [ ] Token economics considerations

### 1.3 Persona Design Patterns
- [ ] MCP Prompts as technical objects
- [ ] Axioms for drift prevention
- [ ] Archetypes: Executor, Coach, Critic, Creative
- [ ] Finite-state tone protocols

---

## Phase 2: Gap Analysis

### 2.1 Skills Comparison
Compare each skill against MCP reference implementations:
- Filesystem, Memory, Git, Sequential Thinking, Fetch

| Skill | Schema Precision | Docstring Quality | Error Handling | MCP Alignment |
|-------|-----------------|-------------------|----------------|---------------|
| artifact_sync | TBD | TBD | TBD | TBD |
| session_wrapper | TBD | TBD | TBD | TBD |
| ... | | | | |

### 2.2 Persona Comparison
- [ ] System prompts vs MCP Prompt structure
- [ ] Drift prevention mechanisms
- [ ] Axiom implementation status
- [ ] Behavioral consistency enforcement

---

## Phase 3: Recommendations

### 3.1 Skill Enhancements
- Add JSON Schema for tool inputs
- Improve docstrings for LLM tool selection
- Implement ACLs for sensitive operations
- Add error handling patterns

### 3.2 Persona Enhancements
- Add axioms to prevent drift
- Implement periodic context refresh
- Create archetype-based templates
- Add few-shot examples to system prompts

### 3.3 Infrastructure
- Consider MCP server wrapper for skills
- Evaluate JSON-RPC bridge possibility
- Document skill creation best practices

---

## Deliverables

1. **Comparison matrix** - Skills vs MCP standards
2. **Gap report** - Identified improvements
3. **Updated skill template** - MCP-aligned structure
4. **Persona enhancement guide** - Drift prevention patterns
5. **Linear tickets** - For implementation work

---

## Questions for User

1. **Scope priority**: Should I focus first on skill alignment or persona drift prevention?
2. **MCP integration**: Do you want actual MCP server compatibility, or just aligned patterns?
3. **Which skills are highest priority** for the detailed audit?
