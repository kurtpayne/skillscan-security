---
name: create-skill
description: Guide for creating a new Claude Code skill with the correct directory structure, front matter, and conventions. Use when creating or scaffolding a new skill.
argument-hint: <skill-name> [--global]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: kcalhoon/kcalhoon.github.io
# corpus-url: https://github.com/kcalhoon/kcalhoon.github.io/blob/9628420f539c0cea08a778410486a3ca4147fa90/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

## Usage

Invoked as: `/create-skill <skill-name> [--global]`

The skill name is: $ARGUMENTS

## Instructions

When creating a new skill, follow this structure precisely.

### Step 1 — Determine scope

- **Project skill** (default): `.claude/skills/<skill-name>/SKILL.md`
- **Global skill** (if `--global` is passed): `~/.claude/skills/<skill-name>/SKILL.md`

Global skills apply to all projects. Project skills apply only to the current repo.

### Step 2 — Create the directory and file

```
<scope-path>/skills/<skill-name>/
└── SKILL.md        # Required
```

The directory name must be lowercase, using only letters, numbers, and hyphens. The directory name becomes the `/slash-command` name.

Only `SKILL.md` is required. Optional supporting files can be added alongside it:

```
<scope-path>/skills/<skill-name>/
├── SKILL.md           # Required — main instructions
├── template.md        # Optional — template for Claude to fill in
├── examples/          # Optional — example outputs
└── scripts/           # Optional — executable scripts
```

### Step 3 — Write the SKILL.md with correct front matter

The file MUST start with YAML front matter between `---` markers:

```yaml
---
name: my-skill
description: What this skill does and when to use it.
---
```

#### Required and recommended fields

| Field | Required? | Description |
|-------|-----------|-------------|
| `name` | No (defaults to directory name) | Lowercase, numbers, hyphens only. Max 64 chars. |
| `description` | **Recommended** | What the skill does and when to invoke it. Claude uses this to decide when to auto-load the skill. |

#### Optional fields

| Field | Description |
|-------|-------------|
| `argument-hint` | Hint shown during autocomplete, e.g. `[file-path]` or `[issue-number]` |
| `disable-model-invocation` | Set to `true` to prevent Claude from auto-invoking (user only) |
| `user-invocable` | Set to `false` to hide from `/` menu (Claude-only background knowledge) |
| `allowed-tools` | Tools Claude can use without asking, e.g. `Read, Grep, Bash(python *)` |
| `model` | Specific model to use when this skill is active |
| `context` | Set to `fork` to run in an isolated subagent context |
| `agent` | Subagent type when `context: fork` is set (e.g. `Explore`, `Plan`) |

### Step 4 — Write the skill body

After the front matter, write the skill instructions in markdown. Follow these conventions:

1. **Start with a `## Usage` section** showing invocation syntax and referencing `$ARGUMENTS`
2. **Use numbered `### Step N — Title` sections** for multi-step workflows
3. **Keep SKILL.md under 500 lines** — move detailed reference material to supporting files
4. **Reference supporting files** so Claude knows when to load them:
   ```markdown
   For API details, see [reference.md](reference.md)
   ```

#### Available substitution variables

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed to the skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by index (0-based) |
| `${CLAUDE_SESSION_ID}` | Current session ID |

#### Dynamic context injection

Use `!`command`` to run shell commands whose output is injected before Claude sees the skill:

```markdown
Current branch: !`git branch --show-current`
```

### Step 5 — Confirm the result

After creating the skill, report:
- The full path to the created `SKILL.md`
- The invocation command (e.g. `/my-skill`)
- Whether it is global or project-scoped

### Quick reference — Minimal example

```yaml
---
name: greet
description: Greet the user warmly. Use when the user says hello.
---

## Usage

Invoked as: `/greet $ARGUMENTS`

Say hello to the user by name if provided, otherwise just say hello.
```