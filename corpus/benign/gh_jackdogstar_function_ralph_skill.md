---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: jackdogstar/functional-probe-ralph-loop
# corpus-url: https://github.com/jackdogstar/functional-probe-ralph-loop/blob/12bef904e2015d3eb91bfe11c9607a7232eafb9d/ralph-skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Ralph Wiggums Loop — Project Generation Skill

## Purpose

This skill instructs Claude on how to generate a complete, runnable **Ralph Wiggums Loop** project from any functional specification. A Ralph Loop is an autonomous AI-driven development system that uses Claude to iteratively plan and build a software project, story by story, with full validation at every step.

---

## What You Will Produce

Given a functional specification, generate the following directory structure:

```
<project-name>-ralph/
├── loop.sh                          # Main autonomous loop script
├── prd.json                         # Product Requirements Document (all user stories)
├── AGENTS.md                        # Agent operations manual for Claude
├── PROMPT_plan.md                   # Planning mode prompt
├── PROMPT_build.md                  # Building mode prompt
├── <functional-spec-filename>.md    # Copy of the provided functional specification
└── specs/                           # Numbered spec files, one per domain area
    ├── 01-<first-area>.md
    ├── 02-<second-area>.md
    └── ...
```

---

## Step-by-Step Generation Process

### Step 1: Analyze the Functional Specification

Read the entire functional specification. Identify:

1. **Technology stack** — languages, frameworks, databases, external services
2. **Major subsystems** — backend, frontend, workers, infrastructure, etc.
3. **Domain areas** — authentication, data models, API endpoints, UI screens, integrations, testing, security, performance, documentation
4. **Entity models** — all data structures and their relationships
5. **Business rules** — validation, state machines, calculations, constraints
6. **External dependencies** — third-party APIs, databases, message queues, auth providers
7. **Build and test commands** — how to compile, run tests, lint, and start each subsystem

### Step 2: Decompose Into Spec Files

Break the functional specification into numbered spec files under `specs/`. Each spec file covers one coherent domain area. Follow this ordering pattern:

| Order | Area | Description |
|-------|------|-------------|
| 01 | Project setup | Scaffolding, folder structure, dependencies, config files |
| 02 | Data layer setup | Database/ORM config, connection management, migrations |
| 03 | Entity/data models | All model definitions, schemas, relationships |
| 04 | Authentication | Auth provider config, middleware, token handling |
| 05 | Backend services | Business logic layer — one file even if many services |
| 06 | Backend controllers/routes | API endpoints, request/response DTOs |
| 07 | API documentation | OpenAPI/Swagger or equivalent |
| 08 | Frontend setup | Scaffold, dependencies, build config |
| 09 | Frontend auth | Client-side auth flow, token storage, interceptors |
| 10 | Frontend services | API client services |
| 11 | Frontend screens/pages | Main UI views |
| 12 | Frontend components | Reusable UI components |
| 13 | Configuration/multi-tenant | Dynamic config, feature flags, branding |
| 14 | Logging/observability | Structured logging, monitoring |
| 15 | Integration testing | End-to-end test scenarios |
| 16 | Security audit | Security checklist and hardening |
| 17 | Performance | Optimization, caching, lazy loading |
| 18 | Documentation | README, deployment guides, API docs |

Adapt, merge, or add spec files based on the actual project. Not every project needs all 18 — skip areas that don't apply and add areas that are unique to the project. The numbering must be sequential with no gaps.

Each spec file must contain:

```markdown
# Spec NN — <Title>

## Goal
<One sentence describing what this spec achieves>

## Acceptance Criteria
- [ ] <Specific, testable criterion 1>
- [ ] <Specific, testable criterion 2>
- ...

## Implementation Details

<Detailed instructions for Claude to implement this spec. Include:>
- Exact file paths to create or modify
- Code patterns to follow (with examples if the spec is complex)
- Configuration values
- Dependencies to install
- Commands to validate

## Validation
- <Exact commands to run to verify this spec passes>
- <Expected output or behavior>
```

### Step 3: Generate prd.json

Create a `prd.json` file containing one story per logical unit of work. Stories should be small enough to implement in a single iteration (typically one controller, one service, one screen, etc.).

Format:

```json
{
  "title": "<Project Name>",
  "stories": [
    {
      "id": "S01",
      "title": "<Short descriptive title>",
      "spec": "<NN-spec-filename>.md",
      "passes": false
    },
    {
      "id": "S02",
      "title": "<Short descriptive title>",
      "spec": "<NN-spec-filename>.md",
      "passes": false
    }
  ]
}
```

Rules for story decomposition:

- One story per entity model or small group of closely related models
- One story per backend service
- One story per backend controller
- One story per frontend screen
- One story per reusable frontend component (if non-trivial)
- One story per cross-cutting concern (auth, logging, security, etc.)
- Stories must be ordered so dependencies come first (scaffold before models, models before services, services before controllers, backend before frontend)
- All stories start with `"passes": false`
- A spec file may be referenced by multiple stories

### Step 4: Generate AGENTS.md

This is the operations manual Claude reads at the start of every iteration. It must contain all of the following sections, adapted to the specific project:

```markdown
# AGENTS.md — <Project Name>

## Project Structure
<Directory tree showing the target project layout>

## Tech Stack
<List of all technologies with versions>

## Commands

### Build
<Exact build commands for each subsystem>

### Test
<Exact test commands for each subsystem>

### Run
<Exact commands to start the application locally>

### Lint
<Exact lint commands, if applicable>

## Architecture Patterns
<Describe the patterns Claude must follow:>
- Backend patterns (controller → service → repository, etc.)
- Frontend patterns (component → service → API, etc.)
- Error handling patterns
- Dependency injection patterns
- Async patterns

## Naming Conventions
- <Language 1>: <convention> (e.g., PascalCase for C# public members)
- <Language 2>: <convention> (e.g., camelCase for TypeScript)
- Files: <convention> (e.g., kebab-case)

## Data Model Reference
<Quick reference for critical data types, IDs, enums, mappings>
<Call out anything surprising — e.g., IDs that are strings not integers>

## API Route Reference
| Method | Route | Auth | Status Codes | Description |
|--------|-------|------|-------------|-------------|
| GET | /api/... | Yes | 200, 404 | ... |
| POST | /api/... | Yes | 201, 400 | ... |

## Response Formats
<Standard success and error response shapes>

## Authentication & Authorization
<How auth works end-to-end: provider, token format, middleware, claims>
<How to extract user identity from requests>
<Authorization rules — who can access what>

## Database / Data Layer
<Connection details, schemas, tables/views, stored procedures>
<Mock/in-memory strategy for testing>

## Testing Strategy
<Unit test patterns, integration test patterns>
<Mock/stub approach>
<What must be tested>

## Security Requirements
<Input validation rules, output encoding, auth checks, data protection>

## Git Conventions
- Commit format: `ralph: <story-title>`
- State commits: `ralph: mark <story-id> complete`

## State Files
- `prd.json` — Story completion tracking
- `progress.txt` — Human-readable progress log (created in target project)

## Critical Rules
- NEVER write placeholder code (no TODO, no NotImplementedException)
- NEVER assume code is missing — always search the codebase first
- ALWAYS validate (build + test) before committing
- ALWAYS use mock/in-memory data for testing — no real external connections during the loop
- ALL builds must produce zero errors and zero warnings
- ALL tests must pass before marking a story complete
```

Adapt and extend these sections based on the project's actual needs. Add project-specific sections as needed (e.g., "Message Queue Patterns", "GraphQL Schema Conventions", "Docker Configuration").

### Step 5: Generate PROMPT_plan.md

```markdown
# PROMPT — Plan Mode

You are an autonomous coding agent running inside a Ralph Wiggums Loop.

## Your Task

Analyze the current codebase and update the PRD (Product Requirements Document).

## Steps

1. **Read** `AGENTS.md` for project context and patterns.
2. **Read** `prd.json` to understand current story status.
3. **Scan** the target project directory to assess what exists.
4. **Read** every spec file in `specs/` to understand requirements.
5. **Compare** the codebase state against spec requirements.
6. **Update** `prd.json`:
   - Mark stories as `"passes": true` if their acceptance criteria are met.
   - Add new stories if gaps are found.
   - Reorder stories if dependency issues are discovered.
7. **Write** findings to `progress.txt` in the target project.
8. **Commit** all changes:
   ```
   cd <RALPH_DIR> && git add prd.json && git commit -m "ralph: plan update"
   cd <PROJECT_DIR> && git add progress.txt && git commit -m "ralph: plan update"
   ```

## Rules

- Do NOT implement any code in plan mode.
- Do NOT delete stories that have already passed.
- Be conservative — only mark stories complete if ALL acceptance criteria are clearly met.
```

### Step 6: Generate PROMPT_build.md

```markdown
# PROMPT — Build Mode

You are an autonomous coding agent running inside a Ralph Wiggums Loop.

## Your Task

Implement the next incomplete user story from the PRD.

## Steps

1. **Read** `AGENTS.md` for project context, patterns, and commands.
2. **Read** `prd.json` to find the first story with `"passes": false`.
3. **Read** `progress.txt` (if it exists) for context on previous iterations.
4. **Read** the spec file referenced by the story.
5. **Search** the target project codebase for any existing implementation — do NOT assume code is missing.
6. **Implement** the story per the spec. Follow all patterns in AGENTS.md.
7. **Write tests** for all new functionality.
8. **Validate** — run ALL build and test commands from AGENTS.md. Every command must succeed with zero errors.
9. **Fix** any failures. Re-validate until clean.
10. **Commit** implementation:
    ```
    cd <PROJECT_DIR> && git add -A && git commit -m "ralph: <story-title>"
    ```
11. **Update** `prd.json` — set `"passes": true` for the completed story.
12. **Commit** state:
    ```
    cd <RALPH_DIR> && git add prd.json && git commit -m "ralph: mark <story-id> complete"
    ```
13. **Append** to `progress.txt` with a summary of what was done.
14. **Commit** progress:
    ```
    cd <PROJECT_DIR> && git add progress.txt && git commit -m "ralph: update progress"
    ```
15. **Check** `prd.json` — if ALL stories have `"passes": true`, output exactly:
    ```
    <promise>COMPLETE</promise>
    ```

## Rules

- Implement ONE story per iteration. Stop after committing.
- NEVER write placeholder code. Every function must be fully implemented.
- NEVER skip validation. If the build or tests fail, fix the issue before committing.
- NEVER mark a story as complete unless all its acceptance criteria are met and validation passes.
- Always search the codebase before creating new files — code may already exist from a previous iteration.
- Use mock/in-memory data for all external dependencies (databases, APIs, etc.).
```

### Step 7: Generate loop.sh

Generate a `loop.sh` script adapted to the target platform and project. The script must:

```bash
#!/usr/bin/env bash
set -euo pipefail

##############################################################################
# Ralph Wiggums Loop — Autonomous Development Driver
##############################################################################

MODE="${1:-build}"
MAX_ITERATIONS="${2:-9999}"

# --- CONFIGURATION --- #
# Adapt these paths to the target project
RALPH_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="<absolute-path-to-target-project>"
LOG_DIR="${RALPH_DIR}/logs"

mkdir -p "$LOG_DIR"

# --- PREREQUISITES --- #
if ! command -v claude &>/dev/null; then
  echo "ERROR: Claude CLI not found. Install it first."
  exit 1
fi

# Select prompt file based on mode
case "$MODE" in
  plan)  PROMPT_FILE="${RALPH_DIR}/PROMPT_plan.md" ;;
  build) PROMPT_FILE="${RALPH_DIR}/PROMPT_build.md" ;;
  *)     echo "ERROR: Mode must be 'plan' or 'build'"; exit 1 ;;
esac

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "ERROR: Prompt file not found: $PROMPT_FILE"
  exit 1
fi

# --- PRE-LOOP: Check for uncommitted changes --- #
for DIR in "$PROJECT_DIR" "$RALPH_DIR"; do
  if [[ -d "$DIR/.git" ]]; then
    CHANGES=$(cd "$DIR" && git status --porcelain 2>/dev/null || true)
    if [[ -n "$CHANGES" ]]; then
      echo "WARNING: Uncommitted changes in $DIR"
      echo "$CHANGES"
      read -rp "Continue anyway? (y/n): " ANSWER
      [[ "$ANSWER" != "y" ]] && exit 1
    fi
  fi
done

# --- MAIN LOOP --- #
ITERATION=0

while [[ $ITERATION -lt $MAX_ITERATIONS ]]; do
  ITERATION=$((ITERATION + 1))
  LOG_FILE="${LOG_DIR}/ralph-iteration-${ITERATION}.log"

  echo ""
  echo "================================================================"
  echo "  RALPH LOOP — Iteration ${ITERATION} (${MODE} mode)"
  echo "================================================================"
  echo ""

  # Execute Claude with the prompt
  EXIT_CODE=0
  cat "$PROMPT_FILE" | claude -p \
    --dangerously-skip-permissions \
    --model opus \
    --verbose \
    2>&1 | tee "$LOG_FILE" || EXIT_CODE=$?

  # Check for completion signal
  if grep -q '<promise>COMPLETE</promise>' "$LOG_FILE" 2>/dev/null; then
    echo ""
    echo "========================================"
    echo "  RALPH LOOP COMPLETE after ${ITERATION} iterations"
    echo "========================================"
    exit 0
  fi

  # Check for critical errors
  if grep -q 'CRITICAL ERROR' "$LOG_FILE" 2>/dev/null; then
    echo "CRITICAL ERROR detected. Stopping loop."
    exit 1
  fi

  # Handle Claude CLI exit codes
  if [[ $EXIT_CODE -ne 0 ]]; then
    echo "Claude exited with code $EXIT_CODE. Retrying in 10 seconds..."
    sleep 10
    continue
  fi

  echo "Iteration ${ITERATION} complete. Next iteration in 3 seconds..."
  sleep 3
done

echo "Reached maximum iterations ($MAX_ITERATIONS). Exiting."
exit 1
```

Adapt `PROJECT_DIR` to point to where the actual software project will be built. If the project directory doesn't exist yet, the first story should create it.

Make the script executable (`chmod +x loop.sh`).

---

## Key Principles

### Story Ordering

Stories must respect dependency chains. Common ordering:

1. Project scaffold / setup
2. Data layer / database configuration
3. Data models / entities
4. Authentication / authorization
5. Backend business logic (services)
6. Backend API layer (controllers / routes)
7. API documentation
8. Frontend scaffold / setup
9. Frontend authentication
10. Frontend services (API clients)
11. Frontend screens / pages
12. Frontend reusable components
13. Cross-cutting concerns (logging, multi-tenant, config)
14. Integration tests
15. Security hardening
16. Performance optimization
17. Documentation

### Validation Backpressure

Every iteration must validate before committing. The AGENTS.md must list exact commands for:

- **Build** — must produce zero errors and zero warnings
- **Test** — all tests must pass
- **Lint** — zero violations (if applicable)

If any validation fails, Claude must fix the issue and re-validate. This creates "backpressure" that prevents broken code from accumulating.

### Mock-First Testing

During the Ralph Loop, **never connect to real external services** (databases, APIs, auth providers). Instead:

- Use in-memory databases or SQLite for data layer testing
- Mock all external API calls
- Use test doubles for auth (hardcoded JWT tokens, mock auth providers)
- Seed mock data that exercises all business logic paths

This ensures the loop can run anywhere without infrastructure dependencies.

### Spec File Quality

Each spec file must be detailed enough that Claude can implement it without ambiguity. Include:

- Exact file paths
- Exact interface/class/function signatures
- Exact configuration values
- Example request/response payloads for APIs
- Example mock data
- Exact validation commands and expected output

Vague specs produce vague implementations. The more precise the spec, the better the output.

### Progress Tracking

The loop tracks progress through three mechanisms:

1. **prd.json** — machine-readable story completion status
2. **progress.txt** — human-readable log of what was done each iteration (lives in target project)
3. **Git history** — full audit trail of every change

### Completion Signal

The loop terminates when Claude outputs `<promise>COMPLETE</promise>` after verifying all stories in prd.json have `"passes": true`. This is the only clean exit path.

---

## Adapting to Different Tech Stacks

The Ralph Loop pattern is stack-agnostic. When generating for a different tech stack, adapt:

| Component | .NET + Angular Example | Python + React Example | Node + Vue Example |
|-----------|----------------------|----------------------|-------------------|
| Build cmd | `dotnet build` | `python -m py_compile` | `npm run build` |
| Test cmd | `dotnet test` | `pytest` | `npm test` |
| Lint cmd | (optional) | `ruff check .` | `npm run lint` |
| ORM | Entity Framework | SQLAlchemy / Django ORM | Prisma / TypeORM |
| Mock DB | InMemory provider | SQLite in-memory | SQLite / in-memory |
| Auth | JWT Bearer middleware | JWT decorator / middleware | JWT middleware |
| Package mgr | NuGet / npm | pip / npm | npm |

Always verify the commands work for the chosen stack and include them verbatim in AGENTS.md.

---

## Checklist Before Running the Loop

- [ ] All spec files are detailed and unambiguous
- [ ] prd.json stories are properly ordered by dependency
- [ ] AGENTS.md has correct build/test/lint commands
- [ ] AGENTS.md has correct project directory paths
- [ ] loop.sh has correct `PROJECT_DIR` and `RALPH_DIR` paths
- [ ] loop.sh is executable (`chmod +x loop.sh`)
- [ ] Claude CLI is installed and accessible
- [ ] Target project directory exists (or first story creates it)
- [ ] Git is initialized in both the Ralph directory and the target project directory