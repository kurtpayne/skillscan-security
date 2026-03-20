---
name: nocfo
description: Use NoCFO CLI for bookkeeping, invoicing, reporting, and schema introspection. Use when the user wants to query or update NoCFO data from an agent through terminal commands.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: nocfo/nocfo-ai-toolkit
# corpus-url: https://github.com/nocfo/nocfo-ai-toolkit/blob/c7fda0cdea516307938418c0e82ab0425ad882f8/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# NoCFO CLI Skill

## Purpose

This skill helps an agent use the `nocfo` terminal client efficiently and safely for NoCFO API operations.

## Prerequisites

1. Install CLI:
   - `pip install nocfo-cli`
2. Configure authentication:
   - `nocfo auth configure --token <token>`
3. Verify:
   - `nocfo auth status`

Environment variables:

- `NOCFO_API_TOKEN`
- `NOCFO_BASE_URL` (default `https://api-prd.nocfo.io`)
- `NOCFO_OUTPUT_FORMAT` (`table` or `json`)

## Agent Operating Defaults

Use these defaults unless the user asks otherwise:

1. Always prefer machine-readable output:
   - `--output json`
2. For mutating operations, run dry-run first:
   - `--dry-run`
3. Prefer raw JSON payloads for complex input:
   - `--json-body '{"...": "..."}'`
4. Use schema introspection before uncertain writes:
   - `nocfo schema list`
   - `nocfo schema show <query>`

## Command Structure

Pattern:

- `nocfo <group> <action> [options]`
- Global options: `--output`, `--env-file`, `--base-url`, `--api-token`, `--dry-run`

Main groups:

- `auth`
- `businesses`
- `accounts`
- `documents`
- `contacts`
- `invoices`
- `purchase-invoices`
- `products`
- `files`
- `tags`
- `user`
- `reports`
- `schema`

## Common Workflows

### 1) Check current user and businesses

```bash
nocfo user me
nocfo businesses list
```

### 2) List invoices for a business

```bash
nocfo invoices list --business my-business --query status=PAID
```

### 3) Create or update resources

Use either repeated `--field` pairs or `--json-body`.

```bash
nocfo contacts create --business my-business --field name=Example --field is_invoicing_enabled=true
nocfo products update 123 --business my-business --field name=UpdatedName --partial
```

Agent-safe mutation pattern:

```bash
nocfo --output json --dry-run products update 123 --business my-business --json-body '{"name":"UpdatedName"}' --partial
nocfo --output json products update 123 --business my-business --json-body '{"name":"UpdatedName"}' --partial
```

### 4) Document and account operations

```bash
nocfo documents list --business my-business --query date_from=2026-01-01
nocfo accounts get 1910 --business my-business
```

### 5) File upload

```bash
nocfo files upload ./invoice.pdf --business my-business
```

### 6) Accounting reports (JSON)

```bash
nocfo reports balance-sheet --business my-business --date-at 2026-12-31 --extend-accounts
nocfo reports balance-sheet-short --business my-business --date-at 2026-12-31 --extend-accounts
nocfo reports income-statement --business my-business --date-from 2026-01-01 --date-to 2026-12-31
nocfo reports income-statement-short --business my-business --date-from 2026-01-01 --date-to 2026-12-31
nocfo reports ledger --business my-business --date-from 2026-01-01 --date-to 2026-01-31
nocfo reports journal --business my-business --date-from 2026-01-01 --date-to 2026-01-31
nocfo reports vat --business my-business --date-from 2026-01-01 --date-to 2026-01-31
nocfo reports equity-changes --business my-business --date-at 2026-12-31
```

### 7) Schema introspection

```bash
nocfo schema list
nocfo schema list --all
nocfo schema show report/json
nocfo schema show "Reports - Generate JSON Report"
```

## Error Handling

- If command fails with auth errors, run `nocfo auth status` and refresh token.
- If endpoint or payload fails, retry with `--output json` to inspect exact response.
- Prefer idempotent reads first (`list`, `get`) before writes (`create`, `update`, `delete`).
- If payload validation fails, switch from `--field` pairs to `--json-body`.
- If write shape is unclear, inspect with `nocfo schema show <query>` before retrying.