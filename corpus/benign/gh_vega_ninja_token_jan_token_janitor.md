---
name: token-janitor
description: Audit OpenClaw token usage and find waste. Use when the user says "run token janitor", "check my token usage", "audit my tokens", "why are my tokens so high", or wants to know what's inflating their API costs. Checks workspace files being injected every turn, installed skills with platform conflicts, and config settings like caching and model choice.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: vega-ninja/token-janitor
# corpus-url: https://github.com/vega-ninja/token-janitor/blob/3b1a25b744d19ea7a9f3e7bfce91a1c9f7b6daa8/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Token Janitor

Token Janitor audits an OpenClaw setup for token waste. It checks which workspace files are being loaded on every API call, which skills have platform conflicts, and whether caching is configured correctly.

## When to activate

Activate this skill when the user says any of the following (or close variations):
- "run token janitor"
- "check my token usage"
- "audit my tokens"
- "why are my tokens so high"
- "token janitor"

## How to run it

1. Locate this skill's directory — the folder containing this SKILL.md file.
2. Run the bundled script:
   ```
   python3 <skill_dir>/janitor.py
   ```
   On Windows, `python3` may not be available — try `python <skill_dir>/janitor.py` instead.
3. Read the output, then deliver a concise summary to the user in plain language. Highlight anything marked [!!] first. If everything is clean, say so.

## How to report results

Keep it short and direct. The user wants to know what to fix, not read a report.

- [!!] items are high priority — lead with those
- [>>] items are medium priority — mention them briefly
- If nothing is flagged, tell the user their setup looks lean and give them the token counts so they have a baseline

If the script fails for any reason (Python not available, path issues), you can run the checks manually:
- List files at the workspace root and estimate sizes
- Check `~/.openclaw/openclaw.json` for the `cache` setting
- List the contents of the OpenClaw skills directory

## What it checks

1. **Workspace files** — Files at your workspace root are injected into every API call. Large files here inflate every single turn. The script flags anything oversized and tells the user what to do.

2. **Skills** — Each installed skill adds description text to every session's system prompt. The script checks for platform conflicts (e.g. macOS skills installed on a Linux machine) that will never activate and should be removed.

3. **Config** — Checks for caching being disabled and Opus set as the default model. Either will significantly inflate costs.

## What it does NOT check

- Past session costs or billing history
- Engine-level OpenClaw overhead (not user-configurable)
- Which skills the agent has enabled vs disabled (requires session data)