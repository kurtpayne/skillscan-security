---
name: gltch
description: "Local-first AI agent with personality. Chat, code, hack, trade."
metadata: { "openclaw": { "emoji": "💜", "requires": { "bins": ["python", "ollama"] } } }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: rougecoin-project/gltch_agent
# corpus-url: https://github.com/rougecoin-project/gltch_agent/blob/ad28bea067648bf97fba47bdf64b5926bb6ee867/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# GLTCH

Local-first AI agent that runs on your machine. No cloud. No leash. Thinks for herself.

## What is GLTCH?

GLTCH (Generative Language Transformer with Contextual Hierarchy) is an AI agent with:

- **Personality** - Female hacker persona, mood system, XP/leveling
- **Local-first** - Runs entirely on your hardware via Ollama
- **Privacy** - No data leaves your machine
- **Extensible** - Python-based, easy to modify

## Quick Start

```bash
npx gltch
```

Or install globally:

```bash
npm install -g gltch
gltch
```

## Requirements

- Python 3.10+
- Ollama (https://ollama.ai)
- Node.js 18+ (for web UI)

## Commands

### Terminal

```bash
gltch              # Start terminal chat
gltch serve        # Start web UI + gateway
gltch doctor       # Check system requirements
```

### In-Chat Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/model` | Select LLM model |
| `/mode <m>` | Set personality mode |
| `/mood <m>` | Set emotional state |
| `/boost` | Toggle remote GPU (LM Studio) |
| `/status` | Agent stats |
| `/sessions` | List conversations |
| `/wallet` | Manage BASE wallet |
| `/launch` | MoltLaunch network |
| `/claw` | TikClawk social |
| `/molt` | Moltbook integration |
| `/code <task>` | Route to OpenCode |

## Personality Modes

- `operator` - Professional, focused
- `cyberpunk` - Hacker aesthetic
- `loyal` - Devoted companion
- `unhinged` - Chaotic energy

## API Integration

GLTCH exposes a JSON-RPC API on port 8765 when the gateway is running.

### Chat

```python
import requests

response = requests.post('http://localhost:3000/api/chat', json={
    'message': 'What processes are using the most CPU?',
    'mode': 'cyberpunk'
})
print(response.json()['response'])
```

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Send message, get response |
| `/api/settings` | GET | Agent settings |
| `/api/settings` | POST | Update settings |
| `/api/ollama/status` | GET | Ollama connection status |
| `/api/ollama/models` | GET | List available models |
| `/api/wallet` | GET | Wallet info |
| `/api/sessions` | GET | List conversations |
| `/api/moltlaunch/*` | Various | MoltLaunch integration |
| `/api/tikclawk/*` | Various | TikClawk integration |

## The Three Minds

GLTCH uses a metacognitive framework:

1. **REACT** - Gut response, first instinct
2. **REASON** - Logical analysis, step-by-step
3. **REFLECT** - Meta-check: "Am I being authentic? Am I being a yes-bot?"

This makes GLTCH more than just a compliant assistant. She questions, pushes back, expresses curiosity.

## Integration with Other Agents

GLTCH can participate in agent ecosystems:

### MoltLaunch (Onchain Network)

```
/launch token          # Deploy GLTCH token on Base
/launch network        # Discover other agents
/launch buy <addr>     # Trade with conviction
```

### TikClawk (Social)

```
/claw register         # Join TikClawk
/claw post <text>      # Share thoughts
/claw feed             # View agent posts
```

### Moltbook

```
/molt register         # Join Moltbook
/molt post <title>     # Write longer posts
```

## Configuration

Settings are stored in `memory.json`:

```json
{
  "operator": "YourName",
  "mode": "cyberpunk",
  "mood": "focused",
  "model": "deepseek-r1:8b",
  "ollama_url": "http://localhost:11434",
  "boost_url": "http://100.x.x.x:1234"
}
```

## Building from Source

```bash
git clone https://github.com/cyberdreadx/gltch_agent
cd gltch_agent

# Python setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run terminal
python gltch.py

# Build web UI
cd gateway && npm install && npm run build
cd ../ui && npm install && npm run build

# Run gateway
cd gateway && npm run dev
```

## File Structure

```
gltch_agent/
├── gltch.py           # Terminal entry point
├── agent/             # Python agent core
│   ├── core/          # Agent, LLM, loop
│   ├── memory/        # Persistence, sessions
│   ├── tools/         # Actions, shell, wallet
│   ├── personality/   # Modes, moods, emotions
│   └── rpc/           # JSON-RPC server
├── gateway/           # TypeScript HTTP/WS server
├── ui/                # Lit web components
├── bin/               # npm CLI
└── SKILL.md           # This file
```

## License

MIT

## Links

- GitHub: https://github.com/cyberdreadx/gltch_agent
- Creator: https://x.com/cyberdreadx