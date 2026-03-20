---
name: ddg-search
description: Web search using DuckDuckGo. No API key required. Use this skill to search the web for current information, facts, documentation, news, or any topic. Triggers when the user asks to search the web, look something up online, find current information, or research a topic.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: guyru/ddg-search
# corpus-url: https://github.com/guyru/ddg-search/blob/92caa366f58f9b995819f0f6a479940ce266a403/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# DuckDuckGo Search

Search the web via DuckDuckGo HTML scraping — no API key or dependencies needed, just Python 3 (stdlib only).

## Search

```bash
python3 {baseDir}/scripts/search.py "query"
python3 {baseDir}/scripts/search.py "query" --count 5
python3 {baseDir}/scripts/search.py "query" --json
```

Returns a numbered list of results with title, URL, and snippet. Use `--count` to control how many results to return (default: 10, max: 50). Use `--json` for structured output.

## Fetch Page Content

To read the content of a specific URL from the search results:

```bash
python3 {baseDir}/scripts/fetch.py https://example.com
python3 {baseDir}/scripts/fetch.py https://example.com --limit 3000
python3 {baseDir}/scripts/fetch.py https://example.com --json
python3 {baseDir}/scripts/fetch.py https://example.com --no-verify-ssl
```

Extracts readable text from a web page, stripping scripts, styles, and navigation. Use `--limit` to control character output (default: 5000). Use `--no-verify-ssl` to disable SSL certificate verification if needed (use with caution).

## Workflow

1. Run `search.py` with the user's query
2. Present the results (titles, URLs, snippets) to the user
3. If deeper information is needed, run `fetch.py` on the most relevant URL(s)
4. Summarize the findings

## Notes

- No setup or installation required — uses Python 3 stdlib only
- Results come from DuckDuckGo's HTML search page (html.duckduckgo.com)
- Uses a text-browser User-Agent (Lynx) since html.duckduckgo.com is designed for text-mode browsers and blocks conventional HTTP clients
- If a query returns no results, try rephrasing with different keywords
- For time-sensitive queries, add the current year to the query for fresher results
- URL validation ensures only http/https URLs are fetched
- Error messages distinguish between CAPTCHA challenges, parsing failures, and genuinely empty search results
- SSL verification can be disabled with `--no-verify-ssl` if encountering certificate errors