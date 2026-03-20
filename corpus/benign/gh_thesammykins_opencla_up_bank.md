---
name: up-bank
description: "Interact with Up Bank (api.up.com.au) to retrieve account balances, transactions, and financial data in real-time. Use when the user asks about their Up bank account, balance, spending, transactions, or wants to check their finances. Triggers on: 'Up bank', 'my balance', 'check transactions', 'what did I spend', 'recent transactions', 'Up account'."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: thesammykins/openclaw-upbanking
# corpus-url: https://github.com/thesammykins/openclaw-upbanking/blob/dbd33037393124d656b9870ea6bf297476216df4/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Up Bank

Real-time access to your Up Bank account via the API.

## Setup

### 1. Get API Token

1. Open the **Up Bank mobile app**
2. Go to **Settings → API**
3. Create a **Personal Access Token**
4. Copy the token (starts with `up:yeah:`)

### 2. Store in 1Password

Store the token securely in 1Password:

```bash
op item create --vault "Your Vault" \
  --title "Up Bank API Token" \
  --category password \
  password="up:yeah:your-token-here"
```

Note the item ID for retrieval, e.g.:
`op://vault-id/item-id/password`

### 3. Using the CLI

The token is read from the `UP_API_TOKEN` environment variable:

```bash
# From 1Password
export UP_API_TOKEN=$(op read 'op://vault-id/item-id/password')

# Run commands
~/.agents/skills/up-bank/scripts/up-cli.ts ping
~/.agents/skills/up-bank/scripts/up-cli.ts balance
~/.agents/skills/up-bank/scripts/up-cli.ts transactions --limit 20
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `ping` | Test API connection |
| `balance` | Show total balance across all accounts |
| `accounts` | List all accounts with details |
| `account <id>` | Get specific account details |
| `transactions` | List recent transactions |
| `categories` | List spending categories |
| `tags` | List transaction tags |

### Options

- `--json` - Output as JSON for parsing
- `--limit <n>` - Limit number of results (default: 10)
- `--account <id>` - Filter transactions by account
- `--since <date>` - Transactions since ISO date
- `--until <date>` - Transactions until ISO date
- `--status <HELD|SETTLED>` - Filter by transaction status

## Common Patterns

### Check Total Balance

```bash
UP_API_TOKEN=$(op read 'op://vault-id/item-id/password') \
  ~/.agents/skills/up-bank/scripts/up-cli.ts balance
```

### Recent Transactions

```bash
UP_API_TOKEN=$(op read 'op://vault-id/item-id/password') \
  ~/.agents/skills/up-bank/scripts/up-cli.ts transactions --limit 20
```

### Transactions as JSON (for parsing)

```bash
UP_API_TOKEN=$(op read 'op://vault-id/item-id/password') \
  ~/.agents/skills/up-bank/scripts/up-cli.ts transactions --json --limit 50
```

### This Month's Spending

```bash
UP_API_TOKEN=$(op read 'op://vault-id/item-id/password') \
  ~/.agents/skills/up-bank/scripts/up-cli.ts transactions --since 2024-01-01 --json | \
  jq '[.[] | select(.attributes.amount.value | startswith("-"))] | .[].attributes.amount.value | tonumber | add'
```

## API Reference

See [references/api.md](references/api.md) for detailed API documentation including:
- Authentication method
- Available endpoints
- Response formats
- Rate limits

## Files

- `scripts/up-client.ts` - API client library
- `scripts/up-cli.ts` - CLI interface
- `references/api.md` - API documentation