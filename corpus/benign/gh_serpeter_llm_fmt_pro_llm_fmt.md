---
name: llm-fmt
description: Convert JSON/YAML/XML/CSV to token-efficient formats (30-70% savings)
allowed-tools: Bash
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: SerPeter/llm-fmt-project
# corpus-url: https://github.com/SerPeter/llm-fmt-project/blob/c4cc13a375d7fd579622833b5192b0a6909dda14/llm-fmt.skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# llm-fmt

Reduces tokens by 30-70% for structured data in LLM contexts.

## Usage

```bash
llm-fmt data.json                    # TOON output (default)
llm-fmt data.json -f tsv             # TSV (best for tables, 60-75% savings)
llm-fmt data.json -f yaml            # YAML (nested configs, 25-35%)
llm-fmt data.json --analyze          # Compare all formats
```

## Filtering & Truncation

```bash
llm-fmt data.json -i "users[*].name"           # Extract paths
llm-fmt data.json --max-depth 3                # Limit nesting
llm-fmt data.json --max-items 50               # Limit arrays
llm-fmt data.json --max-string-length 200      # Limit strings
llm-fmt data.json --truncation-strategy tail   # head|tail|balanced|sample
```

## Format Guide

| Data | Format | Savings |
|------|--------|---------|
| Tables, uniform arrays | tsv | 60-75% |
| Object arrays (API/logs) | toon | 45-60% |
| Nested configs | yaml | 25-35% |
| Mixed/complex | json | 10-15% |

## Pipes

```bash
curl -s api.example.com/data | llm-fmt -f tsv
cat large.json | llm-fmt --max-items 100
```