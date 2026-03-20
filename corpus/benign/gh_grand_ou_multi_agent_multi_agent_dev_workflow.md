---
name: multi-agent-dev-workflow
description: >
  Standardized multi-agent collaborative development workflow for large projects
  with Git Feature Branch integration. Use when: (1) developing features in
  parallel with multiple Sub-Agents, (2) coordinating code across feature branches,
  (3) enforcing "understand → plan → execute" discipline before writing code,
  (4) managing task decomposition, code review, and merge workflows for team or
  AI-driven development. NOT for: single-file scripts, quick fixes, or tasks
  that don't need branching or multi-agent coordination.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Grand-ou/multi-agent-dev-workflow
# corpus-url: https://github.com/Grand-ou/multi-agent-dev-workflow/blob/a0ea0e6a9f587bb49b6329e3be5de7e20d617680/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Multi-Agent Development Workflow

Create standardized multi-agent collaborative development workflows. The quality of a workflow is measured by how well it enables parallel development while maintaining code quality and preventing direction errors.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality multi-agent development workflow involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand the Boris Tane Method

> **"先不要寫代碼" is the hardest instruction to follow.**

The biggest risk in AI-collaborative development is not syntax errors — it's **direction errors**: code that runs but breaks architecture, ignores existing caching, violates ORM conventions, or re-implements existing features.

**Solution**: Completely separate "thinking" from "execution".

**Load [🧠 Boris Tane Method](./reference/boris_tane_method.md) for the complete three-step methodology.**

#### 1.2 Analyze the Project

Before spawning any Sub-Agent, force AI to produce `research.md`:

```
sessions_spawn(
  task="Deeply analyze this project. Output research.md covering:
  1. Project structure and architecture
  2. Database schema and relationships
  3. API design conventions
  4. Frameworks and packages
  5. Caching strategies
  6. Error handling patterns
  7. Test coverage
  DO NOT write code. Only produce research.md.",
  label="research-phase",
  cleanup="keep"
)
```

**Human reviews** research.md — verify AI truly understands the system. If misunderstandings found → annotate and request rewrite. This step eliminates misunderstandings before they become code.

#### 1.3 Plan Your Tasks

**Create `PLAN.md`** using the template: `templates/PLAN_TEMPLATE.md`

For each task, define:
- Task name and description
- Agent label and branch name
- Priority (P0/P1/P2/P3)
- Scope and completion criteria
- Dependencies
- Estimated time

**Task decomposition principles**:
- Each task should be independently developable
- Avoid tasks that modify the same files (prevents merge conflicts)
- Order by dependency: foundation first, features second
- P0 tasks have no dependencies; P1+ tasks depend on P0

---

### Phase 2: Implementation

#### 2.1 Launch Sub-Agents with Plan-First Discipline

For each task, follow this strict sequence:

**Step 1: Create Feature Branch**
```bash
# Or use: scripts/start-task.sh <task-name> <branch-name> "<description>"
git checkout main && git pull
git checkout -b feature/<task-name>
git push -u origin feature/<task-name>
```

**Step 2: Plan Before Code** (Boris Tane Step 2)

For frontend tasks, include design requirements. Load [🎨 Frontend Design Guide](./reference/frontend_design.md) for aesthetic guidelines and anti-patterns.

```
sessions_spawn(
  task="Based on research.md, generate plan-<task>.md for [task].
  Include: implementation steps, files to modify, new files, API design,
  DB changes, test strategy, risks.
  For frontend tasks: also include font pairing, color palette, animation strategy.
  DO NOT write code. Wait for review.",
  label="<task-name>",
  cleanup="keep"
)
```

**Step 3: Annotation Loop** (1-6 iterations)
- Human reviews plan, adds inline annotations (`> 【批注】...`)
- Send back: "Update plan per annotations. DO NOT write code."
- Repeat until plan is satisfactory
- **Always include "DO NOT write code"** — AI tends to start coding prematurely

**Step 4: Execute**
```
sessions_send(
  sessionKey="agent:main:isolated:<task-name>",
  message="Plan confirmed. Execute plan-<task>.md strictly.
  Rules: 1) Follow plan exactly  2) Mark [x] as you go
  3) Don't stop until done  4) Record issues in issues.md
  5) Use Conventional Commits  6) Report when complete."
)
```

#### 2.2 Sub-Agent Execution Standards

Sub-Agents must follow:

**Branch Discipline**:
- Work only on assigned feature branch
- Pull latest before starting

**Commit Convention** (Conventional Commits):
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` restructuring
- `test:` testing
- `chore:` maintenance

**Completion Protocol**:
1. All plan items marked `[x]`
2. Tests pass
3. Code pushed to remote
4. Status reported to Main Agent

#### 2.3 Track Status

Use `templates/AGENTS_STATUS_TEMPLATE.md` to track all Sub-Agents:

```bash
# Check all Sub-Agents
sessions_list(kinds=["isolated"])

# Check specific Sub-Agent
sessions_history(sessionKey="agent:main:isolated:<label>")

# Send message to Sub-Agent
sessions_send(sessionKey="agent:main:isolated:<label>", message="Progress?")
```

---

### Phase 3: Review and Merge

#### 3.1 Code Review

For each completed task:

```bash
# Switch to feature branch
git checkout feature/<task-name>

# Review changes against main
git diff main..feature/<task-name>

# Run tests
npm test  # or project-specific test command
```

**Review checklist**:
- [ ] Code follows project conventions
- [ ] All tests pass
- [ ] No obvious performance issues
- [ ] Comments and documentation adequate
- [ ] No security vulnerabilities
- [ ] Integrates well with existing features
- [ ] Plan was followed (no freelancing)

#### 3.2 Merge

```bash
# Or use: scripts/merge-task.sh feature/<task-name>
git checkout main && git pull
git merge feature/<task-name> --no-ff -m "merge: <task description>"
git push
```

**Conflict Resolution**:
- **Prevention**: Design tasks to avoid modifying same files
- **Detection**: Regularly pull main into feature branches
- **Resolution**: Main Agent resolves conflicts, consults Sub-Agent if needed

#### 3.3 Cleanup

```bash
# Optional: delete merged branches
git branch -d feature/<task-name>
git push origin --delete feature/<task-name>
```

Update AGENTS_STATUS.md: mark task as "completed" with merge timestamp.

---

### Phase 4: Integration Testing and Evaluation

#### 4.1 Integration Testing

```bash
git checkout main && git pull
npm install    # ensure dependencies up to date
npm test       # full test suite
npm run build  # build verification
```

**Automated UI Testing** (for web applications):

Use Playwright for automated verification. Load [🧪 Testing Guide](./reference/webapp_testing.md) for full patterns.

```bash
# Start servers + run integration tests
python scripts/testing/with_server.py \
  --server "node index.js" --port 3000 \
  --server "cd web && npm run dev" --port 5173 \
  -- python tests/integration_test.py
```

See `examples/` for Playwright patterns: element discovery, console logging, static HTML testing.

Verify:
- All new features work correctly
- No regression in existing features
- Cross-feature integration is sound
- UI renders correctly (screenshot verification)

#### 4.2 Create Evaluation Report

Document results in `INTEGRATION_REPORT.md`:
- Features tested
- Test results (pass/fail)
- Performance observations
- Issues found
- Overall assessment

#### 4.3 Retrospective

After each development cycle:
- What went well? What didn't?
- Which plans needed most iterations?
- Were task boundaries well-defined?
- Update workflow based on learnings

---

# Key Principles

| Principle | Why |
|-----------|-----|
| **Always say "DO NOT write code"** | AI starts coding prematurely if you don't |
| **Plan dissatisfaction = don't execute** | Iterate until the plan is right |
| **Big problems = rollback & redo** | Cheaper than patching |
| **Keep plan files persistent** | They survive context loss |
| **One feature = one branch = one agent** | Clean isolation |
| **Alignment over generation speed** | AI's value is alignment, not execution |

---

# Decision Tree: When to Use This Workflow

```
Your development task →
  ├─ Single file / quick fix → Don't use this workflow
  ├─ One feature, no branching needed → Don't use this workflow
  └─ Multiple features / parallel development?
      ├─ Yes → Use this workflow
      │   ├─ New project → Start at Phase 1.2 (analyze)
      │   └─ Existing project → Start at Phase 1.2 (research.md first)
      └─ Complex single feature?
          └─ Use Boris Tane method only (research → plan → execute)
```

---

# Scripts

- `scripts/start-task.sh <task-name> <branch> "<description>"` — Create branch, push, update status
- `scripts/merge-task.sh <branch>` — Test, merge, push, optional cleanup
- `scripts/testing/with_server.py` — Start server(s), run test command, cleanup

**Always run scripts with `--help` first** to see usage.

---

# Reference Files

## 📚 Documentation Library

Load these resources as needed during development:

### Core Methodology (Load During Phase 1)
- [🧠 Boris Tane Method](./reference/boris_tane_method.md) — Complete three-step methodology:
  - Step 1: Understand (research.md)
  - Step 2: Plan with annotation loops (plan.md)
  - Step 3: One-shot execution
  - Why this method works
  - DO's and DON'T's

### Frontend Design (Load During Phase 2 — Frontend Tasks)
- [🎨 Frontend Design Guide](./reference/frontend_design.md) — Aesthetic guidelines:
  - Design thinking process (purpose, tone, differentiation)
  - Typography, color, motion, spatial composition
  - Anti-patterns ("AI slop" to avoid)
  - Frontend Sub-Agent checklist

### Testing (Load During Phase 4)
- [🧪 Webapp Testing Guide](./reference/webapp_testing.md) — Playwright automation:
  - Decision tree: static vs dynamic testing
  - Reconnaissance-then-action pattern
  - Server lifecycle management (with_server.py)
  - Integration test examples

### Best Practices (Load During Phase 2)
- [📋 Development Best Practices](./reference/dev_best_practices.md) — Universal guidelines:
  - Conventional Commits format
  - Branch naming conventions
  - Conflict resolution strategies
  - Sub-Agent communication patterns
  - Code review checklist

### Templates (Copy During Phase 1)
- [📝 Plan Template](./templates/PLAN_TEMPLATE.md) — Task decomposition template
- [📊 Status Template](./templates/AGENTS_STATUS_TEMPLATE.md) — Sub-Agent tracking

### Example (Load for Reference)
- [💡 Example Plan](./reference/example_plan.md) — Complete development plan for a real project