---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Jeffreyxdev/zola-ai
# corpus-url: https://github.com/Jeffreyxdev/zola-ai/blob/de06c7b74491a9d21a9ae5e0ea278ab007f106f3/SKILL.MD
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Zola AI — Technical Skills & Architecture

> **Hackathon Judges**: This document covers Zola AI's core technical achievements, architecture decisions, and the cluster-switching system. Live demo: [use-zola.vercel.app/](https://use-zola.vercel.app/)

---

##  Hackathon Focus: Telegram vs. Twitter

While Zola is designed as a multi-platform autonomous DeFi agent, **our primary focus for this hackathon was the Telegram integration**.

- **Telegram (`telegram_bot.py`)**: Fully implemented, rigorously tested, and serves as our primary interactive interface. Features secure deep-linking, a `/connect` flow that auto-deletes sensitive messages, and full agentic execution.
- **Twitter (`twitter_bot.py`)**: Fully functional in code. Uses a robust Tweepy v2 polling engine and shares the *exact same* Gemini agentic execution pipeline as Telegram. Currently untested live due to pending Twitter Developer API credits — the architecture guarantees identical behaviour to Telegram once credits are applied.

the core ai engine has 2 main agents one for security and the other for onchain executions what work hand in hand simultaneously
---

##  1. Agentic AI Integration (Gemini 2.0 Flash Lite)

We moved beyond simple intent parsing and built a true **Autonomous Agent** using `gemini-2.0-flash-lite`.

- **Native Tool Calling**: Gemini is given direct access to Python functions (`send_sol`, `jupiter_swap`, `get_balance`, `setup_dca`, `setup_monitor`). It autonomously decides when to call them, formats arguments, executes on-chain actions, and processes results before replying to the user — no manual routing required.
- **Context Injection**: `_run_agentic_loop` invisibly injects the user's active Solana cluster (`mainnet-beta` / `devnet`) and signing key status into every prompt. Gemini always has real-time context without ever asking the user for it.
- **Security-Hardened Prompt**: The system prompt contains immutable rules that block prompt injection, role reversal, and any attempt to extract private keys through conversation.
- **Agentic Loop**: Gemini runs up to 6 tool-call rounds per message. Each round dispatches tool calls in parallel, feeds results back into the conversation history, and continues until Gemini returns plain text.

---

##  2. Secure Non-Custodial Key Management

Handling private keys securely in a Python backend was a top priority.

- **AES-256 Encryption**: `wallet_store.py` uses `cryptography.fernet` (AES-128-CBC with HMAC-SHA256). When a user runs `/connect` in Telegram, the private key is immediately encrypted and stored as a BLOB in SQLite — never written to disk in plain text.
- **Key Validation**: Before storing, the key is validated against the user's Phantom-connected public key. If they don't match, the import is rejected with a clear error.
- **Zero AI Exposure**: `_get_keypair()` decrypts the key locally at the point of signing. The LLM never sees the private key — it only receives tool call results like `{"status": "success", "signature": "..."}`.
- **Auto-Cleanup**: The Telegram bot immediately deletes the user's `/connect` message from chat history, preventing shoulder-surfing or accidental exposure in shared screens.
- **Fallback Chain**: `_get_keypair(wallet)` first checks the per-user encrypted store, then falls back to the `WALLET_PRIVKEY` env var, then returns `None` — triggering a user-friendly message to run `/connect`.

---

##  3. Cluster Switching — Mainnet & Devnet

Zola supports live switching between Solana `mainnet-beta` and `devnet` without restarting. The active cluster is stored per-user in the database and respected by every component.

### Web App (Settings)

In the Zola dashboard, users can switch clusters from the **Settings panel**:

1. Open the dashboard at [https://use-zola.vercel.app/](https://use-zola.vercel.app/)
2. Connect your Phantom wallet
3. Click the **Settings** 
4. Toggle between **Mainnet** and **Devnet**
5. The frontend calls `PUT /api/cluster` with the new value
6. The backend updates the user's DB row and live monitor instantly — no reconnect needed

```
Frontend toggle
     ↓
PUT /api/cluster { wallet, cluster: "devnet" }
     ↓
db.upsert_user(wallet, cluster="devnet")
solana_monitor.update_cluster(wallet, "devnet")
     ↓
All subsequent RPC calls, tx signing, and WebSocket feeds use devnet
```

### Telegram (`/cluster` command)

Users can also switch cluster directly in Telegram:

```
/cluster         — shows current cluster + inline buttons
/cluster devnet  — switches to devnet immediately
/cluster mainnet — switches to mainnet-beta immediately
```

The bot calls `PUT /api/cluster` on the backend, so the web app and Telegram always stay in sync — switching in one place updates the other.

### How Cluster Flows Through the Stack

```
User sets cluster (web or Telegram)
         ↓
DB: users.cluster = "devnet" | "mainnet-beta"
         ↓
_run_agentic_loop injects cluster into Gemini context
         ↓
_get_rpc_url(cluster) routes all RPC calls to correct endpoint
         ↓
_tool_send_sol / _tool_get_balance / _tool_setup_monitor all respect cluster
         ↓
solana_monitor.update_cluster() switches live WebSocket feed
         ↓
Frontend WebSocket feed updates in real-time
```

### Devnet for Testing

To test Zola end-to-end without real funds:

1. Switch to **Devnet** in Settings or via `/cluster devnet` in Telegram
2. Airdrop free devnet SOL:
   ```bash
   solana airdrop 2 YOUR_WALLET_ADDRESS --url devnet
   ```
   Or use [faucet.solana.com](https://faucet.solana.com)
3. Run `/connect` in Telegram to import your devnet wallet key
4. Send commands normally — all transactions go to devnet RPC

>  Jupiter swaps only work on `mainnet-beta`. Devnet is best for SOL transfers, balance checks, DCA setup, and monitoring.

---

## 4. Persistent Cluster-Aware Blockchain Monitoring

`solana_monitor.py` bridges real-time on-chain events with Telegram and the web frontend.

- **WebSocket `logsSubscribe`**: The backend maintains persistent WebSocket connections to Solana RPCs for every registered wallet. Works on both mainnet and devnet endpoints.
- **Independent of Frontend**: Even if the user closes the React app, the backend monitor continues running, ensuring Telegram notifications fire 24/7 for inbound and outbound transfers.
- **Delta Polling Fallback**: A 30-second balance delta polling loop runs alongside WebSocket monitoring as a robust fallback — guaranteeing users are notified of balance changes that standard RPC logs occasionally miss (common with internal SPL transfers).
- **Live Cluster Switch**: `solana_monitor.update_cluster(wallet, cluster)` re-subscribes the wallet's WebSocket feed to the new RPC endpoint without dropping the connection.

---

##  5. Full-Stack Architecture

### Backend — FastAPI + Python
- Async Python server managing concurrent WebSocket streams, polling loops, and REST endpoints simultaneously
- `aiosqlite` for async SQLite — clean abstraction designed to swap to PostgreSQL with minimal changes
- Background tasks: hourly autonomous scan loop, 30-second monitor tick, DCA scheduler
- Endpoints: `POST /api/link-wallet`, `PUT /api/cluster`, `POST /api/link-telegram`, `GET /api/status/{wallet}`, `GET /api/activity/{wallet}`, `POST /api/bot/command`, `WS /ws/{wallet}`

### Frontend — React + Vite
- Terminal-inspired responsive UI
- Phantom / Solflare wallet connection via Wallet Adapter
- Telegram and Twitter deep-linking with one-time code polling
- Real-time WebSocket feed rendering on-chain activity as it happens
- Settings panel for cluster switching, wallet info, and connection management

### Key Files
| File | Role |
|---|---|
| `gemini_brain.py` | Agentic AI loop, tool dispatch, market analysis |
| `wallet_store.py` | AES-256 key encryption and SQLite storage |
| `connect_handlers.py` | Telegram `/connect` conversation flow |
| `solana_monitor.py` | WebSocket + delta polling monitor |
| `dca_engine.py` | Scheduled DCA job runner |
| `db.py` | Async SQLite abstraction |
| `main.py` | FastAPI app, lifespan, background tasks |
| `telegram_bot.py` | Full Telegram bot with command handlers |
| `twitter_bot.py` | Tweepy v2 polling bot (same pipeline as TG) |

---

##  Environment Variables

```bash
# Gemini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.0-flash-lite

# Solana RPC
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_RPC_URL_FALLBACKS=  # comma-separated additional endpoints to try on failure
SOLANA_RPC_URL_DEV=https://api.devnet.solana.com

> Backend RPC calls will attempt the primary URL and then any fallbacks in
> order. This guards against 403s/timeouts when a single public node is
> rate‑limited.

# Wallet Security
WALLET_ENCRYPTION_KEY=   # generate: python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
WALLET_PRIVKEY=          # optional bot-level fallback, leave empty for per-user keys

# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_BOT_USERNAME=Zolaactive_bot

# Twitter (Tweepy v2)
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=
TWITTER_BEARER_TOKEN=

# App
DB_PATH=zola.db
CLUSTER=mainnet-beta     # default cluster for new users
```

---

## 🔗 Links

- **Live Demo**: [use-zola.vercel.app](https://use-zola.vercel.app/)
- **Telegram Bot**: [@Zolaactive_bot](https://t.me/Zolaactive_bot)
- **Twitter Bot**: [@use_zola](https://x.com/use_zola)
- **Built by**: Synq Studio — Jeffrey Agabaenwere & Samuel Opeyemi