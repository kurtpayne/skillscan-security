---
name: sentry
description: Set up Sentry observability for OpenClaw (install plugin, configure DSN, investigate issues with Sentry CLI). Use when setting up error tracking, traces, or structured logs for an OpenClaw instance, or when investigating Sentry issues/errors.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sergical/openclaw-skill-sentry
# corpus-url: https://github.com/sergical/openclaw-skill-sentry/blob/c6fb08fa3fd298c1c065f9962d767324718e7494/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Sentry Observability for OpenClaw

## Overview

This skill covers two things:
1. **Setting up** the `openclaw-plugin-sentry` plugin for error/trace/log collection
2. **Investigating** issues using the Sentry CLI

## Plugin Setup

### Install

```bash
openclaw plugins install openclaw-plugin-sentry
```

### Configure

Two config changes needed in `openclaw.json`:

1. **Enable diagnostics** (required for traces):
```json
{ "diagnostics": { "enabled": true } }
```

2. **Configure the plugin**:
```json
{
  "plugins": {
    "allow": ["sentry"],
    "entries": {
      "sentry": {
        "enabled": true,
        "config": {
          "dsn": "<your-sentry-dsn>",
          "environment": "production",
          "tracesSampleRate": 1.0,
          "enableLogs": true
        }
      }
    }
  }
}
```

Config lives under `plugins.entries.sentry.config` — not top-level under `sentry`.

### Get your DSN

1. Go to Sentry → Project Settings → Client Keys (DSN)
2. Copy the DSN URL (looks like `https://key@o000000.ingest.us.sentry.io/0000000`)

### What gets captured

| Signal | Source | Sentry Feature |
|--------|--------|----------------|
| Errors | Auto-captured exceptions (fetch failures, AbortError, etc.) | Issues |
| Traces | `model.usage` → `ai.chat` spans, `message.processed` → `openclaw.message` spans | Tracing |
| Messages | `webhook.error`, `session.stuck` → captureMessage | Issues |
| Logs | Gateway log transport → `Sentry.logger` | Structured Logs |

### Verify it works

After restart, send a message to your bot and check:
```bash
sentry issue list <org>/<project>        # Should see any errors
sentry event list <org>/<project>        # Should see events
```

Or via API:
```bash
curl -s "https://sentry.io/api/0/organizations/<org>/events/?project=<project-id>&dataset=discover&field=id&field=title&field=event.type&field=timestamp&sort=-timestamp" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

## Sentry CLI Investigation

### Auth setup

```bash
npm install -g sentry
sentry login
# Follow browser auth flow — stores config in ~/.sentry/cli.db
```

### Common commands

```bash
# List issues for a project
sentry issue list <org>/<project>

# View issue details
sentry issue view <short-id>

# AI-powered root cause analysis
sentry issue explain <short-id>

# List recent events
sentry event list <org>/<project>

# Direct API calls
sentry api /organizations/<org>/projects/
```

### Checking traces via API

Traces don't show in the CLI directly. Use the API:
```bash
SENTRY_TOKEN="..."
curl -s "https://sentry.io/api/0/organizations/<org>/events/?project=<id>&dataset=discover&per_page=10&sort=-timestamp&field=id&field=title&field=timestamp&field=transaction.duration&field=transaction.op&query=event.type:transaction" \
  -H "Authorization: Bearer $SENTRY_TOKEN"
```

## Troubleshooting

### No traces appearing
- Check `diagnostics.enabled: true` in config (this gates event emission)
- Check plugin loaded: look for `sentry: initialized` in gateway logs
- Check for module isolation: plugin's `onDiagnosticEvent` must share the same listener set as the gateway (OpenClaw patches `globalThis.__oc_diag` for this)

### Traces show 0ms duration
- Sentry SDK v10 expects timestamps in **milliseconds** (not seconds)
- The plugin uses `evt.ts` and `evt.durationMs` from diagnostic events

### Plugin not loading
- Ensure `"sentry"` is in `plugins.allow` array
- Ensure `openclaw.plugin.json` has `configSchema` with `additionalProperties: true`
- Check gateway logs for config validation errors

### Logs not appearing
- `enableLogs: true` must be set in plugin config
- Sentry structured logs may need to be enabled in your Sentry project settings
- `Sentry.logger` API requires `@sentry/node` v10+