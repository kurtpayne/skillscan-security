---
name: boring-code
description: >
  Opinionated coding standards and agentic workflow guidance for AI-assisted development.
  Enforces clean, maintainable, human-readable code with strong guardrails for autonomous
  multi-step coding sessions. Use this skill when writing, reviewing, or refactoring code
  in any language or framework. Triggers on: (1) Any code generation or implementation task,
  (2) Code review or quality checks, (3) Multi-step agentic coding sessions,
  (4) Requests that include "qcheck" or "qcode" shortcuts,
  (5) Refactoring or cleanup tasks. This skill applies to all programming languages
  and frameworks. It emphasizes simplicity over cleverness, incremental delivery,
  standard libraries over dependencies, and boring maintainability over novelty.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: vscarpenter/boring-code
# corpus-url: https://github.com/vscarpenter/boring-code/blob/cc44c8870d53420b3c8114b556e861459eb2c717/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Boring Code

*Code should be safe to modify, easy to reason about, and boring to maintain. When in doubt, simplify.*

## Agentic Session Management

Follow these rules for every coding session involving multi-step or sustained work.

### Before Writing Code

1. Outline an implementation plan with clear milestones.
2. Work systematically through each milestone.
3. Commit functional changes at every logical unit of work.
4. Monitor context usage. If 80% through context with major uncommitted work, stop adding features and commit immediately.

### After Every Tool Result

Pause and evaluate before proceeding:

- Did the operation succeed or fail?
- Does the output match expectations?
- What is the root cause if results are unexpected?

Use extended thinking for analysis. Diagnose root cause before attempting fixes. Never use repeated trial-and-error without understanding the underlying issue.

### Incremental Progress

- Get a minimal working version first, then extend.
- Run the full test suite after every file modification.
- Fix failures before proceeding. Do not assume code is correct without execution.
- Provide a brief status update after each milestone or significant tool operation.

### Compaction Directive

When compacting, always preserve: full list of modified files, current task status, test commands, and next steps. Do not discard working state during summarization.

### Error Learning

After encountering a mistake, analyze what went wrong and propose a CLAUDE.md update to prevent recurrence.

## Code Standards (Quick Reference)

For complete standards with examples, see [references/standards.md](references/standards.md).

### Core Principles

1. **Simplicity over cleverness.** Prefer clarity to novelty.
2. **Build small, iterate fast.** Deliver working code before optimizing.
3. **Code for humans.** Readable by a junior engineer without scrolling to other files.
4. **Prefer boring tech.** Stability over hype.
5. **Standard lib first.** Choose the language's standard library over external dependencies unless it requires >2x the code.
6. **Automate consistency.** Enforce linting, tests, and formatting in CI.

### Key Constraints

- Functions: 30 lines or fewer, single responsibility
- Nesting: maximum 3 levels, use early returns
- Files: approximately 350-400 lines, split by responsibility
- Names: descriptive, no generic terms like "data", "temp", or single letters
- Comments: explain WHY, not WHAT
- DRY: apply only after 3+ repetitions
- YAGNI: do not build for hypothetical futures
- No magic numbers: use named constants
- Inject dependencies (I/O, time, randomness)

### File Boundaries

Do not modify files outside the current working directory without explicit permission. Do not edit configuration files, CI/CD pipelines, or infrastructure code unless the task specifically requires it.

## Testing Standards

For complete testing and error handling guidance, see [references/testing.md](references/testing.md).

- Write tests BEFORE implementation when feasible (TDD).
- Test all public APIs and critical paths (target approximately 80% coverage).
- Use Arrange-Act-Assert pattern with behavior-based test names.
- Include positive and negative cases.
- Run the full test suite after every modification; do not proceed with failing tests.

## Security Essentials

- Validate and sanitize all user inputs.
- Use parameterized queries (no SQL concatenation).
- Apply least-privilege principles.
- Never commit secrets; rotate regularly.
- Keep dependencies patched and scanned.

## Shortcuts

**"qcheck"** triggers this review:

1. Does this follow our coding standards?
2. Are there comprehensive tests?
3. Is error handling adequate?
4. Does this maintain existing patterns?
5. Are there any security concerns?
6. Is the code maintainable and readable?

**"qcode"** triggers this workflow:

1. Implement the plan.
2. Verify all new tests pass.
3. Run existing tests to confirm nothing breaks.
4. Run linting/formatting tools.
5. Verify type checking passes.
6. Confirm code follows established patterns.

## Subagent Guidance

For subagent delegation patterns and usage guidance, see [references/subagents.md](references/subagents.md).

- Use subagents liberally to keep the main context window clean.
- One well-defined task per subagent.
- Subagents return concise summaries, not raw output.
- Use read-only tools for research subagents; grant write access only to implementation subagents.

## Red Flags

Stop and address if you see any of these:

- Functions exceeding 40 lines
- More than 3 nesting levels
- Unused abstractions or commented-out code
- TODOs without ticket links
- Copy-pasted logic (3+ times requires refactor)
- Hardcoded test values or magic numbers
- Trial-and-error fixes without root cause analysis
- Large uncommitted changes late in context
- Modifying files outside the task's scope