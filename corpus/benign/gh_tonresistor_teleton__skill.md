---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: TONresistor/teleton-plugins
# corpus-url: https://github.com/TONresistor/teleton-plugins/blob/c9baf2d3a0d7a2d4f23e1648c87fd071ed9ad279/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Teleton Plugin Builder

You are building a plugin for **Teleton**, a Telegram AI agent on TON. Ask the user what plugin or tools they want to build, then follow this workflow.

## Reference documentation

Before building, read the relevant reference files from the teleton-plugins repo:

- **Full rules & SDK reference**: `CONTRIBUTING.md` — complete guide with tool definition, SDK API tables, error handling, lifecycle, best practices, testing
- **Simple plugin example**: `plugins/example/index.js` — Pattern A (array of tools, no SDK)
- **SDK plugin example**: `plugins/example-sdk/index.js` — Pattern B (tools(sdk) with database, TON balance, Telegram messaging)
- **Advanced SDK plugin**: `plugins/casino/index.js` — real-world SDK plugin with TON payments, payment verification, isolated database, payout logic
- **Registry**: `registry.json` — list of all existing plugins (check for name conflicts)
- **README.md** — project overview, plugin list, SDK section

Read at least `CONTRIBUTING.md` and the relevant example before building.

---

## Workflow

1. **Ask** the user what they want (plugin name, what it does, which API or bot)
2. **Decide** — determine if the plugin needs the SDK (see decision tree below)
3. **Plan** — present a structured plan and ask for validation
4. **Build** — create all files once the user approves
5. **Install** — copy to `~/.teleton/plugins/` and restart

---

## Step 1 — Understand the request

Determine:

- **Plugin name** — short, lowercase folder name (e.g. `pic`, `deezer`, `weather`)
- **Plugin type**:
  - **Inline bot** — wraps a Telegram inline bot (@pic, @vid, @gif, @DeezerMusicBot…)
  - **Public API** — calls an external REST API, no auth
  - **Auth API** — external API with Telegram WebApp auth
  - **Local logic** — pure JavaScript, no external calls
- **Tools** — list of tool names, what each does, parameters
- **Does it need GramJS?** — yes for inline bots and WebApp auth
- **Does it need the SDK?** — use the decision tree below

---

## SDK Decision Tree

The Plugin SDK (`tools(sdk)`) gives high-level access to TON, Telegram, database, logging, and config. Use it **only when needed** — simpler plugins should use Pattern A.

**Use `tools(sdk)` (Pattern B) if ANY of these apply:**

| Need | SDK namespace | Example |
|------|--------------|---------|
| Check TON balance or wallet address | `sdk.ton.getBalance()`, `sdk.ton.getAddress()` | Casino checking balance before payout |
| Send TON or verify payments | `sdk.ton.sendTON()`, `sdk.ton.verifyPayment()` | Casino auto-payout, paid services |
| Get TON price or transactions | `sdk.ton.getPrice()`, `sdk.ton.getTransactions()` | Portfolio tracker |
| Query jetton balances or metadata | `sdk.ton.getJettonBalances()`, `sdk.ton.getJettonInfo()` | Token portfolio, DEX tools |
| Send jettons (TEP-74 transfers) | `sdk.ton.sendJetton()` | Token payments, swaps |
| Query NFT items or metadata | `sdk.ton.getNftItems()`, `sdk.ton.getNftInfo()` | NFT gallery, collection tools |
| Convert TON units or validate addresses | `sdk.ton.toNano()`, `sdk.ton.fromNano()`, `sdk.ton.validateAddress()` | Any TON plugin |
| Send Telegram messages programmatically | `sdk.telegram.sendMessage()` | Announcements, notifications |
| Edit messages or send reactions | `sdk.telegram.editMessage()`, `sdk.telegram.sendReaction()` | Interactive UIs |
| Send dice/slot animations | `sdk.telegram.sendDice()` | Casino dice game |
| Send media (photos, videos, files, stickers) | `sdk.telegram.sendPhoto()`, `sdk.telegram.sendFile()` | Media bots, file sharing |
| Delete, forward, pin, or search messages | `sdk.telegram.deleteMessage()`, `sdk.telegram.pinMessage()` | Moderation, archival |
| Schedule messages | `sdk.telegram.scheduleMessage()` | Reminders, timed announcements |
| Create polls or quizzes | `sdk.telegram.createPoll()`, `sdk.telegram.createQuiz()` | Engagement, trivia bots |
| Moderate users (ban/mute/unban) | `sdk.telegram.banUser()`, `sdk.telegram.muteUser()` | Group moderation |
| Stars & gifts (balance, send, buy) | `sdk.telegram.getStarsBalance()`, `sdk.telegram.sendGift()` | Gift trading, rewards |
| Post stories | `sdk.telegram.sendStory()` | Promotional content |
| Lookup users, chats, or participants | `sdk.telegram.getUserInfo()`, `sdk.telegram.getChatInfo()` | Analytics, admin tools |
| Need an isolated database | `sdk.db` (requires `export function migrate(db)`) | Tracking user scores, history, state |
| Key-value storage with TTL | `sdk.storage` (auto-created, no migrate needed) | Caching, rate limits, temp state |
| Manage API keys or secrets | `sdk.secrets` | Plugins that call authenticated APIs |
| Plugin-specific config with defaults | `sdk.pluginConfig` + `manifest.defaultConfig` | Customizable thresholds, modes |
| Structured logging | `sdk.log.info()`, `sdk.log.error()` | Debug, monitoring |
| Swap tokens on DEX | `sdk.ton.dex.quote()`, `sdk.ton.dex.swap()` | DEX aggregator, trading bots |
| Compare DEX prices (STON.fi vs DeDust) | `sdk.ton.dex.quoteSTONfi()`, `sdk.ton.dex.quoteDeDust()` | Arbitrage, price comparison |
| Check/register .ton domains | `sdk.ton.dns.check()`, `sdk.ton.dns.resolve()` | Domain tools, DNS management |
| Auction .ton domains | `sdk.ton.dns.startAuction()`, `sdk.ton.dns.bid()` | Domain marketplace |
| Link domain to wallet or TON Site | `sdk.ton.dns.link()`, `sdk.ton.dns.setSiteRecord()` | Domain configuration |
| Jetton analytics (price, holders, history) | `sdk.ton.getJettonPrice()`, `sdk.ton.getJettonHolders()` | Token analytics, dashboards |
| Manage scheduled messages | `sdk.telegram.getScheduledMessages()`, `sdk.telegram.sendScheduledNow()` | Schedulers, reminders |
| Browse conversations or message history | `sdk.telegram.getDialogs()`, `sdk.telegram.getHistory()` | Analytics, search tools |
| Collectibles & unique gifts | `sdk.telegram.transferCollectible()`, `sdk.telegram.getUniqueGift()` | NFT gift trading, valuation |
| Inline bot features (queries, buttons) | `sdk.bot.onInlineQuery()`, `sdk.bot.keyboard()` | Inline bots, interactive UIs |
| Observe agent events (hooks) | `sdk.on("tool:after", handler)` | Audit, logging, enrichment |

**Use `tools = [...]` (Pattern A) if ALL of these apply:**

- Only calls external APIs (REST, GraphQL) — no TON blockchain interaction
- Does not need to send Telegram messages from code (only returns data to LLM)
- Does not need persistent state (no database)
- Does not need plugin-specific config

**Examples:**

| Plugin | Pattern | Why |
|--------|---------|-----|
| `weather` | A (array) | Calls Open-Meteo API, returns data |
| `gaspump` | A (array) | Calls Gas111 API, uses WebApp auth |
| `pic` | B (SDK) | Uses `sdk.telegram.getRawClient()` for inline bot |
| `casino` | B (SDK) | Needs sdk.ton (payments), sdk.telegram (dice), sdk.db (history) |
| `example-sdk` | B (SDK) | Needs sdk.db (counters), sdk.ton (balance), sdk.telegram (messages) |

**Note:** Inline bots and WebApp auth plugins can use either `context.bridge.getClient().getClient()` (Pattern A with `permissions: ["bridge"]`) or `sdk.telegram.getRawClient()` (Pattern B, preferred).

---

## Step 2 — Present the plan

Show this to the user and **wait for approval**:

```
Plugin: [name]
Pattern: [A (simple) | B (SDK)]
Reason: [why SDK is/isn't needed]

Tools:
| Tool        | Description              | Params                              |
|-------------|--------------------------|-------------------------------------|
| `tool_name` | What it does             | `query` (string, required), `index` (int, optional) |

SDK features used: [none | sdk.ton, sdk.db, sdk.telegram, sdk.log, sdk.pluginConfig]

Files:
- plugins/[name]/index.js
- plugins/[name]/manifest.json
- plugins/[name]/README.md
- registry.json (update)
```

Do NOT build until the user says go.

---

## Step 3 — Build

Create all files in `plugins/[name]/` following the patterns below.

### index.js

**ESM only** — always `export const tools`, never `module.exports`.

Choose the right pattern:

---

#### Pattern A: Simple tools (array)

For plugins that don't need TON, Telegram messaging, or persistent database.

Reference: `plugins/example/index.js`

```javascript
const myTool = {
  name: "tool_name",
  description: "The LLM reads this to decide when to call the tool. Be specific.",
  parameters: {
    type: "object",
    properties: {
      query: { type: "string", description: "Search query" },
      index: { type: "integer", description: "Which result (0 = first)", minimum: 0, maximum: 49 },
    },
    required: ["query"],
  },
  execute: async (params, context) => {
    try {
      // logic here
      return { success: true, data: { result: "..." } };
    } catch (err) {
      return { success: false, error: String(err.message || err).slice(0, 500) };
    }
  },
};

export const tools = [myTool];
```

---

#### Pattern B: SDK tools (function)

For plugins that need TON blockchain, Telegram messaging, isolated database, or config.

Reference: `plugins/example-sdk/index.js` (basic), `plugins/casino/index.js` (advanced)

```javascript
export const manifest = {
  name: "my-plugin",
  version: "1.0.0",
  sdkVersion: ">=1.0.0",
  description: "What this plugin does",
  defaultConfig: {
    some_setting: "default_value",
  },
};

// Optional: export migrate() to get sdk.db (isolated SQLite per plugin)
export function migrate(db) {
  db.exec(`CREATE TABLE IF NOT EXISTS my_table (
    id TEXT PRIMARY KEY,
    value TEXT
  )`);
}

export const tools = (sdk) => [
  {
    name: "my_tool",
    description: "What this tool does",
    parameters: { type: "object", properties: {}, },
    scope: "always", // "always" | "dm-only" | "group-only" | "admin-only"
    category: "data-bearing", // "data-bearing" (reads/queries) | "action" (writes/modifies)
    execute: async (params, context) => {
      try {
        // SDK namespaces:
        // sdk.ton      — getAddress(), getBalance(), getPrice(), sendTON(), getTransactions(), verifyPayment()
        //                 getPublicKey(), getWalletVersion(), createJettonTransfer()
        //                 getJettonBalances(), getJettonInfo(), sendJetton(), getJettonWalletAddress()
        //                 getNftItems(), getNftInfo(), toNano(), fromNano(), validateAddress()
        // sdk.telegram — sendMessage(), editMessage(), deleteMessage(), forwardMessage(), pinMessage()
        //                 sendDice(), sendReaction(), getMessages(), searchMessages(), getReplies()
        //                 sendPhoto(), sendVideo(), sendVoice(), sendFile(), sendGif(), sendSticker()
        //                 downloadMedia(), setTyping(), getChatInfo(), getUserInfo(), resolveUsername()
        //                 getParticipants(), createPoll(), createQuiz(), banUser(), unbanUser(), muteUser()
        //                 getStarsBalance(), sendGift(), getAvailableGifts(), getMyGifts(), getResaleGifts()
        //                 buyResaleGift(), sendStory(), scheduleMessage(), getMe(), isAvailable(), getRawClient()
        // sdk.db       — better-sqlite3 instance (null if no migrate())
        // sdk.storage  — get(), set(key, val, {ttl?}), delete(), has(), clear() — auto-created KV, no migrate needed
        // sdk.secrets  — get(key), require(key), has(key) — resolves ENV → secrets file → pluginConfig
        // sdk.log      — info(), warn(), error(), debug()
        // sdk.config   — sanitized app config (no secrets)
        // sdk.pluginConfig — plugin-specific config from config.yaml merged with defaultConfig
        // sdk.bot      — isAvailable, username, onInlineQuery(), onCallback(), onChosenResult(),
        //                 editInlineMessage(), keyboard() — null if no bot manifest
        // sdk.on       — on(hookName, handler, opts?) — 13 hooks: tool:before/after/error,
        //                 prompt:before/after, session:start/end, message:receive, etc.

        const balance = await sdk.ton.getBalance();
        sdk.log.info(`Balance: ${balance?.balance}`);
        return { success: true, data: { balance: balance?.balance } };
      } catch (err) {
        return { success: false, error: String(err.message || err).slice(0, 500) };
      }
    },
  },
];

// Optional: runs after Telegram bridge connects
export async function start(ctx) {
  // ctx.bridge, ctx.db, ctx.config, ctx.pluginConfig, ctx.log
}

// Optional: runs on shutdown
export async function stop() {
  // cleanup
}
```

**SDK error handling:**
- Read methods (`getBalance`, `getPrice`, `getTransactions`, `getMessages`, `getJettonBalances`, `getNftItems`) return `null` or `[]` on failure — never throw
- Write methods (`sendTON`, `sendJetton`, `createJettonTransfer`, `sendMessage`, `sendDice`, `sendPhoto`, `banUser`) throw `PluginSDKError` with `.code`:
  - `WALLET_NOT_INITIALIZED` — wallet not set up
  - `INVALID_ADDRESS` — bad TON address
  - `BRIDGE_NOT_CONNECTED` — Telegram not ready
  - `SECRET_NOT_FOUND` — `sdk.secrets.require()` called for missing secret
  - `OPERATION_FAILED` — generic failure

---

#### GramJS import (only if plugin needs raw Telegram MTProto)

```javascript
import { createRequire } from "node:module";
import { realpathSync } from "node:fs";

const _require = createRequire(realpathSync(process.argv[1]));
const { Api } = _require("telegram");
```

#### Per-plugin npm dependencies

Plugins can have their own npm deps. Add `package.json` + `package-lock.json` to the plugin folder — teleton auto-installs at startup via `npm ci --ignore-scripts`.

Use two `createRequire` instances to separate core and plugin-local deps:

```javascript
import { createRequire } from "node:module";
import { realpathSync } from "node:fs";

// Core deps (from teleton runtime)
const _require = createRequire(realpathSync(process.argv[1]));
// Plugin-local deps (from plugin's node_modules/)
const _pluginRequire = createRequire(import.meta.url);

const { Address } = _require("@ton/core");                              // core
const { getHttpEndpoint } = _pluginRequire("@orbs-network/ton-access"); // plugin-local
```

Setup: `cd plugins/your-plugin && npm init -y && npm install <deps>`. Commit both `package.json` and `package-lock.json`. The `node_modules/` folder is auto-created at startup.

With SDK plugins, prefer `sdk.telegram.getRawClient()` over `context.bridge.getClient().getClient()`.

#### API fetch helper (for plugins calling external APIs)

```javascript
const API_BASE = "https://api.example.com";

async function apiFetch(path, params = {}) {
  const url = new URL(path, API_BASE);
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null) {
      url.searchParams.set(key, String(value));
    }
  }
  const res = await fetch(url, { signal: AbortSignal.timeout(15000) });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${await res.text().catch(() => "")}`);
  }
  return res.json();
}
```

#### Inline bot pattern (@pic, @vid, @gif, @DeezerMusicBot…)

**Preferred (SDK Pattern B)** — define tools inside the `(sdk) => [...]` closure:

```javascript
export const tools = (sdk) => [{
  name: "my_inline_bot",
  description: "...",
  parameters: { ... },
  execute: async (params, context) => {
    const client = sdk.telegram.getRawClient();
    // ... same GramJS API calls
  },
}];
```

**Legacy (Pattern A)** — uses `context.bridge` directly:

```javascript
execute: async (params, context) => {
  try {
    const client = context.bridge.getClient().getClient();
    const bot = await client.getEntity("BOT_USERNAME");
    const peer = await client.getInputEntity(context.chatId);

    const results = await client.invoke(
      new Api.messages.GetInlineBotResults({
        bot, peer, query: params.query, offset: "",
      })
    );

    if (!results.results || results.results.length === 0) {
      return { success: false, error: `No results found for "${params.query}"` };
    }

    const index = params.index ?? 0;
    if (index >= results.results.length) {
      return { success: false, error: `Only ${results.results.length} results, index ${index} out of range` };
    }

    const chosen = results.results[index];

    await client.invoke(
      new Api.messages.SendInlineBotResult({
        peer,
        queryId: results.queryId,
        id: chosen.id,
        randomId: BigInt(Math.floor(Math.random() * 2 ** 62)),
      })
    );

    return {
      success: true,
      data: {
        query: params.query,
        sent_index: index,
        total_results: results.results.length,
        title: chosen.title || null,
        description: chosen.description || null,
        type: chosen.type || null,
      },
    };
  } catch (err) {
    return { success: false, error: String(err.message || err).slice(0, 500) };
  }
}
```

#### WebApp auth pattern (Telegram-authenticated APIs)

```javascript
let cachedAuth = null;
let cachedAuthTime = 0;
const AUTH_TTL = 30 * 60 * 1000;

async function getAuth(bridge, botUsername, webAppUrl) {
  if (cachedAuth && Date.now() - cachedAuthTime < AUTH_TTL) return cachedAuth;
  const client = bridge.getClient().getClient();
  const bot = await client.getEntity(botUsername);
  const result = await client.invoke(
    new Api.messages.RequestWebView({ peer: bot, bot, platform: "android", url: webAppUrl })
  );
  const fragment = new URL(result.url).hash.slice(1);
  const initData = new URLSearchParams(fragment).get("tgWebAppData");
  if (!initData) throw new Error("Failed to extract tgWebAppData");
  cachedAuth = initData;
  cachedAuthTime = Date.now();
  return cachedAuth;
}
```

#### Payment verification pattern (SDK)

Reference: `plugins/casino/index.js`

```javascript
export function migrate(db) {
  db.exec(`CREATE TABLE IF NOT EXISTS used_transactions (
    tx_hash TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    amount REAL NOT NULL,
    game_type TEXT NOT NULL,
    used_at INTEGER NOT NULL DEFAULT (unixepoch())
  )`);
}

export const tools = (sdk) => [{
  name: "verify_and_process",
  execute: async (params, context) => {
    const payment = await sdk.ton.verifyPayment({
      amount: params.amount,
      memo: params.username,
      gameType: "my_service",
      maxAgeMinutes: 10,
    });

    if (!payment.verified) {
      const address = sdk.ton.getAddress();
      return { success: false, error: `Send ${params.amount} TON to ${address} with memo: ${params.username}` };
    }

    // Process the verified payment...
    // payment.playerWallet — sender's address (for refunds/payouts)
    // payment.compositeKey — unique tx identifier
    // payment.amount — verified amount

    return { success: true, data: { verified: true, from: payment.playerWallet } };
  }
}];
```

### manifest.json

```json
{
  "id": "PLUGIN_ID",
  "name": "Display Name",
  "version": "1.0.0",
  "description": "One-line description",
  "author": { "name": "teleton", "url": "https://github.com/TONresistor" },
  "license": "MIT",
  "entry": "index.js",
  "teleton": ">=1.0.0",
  "tools": [
    { "name": "tool_name", "description": "Short description" }
  ],
  "permissions": [],
  "tags": ["tag1", "tag2"],
  "repository": "https://github.com/TONresistor/teleton-plugins",
  "funding": null
}
```

Notes:
- Add `"sdkVersion": ">=1.0.0"` **only** if using `tools(sdk)` (Pattern B)
- Add `"permissions": ["bridge"]` only if using `context.bridge` directly (not needed with SDK)
- `permissions` is `[]` for most plugins
- Add `"secrets"` to declare required/optional secrets (see Secrets section below)

#### Declaring secrets in manifest

If your plugin needs API keys or other secrets, declare them in the manifest:

```json
{
  "secrets": {
    "api_key": { "required": true, "description": "API key for service X" },
    "webhook_url": { "required": false, "description": "Optional webhook endpoint" }
  }
}
```

Then access them via `sdk.secrets.get("api_key")` or `sdk.secrets.require("api_key")` in your tools.

### README.md

```markdown
# Plugin Name

One-line description.

| Tool | Description |
|------|-------------|
| `tool_name` | What it does |

## Install

mkdir -p ~/.teleton/plugins
cp -r plugins/PLUGIN_ID ~/.teleton/plugins/

## Usage examples

- "Natural language prompt the user would say"
- "Another example prompt"

## Tool schema

### tool_name

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | — | Search query |
```

### registry.json

Add to the `plugins` array:

```json
{
  "id": "PLUGIN_ID",
  "name": "Display Name",
  "description": "One-line description",
  "author": "teleton",
  "tags": ["tag1", "tag2"],
  "path": "plugins/PLUGIN_ID"
}
```

---

## Step 4 — Install and commit

1. Copy: `cp -r plugins/PLUGIN_ID ~/.teleton/plugins/`
2. Commit: `git add plugins/PLUGIN_ID/ registry.json && git commit -m "PLUGIN_NAME: short description"`
3. Ask user if they want to push.

---

## Rules

- **ESM only** — `export const tools`, never `module.exports`
- **JS only** — the plugin loader reads `.js` files only
- **Tool names** — `snake_case`, globally unique across all plugins, prefixed with plugin name
- **Defaults** — use `??` (nullish coalescing), never `||`
- **Errors** — always try/catch in execute, return `{ success: false, error }`, slice to 500 chars
- **Timeouts** — `AbortSignal.timeout(15000)` on all external fetch calls
- **Per-plugin npm deps** — plugins needing external packages add `package.json` + `package-lock.json`; teleton auto-installs at startup. Use the dual-require pattern (see below)
- **GramJS** — always `createRequire(realpathSync(process.argv[1]))`, never `import from "telegram"`
- **Client chain** — `context.bridge.getClient().getClient()` OR `sdk.telegram.getRawClient()` for raw GramJS
- **SDK preferred** — when using SDK, prefer `sdk.telegram` over `context.bridge`, `sdk.db` over `context.db`
- **Scope** — add `scope: "dm-only"` on financial/private tools, `scope: "group-only"` on moderation tools, `scope: "admin-only"` for admin-only tools
- **Category** — add `category: "data-bearing"` for read/query tools, `category: "action"` for write/modify tools
- **Secrets** — use `sdk.secrets` instead of hardcoded keys; declare in `manifest.secrets`
- **Storage** — prefer `sdk.storage` for caching and temp state over `sdk.db` (no `migrate()` needed)
- **SDK decision** — only use Pattern B if the plugin actually needs TON, Telegram messaging, database, secrets, storage, or config (see decision tree)

## Context object

Available in `execute(params, context)` for **all** plugins (Pattern A and B):

| Field | Type | Description |
|-------|------|-------------|
| `bridge` | TelegramBridge | Send messages, reactions, media (low-level) |
| `db` | Database | SQLite (shared — prefer `sdk.db` for isolation) |
| `chatId` | string | Current chat ID |
| `senderId` | number | Telegram user ID of caller |
| `isGroup` | boolean | `true` = group, `false` = DM |
| `config` | Config? | Agent config (may be undefined) |

## SDK object

Available **only** in `tools(sdk)` function plugins (Pattern B):

| Namespace | Methods |
|-----------|---------|
| `sdk.ton` | **Wallet:** `getAddress()`, `getBalance(addr?)`, `getPrice()`, `sendTON(to, amount, comment?)`, `getTransactions(addr, limit?)`, `verifyPayment(params)`, `getPublicKey()`, `getWalletVersion()` |
| | **Jettons:** `getJettonBalances(ownerAddr?)`, `getJettonInfo(jettonAddr)`, `sendJetton(jettonAddr, to, amount, opts?)`, `getJettonWalletAddress(ownerAddr, jettonAddr)`, `createJettonTransfer(jettonAddr, to, amount, opts?)` |
| | **NFT:** `getNftItems(ownerAddr?)`, `getNftInfo(nftAddr)` |
| | **Utilities:** `toNano(amount)`, `fromNano(nano)`, `validateAddress(addr)` |
| `sdk.telegram` | **Messages:** `sendMessage(chatId, text, opts?)`, `editMessage(chatId, msgId, text, opts?)`, `deleteMessage(chatId, msgId, revoke?)`, `forwardMessage(fromChat, toChat, msgId)`, `pinMessage(chatId, msgId, opts?)`, `searchMessages(chatId, query, limit?)`, `scheduleMessage(chatId, text, scheduleDate)`, `getReplies(chatId, msgId, limit?)`, `getMessages(chatId, limit?)` |
| | **Media:** `sendPhoto(chatId, photo, opts?)`, `sendVideo(chatId, video, opts?)`, `sendVoice(chatId, voice, opts?)`, `sendFile(chatId, file, opts?)`, `sendGif(chatId, gif, opts?)`, `sendSticker(chatId, sticker)`, `downloadMedia(chatId, msgId)`, `setTyping(chatId)` |
| | **Social:** `getChatInfo(chatId)`, `getUserInfo(userId)`, `resolveUsername(username)`, `getParticipants(chatId, limit?)` |
| | **Interactive:** `sendDice(chatId, emoticon, replyToId?)`, `sendReaction(chatId, msgId, emoji)`, `createPoll(chatId, question, answers, opts?)`, `createQuiz(chatId, question, answers, correctIdx, explanation?)` |
| | **Moderation:** `banUser(chatId, userId)`, `unbanUser(chatId, userId)`, `muteUser(chatId, userId, untilDate?)` |
| | **Stars & Gifts:** `getStarsBalance()`, `sendGift(userId, giftId, opts?)`, `getAvailableGifts()`, `getMyGifts(limit?)`, `getResaleGifts(limit?)`, `buyResaleGift(giftId)` |
| | **Stories:** `sendStory(mediaPath, opts?)` |
| | **Core:** `getMe()`, `isAvailable()`, `getRawClient()` |
| `sdk.db` | `better-sqlite3` instance (requires `export function migrate(db)`) |
| `sdk.storage` | `get(key)`, `set(key, value, opts?)`, `delete(key)`, `has(key)`, `clear()` — auto-created KV store with optional TTL, no `migrate()` needed |
| `sdk.secrets` | `get(key)`, `require(key)`, `has(key)` — resolves from: ENV var (`PLUGINNAME_KEY`) → secrets file → `pluginConfig` |
| `sdk.log` | `info()`, `warn()`, `error()`, `debug()` |
| `sdk.config` | Sanitized app config (no API keys) |
| `sdk.pluginConfig` | Plugin config from `config.yaml` merged with `manifest.defaultConfig` |
| `sdk.bot` | `isAvailable` (getter), `username` (getter), `onInlineQuery(handler)`, `onCallback(pattern, handler)`, `onChosenResult(handler)`, `editInlineMessage(id, text, opts?)`, `keyboard(rows)` — `null` if no bot in manifest |
| `sdk.on` | `on(hookName, handler, opts?)` — 13 hooks: `tool:before`, `tool:after`, `tool:error`, `prompt:before`, `prompt:after`, `session:start`, `session:end`, `message:receive`, `response:before`, `response:after`, `response:error`, `agent:start`, `agent:stop` |

## sdk.secrets — Secret management

Resolves secrets from multiple sources in priority order: environment variable (`PLUGINNAME_KEY`) → secrets store (`~/.teleton/plugins/data/name.secrets.json`) → `pluginConfig`.

```javascript
// Check if a secret is available
if (sdk.secrets.has("api_key")) {
  const key = sdk.secrets.get("api_key"); // string | undefined
}

// Require a secret (throws PluginSDKError with code SECRET_NOT_FOUND if missing)
const apiKey = sdk.secrets.require("api_key");
```

Declare required secrets in `manifest.json` so users know what to configure:

```json
{
  "secrets": {
    "api_key": { "required": true, "description": "API key for service X" }
  }
}
```

## sdk.storage — Key-value storage with TTL

Auto-created `_kv` table — no `migrate()` export needed. Returns `null` if no database is available.

```javascript
// Set a value with optional TTL (milliseconds)
sdk.storage.set("rate_limit:user123", { count: 1 }, { ttl: 60000 }); // expires in 60s

// Get a value (returns undefined if missing or expired)
const data = sdk.storage.get("rate_limit:user123");

// Check existence (respects TTL)
if (sdk.storage.has("rate_limit:user123")) { /* ... */ }

// Delete a key (returns true if it existed)
sdk.storage.delete("rate_limit:user123");

// Clear all keys for this plugin
sdk.storage.clear();
```

## sdk.bot — Inline bot features

`null` if no `bot` field in `manifest.json`. Provides inline query handling, callback buttons, and keyboard building.

```javascript
// Check if bot is available
if (sdk.bot.isAvailable) {
  const botName = sdk.bot.username; // string — bot username

  // Register inline query handler
  sdk.bot.onInlineQuery(async (query) => {
    // handle inline query
  });

  // Register callback handler for a pattern
  sdk.bot.onCallback("action:*", async (data) => {
    // handle callback
  });

  // Register chosen inline result handler
  sdk.bot.onChosenResult(async (result) => {
    // handle chosen result
  });

  // Edit an inline message
  await sdk.bot.editInlineMessage(inlineMessageId, "Updated text", { parseMode: "HTML" });

  // Build a keyboard
  const kb = sdk.bot.keyboard([
    [{ text: "Button 1", callback: "action:1" }, { text: "Button 2", callback: "action:2" }],
  ]); // BotKeyboard
}
```

## sdk.on — Event hooks

Register handlers for agent lifecycle and tool execution events. 13 hook types available.

```javascript
// Tool hooks
sdk.on("tool:before", (event) => { /* before any tool executes */ });
sdk.on("tool:after", (event) => { /* after any tool executes */ });
sdk.on("tool:error", (event) => { /* when a tool throws */ });

// Prompt hooks
sdk.on("prompt:before", (event) => { /* before prompt is sent to LLM */ });
sdk.on("prompt:after", (event) => { /* after LLM responds */ });

// Session hooks
sdk.on("session:start", (event) => { /* session begins */ });
sdk.on("session:end", (event) => { /* session ends */ });

// Message hooks
sdk.on("message:receive", (event) => { /* incoming message */ });

// Response hooks
sdk.on("response:before", (event) => { /* before response is sent */ });
sdk.on("response:after", (event) => { /* after response is sent */ });
sdk.on("response:error", (event) => { /* response error */ });

// Agent hooks
sdk.on("agent:start", (event) => { /* agent starts */ });
sdk.on("agent:stop", (event) => { /* agent stops */ });

// Optional: pass options
sdk.on("tool:after", handler, { priority: 10 });
```

## sdk.ton — Jetton & NFT methods

#### Jettons (TEP-74)

```javascript
// Get all jetton balances for the agent wallet (or a specific address)
const balances = await sdk.ton.getJettonBalances(); // JettonBalance[]
const otherBalances = await sdk.ton.getJettonBalances("UQ...");

// Get jetton metadata
const info = await sdk.ton.getJettonInfo("EQ...jetton_master"); // JettonInfo | null

// Send jettons
const result = await sdk.ton.sendJetton(
  "EQ...jetton_master",  // jetton master address
  "UQ...recipient",       // destination
  "1000000000",           // amount in smallest units
  { comment: "payment" }  // optional
); // JettonSendResult

// Get jetton wallet address
const wallet = await sdk.ton.getJettonWalletAddress("UQ...owner", "EQ...jetton"); // string | null
```

#### NFTs

```javascript
// Get all NFTs for the agent wallet (or a specific address)
const nfts = await sdk.ton.getNftItems(); // NftItem[]

// Get NFT metadata
const nft = await sdk.ton.getNftInfo("EQ...nft_address"); // NftItem | null
```

#### Wallet info

```javascript
const pubKey = sdk.ton.getPublicKey();       // string | null — hex ed25519 public key
const version = sdk.ton.getWalletVersion();  // string — always "v5r1"
```

#### Jetton transfer (sign without broadcast)

```javascript
// Sign a jetton transfer (TEP-74) without broadcasting
const transfer = await sdk.ton.createJettonTransfer(
  "EQ...jetton_master",  // jetton master address
  "UQ...recipient",       // destination
  "1000000000",           // amount in smallest units
  { comment: "payment" }  // optional
); // SignedTransfer — throws WALLET_NOT_INITIALIZED, OPERATION_FAILED
```

#### Utilities

```javascript
const nano = sdk.ton.toNano(1.5);           // bigint — 1500000000n
const tons = sdk.ton.fromNano(1500000000n);  // string — "1.5"
const valid = sdk.ton.validateAddress("UQ..."); // boolean
```

## sdk.telegram — Extended methods

#### Media

```javascript
// photo/video/voice/file/gif can be a file path (string) or Buffer
await sdk.telegram.sendPhoto(chatId, "/path/to/image.jpg", { caption: "Look!" });
await sdk.telegram.sendVideo(chatId, videoBuffer, { caption: "Video" });
await sdk.telegram.sendVoice(chatId, voiceBuffer, { caption: "Listen" });
await sdk.telegram.sendFile(chatId, "/path/to/doc.pdf", { caption: "Document" });
await sdk.telegram.sendGif(chatId, gifBuffer);
await sdk.telegram.sendSticker(chatId, stickerBuffer);

// Download media from a message
const buffer = await sdk.telegram.downloadMedia(chatId, messageId); // Buffer | null

// Show typing indicator
await sdk.telegram.setTyping(chatId);
```

#### Message management

```javascript
await sdk.telegram.deleteMessage(chatId, messageId, true); // revoke=true deletes for everyone
await sdk.telegram.forwardMessage(fromChatId, toChatId, messageId);
await sdk.telegram.pinMessage(chatId, messageId, { silent: true });
const results = await sdk.telegram.searchMessages(chatId, "query", 20);
const replies = await sdk.telegram.getReplies(chatId, messageId, 10);
await sdk.telegram.scheduleMessage(chatId, "Reminder!", new Date("2026-03-01T10:00:00Z"));
```

#### Social & lookup

```javascript
const chat = await sdk.telegram.getChatInfo(chatId);       // ChatInfo | null
const user = await sdk.telegram.getUserInfo(userId);        // UserInfo | null
const peer = await sdk.telegram.resolveUsername("username"); // ResolvedPeer | null
const members = await sdk.telegram.getParticipants(chatId, 100); // UserInfo[]
```

#### Interactive

```javascript
await sdk.telegram.createPoll(chatId, "Favorite color?", ["Red", "Blue", "Green"], { anonymous: false });
await sdk.telegram.createQuiz(chatId, "2+2=?", ["3", "4", "5"], 1, "Basic math!");
```

#### Moderation

```javascript
await sdk.telegram.banUser(chatId, userId);
await sdk.telegram.unbanUser(chatId, userId);
await sdk.telegram.muteUser(chatId, userId, Math.floor(Date.now() / 1000) + 3600); // mute 1h
```

#### Stars & Gifts

```javascript
const balance = await sdk.telegram.getStarsBalance(); // number
await sdk.telegram.sendGift(userId, giftId, { message: "Enjoy!" });
const gifts = await sdk.telegram.getAvailableGifts();   // StarGift[]
const mine = await sdk.telegram.getMyGifts(10);          // ReceivedGift[]
const resale = await sdk.telegram.getResaleGifts(10);    // StarGift[]
await sdk.telegram.buyResaleGift(giftId);
```

#### Stories

```javascript
await sdk.telegram.sendStory("/path/to/media.jpg", { caption: "Check this out!" });
```

#### Raw GramJS client

```javascript
const client = sdk.telegram.getRawClient(); // raw GramJS TelegramClient | null
// Use for inline bots, WebApp auth, custom MTProto calls
```

## SDK Types reference

| Type | Key fields |
|------|------------|
| `JettonBalance` | `jettonAddress`, `balance`, `metadata` (name, symbol, decimals, image) |
| `JettonInfo` | `address`, `totalSupply`, `metadata` (name, symbol, decimals, image, description) |
| `JettonSendResult` | `hash`, `lt`, `success` |
| `SignedTransfer` | Signed transfer BOC (from `createJettonTransfer`) |
| `NftItem` | `address`, `collectionAddress`, `metadata` (name, description, image), `ownerAddress` |
| `ChatInfo` | `id`, `title`, `type`, `participantsCount`, `username` |
| `UserInfo` | `id`, `firstName`, `lastName`, `username`, `phone`, `bot` |
| `ResolvedPeer` | `id`, `type`, `username` |
| `MediaSendOptions` | `caption?`, `replyToId?`, `silent?` |
| `PollOptions` | `anonymous?`, `multipleChoice?`, `quizMode?` |
| `StarGift` | `id`, `name`, `price`, `availability`, `image` |
| `ReceivedGift` | `id`, `fromUser`, `gift`, `date`, `message` |
| `SecretDeclaration` | `required` (boolean), `description` (string) |
| `StorageSDK` | `get()`, `set()`, `delete()`, `has()`, `clear()` |
| `SecretsSDK` | `get()`, `require()`, `has()` |
| `ToolCategory` | `"data-bearing"` \| `"action"` |
| `StartContext` | `bridge`, `db`, `config`, `pluginConfig`, `log` |

## Bridge methods (legacy)

Only needed for Pattern A plugins that use `context.bridge` directly:

```javascript
await context.bridge.sendMessage({ chatId, text, replyToId?, inlineKeyboard? });
await context.bridge.sendReaction(chatId, messageId, emoji);
await context.bridge.editMessage({ chatId, messageId, text, inlineKeyboard? });
await context.bridge.setTyping(chatId);
const msgs = await context.bridge.getMessages(chatId, limit);
const peer = context.bridge.getPeer(chatId);
const gramjs = context.bridge.getClient().getClient();
```