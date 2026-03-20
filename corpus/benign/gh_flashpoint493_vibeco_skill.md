---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: flashpoint493/VibeCollab
# corpus-url: https://github.com/flashpoint493/VibeCollab/blob/3c5a847a3d4b6792313ba82f3f597caadb4cc44c/skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# VibeCollab — Setup Instructions for AI Assistants

You are helping a user set up VibeCollab in their project.
Execute the following steps in order. Stop and report if any step fails.

## Prerequisites

VibeCollab requires **Python 3.10 or higher**. Recommended version: **Python 3.12** (best balance of performance and compatibility).

Before installing, check the user's Python version:

```bash
python --version
```

If Python is not installed or is below 3.10, guide the user to install Python 3.12+ from https://www.python.org/downloads/

**Virtual environment** (strongly recommended): To keep the user's system clean and avoid dependency conflicts, always create a virtual environment before installing:

```bash
# Create a virtual environment (run once)
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

> If the project already has a virtual environment (`.venv/`, `venv/`, or similar), activate it instead of creating a new one.

## Step 1: Install

```bash
pip install vibe-collab
```

## Step 2: Initialize

Run in the user's project root directory:

```bash
vibecollab init -n "<PROJECT_NAME>" -d <DOMAIN>
```

- `<PROJECT_NAME>`: Ask the user for their project name
- `<DOMAIN>`: Ask the user to choose: `web` / `mobile` / `game` / `data` / `generic`

This creates `project.yaml`, `CONTRIBUTING_AI.md`, and `docs/` directory with protocol documents.

### For Existing Projects

If the project already has code (not an empty directory), do the following **after** `vibecollab init`:

1. **Backfill CONTEXT.md**: Review recent git commits and summarize the project's current state, active tasks, and recent decisions into `docs/CONTEXT.md`

2. **Backfill DECISIONS.md**: Look for important architectural choices in git history and record them in `docs/DECISIONS.md` with proper decision levels (S/A/B/C)

3. **Create ROADMAP.md**: If the project has future plans, create `docs/ROADMAP.md` following the milestone format (see ROADMAP Format section below)

4. **Capture Insights**: If reusable development experiences are found (debugging tricks, architectural patterns, workflow optimizations), capture them using `insight_add` MCP tool

### Quick Start After Init

After initialization completes, tell the user:

> VibeCollab is ready! Here's how to start:
> 
> 1. **Describe your current task** — I'll help you work on it while following the collaboration protocol
> 2. **Or say "onboard"** — I'll read the project context and suggest what to do next
> 3. **Or show me a file/feature** — I'll understand it within the project's structured context

This gives users an immediate path forward instead of leaving them wondering "what now?"

## Step 3: Connect MCP to IDE

Ask the user which IDE they use, then run:

```bash
vibecollab mcp inject --ide cursor   # or: cline / codebuddy / all
```

This injects VibeCollab MCP Server config into the IDE config file.
Use `--ide all` to inject config for all supported IDEs at once.

**OpenClaw / other MCP agents**: VibeCollab is a standard MCP Server. Any MCP-compatible agent can connect directly:

```bash
openclaw mcp add --transport stdio vibecollab vibecollab mcp serve
```

## Step 4: Verify

```bash
vibecollab check
```

Should return zero errors. Warnings about document staleness are normal for new projects. Insight consistency checks are included by default (use `--no-insights` to skip).

## Setup Complete

VibeCollab is ready. You now have MCP tools available in your IDE:

| Tool | When to use |
|------|-------------|
| `onboard` | **Start of every conversation** — get project context |
| `check` | **End of every conversation** — verify protocol compliance |
| `next_step` | When unsure what to do next |
| `insight_search` | Search past development experience |
| `insight_add` | Save a reusable insight |
| `insight_suggest` | Get signal-driven insight recommendations |
| `insight_graph` | View insight relationship graph |
| `insight_export` | Export insights in YAML format |
| `search_docs` | Semantic search across project documents |
| `task_list` | List current tasks |
| `task_create` | Create a new task (auto-links insights) |
| `task_transition` | Move task status (TODO → IN_PROGRESS → REVIEW → DONE) |
| `developer_context` | Get a specific role's context |
| `project_prompt` | Generate full context prompt |
| `roadmap_status` | View milestone progress |
| `roadmap_sync` | Sync ROADMAP.md <-> tasks.json |
| `session_save` | **End of conversation** — save session summary |

## Execution Plan — YAML-Driven Workflow Automation

VibeCollab includes a plan runner that orchestrates multi-round workflows with two modes:

| Mode | Command | Host Adapter | Description |
|------|---------|-------------|-------------|
| **File Exchange** | `vibecollab plan run --host file_exchange` | `file_exchange` | File polling with IDE AI (requires IDE rules setup) |
| **Subprocess** | `vibecollab plan run --host subprocess` | `subprocess` | Drives CLI tools (aider, claude) via stdin/stdout |
| **Auto (Keyboard)** | `vibecollab plan run --host auto:cursor` | `auto` | Keyboard simulation for hands-free IDE automation |

All modes use `vibecollab plan run` as the **unified execution engine**.

### Mode 1: File Exchange

Use when you want to stay in the IDE conversation and have AI execute plan steps.

```bash
vibecollab plan run plans/dev.yaml -v
```

**How it works**: vibecollab writes instructions to a file, IDE AI monitors and executes, writes response back.

```
vibecollab plan run              IDE AI (Cursor/Cline)
       │                                │
       │  write instruction.md          │
       ├──────────────────────────────->│
       │                                │ execute with tool-use
       │  poll response.md              │
       │<───────────────────────────────┤ write response
       │                                │
       │  check goal, next round        │
       └────────────────────────────────┘
```

**Limitation**: Requires active IDE conversation. If conversation ends, loop stops.

**IDE Setup** — Add to Cursor Rules or Cline Custom Instructions:

```
Monitor .vibecollab/loop/instruction.md for new instructions.
When you see <!-- VIBECOLLAB_INSTRUCTION -->, execute the task using your tools.
After completion, write results to .vibecollab/loop/response.md and include
<!-- VIBECOLLAB_RESPONSE_READY --> at the end to signal completion.
```

### Mode 2: Auto (Keyboard Simulation)

Use when you want hands-free automation that can run for hours. The `auto` host adapter drives IDE AI through keyboard simulation (pyautogui).

**Step 1**: Create a launcher script
```bash
vibecollab auto init plans/dev.yaml --ide cursor
```
This creates `auto_dev.bat` that runs `vibecollab plan run ... --host auto:cursor`.

**Step 2**: Double-click the .bat file to start
- A cmd window opens
- Auto adapter finds IDE window, simulates Ctrl+L → paste → Enter
- PlanRunner polls response.md for completion
- Loop continues until goal met or max rounds

**How it works**:

```
vibecollab plan run --host auto:cursor    IDE Window (Cursor/Cline)
       │                                         │
       │  PlanRunner._exec_loop()                │
       │  → AutoAdapter.send(instruction)        │
       │    → pyautogui: Ctrl+L                  │
       │    → paste instruction via clipboard     │
       │    → Enter                               │
       ├──────────────────────────────────────->│
       │                                         │ AI executes task
       │    <- poll response.md                   │
       │<────────────────────────────────────────┤ write response
       │                                         │
       │  check_goal() → next round              │
       └─────────────────────────────────────────┘
```

**Requirements**: `pip install vibe-collab[auto]` (includes pyautogui, pygetwindow, pyperclip)

**Commands**:
```bash
vibecollab auto list                     # Show preset plans
vibecollab auto init --preset dev-loop   # Copy preset & create .bat launcher
vibecollab auto init plans/custom.yaml   # Create .bat from local plan
vibecollab auto status                   # Check status
vibecollab auto stop                     # Stop running process

# Direct CLI usage (equivalent to double-clicking .bat):
vibecollab plan run plans/dev.yaml --host auto:cursor -v
```

### Preset Plans

VibeCollab includes ready-to-use automation plans:

| Plan | Purpose | Rounds |
|------|---------|--------|
| `dev-loop` | **Full development cycle** — onboard, develop, insight, check | 50 |
| `feature-dev` | **Feature implementation** — follow ROADMAP tasks | 30 |
| `quick-fix` | **Bug fixes** — rapid check-fix-commit loop | 10 |
| `doc-sync` | **Documentation** — sync CONTEXT/CHANGELOG/ROADMAP | 5 |
| `insight-harvest` | **Knowledge capture** — extract insights from work | 10 |

**Quick Start**:
```bash
# List available presets
vibecollab auto list

# Use a preset plan (copies to plans/ and creates .bat)
vibecollab auto init --preset dev-loop

# Double-click the generated .bat file to start!
```

### Example Plan

```yaml
name: "Iterate project"
host: file_exchange
steps:
  - action: loop
    max_rounds: 20
    goal: "All vibecollab checks pass"
    state_command: "vibecollab next --json"
    prompt_template: |
      ## Round {{round}}/{{max_rounds}}
      
      Current state:
      {{state}}
      
      Please complete the next recommended task using your tools.
      Run `vibecollab check` when done.
    check_command: "vibecollab check"
    check_expect:
      exit_code: 0
```

### CLI Commands

```bash
vibecollab plan run <plan.yaml>                     # Execute (default: file_exchange)
vibecollab plan run <plan.yaml> -v                  # Verbose logging
vibecollab plan run <plan.yaml> --host auto:cursor  # Auto adapter (keyboard simulation)
vibecollab plan run <plan.yaml> --dry-run           # Preview only
vibecollab plan validate <plan.yaml>                # Validate syntax
```

### Plan Step Actions

| Action | Purpose | Example |
|--------|---------|---------|
| `cli` | Run shell command | `command: "vibecollab check"` |
| `assert` | Check file/content | `file: "README.md"`, `contains: "test"` |
| `wait` | Delay | `seconds: 1` |
| `prompt` | Send single message to host | `message: "Create a task"` |
| `loop` | Multi-round iteration | `max_rounds: 20`, `state_command: "..."` |

### Loop Configuration

| Field | Description |
|-------|-------------|
| `max_rounds` | Maximum iteration rounds |
| `goal` | Human-readable goal description |
| `state_command` | Command to gather current project state |
| `prompt_template` | Template with `{{state}}`, `{{round}}`, `{{max_rounds}}`, `{{goal}}` |
| `check_command` | Command to test if goal is met |
| `check_expect` | Expected `exit_code` and/or `stdout_contains` |

### Host Adapters

| Host | Config | Use Case |
|------|--------|----------|
| `file_exchange` | `host: file_exchange` | **Cursor/Cline/CodeBuddy** — drives IDE AI via file polling |
| `subprocess` | `host: {type: subprocess, command: "aider"}` | CLI tools (aider, claude, etc.) with stdin/stdout |
| `auto` | `host: auto:cursor` or `--host auto:cursor` | **Cursor/Cline/CodeBuddy** — drives IDE AI via keyboard simulation (pyautogui) |

> The `auto` adapter supports IDE sub-options via colon syntax: `auto:cursor`, `auto:cline`, `auto:codebuddy`. Default: `auto:cursor`.

### Auto Adapter Options

```yaml
host:
  type: auto:cursor              # or auto:cline, auto:codebuddy
  response_timeout: 600          # wait up to 10 minutes per round (default: 600)
  poll_interval: 5               # check every 5 seconds (default: 5)
```

Or via CLI flag:
```bash
vibecollab plan run plans/dev.yaml --host auto:cursor -v
```

### File Exchange Options

```yaml
host:
  type: file_exchange
  timeout: 600           # wait up to 10 minutes per round (default: 300)
  poll_interval: 3       # check every 3 seconds (default: 2)
  exchange_dir: ".vibecollab/loop"  # directory for exchange files
```

### Variable Passing

Steps can store output and pass to later steps:

```yaml
steps:
  - action: cli
    command: "vibecollab health --json"
    store_as: health_data
  - action: prompt
    message: "Health report: {{health_data}}"
```

## ROADMAP Format

If the project has a `docs/ROADMAP.md`, milestones must use this format for `roadmap_status` / `roadmap_sync` to work:

```markdown
### v0.1.0 - Milestone title

- [ ] Feature description (TASK-DEV-001)
- [x] Completed feature TASK-DEV-002
```

- Only `###` (H3) headers are recognized — `####` or `##` will not be parsed
- Version must start with `v` (semantic versioning)
- Task IDs follow `TASK-{ROLE}-{SEQ}` format (e.g., `TASK-DEV-001`)

## Daily Workflow

```
Conversation start → call onboard
                      ↓
                 Work on tasks
                      ↓
    Reusable experience? → call insight_add (capture knowledge)
                      ↓
    Need past experience? → call insight_search
                      ↓
    Important decisions → record in docs/DECISIONS.md
                      ↓
    Conversation end → update docs/CONTEXT.md
                     → update docs/CHANGELOG.md
                     → call check (includes Insight consistency by default)
                     → call session_save
                     → git commit
```

> **Key**: Insight is enabled by default in `check`. Every conversation should consider capturing reusable knowledge via `insight_add`.