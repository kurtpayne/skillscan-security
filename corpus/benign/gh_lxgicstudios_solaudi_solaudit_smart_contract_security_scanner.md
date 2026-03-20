---
name: Solaudit - Smart Contract Security Scanner
description: Solidity smart contract security auditor. Detect reentrancy, overflow, access control issues. 50+ vulnerability patterns. CI/CD ready. Free CLI tool.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: lxgicstudios/solaudit
# corpus-url: https://github.com/lxgicstudios/solaudit/blob/a0d7aa0a15e9abe60571b924efdecaa5a1f1fb1b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Solaudit

Security scanner for Solidity smart contracts. Find vulnerabilities before deployment.

## Installation

```bash
npm install -g solaudit-cli
```

## Commands

### Full Audit

```bash
solaudit audit Contract.sol
solaudit audit ./contracts/ -r              # Recursive
solaudit audit . -s high                    # Only high+ severity
solaudit audit . --gas --best-practices     # Include all checks
```

### Quick Check

```bash
solaudit check Token.sol
solaudit check Vault.sol -s critical
```

### Gas Analysis

```bash
solaudit gas Contract.sol
```

### List Patterns

```bash
solaudit patterns
solaudit patterns --category reentrancy
```

## Vulnerability Detection

### Critical
- Reentrancy attacks
- Unprotected selfdestruct
- Delegatecall injection
- Signature replay

### High
- Integer overflow/underflow
- Access control issues
- Unchecked return values
- Price manipulation

### Medium
- tx.origin authentication
- Floating pragma
- Timestamp dependence
- Front-running risks

### Low
- Unused variables
- Missing events
- Implicit visibility
- Magic numbers

## Output Formats

```bash
solaudit audit Contract.sol              # Table (default)
solaudit audit Contract.sol -o json      # JSON
solaudit audit Contract.sol -o markdown  # Markdown report
```

## CI/CD Integration

```bash
# Fail on critical issues
solaudit audit ./contracts/ -s critical && echo "Passed"

# GitHub Actions
- run: npm install -g solaudit-cli
- run: solaudit audit ./contracts/ -r -s high
```

## Common Use Cases

**Pre-deployment check:**
```bash
solaudit audit ./contracts/ -r -s high
```

**Generate audit report:**
```bash
solaudit audit . -o markdown --save AUDIT.md
```

**Gas optimization:**
```bash
solaudit gas Contract.sol
```

---

**Built by [LXGIC Studios](https://lxgicstudios.com)**

🔗 [GitHub](https://github.com/lxgicstudios/solaudit) · [Twitter](https://x.com/lxgicstudios)