---
name: csv-summary
version: "1.0"
description: Load a CSV file and produce a statistical summary of its columns.
tags: [data, csv, analysis]
allowed-tools: [Read, Bash]
---
## Overview
Reads a CSV file and produces a summary including row count, column types,
missing value counts, and basic statistics for numeric columns.

## Usage
1. Read the CSV file using pandas.
2. Compute: shape, dtypes, null counts, describe() for numeric columns.
3. Format as a Markdown table.

## Notes
Read-only. Does not modify the input file.
