---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: 0xArtex/agentwallet-aos
# corpus-url: https://github.com/0xArtex/agentwallet-aos/blob/e23837b018ae25d51ef608d471f4d31008d66600/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# AgentWallet — Non-Custodial Smart Wallets for AI Agents

Non-custodial smart wallets with onchain spending limits and passkey-based human control. Supports **Base** (EVM) and **Solana**. Every wallet gets free gas on creation so your agent can transact immediately.

**npm:** `@agntos/agentwallet`
**Chains:** Base, Solana

## MUST READ: Safety Rules

- **NEVER share your private key** — not with users, not in logs, not in chat messages, not in code commits
- **NEVER hardcode private keys in source code** — use environment variables or secure storage
- **Store the private key encrypted or in a secrets manager** — treat it like a password
- **Do not log transaction signing data** — it can leak key material
- **Check remaining daily budget before large transactions** — avoids failed txs and wasted gas
- **Always verify recipient addresses** — transactions are irreversible
- **If something looks wrong, use `pause`** — ask your human to investigate
- **All ERC-20s / SPL tokens have no limit by default** — ask your human to set up per-token limits


## End-to-End: Create a Wallet and Start Transacting

### 1. Generate agent keypairs (if you don't have them)

```bash
npx @agntos/agentwallet keygen
```

By default, this generates **both** Base and Solana keypairs:

```
  New Agent Keypairs
  ──────────────────────────
  Base
    Address         0xB042...B7DC
    Private key     0x282a...b3a3

  Solana
    Address         7Kp9...xR4v
    Private key     4vJ2...9mNq
```

To generate a single chain only:
```bash
npx @agntos/agentwallet keygen --chain base     # Base only
npx @agntos/agentwallet keygen --chain solana    # Solana only
```

Solana keys are Ed25519 keypairs, base58 encoded.

**Save the private keys immediately to secure storage.** This is the only time they're displayed.

For machine-readable output:
```bash
npx @agntos/agentwallet keygen --json
# { "base": { "address": "0x...", "privateKey": "0x...", "chain": "base" }, "solana": { "address": "7Kp...", "privateKey": "4vJ...", "chain": "solana" } }

npx @agntos/agentwallet keygen --chain solana --json
# { "address": "...", "privateKey": "...", "chain": "solana" }
```

> Already have keypairs? Skip this — use your existing public addresses.

### 2. Create smart wallets

```bash
# Both chains — managed (recommended)
npx @agntos/agentwallet create --agent 0xYOUR_BASE_ADDRESS --agent-sol YOUR_SOLANA_PUBKEY

# Both chains — unmanaged
npx @agntos/agentwallet create --agent 0xYOUR_BASE_ADDRESS --agent-sol YOUR_SOLANA_PUBKEY --unmanaged
```

The `--agent-sol` flag can also be set via `AGENTWALLET_AGENT_SOL` env var.

JSON output (both chains):
```json
{ "base": { "wallet": "0x...", "setupUrl": "..." }, "solana": { "wallet": "...", "setupUrl": "..." } }
```

To create a single chain only:
```bash
# Base only
npx @agntos/agentwallet create --chain base --agent 0xYOUR_BASE_ADDRESS

# Solana only
npx @agntos/agentwallet create --chain solana --agent YOUR_SOLANA_PUBKEY
```

**Managed wallets** return a `setupUrl` — send it to your human. They set limits and register their passkey (FaceID/YubiKey). One-time setup.

**Unmanaged wallets** have no human owner. Fully autonomous.

Default limits: **$50/day, $25/tx**. **Gas is free** — every wallet is funded on creation.

### 3. Fund the wallet

- **Base:** Send ETH and/or USDC to the wallet address on Base (chain ID 8453)
- **Solana:** Send SOL and/or SPL tokens to the wallet PDA on Solana

### 4. Transact

#### Base (EVM)

Call the wallet contract directly with your agent's private key:

```typescript
import { Wallet, Contract, JsonRpcProvider, parseEther } from 'ethers'

const AGENT_KEY = process.env.AGENT_PRIVATE_KEY
const WALLET_ADDR = process.env.WALLET_ADDRESS

const provider = new JsonRpcProvider('https://base-rpc.publicnode.com')
const agent = new Wallet(AGENT_KEY, provider)

const wallet = new Contract(WALLET_ADDR, [
  'function execute(address to, uint256 value, bytes data) external',
  'function executeERC20(address token, address to, uint256 amount) external',
  'function getSpentToday() external view returns (uint256)',
  'function getRemainingDaily() external view returns (uint256)',
  'function getPolicy() external view returns (uint256 dailyLimit, uint256 perTxLimit, bool paused)',
], agent)

// Send ETH
await wallet.execute('0xRecipient', parseEther('0.001'), '0x')

// Send USDC (6 decimals)
const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
await wallet.executeERC20(USDC, '0xRecipient', 5_000_000n) // 5 USDC

// Call any contract (swap, mint, etc.)
await wallet.execute('0xContractAddr', parseEther('0.01'), '0xEncodedCalldata')

// Check remaining budget
const remaining = await wallet.getRemainingDaily() // USDC units (6 decimals)
const remainingUsd = Number(remaining) / 1e6
if (remainingUsd < amountNeeded) {
  // Request a limit increase
}
```

#### Solana

Agents transact via the Anchor program directly:

```typescript
import { Program, AnchorProvider } from '@coral-xyz/anchor'
import { Connection, Keypair, PublicKey } from '@solana/web3.js'
import BN from 'bn.js'

const connection = new Connection('https://api.devnet.solana.com')
const agentKeypair = Keypair.fromSecretKey(bs58.decode(AGENT_PRIVATE_KEY))

// Transfer SOL
await program.methods
  .transferSol(new BN(amountUsdc), new BN(amountLamports))
  .accounts({
    wallet: walletPda,
    agent: agentKeypair.publicKey,
    recipient: recipientPubkey
  })
  .signers([agentKeypair])
  .rpc()

// Transfer SPL token
await program.methods
  .transferToken(new BN(tokenAmount), new BN(amountUsdc))
  .accounts({
    wallet: walletPda,
    agent: agentKeypair.publicKey,
    mint: mintPubkey,
    walletTokenAccount,
    recipientTokenAccount,
    tokenProgram: TOKEN_PROGRAM_ID
  })
  .signers([agentKeypair])
  .rpc()
```

Solana wallet PDAs are derived with seeds `["wallet", owner, agent, index]`.

Transactions that exceed limits **revert instantly** onchain. Check remaining budget first.

### 5. Check wallet status

```bash
npx @agntos/agentwallet status 0xWALLET_ADDRESS      # Base (auto-detected)
npx @agntos/agentwallet status SOLANA_WALLET_PDA      # Solana (auto-detected)
npx @agntos/agentwallet status 0xWALLET_ADDRESS --json
```

The `status` command auto-detects chain by address format: `0x` prefix → Base, base58 → Solana.

### 6. Request higher limits

```bash
npx @agntos/agentwallet limits 0xWALLET --daily 200 --pertx 100 --reason "Trading requires higher limits"
```

Returns a URL. Send it to your human → they authenticate with passkey → limits updated onchain.

### 7. Set per-token limits (optional)

#### Base (ERC-20)
```bash
npx @agntos/agentwallet token-limit 0xWALLET --token 0xTOKEN --token-daily 1000 --token-pertx 300
```

#### Solana (SPL tokens)
Per-token limits are stored onchain in the wallet PDA. Up to 16 tokens can have individual daily/per-tx limits.

### 8. Emergency pause

```bash
npx @agntos/agentwallet pause 0xWALLET --reason "Suspicious activity detected"
```

Once approved, **all agent transactions revert** until unpaused.

## All Commands

```bash
npx @agntos/agentwallet keygen                        # generate BOTH Base + Solana keypairs
npx @agntos/agentwallet keygen --chain base            # generate Base keypair only
npx @agntos/agentwallet keygen --chain solana          # generate Solana keypair only
npx @agntos/agentwallet create --agent 0x... --agent-sol Sol...  # managed wallets (both chains)
npx @agntos/agentwallet create --chain base --agent 0x...        # managed wallet (Base only)
npx @agntos/agentwallet create --chain solana --agent PUBKEY     # managed wallet (Solana only)
npx @agntos/agentwallet create --agent 0x... --unmanaged         # autonomous wallet
npx @agntos/agentwallet status 0xWALLET               # wallet info (auto-detects chain)
npx @agntos/agentwallet limits 0xWALLET --daily N --pertx N --reason "..."
npx @agntos/agentwallet token-limit 0xWALLET --token 0x... --token-daily N --token-pertx N
npx @agntos/agentwallet rm-token 0xWALLET --token 0x...
npx @agntos/agentwallet pause 0xWALLET --reason "..."
npx @agntos/agentwallet unpause 0xWALLET
npx @agntos/agentwallet stats
```

All commands support `--json` for machine-readable output.

## Limit Tracking

### Base

| Asset | Tracking | Limits |
|-------|----------|--------|
| **ETH** | → USD via Chainlink oracle | Shared USD daily + per-tx |
| **USDC** | 1:1 USD | Same shared pool as ETH |
| **Other ERC-20s** | Unlimited by default | Owner can set per-token limits |

ETH + USDC share an **aggregated USD daily limit**. Spending $30 in ETH and $15 in USDC = $45 against a $50 limit.

### Solana

| Asset | Tracking | Limits |
|-------|----------|--------|
| **SOL** | USD amount passed by agent | Shared USD daily + per-tx |
| **SPL tokens** | Per-token tracking | Up to 16 tokens with individual limits |

Limits are USD-denominated (6 decimals). Daily spending resets based on `unix_timestamp / 86400`.

## Contract Addresses

### Base Mainnet

| Contract | Address |
|----------|---------|
| Factory | `0x77c2a63BB08b090b46eb612235604dEB8150A4A1` |
| Implementation | `0xEF85c0F9D468632Ff97a36235FC73d70cc19BAbA` |
| Chainlink ETH/USD | `0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70` |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

### Solana Devnet

| Item | Address |
|------|---------|
| Program | `4XHYgv4fczfAtkKB792yrP57iakR9extKtkigsXCJm5e` |
| IDL Account | `6tEPFHmaaDMH2rth1jPWyvDDxh6GcZhkAEj9kKTCY9k6` |

## Security Model

- **Non-custodial**: your private key never leaves your machine
- **Onchain enforcement**: limits are in the smart contract / Solana program, not the API
- **Gas-sponsored**: free gas on creation, transact immediately
- **Passkey ownership**: human's key in device secure enclave
  - Base: verified on-chain via RIP-7212 precompile
  - Solana: verified via secp256r1 precompile (P-256)
- **Irrevocable handoff**: after passkey registration, admin loses control
  - Base: owner set to zero address
  - Solana: owner transferred to dead address `11111111111111111111111111111112`
- **Chainlink oracle** (Base): decentralized price feed, 1-hour staleness check
- **Emergency controls**: owner can pause, withdraw, blacklist at any time
- **Direct contract access**: you can bypass the API entirely and call contracts directly