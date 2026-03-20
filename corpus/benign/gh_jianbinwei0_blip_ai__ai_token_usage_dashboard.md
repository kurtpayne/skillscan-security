---
name: ai-token-usage-dashboard
description: Build, refresh, and customize a local multi-provider AI token usage dashboard served on 127.0.0.1:8765. Current providers are Codex, Claude, and PI from ~/.codex/sessions, ~/.claude/projects, and ~/.pi/agent. Use when the user asks for provider-specific token usage updates, chart/stat card changes, date-range/preset behavior, refresh cadence updates, or recalc-service troubleshooting.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: jianbinwei0-blip/ai-token-usage-dashboard
# corpus-url: https://github.com/jianbinwei0-blip/ai-token-usage-dashboard/blob/df253189f39a9644f539c25ea88d90396716c45b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# AI Token Usage Dashboard

## Overview

Use this skill to maintain a local token-usage dashboard that:
- Reads session data from `~/.codex/sessions`, `~/.claude/projects`, and `~/.pi/agent/sessions`
- Recalculates stats/tables via a local Python service
- Serves the dashboard at `http://127.0.0.1:8765/`
- Currently supports Codex, Claude, and PI providers

Primary files:
- `dashboard/index.html`: dashboard UI and client-side behavior
- `scripts/ai_usage_recalc_server.py`: `/health` and `/recalc` HTTP entrypoint
- `scripts/dashboard_core/pipeline.py`: recalc orchestration logic
- `scripts/dashboard_core/collectors.py`: provider ingestion
- `scripts/dashboard_core/aggregation.py`: date windows and summaries
- `scripts/dashboard_core/render.py`: HTML rewrite and embedded dataset output
- `scripts/run_local.sh`: local launcher

## Quick Commands

- Start local service:
  - `./scripts/run_local.sh`
- Health check:
  - `curl -s http://127.0.0.1:8765/health`
- Recalculate immediately:
  - `curl -s http://127.0.0.1:8765/recalc`
- Open dashboard:
  - `open http://127.0.0.1:8765/`

## Working Workflow

1. Confirm service is running (`/health`).
2. Trigger `/recalc` before reviewing token numbers.
3. Make UI changes in `dashboard/index.html`.
4. Make aggregation/range logic changes in `scripts/ai_usage_recalc_server.py` only when server-side totals must change.
5. Validate with:
   - `curl -s http://127.0.0.1:8765/recalc` returns JSON containing `"ok": true`
   - Dashboard reflects requested UI/number updates after refresh.

## Data/Behavior Notes

- `/recalc` rewrites the configured dashboard HTML file in place.
- Defaults:
  - Host: `127.0.0.1`
  - Port: `8765`
  - Codex sessions root: `~/.codex/sessions`
  - Claude projects root: `~/.claude/projects`
  - PI agent root: `~/.pi/agent`
  - Dashboard HTML (via `run_local.sh`): `tmp/index.runtime.html` seeded from `dashboard/index.html`
- Override with env vars:
  - `AI_USAGE_SERVER_HOST`
  - `AI_USAGE_SERVER_PORT`
  - `AI_USAGE_CODEX_SESSIONS_ROOT`
  - `AI_USAGE_CLAUDE_PROJECTS_ROOT`
  - `AI_USAGE_PI_AGENT_ROOT`
  - `AI_USAGE_DASHBOARD_HTML`

## Guardrails

- Preserve existing functionality unless the user explicitly requests behavior changes.
- Keep number formatting user-friendly (`toLocaleString("en-US")` for display).
- Prefer small, targeted UI edits over broad redesigns for dashboard maintenance requests.