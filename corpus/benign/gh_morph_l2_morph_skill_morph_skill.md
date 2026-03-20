---
name: morph-skill
version: 1.3.0
description: AI Agent skill for Morph L2 — wallet, explorer, DEX swap, cross-chain bridge with order management, and alt-fee gas payment
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: morph-l2/morph-skill
# corpus-url: https://github.com/morph-l2/morph-skill/blob/ee80e7c7b6abb6c92db19f99f3d622c8e2088857/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Morph Skill — AI Agent Reference

> CLI toolkit for AI agents to interact with the **Morph Mainnet** (Chain ID: 2818).
> All commands output JSON. All amounts use human-readable units (e.g. `0.1` ETH, not wei).

## Quick Start

```bash
# Install dependencies
pip install requests eth_account

# Run any command
python3 scripts/morph_api.py <command> [options]
```

No API keys required for queries. Bridge order management requires JWT authentication via `bridge-login`.

---

## Data Sources

| Source | Base URL | Auth |
|--------|----------|------|
| Morph RPC | `https://rpc.morph.network/` | None |
| Explorer API (Blockscout) | `https://explorer-api.morph.network/api/v2` | None |
| DEX Aggregator | `https://api.bulbaswap.io` | None (queries) / JWT (orders) |

---

## Commands

### Wallet (RPC)

#### `create-wallet`
Generate a new Ethereum key pair locally. No network call.
```bash
python3 scripts/morph_api.py create-wallet
```

#### `balance`
Query native ETH balance.
```bash
python3 scripts/morph_api.py balance --address 0xYourAddress
```

#### `token-balance`
Query ERC20 token balance. Pass the token contract address.
```bash
python3 scripts/morph_api.py token-balance --address 0xAddr --token 0xe7cd86e13AC4309349F30B3435a9d337750fC82D
```

#### `transfer`
Send ETH. Amount is in ETH (e.g. `0.01`).
```bash
python3 scripts/morph_api.py transfer --to 0xRecipient --amount 0.01 --private-key 0xYourKey
```

#### `transfer-token`
Send ERC20 tokens. Amount is in token units (e.g. `10.5` USDC).
```bash
python3 scripts/morph_api.py transfer-token --token 0xe7cd86e13AC4309349F30B3435a9d337750fC82D --to 0xRecipient --amount 10 --private-key 0xKey
```

#### `tx-receipt`
Get transaction receipt (status, gas used, logs).
```bash
python3 scripts/morph_api.py tx-receipt --hash 0xTxHash
```

### Explorer (Blockscout)

#### `address-info`
Address summary: balance, tx count, type.
```bash
python3 scripts/morph_api.py address-info --address 0xAddr
```

#### `address-txs`
List transactions for an address. Optional `--limit`.
```bash
python3 scripts/morph_api.py address-txs --address 0xAddr --limit 5
```

#### `address-tokens`
List all token holdings.
```bash
python3 scripts/morph_api.py address-tokens --address 0xAddr
```

#### `tx-detail`
Full transaction details from explorer (decoded input, token transfers, etc.).
```bash
python3 scripts/morph_api.py tx-detail --hash 0xTxHash
```

#### `token-search`
Search tokens by name or symbol.
```bash
python3 scripts/morph_api.py token-search --query "USDC"
```

#### `contract-info`
Get smart contract info: source code, ABI, verification status, compiler, proxy type.
```bash
python3 scripts/morph_api.py contract-info --address 0xe7cd86e13AC4309349F30B3435a9d337750fC82D
```

#### `token-transfers`
Get recent token transfers by token or by address.
```bash
# All transfers of a specific token
python3 scripts/morph_api.py token-transfers --token USDT0

# Token transfers involving a specific address
python3 scripts/morph_api.py token-transfers --address 0xYourAddress
```

#### `token-info`
Get token details: name, symbol, total supply, holders count, transfer count, market data.
```bash
python3 scripts/morph_api.py token-info --token USDT0
python3 scripts/morph_api.py token-info --token 0xe7cd86e13AC4309349F30B3435a9d337750fC82D
```

#### `token-list`
List top tracked tokens from the explorer (single page response).
```bash
python3 scripts/morph_api.py token-list
```

### DEX (Morph only)

#### `dex-quote`
Get a swap quote on **Morph chain only**. Returns estimated output amount and price impact. Pass `--recipient` to include `methodParameters` (calldata for on-chain execution).
```bash
# Preview quote only
python3 scripts/morph_api.py dex-quote --amount 1 --token-in ETH --token-out 0xe7cd86e13AC4309349F30B3435a9d337750fC82D

# With recipient (returns methodParameters.calldata for dex-send)
python3 scripts/morph_api.py dex-quote --amount 1 --token-in ETH --token-out USDT0 --recipient 0xYourAddr
```

Optional: `--slippage 0.5` (default: 1%), `--deadline 300` (seconds, default: 300), `--protocols v2,v3`.

#### `dex-send`
Sign and broadcast a swap transaction using calldata from `dex-quote --recipient`. Uses `methodParameters` fields (to, value, calldata) from the quote response.
```bash
python3 scripts/morph_api.py dex-send --to 0xRouterAddr --value 0.001 --data 0xCalldata... --private-key 0xKey
```

### Bridge (Cross-Chain & Multi-Chain Swap)

#### `bridge-chains`
List all supported chains for cross-chain swap.
```bash
python3 scripts/morph_api.py bridge-chains
```

#### `bridge-tokens`
List available tokens for cross-chain swap. Optionally filter by chain.
```bash
python3 scripts/morph_api.py bridge-tokens --chain morph
```

#### `bridge-token-search`
Search tokens by symbol or contract address across chains.
```bash
python3 scripts/morph_api.py bridge-token-search --keyword USDT --chain base
```

#### `bridge-quote`
Get a cross-chain or same-chain swap quote with price, fees, and route info.
```bash
python3 scripts/morph_api.py bridge-quote \
  --from-chain base --from-token 0x833589fcd6edb6e08f4c7c32d4f71b54bda02913 \
  --amount 2 --to-chain bnb \
  --to-token 0x55d398326f99059ff775485246999027b3197955 \
  --from-address 0xYourAddress
```

#### `bridge-balance`
Query token balance and USD price for an address on any supported chain.
```bash
python3 scripts/morph_api.py bridge-balance --chain morph --token USDT0 --address 0xYourAddress
```

#### `bridge-login`
Sign in with EIP-191 wallet signature to get a JWT access token (valid 24h).
```bash
python3 scripts/morph_api.py bridge-login --private-key 0xYourKey
```

#### `bridge-make-order`
Create a cross-chain swap order. Returns `orderId` and unsigned transactions to sign.
```bash
python3 scripts/morph_api.py bridge-make-order --jwt <JWT> \
  --from-chain morph --from-contract 0xe7cd86e13AC4309349F30B3435a9d337750fC82D \
  --from-amount 10 --to-chain base \
  --to-contract 0x833589fcd6edb6e08f4c7c32d4f71b54bda02913 \
  --to-address 0xRecipient --market stargate
```

#### `bridge-submit-order`
Submit signed transactions for a swap order.
```bash
python3 scripts/morph_api.py bridge-submit-order --jwt <JWT> --order-id abc123 --signed-txs 0xSignedTx1,0xSignedTx2
```

#### `bridge-swap`
One-step cross-chain swap: create order, sign transactions, and submit — all in one command. This is the recommended way for agents to execute bridge swaps.
```bash
python3 scripts/morph_api.py bridge-swap --jwt <JWT> \
  --from-chain morph --from-contract USDT.e --from-amount 5 \
  --to-chain base --to-contract USDC \
  --market stargate --private-key 0xYourKey
```
Optional: `--to-address` (default: sender), `--slippage 0.5`, `--feature no_gas`.

#### `bridge-order`
Query the status of a swap order.
```bash
python3 scripts/morph_api.py bridge-order --jwt <JWT> --order-id abc123
```

#### `bridge-history`
Query historical swap orders with optional pagination and status filter.
```bash
python3 scripts/morph_api.py bridge-history --jwt <JWT> --page 1 --page-size 10
```

### Alt-Fee (pay gas with alternative tokens)

Morph supports paying gas fees with alternative tokens (tx type `0x7f`) instead of ETH. Use these commands to query fee token info, estimate costs, and send alt-fee transactions.

#### `altfee-tokens`
List all supported fee tokens from the on-chain TokenRegistry.
```bash
python3 scripts/morph_api.py altfee-tokens
```

#### `altfee-token-info`
Get details for a specific fee token: contract address, scale, feeRate, decimals, active status.
```bash
python3 scripts/morph_api.py altfee-token-info --id 5
```

#### `altfee-estimate`
Estimate the minimum feeLimit needed to pay gas with a fee token. Includes a 10% safety margin.
```bash
# Estimate for a simple ETH transfer (21000 gas)
python3 scripts/morph_api.py altfee-estimate --id 5

# Estimate for an ERC20 transfer (200000 gas)
python3 scripts/morph_api.py altfee-estimate --id 5 --gas-limit 200000
```

#### `altfee-send`
Sign and broadcast a transaction paying gas with an alternative fee token (tx type `0x7f`). `--fee-limit` defaults to 0 (no limit — uses available balance, unused portion is refunded).
```bash
# Simple ETH transfer, pay gas with USDT0 (token ID 5)
python3 scripts/morph_api.py altfee-send --to 0xRecipient --value 0.01 --fee-token-id 5 --private-key 0xKey

# Contract call with explicit fee limit and gas limit
python3 scripts/morph_api.py altfee-send --to 0xContract --data 0xCalldata... --fee-token-id 5 --fee-limit 500000 --gas-limit 200000 --private-key 0xKey
```

---

## Well-Known Token Addresses (Morph Mainnet)

For native ETH, use empty string `""` or `ETH` as the contract address.

| Symbol | Name | Contract Address |
|--------|------|-----------------|
| USDT0 | USDT0 | `0xe7cd86e13AC4309349F30B3435a9d337750fC82D` |
| USDT.e | Tether Morph Bridged | `0xc7D67A9cBB121b3b0b9c053DD9f469523243379A` |
| USDC | USD Coin | `0xCfb1186F4e93D60E60a8bDd997427D1F33bc372B` |
| USDC.e | USD Coin Morph Bridged | `0xe34c91815d7fc18A9e2148bcD4241d0a5848b693` |
| WETH | Wrapped Ether | `0x5300000000000000000000000000000000000011` |
| BGB | BitgetToken | `0x389C08Bc23A7317000a1FD76c7c5B0cb0b4640b5` |
| BGB(old) | BitgetToken | `0x55d1f1879969bdbB9960d269974564C58DBc3238` |

> **Note:** Morph has two USDT variants and two USDC variants. When the user says "USDT" or "USDC" without specifying, **ask the user to choose** (USDT0 vs USDT.e, or USDC vs USDC.e) before proceeding.

For other tokens, use `token-search` to look up the contract address:
```bash
python3 scripts/morph_api.py token-search --query "USDC"
```

---

## Domain Knowledge

### Morph Chain
- **Network**: Morph Mainnet
- **Chain ID**: 2818
- **Layer**: L2 (optimistic rollup on Ethereum)
- **Gas token**: ETH
- **Block time**: ~2 seconds
- **Explorer API**: https://explorer-api.morph.network/api/v2

### Safety Rules
1. **Always confirm with the user before executing send commands** (`transfer`, `transfer-token`, `dex-send`, `altfee-send`, `bridge-make-order`, `bridge-submit-order`, `bridge-swap`) — show the recipient, amount, and token before signing. For `bridge-submit-order`, confirm the orderId and number of transactions before broadcasting. For `bridge-swap`, confirm the swap details (chains, tokens, amounts) before executing.
2. All amounts are in human-readable units — `0.1` means 0.1 ETH, not 0.1 wei.
3. Private keys are only used locally for signing. They are never sent to any API.
4. `create-wallet` is purely local — it generates a key pair without any network call.
5. For large amounts, suggest the user verify the recipient address character by character.
6. DEX quotes may change between quote and execution — always use the `--slippage` parameter.
7. **JWT tokens** from `bridge-login` expire after 24h. Re-authenticate if order commands return auth errors.

### Alt-Fee (Alternative Gas Payment)
- Morph supports paying gas with alternative tokens via transaction type `0x7f`
- Use `altfee-tokens` to list available fee tokens (IDs 1-5)
- Use `altfee-estimate` to calculate how much fee token is needed for a given gas limit
- Formula: `feeLimit >= (gasFeeCap × gasLimit + L1DataFee) × tokenScale / feeRate`
- Fee token 5 = USDT0 (`0xe7cd86e13AC4309349F30B3435a9d337750fC82D`)
- Alt-fee and EIP-7702 are mutually exclusive — cannot use both in one transaction

### Common Workflows

**Agent routing — swap/bridge decision:**
```
User wants to swap tokens?
  ├── Same chain, on Morph? → dex-quote → dex-send (faster, lower fees)
  ├── Same chain, on other chain (Base/BNB/etc.)? → bridge-quote (same fromChain/toChain) → bridge-swap
  └── Cross-chain? → bridge-quote → bridge-swap
```

> **Important**: `dex-quote` / `dex-send` only work on Morph. For swaps on other chains or cross-chain transfers, always use bridge commands.

**Check a wallet's portfolio:**
```
balance → token-balance (for each token) → address-tokens (for full list)
```

**Send tokens safely:**
```
balance (verify funds) → transfer/transfer-token → tx-receipt (confirm)
```

**Swap tokens on Morph:**
```
dex-quote --recipient (get calldata in methodParameters) → dex-send (sign & broadcast)
```

**Swap or bridge on any chain:**
```
bridge-login (get JWT) → bridge-quote (get price + market) → bridge-swap (create, sign, submit in one step) → bridge-order (track status)
```

> **Advanced**: `bridge-make-order` → sign txs → `bridge-submit-order` is still available for scenarios requiring manual transaction inspection or custom signing.

**Investigate a transaction:**
```
tx-detail (explorer view) → tx-receipt (RPC receipt with logs)
```

**Pay gas with alternative token:**
```
altfee-tokens (list available) → altfee-estimate (calculate feeLimit) → altfee-send (sign & broadcast with 0x7f)
```

---

## Extended Documentation

For complex workflows, load these guides on demand:

| Document | When to Load |
|----------|-------------|
| [docs/altfee.md](docs/altfee.md) | User asks about paying gas with non-ETH tokens, 0x7f transactions, or feeLimit calculation |
| [docs/dex-swap.md](docs/dex-swap.md) | User wants to swap tokens, needs slippage guidance, or wants to combine swap with alt-fee |
| [docs/bridge.md](docs/bridge.md) | User asks about cross-chain swaps, bridge quotes, or multi-chain token operations |
| [docs/explorer.md](docs/explorer.md) | User wants to investigate addresses, transactions, tokens, or analyze contracts |

---

## Version Check Protocol

On each session start, before executing any command:

1. Read the `version` from this file's YAML frontmatter (current: `1.2.0`)
2. Fetch the latest CHANGELOG.md from the remote:
   ```bash
   git -C <skill_path> fetch origin && git -C <skill_path> diff HEAD..origin/main -- CHANGELOG.md
   ```
   Or if git is unavailable, fetch via HTTP:
   ```
   https://raw.githubusercontent.com/morph-l2/morph-skill/main/CHANGELOG.md
   ```
3. Compare the local version against the first `## [x.y.z]` entry in the remote CHANGELOG
4. If a newer version exists:
   - Show the user: "Morph Skill update available: vX.Y.Z → vA.B.C"
   - Summarize what changed (from CHANGELOG entries between versions)
   - If the update includes a **Security Audit** section mentioning credential, endpoint, or dependency changes, flag it explicitly
   - Prompt the user to update: `cd <skill_path> && git pull`
5. If versions match, proceed silently