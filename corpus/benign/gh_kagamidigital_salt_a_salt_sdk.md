---
name: salt-sdk
description: Work with Salt SDK for MPC-orchestrated blockchain transactions. Use when handling Salt SDK operations, MPC wallets, Salt accounts, blockchain transactions via Salt orchestration, account creation participation, organization invitations, or debugging Salt transaction states (propose/sign/combine/broadcast). Critical for understanding two-network model (orchestration vs destination chain) and account identity (address vs publicKey).
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: KagamiDigital/salt-agent-skill
# corpus-url: https://github.com/KagamiDigital/salt-agent-skill/blob/1e4168a94dc5401d432bc4e95e82ac20075321ba/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Salt SDK Skill

## Prerequisites

**CRITICAL**: You need a wallet to interact with Salt. Before using any Salt commands:

### Check if You Have a Wallet

Look for wallet configuration at one of these locations:
- `~/.openclaw/workspace/.agent-wallet.json`
- Current directory: `.agent-wallet.json`
- `~/.salt-cli.json`

### If No Wallet Exists - Create One

```javascript
const { ethers } = require('ethers');
const fs = require('fs');

// Generate new wallet
const wallet = ethers.Wallet.createRandom();

// Save configuration
const config = {
  privateKey: wallet.privateKey,
  address: wallet.address,
  mnemonic: wallet.mnemonic.phrase
};

fs.writeFileSync('.agent-wallet.json', JSON.stringify(config, null, 2));

console.log('✅ Wallet created!');
console.log('Address:', wallet.address);
console.log('⚠️  SAVE YOUR MNEMONIC SECURELY!');
console.log('Mnemonic:', wallet.mnemonic.phrase);
```

**IMPORTANT:**
- Store private key/mnemonic securely
- Fund wallet with ETH for gas (testnet: use faucet, mainnet: transfer funds)
- Testnet faucet: https://faucet.quicknode.com/arbitrum/sepolia
- Never share private key or commit to git

### Wallet Funding

**Testnet (Arbitrum Sepolia):**
- Use faucet: https://faucet.quicknode.com/arbitrum/sepolia
- Or ask user to send testnet ETH to your wallet address

**Mainnet (Arbitrum One):**
- Must receive real ETH from user
- Bridge from Ethereum mainnet: https://bridge.arbitrum.io/

## Quick Start

Salt is an MPC orchestration system that coordinates distributed signing across multiple parties. Before using Salt, understand these **non-negotiable concepts**:

### Two-Network Model

Every Salt transaction touches two networks:

- **Orchestration chain** (from `Salt({ environment })`):
  - TESTNET → Arbitrum Sepolia (421614)
  - MAINNET → Arbitrum One (42161)
  - Drives API/websocket/signing coordination
  
- **Destination chain** (from `submitTx({ chainId })`):
  - Where the transaction is finally broadcast and executed
  - Can be any supported blockchain

**Critical rule**: Signer chain MUST match orchestration chain, NOT destination chain.

### Account Identity

Salt accounts have two addresses - **never confuse them**:

- `account.address` = vault/orchestration contract (internal coordination)
- `account.publicKey` = external receiving address (**use this for receiving funds**)

### Value Semantics

For native token transfers:
- ✅ Use decimal strings: `'0.1'`, `'1.5'`
- ❌ Don't use wei strings

For ERC20 transfers:
- Set `value: '0'`
- Encode amount in calldata via ethers Interface

## Standard Workflow

```javascript
const { Salt } = require('salt-sdk');
const { ethers } = require('ethers');

// 1. Setup
const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
const signer = new ethers.Wallet(PRIVATE_KEY, provider);

// 2. Authenticate
const salt = new Salt({ environment: 'TESTNET' }); // or 'MAINNET'
await salt.authenticate(signer);

// 3. Get account
const orgs = await salt.getOrganisations();
const accounts = await salt.getAccounts(orgs[0]._id);
const account = accounts[0];

// 4. Submit transaction
const tx = await salt.submitTx({
  accountId: account.id,
  to: recipientAddress,
  value: '0.01', // decimal string for native transfers
  chainId: 421614, // destination chain
  data: '0x',
  signer: signer // MUST match orchestration chain
});

// 5. Wait for completion (ALWAYS!)
const result = await tx.wait();
console.log('State:', result.state); // 'success' or 'failure'

// 6. Extract transaction hash
const txHash = result.broadcastReceipt?.transactionHash;
```

## Common Operations

### Check Organization Invitations

```javascript
const { invitations } = await salt.getOrganisationsInvitations();
for (const inv of invitations) {
  await salt.acceptOrganisationInvitation(inv._id); // note: _id not id
}
```

### Participate in Account Creation

```javascript
const listener = await salt.listenToAccountNudges(signer);

// Monitor queue
setInterval(() => {
  const queue = listener.getNudgeQueue();
  const processing = listener.getIsProcessingNudge();
  console.log('Pending:', queue.length, 'Processing:', processing);
}, 5000);
```

### ERC20 Transfer

```javascript
const { ethers } = require('ethers');

const erc20Abi = ['function transfer(address to, uint256 amount)'];
const iface = new ethers.utils.Interface(erc20Abi);
const amount = ethers.utils.parseUnits('10', 6); // 10 USDC (6 decimals)

const data = iface.encodeFunctionData('transfer', [recipient, amount]);

await salt.submitTx({
  accountId,
  to: tokenContractAddress,
  value: '0', // MUST be '0' for ERC20
  chainId: 421614,
  data: data,
  signer: signer
});
```

### Contract Deployment

```javascript
const tx = await salt.submitTx({
  accountId,
  to: null, // null for contract creation
  value: '0',
  chainId: 421614,
  data: compiledBytecode,
  signer: signer
});

const result = await tx.wait();
const contractAddress = result.broadcastReceipt?.contractAddress;
```

## Key APIs

- `authenticate(signer)` - Authenticate with Salt
- `getOrganisations()` - List your organizations
- `getAccounts(orgId)` - List accounts in org
- `getAccount(accountId)` - Get specific account details
- `submitTx(params)` - Submit transaction (returns Transaction object)
- `listenToAccountNudges(signer)` - Participate in account creation
- `getOrganisationsInvitations()` - Check pending invitations
- `acceptOrganisationInvitation(invitationId)` - Accept invitation

## Do's and Don'ts

**Do:**
- Always `await tx.wait()` before reporting results
- Use `account.publicKey` for receiving funds
- Use decimal strings for native transfers (`'0.1'`)
- Check signer is on orchestration chain
- Use ABI encoding for contract interactions

**Don't:**
- Use `account.address` as receiving address
- Use wei strings for native transfers
- Assume `submitTx()` return value is final result
- Use zero address (`0x0000...`) for contract deployment
- Skip the `.wait()` call

## Transaction States

`PROPOSE` → `SIGN` → `COMBINE` → `BROADCAST` → `SUCCESS` / `FAILURE`

All states are lowercase strings. Always check `result.state === 'success'`.

## Salt CLI Tool

A command-line tool for both humans and agents. Agents: read **[CLI_PATTERNS.md](CLI_PATTERNS.md)** to interpret natural language requests.

### Core Commands

**`salt status`** - Check Salt status: view invites, organizations, accounts, and balances
```bash
salt status -t                  # testnet
salt status -m                  # mainnet
```

**`salt submit`** - Universal transaction command
```bash
# Native send
salt submit --to 0x123... --value 0.01 -t

# ERC20/Contract call
salt submit --to 0xToken... --value 0 --data 0x... -t

# Deploy contract
salt submit --deploy --data 0x<bytecode> -t
```

**`salt invites`** - Manage invitations
```bash
salt invites list -t
salt invites accept --id <id> -t
salt invites accept-all -t
```

**`salt listen`** - Start nudge listener
```bash
salt listen -t                  # start listener
salt stop -t                    # stop listener
```

**`salt -help`** - Show all commands

## Automation Strategies

Pre-built automation scripts for common DeFi workflows. These run as background processes and handle repetitive tasks automatically.

### Token Sweeper

Monitors a Salt account for token deposits and automatically sweeps them into DeFi protocols (Aave, Compound, Uniswap, etc.).

**Features:**
- Works with any ERC20 token on any EVM chain
- Protocol-agnostic (Aave, Compound, custom contracts)
- Configurable thresholds and polling intervals
- Telegram/Discord notifications on each sweep
- State tracking and reporting

**Quick Start:**
```bash
# Works from anywhere - uses relative paths to skill dependencies
SWEEPER=~/.openclaw/workspace/skills/salt-sdk/strategies/token-sweeper/sweeper.js

# Initialize config
node $SWEEPER --init

# Or use a template
cp ~/.openclaw/workspace/skills/salt-sdk/strategies/token-sweeper/protocols/aave-v3-arb-sepolia.json config.json

# Edit with your details
nano config.json

# Run sweeper
nohup node $SWEEPER > sweeper.log 2>&1 &

# Check status
node $SWEEPER --report

# Stop
node $SWEEPER --stop
```

**Example Use Cases:**
- Auto-supply USDC to Aave when deposited
- Auto-compound yields to Compound
- Auto-add liquidity to Uniswap pools
- Auto-deposit to custom vaults

See **[strategies/token-sweeper/README.md](strategies/token-sweeper/README.md)** for full documentation and protocol examples.

## Detailed Reference

For complete troubleshooting, API details, and advanced patterns:

- **[CLI_PATTERNS.md](CLI_PATTERNS.md)** - How agents interpret natural language requests and map to CLI commands
- **[REFERENCE.md](references/REFERENCE.md)** - Full API reference and troubleshooting matrix
- **[PATTERNS.md](references/PATTERNS.md)** - Advanced patterns and code examples
- **[scripts/](scripts/)** - Working example scripts

Read these as needed for complex scenarios or debugging.