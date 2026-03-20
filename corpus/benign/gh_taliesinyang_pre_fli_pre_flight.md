---
name: pre-flight
description: >
  Run before starting any new feature, requirement, or non-trivial task to assess readiness.
  Performs 4 checks: (1) inventory existing skills/tools/MCP servers for relevance,
  (2) search community for available skills and plugins, (3) search for open-source reference
  projects, (4) evaluate all findings with security-first criteria (stars, maintenance, safety).
  Use when: user says "pre-flight", "capability check", "readiness check", starts a new feature,
  or before invoking superpowers:brainstorming on non-trivial work. Complements Superpowers —
  runs BEFORE brainstorming to ensure the right tools are in place.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: TaliesinYang/pre-flight-skill
# corpus-url: https://github.com/TaliesinYang/pre-flight-skill/blob/572df4b6fa4e73a6e83cbb8bf310337e3f66fdcc/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Pre-Flight: Capability & Community Assessment

Assess readiness before starting work. Output a structured report, then hand off to the next
workflow step (typically `superpowers:brainstorming`).

## Workflow

```
/pre-flight $ARGUMENTS
    │
    ├─ Step 1: Local Inventory
    ├─ Step 2: Community Search
    ├─ Step 3: Gap Analysis & Evaluation
    └─ Step 4: Recommendation
```

## Step 1: Local Inventory

Scan what is already available in the current environment.

### 1a. Skills

```bash
find ~/.claude/skills -name "SKILL.md" -maxdepth 2 2>/dev/null
find .claude/skills -name "SKILL.md" -maxdepth 2 2>/dev/null
```

For each skill found, read its frontmatter `name` and `description`. Determine relevance
to `$ARGUMENTS` by semantic matching. Build a table:

| Skill | Relevance | Notes |
|-------|-----------|-------|
| ... | ✅ High / ⚠️ Partial / ➖ None | ... |

### 1b. Plugins

```bash
cat ~/.claude/plugins/installed_plugins.json 2>/dev/null
```

Check each plugin's skill list for relevant capabilities.

### 1c. MCP Servers & Tools

Review currently available MCP tools. Flag which ones are relevant to the task
(e.g., browser automation, database, search, file processing).

### 1d. Codebase Context

If inside a project directory:

```bash
grep -r "keyword" --include="*.{ts,js,py,go,rs}" -l . 2>/dev/null | head -20
```

Look for existing code, configs, or dependencies that relate to `$ARGUMENTS`.

## Step 2: Community Search

Search for skills, plugins, and reference projects the community has built.
Use **any available search tool** — do not depend on a specific one.

### Search strategy (pick the first available)

1. **Web search tool available** (Perplexity, WebSearch, web_search_prime, etc.)
   → Execute all searches below
2. **No web search available**
   → Use bundled offline index at `references/skill-registry.md`
   → Tell the user: "Install a web search MCP for richer community results"

### Searches to execute

Run these in parallel when possible:

**Skills & Plugins:**
- `claude code skill [task keywords]`
- `claude code plugin [task keywords]`
- Search known registries: skillsmp.com, skillhub.club, claudeskills.info

**Open-source projects:**
- `[task keywords] open source [language/framework if known]`
- `github [task keywords] [language/framework]`

**Best practices:**
- `[task keywords] best practices implementation guide`

### Marketplace scan

Scan local marketplace caches for uninstalled but available plugins:

```bash
find ~/.claude/plugins/cache -name "marketplace.json" 2>/dev/null
```

Read each marketplace.json and check for relevant uninstalled plugins.

## Step 3: Gap Analysis & Evaluation

### 3a. Categorize findings

| Category | Icon | Meaning |
|----------|------|---------|
| Ready | ✅ | Already installed and directly usable |
| Available | 📦 | Exists in community, can be installed |
| Reference | 🔗 | Open-source project to learn from |
| Missing | ❌ | No existing solution found, must build |

### 3b. Security-First Evaluation

**Every community resource MUST be evaluated before recommending.**
Read `references/evaluation-criteria.md` for the full rubric.

**Hard reject (any one = do not recommend):**
- Obfuscated code or suspicious tool calls
- Requests credentials/tokens beyond task scope
- Overly broad `allowed-tools` (e.g., unrestricted Bash)
- Anonymous throwaway account with no history

**Trust tiers:**

| Tier | Label | Criteria |
|------|-------|----------|
| T1 | 🟢 Trusted | Official Anthropic, or 1k+ stars + known org + active |
| T2 | 🟡 Verified | 100+ stars + identifiable author + no security flags |
| T3 | 🟠 Community | <100 stars but readable code + no security flags |
| T4 | 🔴 Unverified | Anonymous, no stars, or any security concern |

**Rules:** T1/T2 → safe to recommend. T3 → recommend with "review before installing".
T4 → do NOT recommend, mention with warning only if nothing better exists.

## Step 4: Recommendation

Output this report:

```markdown
## Pre-Flight Report: [task description]

### Environment Readiness
| Area | Status | Details |
|------|--------|---------|
| Skills | ✅/⚠️/❌ | [relevant skills found] |
| MCP Tools | ✅/⚠️/❌ | [relevant tools available] |
| Codebase | ✅/⚠️/❌ | [existing code/patterns] |

### Community Resources Found
| Resource | Type | Trust | Stars | Notes |
|----------|------|-------|-------|-------|
| [name] | Skill/Plugin/Repo | 🟢/🟡/🟠/🔴 | N | [summary] |

### Recommended Path
[One of:]
- **Ready to go** → Proceed to `superpowers:brainstorming`
- **Install first** → `[install commands]`, then brainstorm
- **Build new skill** → Use `skill-creator`, then brainstorm
- **Reference available** → Study [project], then brainstorm

### Gaps & Risks
- [Capability gaps that remain]
- [Security concerns noted]
```

After presenting the report, ask:
1. "Proceed to `superpowers:brainstorming` with this context?"
2. "Install any recommended community resources first?"
3. "Create a new skill for the missing capability?"

## Important Notes

- This skill is **read-only** — never installs, modifies, or executes community code
- Installation decisions are always left to the user
- When in doubt about security, err on the side of caution (flag 🔴)
- Keep the report concise — actionable info, not exhaustive lists