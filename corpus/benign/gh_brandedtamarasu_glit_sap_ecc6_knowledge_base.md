---
name: sap-ecc6-knowledge-base
description: Use when answering SAP ECC 6.0 questions about transaction codes, SPRO/IMG configuration paths, business process flows, or cross-module integration across MM (Materials Management), SD (Sales & Distribution), FI (Financial Accounting), and CO (Controlling). Covers Procure-to-Pay, Order-to-Cash, Record-to-Report, account determination (OBYC, VKOA), period-end close sequences, and master data tables.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: BrandedTamarasu-glitch/SAPKnowledge
# corpus-url: https://github.com/BrandedTamarasu-glitch/SAPKnowledge/blob/6590f425ac9c3897db50fcd4666fbc335d66bdd2/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# SAP ECC 6.0 Knowledge Base

A curated reference for SAP ECC 6.0 (Enhancement Packs 0–8). Covers transaction codes, SPRO configuration paths, process flows, master data, and integration points across MM, SD, FI, and CO.

**Scope:** ECC 6.0 only. S/4HANA differences are noted for disambiguation, not as primary reference.

## How to Use This Knowledge Base

### Step 1 — Identify the module

| Topic | Module |
|---|---|
| Procurement, purchasing, POs, goods movements, inventory, vendors | MM |
| Sales orders, deliveries, billing, pricing, customer master | SD |
| General ledger, AP, AR, asset accounting, bank accounting | FI |
| Cost centers, internal orders, profit centers, allocations, settlement | CO |
| Account determination (OBYC, VKOA), P2P, O2C, R2R, period-end close | Cross-module |

### Step 2 — Fetch the module content

Use `get_library_docs` with the library ID for this repository to retrieve content from the relevant module file:

| Need | File to fetch |
|---|---|
| Transaction codes and menu paths | `modules/{mm\|sd\|fi\|co}/tcodes.md` |
| SPRO/IMG configuration paths | `modules/{mm\|sd\|fi\|co}/config-spro.md` |
| Business process flows | `modules/{mm\|sd\|fi\|co}/processes.md` |
| Master data tables and fields | `modules/{mm\|sd\|fi\|co}/master-data.md` |
| Integration points between modules | `modules/{mm\|sd\|fi\|co}/integration.md` |
| Decision trees and troubleshooting | `modules/{mm\|sd\|fi\|co}/co-advanced.md` (CO) or `mm-advanced.md` (MM) or `sd-advanced.md` (SD) or `fi-advanced.md` (FI) |
| End-to-end Procure-to-Pay | `cross-module/procure-to-pay.md` |
| End-to-end Order-to-Cash | `cross-module/order-to-cash.md` |
| Period-end close sequence (all modules) | `cross-module/record-to-report.md` |
| FI account determination (OBYC, VKOA) | `modules/fi/account-determination.md` |
| Movement types reference | `reference/movement-types.md` |
| ECC 6 vs S/4HANA disambiguation | `.claude/rules/sap-disambiguation.md` |

### Step 3 — Apply confidence levels

Each file has a frontmatter `confidence` field:
- `high` — verified against SAP documentation or confirmed in live systems
- `medium` — standard practice, likely accurate
- `low` — needs verification before treating as authoritative

Note the confidence level when answering, especially for configuration details.

## Key SAP Concepts

- **T-code** — transaction code used to launch a function in SAP GUI (e.g., ME21N = create PO)
- **SPRO/IMG** — configuration tree path (e.g., `Materials Management → Purchasing → ...`)
- **Movement type** — 3-digit code controlling goods movement behavior in MIGO (101 = GR, 261 = GI to production)
- **Account determination** — how SAP maps business events to GL accounts (OBYC for MM, VKOA for SD)
- **Controlling area** — CO organizational unit that spans one or more company codes

## Common Query Patterns

**"What T-code does X?"** → fetch `tcodes.md` for the relevant module, search for the functional description

**"What's the SPRO path to configure Y?"** → fetch `config-spro.md` for the relevant module

**"Walk me through process Z end to end"** → fetch `processes.md` or the relevant `cross-module/` file

**"Why is account determination failing?"** → fetch `modules/fi/account-determination.md` and the module's `integration.md`

**"How does X work in S/4HANA vs ECC 6?"** → fetch `.claude/rules/sap-disambiguation.md`