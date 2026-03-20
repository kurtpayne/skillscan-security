---
name: hact
description: History-aware collaboration tuning for Codex projects. Use when asked to review past conversations/threads/sessions, summarize user preferences from project history, convert recurring patterns into guardrails or execution protocols, or update collaboration docs based on prior interaction evidence.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sidecus/hact
# corpus-url: https://github.com/sidecus/hact/blob/cc13cde4b69cddb5b385471ad72fac0f668286f9/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# HACT

## Overview

Use this skill to tune collaboration quality from real project history instead of single-thread memory.  
Extract recurring user preferences from Codex session artifacts, convert them into actionable principles/protocols, and apply doc updates when requested.

## Workflow

### 1) Scope Evidence

- Identify the target project path (`cwd`) and optional date window.
- Prefer project-scoped session records over global history snippets.
- Report evidence coverage early: session count and date range.

### 2) Collect History

- Find session/archived-session artifacts that match `cwd`.
- Extract user messages and key assistant responses.
- Keep only content needed for preference inference.

### 3) Clean and Normalize

- Remove boilerplate (injected instructions, environment headers, interrupted-turn markers).
- De-duplicate repeated prompts.
- Sanitize identifiable values in user-facing output:
  - personal names
  - home directory segments
  - machine-specific paths

### 4) Derive Preferences

- Cluster recurring signals using the taxonomy in [references/taxonomy.md](references/taxonomy.md).
- Weight by:
  - frequency
  - recency
  - explicitness ("do this", "I prefer", "not good enough")
- Reject weak one-off signals.

### 5) Synthesize Rules

- Produce:
  - 3-7 concise design principles (cross-project when requested)
  - execution protocol (how to apply principles during delivery)
- Keep principles non-overlapping and testable.
- Check for conflicts with existing project guardrails before proposing edits.

### 6) Apply Changes

- If asked, patch collaboration docs (for example `AGENTS.md`) with:
  - updated principles
  - execution protocol
- Keep wording short and enforceable.
- Avoid verbose rationale in docs; keep rationale in handoff message.

### 7) Quality Gate

- Always include:
  - evidence window (count + dates)
  - what was inferred vs explicit
  - residual uncertainty
- If history is inaccessible, say so and fall back to current-thread + repository evidence.

## Output Contract

When running HACT, return these sections unless user asks otherwise:

- `Evidence Window`
- `Recurring Preferences`
- `Proposed Principles`
- `Execution Protocol`
- `Doc Update Plan` (or applied file path)
- `Uncertainty`

## References

- Preference taxonomy and scoring: [references/taxonomy.md](references/taxonomy.md)
- Final pass checklist: [references/output_checklist.md](references/output_checklist.md)