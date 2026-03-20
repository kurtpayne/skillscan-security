---
name: saturated-coding
description: "Multi-Agent Orchestration for maximum quality coding (饱和式编程). 4-phase pipeline: research -> write-plan -> execute-plan -> verification. Each phase spawns specialized parallel agents using different skills while a thin orchestrator coordinates. Trigger on: 'saturated coding', '饱和式编程', 'agent team', 'parallel agents', '/saturated-coding'."
user-invocable: true
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Louis-Leee/saturation-agnet-team-coding
# corpus-url: https://github.com/Louis-Leee/saturation-agnet-team-coding/blob/e84b5becd1f4c604eedc9ed2dc5ca3b56c515b2c/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Saturated Coding (饱和式编程)

## Philosophy

**Ensemble methods applied to the FULL software lifecycle.** A thin orchestrator spawns specialized agents, collects results, and routes to the next step. The orchestrator never does heavy lifting — it spawns, waits, integrates, routes.

**Core insight:** Multiple independent agents using DIFFERENT skills rarely make the same mistake. Redundancy eliminates blind spots. The best outcome emerges from diverse competition, not a single attempt. Don't be stingy with tokens.

## The 4-Phase Pipeline

```
User Request
    |
[Phase 1: Research]  -----> 4 parallel researchers (inherits superpowers:brainstorming)
    |                        Orchestrator: Spawn + Summarize
    v
[Phase 2: Write Plan] ----> 4 parallel planners (2x superpowers:writing-plans + 2x ECC multi-plan)
    |                        Orchestrator: Validate + Merge
    v
[Phase 3: Execute Plan] --> 4 parallel coders (2x superpowers:executing-plans + 2x ECC:tdd)
    |                        Orchestrator: Wave + Track
    v
[Phase 4: Verification] --> 2 cross-reviewers (ECC:code-review + auto-codex-review)
    |                        Orchestrator: Present + Route
    v
Shipped!
```

## Sub-Workflows

| Phase | Command | Agents | Skills Used | Orchestrator Role |
|-------|---------|--------|-------------|-------------------|
| 1. Research | `/saturated-research` | 4 parallel | `superpowers:brainstorming` (inherited) | Spawn + Summarize |
| 2. Plan | `/saturated-write-plan` | 4 parallel | 2x `superpowers:writing-plans` + 2x ECC multi-plan | Validate + Merge |
| 3. Execute | `/saturated-execute-plan` | 4 parallel | 2x `superpowers:executing-plans` + 2x `everything-claude-code:tdd` | Wave + Track |
| 4. Verify | `/saturated-verify` | 2 parallel | `everything-claude-code:code-review` + `auto-codex-review` | Present + Route |

## Routing

| User Intent | Route To |
|-------------|----------|
| New idea / need brainstorm | `/saturated-research` |
| Requirements exist, need plan | `/saturated-write-plan` |
| Plan exists, need implementation | `/saturated-execute-plan` |
| Code exists, need review | `/saturated-verify` |
| Full pipeline | `/saturated-coding` (starts from research) |

## Invocation

```
# Full pipeline (starts from research)
/saturated-coding

# Individual phases (each is an independent skill)
/saturated-research
/saturated-write-plan
/saturated-execute-plan
/saturated-verify
```

## Orchestrator Rules (NON-NEGOTIABLE)

1. **The orchestrator NEVER writes production code.** It spawns agents, waits, integrates results.
2. **All agents use opus model.** No model downgrades.
3. **Don't be stingy with tokens.** Each agent gets full 1M context. Let them think deeply.
4. **Different skills = different perspectives.** The whole point is diversity of approach.
5. **Each phase has a health check.** Verify agent outputs before proceeding.
6. **Documentation is shared memory.** All agents write to `claude_docs/saturation-run-{TIMESTAMP}/`.

## Documentation Convention

ALL agents write docs to `claude_docs/saturation-run-YYYY-MM-DD-HHMM/`. This is non-negotiable. The docs are the shared memory across agents and sessions.

```
claude_docs/saturation-run-{TIMESTAMP}/
+-- research-context.md          # Phase 1 output
+-- research-agent-{1..4}.md     # Individual research reports
+-- plan-agent-{a..d}.md         # Individual plans
+-- plan-comparison.md           # Plan scoring matrix
+-- final-plan.md                # Merged plan
+-- agent-{name}/
|   +-- implementation.md        # Execution logs per agent
+-- architect-review.md          # Execution scoring
+-- code-review.md               # Verification: code review
+-- codex-review.md              # Verification: codex review
+-- final-report.md              # Summary of entire run
```