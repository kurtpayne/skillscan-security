---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: DefiRevived/lido-mcp-server
# corpus-url: https://github.com/DefiRevived/lido-mcp-server/blob/d4252b68880470ca2a7d6210521dd6bd5189e89b/lido.skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# lido.skill.md - Lido Staking Agent Skill

## Mental Model

Lido is liquid staking for Ethereum. You stake ETH → get stETH (rebasing token that accrues rewards). stETH balance increases daily via rebasing.

wstETH is wrapped stETH (non-rebasing, better for DeFi). Wrap when you need fixed balance (e.g., collateral). Unwrap to get rebasing stETH.

## Contract Addresses

### Mainnet
- stETH: `0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84`
- wstETH: `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0`
- Withdrawal Queue: `0x889edC2eDab5f40e902b864aD4d7AdE5E42c52D9`
- Lido DAO (Aragon): `0x2e59A20f205bB85a89C53f1936454680651E618e`

### Holesky Testnet
- stETH: `0x3e01Fe8c67D60E9387D1A6f4A6a6d01d80C1e607`
- wstETH: `0x25f746BB206043ed99BbE747fB5c2fE79A0f9223`
- Withdrawal Queue: `0x07495387A3C19A04f0d83E66879d4c0e87E42aEf`

## Safe Patterns

1. **Always dry_run before stake/unstake** - simulate first, verify params
2. **Check gas prices** - staking is gas-intensive
3. **Unbonding period** - unstaking takes ~7 days via withdrawal queue
4. **Governance voting** - only vote if holder has stETH delegation
5. **Use testnet first** - test on Holesky before mainnet operations

## Common Flows

### Stake ETH
```
stake_eth(amount="1.5") → dry_run first
```

### Check Rewards
```
get_rewards(address) → query monthly
```

### Wrap for DeFi
```
wrap_steth(amount="5.0") → use wstETH as collateral
```

### Unstake
```
unstake_steth(amount="2.0") → wait 7 days for ETH
```

### Governance Vote
```
vote_on_governance(proposalId="123", support=true)
```

## MCP Tools Reference

| Tool | Type | Description |
|------|------|-------------|
| `stake_eth` | Write | Stake ETH to receive stETH |
| `unstake_steth` | Write | Request withdrawal via queue |
| `wrap_steth` | Write | Wrap stETH → wstETH |
| `unwrap_wsteth` | Write | Unwrap wstETH → stETH |
| `get_balance` | Read | Query ETH, stETH, wstETH balances |
| `get_rewards` | Read | Calculate accrued rewards |
| `vote_on_governance` | Write | Vote on Aragon proposals |
| `dry_run` | Read | Simulate any transaction |

## Error Handling

- Insufficient balance → check `get_balance` first
- Gas too low → increase gas price or wait for lower network congestion
- Unbonding period → inform user of ~7 day wait for unstaking
- Governance inactive → check voting period status before voting

## Best Practices

1. Query balance before any write operation
2. Always use dry_run for stake/unstake/wrap/unwrap
3. Inform users of unbonding periods
4. Check APY/rewards periodically for users
5. Use Holesky for testing, mainnet for production