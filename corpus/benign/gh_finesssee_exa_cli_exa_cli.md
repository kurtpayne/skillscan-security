---
name: exa-cli
description: AI-powered web search and content extraction via Exa API. Use for web searches, documentation lookup, semantic/conceptual searches, extracting page content, getting AI answers with sources, or deep multi-step research tasks. Triggers on requests like "search for X", "find documentation about Y", "research Z", "what is X", or any web search need.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Finesssee/exa-cli
# corpus-url: https://github.com/Finesssee/exa-cli/blob/d4f60b51dc1ba3b6f21dab12b178582b7b84593b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Exa CLI

AI-powered web search with automatic API key rotation. Rust binary, ~57ms cached / ~570ms live.

**Always use `--compact` when calling from an AI agent.** Piped output auto-enables compact mode.

## Environment

| Variable | Description |
|----------|-------------|
| `EXA_API_KEYS` | Comma-separated API keys (recommended) |
| `EXA_API_KEY` | Single key (fallback) |
| `EXA_LOG_REQUESTS` | Set to `1` to enable logging |

## Commands

```bash
exa search "query" --compact -n 3              # Web search (instant type, sub-150ms)
exa search "query" --compact --fields url      # Only URLs (minimal tokens)
exa search "query" --tsv -n 5                  # Tab-separated output
exa search "query" --type auto --compact       # Highest quality search
exa search "query" --type deep --compact       # Comprehensive research
exa search "AI startups" --category company    # Category-filtered search
exa search "news" --highlights --compact       # Token-efficient excerpts
exa search "breaking" --max-age 1 --compact    # Fresh content only (hours)
exa find "similar to this" --compact           # Semantic similarity
exa content https://example.com --compact      # Extract page content
exa answer "what is X" --compact               # AI answer with sources
exa research "compare X vs Y" --compact        # Deep async research
exa research "topic" --model exa-research-pro  # Thorough research model
exa research "list items" --schema schema.json # Structured output
```

## Company Research

Use `--type auto --category company` to get structured company data (HQ, employees, funding, traffic):

```bash
exa search "Anthropic" --type auto --category company --compact -n 1
# Output includes: about, hq, employees, funding, traffic

exa search "fintech startups in Europe" --type auto --category company --compact -n 5
exa search "AI companies" --type auto --category company --json -n 3  # Structured JSON
```

## Key Flags

- `--compact` — **Always use.** Terse output for AI/LLM consumption
- `--fields <list>` — Comma-separated: `title,url,date,content`
- `--tsv` — Tab-separated output (header + one row per result)
- `--max-chars <n>` — Content truncation (default: 300 compact, 500 normal)
- `-n <num>` — Number of results (default: 5)
- `--content` — Include page content in search/find
- `--highlights [n]` — Key excerpts instead of full text (max chars, default: 2000)
- `--type <t>` — Search type: `instant` (default, sub-150ms), `auto`, `fast`, `deep`, `neural`
- `--category <c>` — Content category: `company`, `people`, `tweet`, `news`, `research paper`
- `--max-age <hrs>` — Max content age in hours (`0`=always live, `-1`=cache only)
- `--verbosity <v>` — Content verbosity: `compact`, `standard`, `full`
- `--json` — JSON output (compact single-line with `--compact`)
- `--domain <d>` — Filter to domain
- `--after/--before <YYYY-MM-DD>` — Date filter
- `--no-cache` — Bypass response cache
- `--cache-ttl <min>` — Cache TTL in minutes (default: 60)
- `--model exa-research-pro` — Thorough research model
- `--schema <file>` — Structured research output

## Key Management

```bash
exa status    # Show keys, cooldowns, usage stats
exa reset     # Clear cooldowns and statistics
```

## Key Rotation

- Round-robin across multiple keys
- Auto-retry on 429 (up to 3 times)
- Respects Retry-After headers
- Waits if all keys exhausted
- State persists in config dir