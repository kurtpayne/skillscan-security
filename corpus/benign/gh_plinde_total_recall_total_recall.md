---
name: total-recall
description: Memory preservation for Claude Code sessions. Use when approaching token limits, needing to /reset or /compact, switching between complex tasks, or preserving critical session state before context loss. Creates comprehensive memory dumps at /tmp/total-recall containing current state, decisions, artifacts, and next steps for seamless context restoration.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: plinde/total-recall
# corpus-url: https://github.com/plinde/total-recall/blob/d5fe5fad2b75cf049ceadd57cba6a347f9d4c923/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Total Recall - Context Preservation for Claude Code

## Quick Start

When you need to preserve session context before `/reset` or `/compact`:

```bash
# Save current session context
/total-recall
```

This creates a memory dump at `/tmp/total-recall` containing:
- Current work state and project context
- Key decisions and rationale
- Generated files and artifacts with paths
- Next steps and action items
- Important technical notes and constraints

## When to Use

Use this skill when:
- Approaching token limits (`Context left until auto-compact: 0%`)
- Need to `/reset` but can't afford to lose state
- Switching between multiple complex tasks
- Building up conversation history debt
- Working on multi-step tasks with critical state