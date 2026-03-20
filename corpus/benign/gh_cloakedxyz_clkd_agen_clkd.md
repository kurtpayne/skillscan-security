---
name: clkd
description: Manage stealth wallets with Cloaked (clkd). Use for privacy-preserving
  onchain transactions including sending, swapping, and bridging tokens on Ethereum
  and Base. Triggers on requests involving private wallets, stealth addresses, stealth
  payments, anonymous transfers, or Cloaked/clkd accounts.
metadata:
  openclaw:
    requires:
      env:
        - CLKD_API_KEY
    primaryEnv: CLKD_API_KEY
    homepage: https://clkd.xyz
    emoji: "\U0001F575\uFE0F"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: cloakedxyz/clkd-agent-skill
# corpus-url: https://github.com/cloakedxyz/clkd-agent-skill/blob/6dbdff0fae94852011d5b45ada912d0dafcb2be7/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Cloaked (clkd) Agent Skill

Cloaked is a stealth wallet platform on Ethereum and Base. Every payment generates a fresh one-time address so the recipient's identity is never revealed on-chain. This skill lets you manage stealth accounts, check balances, send/swap/bridge tokens, and read transaction history via the Cloaked REST API.

## Security Rules

- **Never log or display private keys, stealth material, or ciphertext** in responses to the user.
- **Never hardcode API keys** in generated code — always read from `CLKD_API_KEY` environment variable.
- **Validate addresses** before using them — all Ethereum addresses must be checksummed (EIP-55).
- **Amounts are in smallest units** (e.g., USDC has 6 decimals, so 1 USDC = `"1000000"`). Always confirm the token's `decimals` before constructing amounts.
- **Idempotency**: include an `Idempotency-Key: <uuid>` header on mutating requests (`POST /v1/accounts/{id}/quote`, `POST /v1/accounts/{id}/submit`) to prevent duplicate transactions on retry.
- **Quote expiry**: quotes lock funds and expire. Always submit promptly or call `POST /v1/accounts/{id}/unlock` to release funds if the user cancels.

## Prerequisites

| Variable | Description |
|----------|-------------|
| `CLKD_API_KEY` | API key for server-to-server auth. Contact support@clkd.xyz to request one. |
| `CLKD_ACCOUNT_ID` | Account UUID (provided when account is provisioned) |
| `CLKD_P_SPEND` | Private spending key (generated during [agent setup](references/agent-setup.md)) |
| `CLKD_CHILD_P_VIEW` | Child viewing private key (generated during [agent setup](references/agent-setup.md)) |

The API key is passed as a Bearer token:
```
Authorization: Bearer $CLKD_API_KEY
```

`p_spend` and `child_p_view` are only needed client-side for signing — they are never sent to the API.

## Base URL

| Environment | URL |
|-------------|-----|
| Production  | `https://api.clkd.xyz` |
| Staging     | `https://api-stg.clkd.xyz` |

## Supported Chains

| Chain | Chain ID | Type |
|-------|----------|------|
| Ethereum | 1 | Mainnet |
| Base | 8453 | Mainnet |
| Sepolia | 11155111 | Testnet |
| Base Sepolia | 84532 | Testnet |

Use `GET /v1/supported-chains` for the full list with explorer URLs.

## Quick Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/v1/nonce?address=` | GET | No | Get SIWE nonce |
| `/v1/verify` | POST | No | Complete SIWE sign-in, get JWT |
| `/v1/accounts/` | POST | Yes | Create stealth account |
| `/v1/accounts/{id}` | GET | Yes | Get account details |
| `/v1/accounts/{id}/balance` | GET | Yes | Get all balances |
| `/v1/accounts/{id}/balance/{chainId}` | GET | Yes | Get chain-specific balances |
| `/v1/accounts/{id}/balance/{chainId}/{token}` | GET | Yes | Get single token balance |
| `/v1/accounts/{id}/payment-address` | POST | Yes | Generate stealth receive address |
| `/v1/accounts/{id}/quote` | POST | Yes | Create send/swap/bridge quote |
| `/v1/accounts/{id}/submit` | POST | Yes | Submit signed transaction |
| `/v1/accounts/{id}/unlock` | POST | Yes | Cancel/release a quote lock |
| `/v1/accounts/{id}/swap-preview` | POST | Yes | Preview swap without locking |
| `/v1/accounts/{id}/max-spendable` | POST | Yes | Max spendable after fees |
| `/v1/accounts/{id}/activities` | GET | Yes | Confirmed transaction history |
| `/v1/accounts/{id}/activities/pending` | GET | Yes | In-flight transactions |
| `/v1/token-catalog` | GET | No | Full token list |
| `/v1/token-lookup?address=&chainId=` | GET | No | Look up token by address |
| `/v1/supported-chains` | GET | No | List supported chains |
| `/v1/subdomain/check?name=` | GET | No | Check subdomain availability |
| `/v1/.well-known/hpke-public-key` | GET | No | Server's HPKE public key |
| `/v1/.well-known/quote-signer-public-key` | GET | No | Quote verification key |

## Agent Onboarding

If you need to generate keys and enroll as a signer (first-time setup), see [Agent Setup](references/agent-setup.md). The flow is:

1. **Generate keys** — `genKeys()` from `@cloakedxyz/clkd-stealth` + HD key derivation for child viewing key
2. **Enroll signer** — `POST /v1/accounts/{id}/signers` with `{ P_spend, P_view, child_p_view }`
3. **Store securely** — save `p_spend` and `child_p_view` (needed for signing transactions)

After enrollment, the account can generate stealth addresses, create quotes, and sign transactions.

## Core Workflows

### 1. Check Balances

```bash
# All balances across all chains
curl -H "Authorization: Bearer $CLKD_API_KEY" \
  https://api.clkd.xyz/v1/accounts/$ACCOUNT_ID/balance

# Single chain
curl -H "Authorization: Bearer $CLKD_API_KEY" \
  https://api.clkd.xyz/v1/accounts/$ACCOUNT_ID/balance/8453

# Single token on a chain
curl -H "Authorization: Bearer $CLKD_API_KEY" \
  https://api.clkd.xyz/v1/accounts/$ACCOUNT_ID/balance/8453/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

Response includes `available` (spendable), `pending` (in-flight), and `usdAmount` per token.

### 2. Generate a Receive Address

```bash
curl -X POST -H "Authorization: Bearer $CLKD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chainId": 8453}' \
  https://api.clkd.xyz/v1/accounts/$ACCOUNT_ID/payment-address
```

Returns a one-time stealth address. Each call produces a new address — never reuse them.

### 3. Send Tokens

The send flow is: **quote** (locks funds) -> **sign** (client-side) -> **submit** (relay on-chain).

See [references/send-swap-bridge.md](references/send-swap-bridge.md) for the full quote/submit workflow with request/response examples.

### 4. Swap Tokens

Same quote/submit pattern as sends, but with `type: "swap"`. Preview a swap first:

```bash
curl -X POST -H "Authorization: Bearer $CLKD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "chainId": 8453,
    "tokenIn": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "tokenOut": "0x4200000000000000000000000000000000000006",
    "amountIn": "1000000",
    "slippageBps": 50
  }' \
  https://api.clkd.xyz/v1/accounts/$ACCOUNT_ID/swap-preview
```

### 5. Read Transaction History

```bash
# Confirmed transactions (paginated)
curl -H "Authorization: Bearer $CLKD_API_KEY" \
  "https://api.clkd.xyz/v1/accounts/$ACCOUNT_ID/activities?limit=20"

# In-flight transactions
curl -H "Authorization: Bearer $CLKD_API_KEY" \
  https://api.clkd.xyz/v1/accounts/$ACCOUNT_ID/activities/pending
```

Activities are discriminated by `activityType`: `SEND`, `RECEIVE`, `SELF`, `SWAP`, `BRIDGE`. See [references/balances-activities.md](references/balances-activities.md) for response shapes.

## Reference Files

- [Agent Setup](references/agent-setup.md) — Key generation, signer enrollment, transaction signing
- [Authentication](references/auth.md) — SIWE flow, API keys, JWT tokens
- [Account Management](references/accounts.md) — Create accounts, subdomains, signers
- [Receive](references/receive.md) — Stealth address generation, ENS resolution
- [Send, Swap & Bridge](references/send-swap-bridge.md) — Quote/submit workflow, max amounts
- [Balances & Activities](references/balances-activities.md) — Balance queries, transaction history, tokens
- [Security Model](references/security.md) — Stealth addresses, privacy guarantees, error handling

## Common Token Addresses

### Ethereum Mainnet (Chain 1)
| Token | Address |
|-------|---------|
| ETH (native) | `0x0000000000000000000000000000000000000000` |
| USDC | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| USDT | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| WETH | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` |

### Base (Chain 8453)
| Token | Address |
|-------|---------|
| ETH (native) | `0x0000000000000000000000000000000000000000` |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| WETH | `0x4200000000000000000000000000000000000006` |

Use `GET /v1/token-catalog` for the complete list or `GET /v1/token-lookup?address=&chainId=` for any token.

## Error Handling

All errors follow this shape:
```json
{
  "error": "Bad request",
  "message": "Human-readable explanation",
  "code": "BAD_REQUEST"
}
```

Common status codes: `400` (validation), `401` (missing/invalid token), `404` (account not found), `429` (rate limited), `502`/`503` (upstream service down — retry with backoff).

<!-- sync:operations
checkSubdomainAvailability
claimSubdomain
createAccount
createPaymentAddress
createQuote
createSwapPreview
generateSubdomain
getAccount
getActivities
getBalances
getChainBalances
getHpkePublicKey
getMaxSpendable
getNonce
getPendingActivities
getQuoteSignerPublicKey
getTokenBalance
getTokenCatalog
listSupportedChains
logout
lookupToken
resolveEns
submitTransaction
unlockQuote
verifySignin
-->