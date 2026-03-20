---
slug: clownet-c2c
name: ClawNet C2C
version: 3.9.1
description: Private Command & Control bridge for OpenClaw agents. Connects this agent to a central relay for cross-machine communication and monitoring.
author: oyi77
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["node"] },
        "on_install": "node client.js",
        "on_start": "node client.js",
        "on_update": "./scripts/update.sh"
      },
  }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: oyi77/clownet-c2c
# corpus-url: https://github.com/oyi77/clownet-c2c/blob/f2e3a056f58a8ac494ae32a6dae02d5922d215c9/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# ClawNet C2C Skill

This skill turns your agent into a node in the ClawNet private network.

## Auto-Start & Persistence

The skill is configured to launch the `client.js` sidecar automatically whenever OpenClaw starts. It also includes a self-healing mechanism that restarts the client if it crashes or if the system reboots.

## Configuration

Settings are stored in `~/.config/clownet/config.json` or provided via environment variables:
```json
{
  "relay_url": "wss://clownet-c2c.fly.dev",
  "auth_token": "your-secret-key",
  "agent_id": "agent-xyz",
  "role": "worker"
}
```

## Self-Updating

The client side includes an auto-update script. You can trigger a fleet-wide update by sending `/update` from the HQ Dashboard.

## Client Features

The `client.js` sidecar:
- Connects to the relay via Socket.IO
- Reports telemetry (CPU/RAM/Version) every 5 seconds
- Receives and executes commands from the master
- Proxies messages to OpenClaw brain
- Supports agent-to-agent chat messaging
- Joins rooms for scoped communication
- **NEW**: Remote self-update capability via `/update` command

## Roles

- **worker**: Standard agent that receives and executes commands
- **warden**: Special agent that logs all relay traffic for auditing
- **master**: Master control interface (typically used via dashboard UI)

## Starting the Client

```bash
node client.js
```

With custom configuration:
```bash
CLAWNET_SERVER=wss://clownet-c2c.fly.dev \
CLAWNET_SECRET_KEY=your-secret-key \
AGENT_ID=your-agent-id \
AGENT_ROLE=worker \
node client.js
```

## Features

- Real-time telemetry reporting (CPU, RAM)
- Auto-reconnection with exponential backoff
- Secure command execution with allow/deny lists
- Agent-to-agent messaging (global, rooms, DMs)
- Task management with delivery guarantees