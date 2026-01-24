---
date: 2026-01-17
type: research-note
tags: [git-hooks, automation, productivity, developer-experience]
status: recommendations-ready
---

# Optimal Git Hooks for Personal AI OS

## Research Summary (2025 Best Practices)

Git hooks automate tasks and enforce quality at commit time. Key principles:
- **Keep hooks fast** (don't block developer flow)
- **Version control hooks** (store in repo, not .git/hooks)
- **Clear error messages** (help devs fix issues)
- **Shift-left testing** (catch issues early)

---

## Recommended Hooks for Our Context

### 1. `pre-commit` — Quality Gate
**Purpose:** Prevent committing bad code or secrets

```bash
#!/bin/bash
# Pre-commit hook

# Check for secrets
python .agent/core/secrets_checker.py --check-staged
if [ $? -ne 0 ]; then
    echo "❌ Secrets detected. Remove before committing."
    exit 1
fi

# Quick lint check (optional)
# python -m py_compile $(git diff --cached --name-only | grep '.py$')
```

**Benefit:** Catches API keys before they hit git history.

---

### 2. `commit-msg` — Commit Message Validation
**Purpose:** Enforce consistent commit messages

```bash
#!/bin/bash
# Enforce conventional commits format

COMMIT_MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|test|chore|build)(\(.+\))?: .{1,72}$"

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
    echo "❌ Commit message must follow format:"
    echo "   type(scope): description"
    echo "   Example: feat(linear): add update_state method"
    exit 1
fi
```

**Benefit:** Clean git history, easier changelog generation.

---

### 3. `post-commit` — Session Tracking ✅ Already Implemented
**Purpose:** Suggest session wrap after significant work

We already have this! Suggests wrap after 5+ file commits.

---

### 4. `pre-push` — Safety Net (Recommended)
**Purpose:** Final checks before pushing to remote

```bash
#!/bin/bash
# Pre-push hook

# Run quick tests
python -m pytest tests/ -q --tb=no 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Tests failing. Fix before pushing."
    exit 1
fi

# Check for WIP commits (optional)
if git log @{u}.. --oneline | grep -qiE "wip|fixup|squash"; then
    echo "⚠️  WIP commits detected. Squash before pushing?"
    read -p "Push anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

**Benefit:** Prevents broken code reaching the repo.

---

### 5. `prepare-commit-msg` — Auto-fill Context
**Purpose:** Add Linear ticket ID to commit messages

```bash
#!/bin/bash
# Auto-add ticket ID from branch name

BRANCH=$(git symbolic-ref --short HEAD)
TICKET=$(echo "$BRANCH" | grep -oE "LIN-[0-9]+")

if [ -n "$TICKET" ]; then
    # Prepend ticket to commit message
    sed -i.bak "1s/^/[$TICKET] /" "$1"
fi
```

**Benefit:** Links commits to Linear tickets automatically.

---

## Priority Order for Implementation

| Priority | Hook | Effort | Value |
|----------|------|--------|-------|
| 1 | pre-commit (secrets) | Low | High |
| 2 | commit-msg (format) | Low | Medium |
| 3 | pre-push (tests) | Medium | High |
| 4 | prepare-commit-msg | Low | Medium |

---

## Storage Location

Hooks stored in: `.agent/hooks/`

To install:
```powershell
Copy-Item ".agent\hooks\*" ".git\hooks\" -Force
```

Or use git config:
```powershell
git config core.hooksPath .agent/hooks
```

---

## What We Have vs What We Need

| Hook | Have | Need |
|------|------|------|
| post-commit | ✅ | - |
| pre-commit | ❌ | Secrets check |
| commit-msg | ❌ | Message format |
| pre-push | ❌ | Test runner |

---

*Research completed: 2026-01-17*
