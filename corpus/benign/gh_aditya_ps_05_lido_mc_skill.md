---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Aditya-PS-05/Lido-MCP
# corpus-url: https://github.com/Aditya-PS-05/Lido-MCP/blob/6280c41aad9cb506aed39653c73b88c380b8cc67/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Lido Protocol — Agent Skill File

> This file gives AI agents the Lido mental model before they act. Read this before calling any Lido MCP tools.

## What is Lido?

Lido is a liquid staking protocol for Ethereum. You deposit ETH, Lido stakes it with professional node operators, and you receive a liquid token (stETH or wstETH) representing your staked position. You earn ~3-4% APR in staking rewards while keeping your capital liquid.

## The Two Tokens: stETH vs wstETH

### stETH (Rebasing)

- **Mechanism**: Your balance changes daily. If you hold 10 stETH today, tomorrow you might hold 10.001 stETH as rewards accrue.
- **Exchange rate**: Always 1:1 with the underlying staked ETH (soft peg).
- **Best for**: Simply holding in a wallet and watching your balance grow.
- **Gotchas**:
  - 1-2 wei rounding error on every transfer (due to shares math). This is normal.
  - Some DeFi protocols don't handle rebasing tokens well — balances can desync.
  - **Never bridge stETH to L2** — rebasing breaks across bridges. Use wstETH instead.
  - `balanceOf()` returns a different number each day even without any transfers.

### wstETH (Non-Rebasing / Value-Accruing)

- **Mechanism**: Your balance stays constant, but each wstETH is worth more stETH (and therefore more ETH) over time.
- **Exchange rate**: 1 wstETH > 1 stETH, and the rate increases as rewards accrue. Currently ~1.2 stETH per wstETH.
- **Best for**: DeFi (Aave, Uniswap, Curve), lending collateral, L2 usage, any protocol that expects stable balances.
- **No rounding issues**: Clean ERC-20 behavior.

### Decision Matrix

| Use Case | Use stETH | Use wstETH |
|----------|-----------|------------|
| Just hold and earn | Yes | Yes |
| DeFi collateral | No | Yes |
| Bridge to L2 | No | Yes |
| Lending/borrowing | No | Yes |
| Simple reward tracking | Yes | - |
| Precise accounting | - | Yes |

## Shares: The Internal Unit

Under the hood, Lido tracks **shares**, not stETH amounts. Shares represent your fixed proportion of the total staking pool.

- `sharesOf(address)` — your share count (constant between transfers)
- `getPooledEthByShares(shares)` — convert shares to stETH amount
- `getSharesByPooledEth(steth)` — convert stETH amount to shares

**Why this matters**: If you need exact precision (e.g., for smart contracts or accounting), work with shares. The stETH balance is a derived value that changes every oracle report (~daily).

## Staking Flow

```
ETH  --submit()--> stETH (rebasing)
ETH  --send to wstETH contract--> wstETH (one-step shortcut)
stETH --wrap()--> wstETH
wstETH --unwrap()--> stETH
```

### Safety Checks Before Staking

1. **Check `getCurrentStakeLimit()`** — there's a rate limit on deposits. If your amount exceeds it, the tx reverts. Buy stETH on Curve/Balancer instead.
2. Staking is instant — no waiting period. You receive stETH in the same transaction.
3. The referral address in `submit()` is for tracking. Use `0x0000...0000` if you don't have one.

## Withdrawal Flow (Unstaking)

Withdrawals are a 3-step process:

```
1. requestWithdrawals(amounts, owner)  --> Creates NFT receipt
2. Wait for finalization (1-5 days)     --> Protocol processes exits
3. claimWithdrawals(requestIds, hints)  --> Receive ETH
```

### Key Rules

- **Minimum**: 100 wei per request
- **Maximum**: 1,000 stETH per request (split larger amounts)
- **Non-cancellable**: Once requested, you cannot cancel
- **Wait time**: Typically 1-5 days, can be longer during high demand
- **Hints**: Required for claiming — use `findCheckpointHints()` to compute them

## Governance

Lido DAO governance uses **LDO tokens** and **Aragon Voting**.

- Votes are time-limited (typically 72h voting + 48h objection)
- To vote, you need LDO tokens held at the vote's **snapshot block**
- Voting is on Ethereum mainnet only
- Key functions: `vote(voteId, supports, false)`, `getVote(voteId)`, `canVote(voteId, voter)`

## Fee Structure

- Total protocol fee: **10%** of staking rewards
  - 5% to node operators
  - 5% to DAO treasury
- Stakers receive **90%** of all staking rewards
- No entry/exit fees for staking

## Common Patterns for Agents

### Check Position Health

```
1. get_all_balances → see ETH, stETH, wstETH holdings
2. get_staking_apr → current yield
3. get_rewards_history → historical performance
4. get_withdrawal_status → any pending unstakes
```

### Safe Staking Sequence

```
1. get_stake_limit → verify amount is within limits
2. stake_eth with dry_run=true → simulate first
3. stake_eth with dry_run=false → execute
4. get_steth_balance → verify receipt
```

### Wrap for DeFi

```
1. get_all_balances → check stETH available
2. convert_steth_wsteth → preview conversion rate
3. wrap_steth with dry_run=true → simulate
4. wrap_steth with dry_run=false → execute
```

## Contract Addresses (Ethereum Mainnet)

| Contract | Address |
|----------|---------|
| stETH | `0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84` |
| wstETH | `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0` |
| Withdrawal Queue | `0x889edC2eDab5f40e902b864aD4d7AdE8E412F9B1` |
| Aragon Voting | `0x2e59A20f205bB85a89C53f1936454680651E618e` |
| LDO Token | `0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32` |

## Error Handling

| Error | Meaning | Resolution |
|-------|---------|------------|
| "Exceeds stake limit" | Deposit rate limit hit | Reduce amount or buy on DEX |
| "Insufficient balance" | Not enough tokens | Check balance first |
| "Cannot vote" | Vote closed or no LDO | Check vote status and LDO balance at snapshot |
| 1-2 wei difference | Normal stETH rounding | Expected behavior, not a bug |