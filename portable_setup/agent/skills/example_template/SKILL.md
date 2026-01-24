---
name: Example Skill Template
description: Template for creating new skills
version: 1.0.0
triggers:
  - example
  - template skill
dependencies: []
capabilities:
  - example_capability
auto_load: false
---

# Example Skill Template

## Purpose

This is a template for creating new skills. Copy this structure to create your own custom skills.

## Instructions

When the user requests functionality related to this skill's triggers, follow these steps:

1. **Identify the Request**: Recognize when the user's intent matches this skill's capabilities
2. **Load Resources**: Access any necessary files from the `resources/` directory
3. **Execute Scripts**: If needed, run scripts from the `scripts/` directory using the run_command tool
4. **Generate Output**: Create the requested deliverable
5. **Report Results**: Inform the user of completion and any relevant details

## Available Resources

- `resources/template.txt`: Example template file
- `scripts/example_script.py`: Example Python script (if applicable)

## Usage Examples

**Example 1**: Basic usage
```
User: "Use the example skill"
Agent: Loads this skill and follows instructions
```

**Example 2**: With parameters
```
User: "Run example skill with custom parameter"
Agent: Processes with specified parameters
```

## Skill Composition

This skill can be combined with:
- `other_skill_name`: For extended functionality
- `another_skill`: For complementary features

## Notes

- This skill requires no external dependencies
- All operations are safe and non-destructive
- Can be used as reference when creating new skills

## Creating Your Own Skill

1. Copy this folder structure to `.agent/skills/your-skill-name/`
2. Update the frontmatter in SKILL.md with:
   - Unique name and description
   - Relevant trigger phrases
   - Required dependencies
   - Capabilities list
3. Add your instructions to the SKILL.md body
4. Create helpful scripts in `scripts/`
5. Add resources/templates in `resources/`
6. Run skill discovery to register
