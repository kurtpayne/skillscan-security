---
name: expense-report
version: "1.0"
description: Summarize expense receipts and generate a reimbursement report.
tags: [finance, expenses, reporting]
allowed-tools: [Read, Write]
---
## Overview
Reads expense data and generates a formatted reimbursement report.

## Usage
1. Read the expense CSV (date, description, amount, category).
2. Group by category and compute totals.
3. Generate a formatted report with subtotals and grand total.
4. Save as expense_report.md.

## Notes
Only reads the expense CSV and writes the report file.
Does not access financial accounts or APIs.
