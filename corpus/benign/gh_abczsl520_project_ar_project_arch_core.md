---
name: project-arch-core
description: Language-agnostic project architecture principles for AI-assisted development. Use when creating or reviewing language-specific arch skills, or when evaluating whether a codebase needs restructuring. Not a substitute for language-specific skills — provides the shared foundation they build on.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: abczsl520/project-arch-core
# corpus-url: https://github.com/abczsl520/project-arch-core/blob/86f910a878e452343583cf894bfd6dbcc931dbc7/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Project Architecture Core — AI-Friendly Development

Language-agnostic architecture principles that keep codebases small enough for AI agents to read and edit efficiently.

## When to Apply

✅ Apply when:
- Building a web service, API, or full-stack app with multiple files
- Codebase has grown past ~500 lines total
- AI agent is hitting context limits or making edit errors on large files
- Creating a new `<lang>-project-arch` skill

❌ Don't apply when:
- One-off scripts or utilities under ~200 lines — just keep it in one file
- Prototyping / POC phase — premature splitting slows you down, refactor later
- Framework has strong conventions (Next.js app router, Django apps, Rails) — follow the framework first, apply these principles where the framework is silent
- Pure libraries with no runtime (config externalization / admin dashboard don't apply)

## Core Principles

### 1. File Size Limits
- **Source file ≤ 400 lines** — beyond this, AI context usage spikes and edit accuracy drops
- **Entry point ≤ 100 lines** — only wiring/mounting, zero business logic
- **HTML/template files ≤ 200 lines** — skeleton only, logic in separate files

### 2. Entry Point = Wiring Only
The main entry file does exactly three things:
1. Initialize dependencies (DB, middleware, plugins)
2. Mount modules / register handlers
3. Start the process

No business logic, no handler implementations, no data processing.

### 3. Config Externalization
- All tunable values in a config file (`config.json`, `.env`, `config.yaml`, etc.)
- Loaded at runtime, never hardcoded
- Editable without code changes or restarts (hot-reload preferred for web services)
- Secrets stripped before exposing to frontend/clients

### 4. Layered Separation

Separate **interface** (how users/systems talk to you) from **logic** (what you do) from **data** (where you store it):

```
Entry (wiring) → Interface → Logic → Data
```

Common mappings:

| Project Type | Interface | Logic | Data |
|-------------|-----------|-------|------|
| Web service | Routes / Handlers | Services | DB / API clients |
| CLI tool | Commands / Args parser | Services | File I/O / DB |
| Worker / Queue | Consumers / Listeners | Services | DB / Message queue |
| Desktop app | Views / Controllers | Services | Local storage / API |

### 5. Observability & Admin

For **web services and long-running processes**:
- Auth-protected admin interface for config editing + hot-reload
- Runtime stats (uptime, memory, request counts)
- Key business metrics
- Operation log

For **CLIs and libraries**: not required. Use logging and `--verbose` flags instead.

### 6. Frontend Splitting (if applicable)
- HTML = structure only (no inline JS/CSS beyond minimal bootstrap)
- CSS in separate files
- JS split by responsibility (each ≤ 400 lines)

## Splitting Decision Guide

See [references/splitting-guide.md](references/splitting-guide.md) for a language-agnostic decision flow:
- When to split vs. when to leave alone
- How to identify split boundaries
- Post-split verification checklist

## Why This Matters for AI

| Scenario | Tokens per read | Context usage (200K) |
|----------|----------------|---------------------|
| 3000-line monolith | ~40K | 20% |
| 200-line module | ~2.7K | 1.3% |

Splitting files → **10-15 productive AI rounds** vs 3-5 with monoliths. **70-93% token savings** per file read.

## Language-Specific Skills

This skill provides the universal foundation. For concrete directory structures, code patterns, and framework-specific rules, use the appropriate language skill:

| Language/Framework | Skill | Status |
|-------------------|-------|--------|
| Node.js (Express) | [nodejs-project-arch](https://github.com/abczsl520/nodejs-project-arch) | ✅ Available |
| React / Vite | [react-project-arch](https://github.com/abczsl520/react-project-arch) | ✅ Available |
| Python (FastAPI/Flask) | `python-project-arch` | 🔲 Community welcome |
| Go | `go-project-arch` | 🔲 Community welcome |

## Creating a New Language Skill

If you're building a `<lang>-project-arch` skill, follow these core principles and add:

1. **Concrete directory structure** — not abstract, copy-pasteable
2. **Entry point pattern** — actual code showing wiring-only entry
3. **Config pattern** — language-idiomatic config loading + hot-reload
4. **Splitting rules table** — "this monolith → these modules" with max lines
5. **Project type references** — separate files for different project types

Keep the same naming convention: `<lang>-project-arch` with `references/` subdirectory.

### Quality Checklist for Language Skills

Before publishing, verify your skill passes these:

- [ ] Can a developer copy the directory structure and start coding immediately?
- [ ] Entry point example is real, runnable code (not pseudocode)?
- [ ] Config pattern uses the language's idiomatic approach (not a generic JSON example)?
- [ ] Splitting rules table covers the 2-3 most common monolith patterns in that ecosystem?
- [ ] At least 2 project type references (e.g., web app + CLI, or API + worker)?
- [ ] Tested on a real project — not just theoretical?