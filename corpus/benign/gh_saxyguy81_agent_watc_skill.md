---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: saxyguy81/agent-watchdog-skill
# corpus-url: https://github.com/saxyguy81/agent-watchdog-skill/blob/8be50e278b1c70b0b1f94d066372125fa1c32e63/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Agent Watchdog Skill

Monitor your AI agent's responsiveness and keep it accountable.

## What It Does

The Agent Watchdog watches your agent's Matrix room and ensures it stays responsive to you. When your agent goes silent or gets lost in deep work, the watchdog wakes it up.

### Core Features (Always On)

- **Matrix Responsiveness** — Tracks messages from you to your agent. If your agent doesn't respond within the timeout (default 30s), it triggers a wake event.
- **Subagent Work Detection** — Monitors when your agent is doing heavy work (multiple tool calls, browser automation, long execs) without communicating. Nudges it to spawn a subagent instead of going dark.

### Optional Features

- **Commitment Tracking (LLM-powered)** — Uses Claude Haiku (~$0.001/check) to detect when your agent makes promises like "I'll update you when it's done". Much more accurate than regex. Reminds the agent if it forgets to follow up.
- **Kanban Task Monitoring** — Watches task threads in a Kanban API for messages from you. Useful if you have a custom task tracker. *Disabled by default — requires your own API.*

## Installation

```bash
# Clone or copy to your skills directory
cp -r agent-watchdog-skill ~/.openclaw/skills/

# Install dependencies
cd ~/.openclaw/skills/agent-watchdog-skill
npm install

# Copy and edit config
cp config.example.json config.json
# Edit config.json with your agent's details
```

## Configuration

Create `config.json` in the skill directory:

```json
{
  "agentId": "your-agent-name",
  "matrix": {
    "homeserver": "http://127.0.0.1:8008",
    "roomId": "!yourRoomId:your-homeserver.local",
    "agentUserId": "@your-agent:your-homeserver.local",
    "humanUserId": "@you:your-homeserver.local",
    "accessToken": "your_agent_matrix_token"
  },
  "responsiveness": {
    "enabled": true,
    "timeoutMs": 30000
  },
  "subagentDetection": {
    "enabled": true,
    "toolCallThreshold": 4,
    "heavyToolTypes": ["exec", "browser", "read"]
  },
  "commitments": {
    "enabled": true,
    "model": "claude-3-haiku-20240307",
    "apiKey": "${ANTHROPIC_API_KEY}"
  },
  "kanban": {
    "enabled": false
  }
}
```

### Minimal Config (Just Responsiveness)

```json
{
  "agentId": "sam",
  "matrix": {
    "homeserver": "http://127.0.0.1:8008",
    "roomId": "!abc123:my-server.local",
    "agentUserId": "@sam:my-server.local",
    "humanUserId": "@scott:my-server.local",
    "accessToken": "syt_..."
  }
}
```

### Commitment Tracking with Haiku

```json
{
  "commitments": {
    "enabled": true,
    "model": "claude-3-haiku-20240307",
    "apiKey": "${ANTHROPIC_API_KEY}",
    "apiBaseUrl": "https://api.anthropic.com",
    "defaultTimeoutMs": 600000,
    "subagentTimeoutMs": 900000
  }
}
```

The `apiKey` can be:
- A literal API key: `"sk-ant-..."`
- An environment variable reference: `"${ANTHROPIC_API_KEY}"` (expanded at runtime)

**Cost:** Haiku costs ~$0.001 per commitment check (very cheap).

## Usage

### Start the Watchdog

```bash
# Using config.json
node bin/watchdog.js

# With verbose logging
node bin/watchdog.js --verbose

# Override config via CLI
node bin/watchdog.js --agent sam --timeout 60000
```

### Run as a Service

Add to your agent's startup or use systemd/launchd:

```bash
# Example: run in background with pm2
pm2 start bin/watchdog.js --name "agent-watchdog"
```

### CLI Options

| Option | Description |
|--------|-------------|
| `--verbose` | Enable debug logging |
| `--agent <id>` | Override agent ID |
| `--timeout <ms>` | Override response timeout |
| `--no-responsiveness` | Disable Matrix responsiveness monitoring |
| `--no-subagent-detection` | Disable subagent work detection |
| `--enable-commitments` | Enable commitment tracking (off by default) |
| `--enable-kanban` | Enable Kanban monitoring (off by default) |
| `--config <path>` | Path to config file |

## How It Works

### Responsiveness Monitoring

1. Polls your Matrix room for new messages
2. When you send a message, starts a timer
3. If your agent responds (any message), clears the timer
4. If timeout expires, triggers an OpenClaw wake event with a reminder

### Subagent Detection

1. Monitors your agent's session transcript
2. Counts tool calls since last text response to you
3. If agent does 4+ tool calls (especially exec, browser, read) without responding, suggests spawning a subagent
4. Helps keep the agent responsive during complex work

### Commitment Tracking (Haiku LLM)

Instead of fragile regex patterns, each agent message is sent to Claude Haiku with this prompt:

```
Does this message contain a promise or commitment to follow up with the user later?

Return TRUE only for explicit promises like:
- "I'll update you when done"
- "Will ping you once the build completes"
- "Spawning a subagent - will let you know when it finishes"

Return FALSE for intermediate narration like "let me check" or "searching for".
```

Haiku returns:
```json
{"commit": true, "summary": "will update when build completes", "estimatedMinutes": 10}
```

This is much more accurate than regex and costs only ~$0.001 per check.

**Fulfillment detection** also uses Haiku to check if a subsequent message fulfills a pending commitment.

### Kanban Integration (Optional)

If you have a task tracker API that returns:
```json
{
  "tasks": [
    {
      "id": "task-123",
      "title": "Fix the bug",
      "messages": [
        { "author": "Scott", "text": "Any update?", "timestamp": "..." }
      ]
    }
  ]
}
```

The watchdog will monitor for your messages in task threads and alert the agent if it doesn't respond.

## Wake Events

When the watchdog detects an issue, it creates an OpenClaw cron job that:
1. Wakes the agent immediately
2. Delivers a system event with the reminder
3. Deletes itself after running (one-shot)

Example wake messages:
```
⚠️ RESPONSIVENESS CHECK: You have an unanswered message from Scott. 
Stop current work and respond immediately.

⚠️ COMMITMENT REMINDER: You promised: "will update when build completes". 
Update the human now.
```

## Files

```
agent-watchdog-skill/
├── SKILL.md              # This file
├── README.md             # Quick start guide
├── package.json          # Node.js package
├── config.example.json   # Template configuration
├── config.json           # Your configuration (create this)
├── bin/
│   └── watchdog.js       # Main watchdog script
└── lib/
    └── commitments.js    # LLM-based commitment tracking module
```

## Requirements

- Node.js 18+
- OpenClaw with `openclaw cron add` support
- Matrix homeserver access
- Agent's Matrix access token
- (For commitments) Anthropic API key

## Troubleshooting

### "Matrix API error 401"
Your access token is invalid or expired. Get a new one from your Matrix server.

### "Failed to trigger wake"
The OpenClaw CLI isn't available or the agent doesn't exist. Check that `openclaw cron add --agent <your-agent>` works.

### Too many alerts
Increase `alertCooldownMs` in your config. The default is 2 minutes between similar alerts.

### Commitment detection not working
Check that you have a valid `apiKey` in the commitments config. The watchdog will log a warning if the API key is missing.

## Version History

- **1.1.0** — LLM-based commitment detection
  - Uses Claude Haiku instead of regex for commitment detection
  - Much more accurate promise detection (~$0.001/check)
  - Fulfillment detection also uses Haiku
  
- **1.0.0** — Initial ClawHub release
  - Refactored from sam-watchdog v3.2.0
  - Made Kanban monitoring optional (disabled by default)
  - Made commitment tracking optional (disabled by default)
  - Fixed spam bug (duplicate alerts)
  - Agent-agnostic configuration