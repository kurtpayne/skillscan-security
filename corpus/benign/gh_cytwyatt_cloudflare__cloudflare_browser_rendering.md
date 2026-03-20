---
name: cloudflare-browser-rendering
description: "Use Cloudflare Browser Rendering REST APIs to extract rendered webpage content as Markdown or crawl whole sites asynchronously. Use when normal web_fetch is insufficient because pages are JavaScript-heavy, require render-time extraction, or you need multi-page site crawling for docs, research, monitoring, or RAG preparation. Prefer this skill for: (1) converting a rendered page to Markdown with /markdown, (2) crawling a documentation site or knowledge base with /crawl, (3) controlling render/load behavior via gotoOptions, cookies, auth, userAgent, or request filtering. Do not use it for interactive login/button-click workflows; use browser for those."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"] },
        "primaryEnv": "CLOUDFLARE_API_TOKEN",
        "homepage": "https://github.com/cytwyatt/cloudflare-browser-rendering-skill",
      },
  }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: cytwyatt/cloudflare-browser-rendering-skill
# corpus-url: https://github.com/cytwyatt/cloudflare-browser-rendering-skill/blob/22b59032645ac614603c733bd65bb9e5ce4a7ce2/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Cloudflare Browser Rendering

## Overview

Use this skill to bridge the gap between lightweight `web_fetch` and full interactive browser automation.

Routing rule:
- Use `web_fetch` for simple static pages and quick reads.
- Use this skill when content depends on JavaScript rendering or when you need to crawl many related pages.
- Use `browser` when the task requires interaction such as login, clicking, typing, or manual flow control.

## Quick decision guide

- Single page, static, fastest path matters -> `web_fetch`
- Single page, JS-heavy, want clean markdown -> `/markdown`
- Whole docs/blog/help center crawl -> `/crawl`
- Needs login/UI actions -> `browser`

If uncertain, start with `web_fetch`. Escalate to `/markdown` if the page is incomplete or empty. Escalate to `/crawl` only when multiple pages are needed.

Read `references/decision-guide.md` for routing details and `references/*.md` for endpoint notes.

## Prerequisites

Expect these environment variables to be available before running the scripts:
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

The token needs `Browser Rendering Write` for `/markdown` and crawl creation. Reading crawl results can use `Browser Rendering Read` or `Write`.

## Single-page extraction with /markdown

Use `scripts/cf_markdown.py`.

Examples:

```bash
python3 scripts/cf_markdown.py --url https://example.com
python3 scripts/cf_markdown.py --url https://example.com --wait-until networkidle0
python3 scripts/cf_markdown.py --url https://example.com --wait-until networkidle0 --timeout-ms 60000
python3 scripts/cf_markdown.py --url https://example.com --cache-ttl 0 --json
python3 scripts/cf_markdown.py --html '<div>Hello</div>'
python3 scripts/cf_markdown.py --url https://example.com --user-agent 'Mozilla/5.0 ...'
python3 scripts/cf_markdown.py --url https://example.com --cookies-json '[{"name":"session","value":"abc","domain":"example.com"}]'
python3 scripts/cf_markdown.py --url https://example.com --authenticate-json '{"username":"u","password":"p"}'
python3 scripts/cf_markdown.py --url https://example.com --reject-request-pattern-json '["/^.*\\\\.(css)$/"]'
```

Guidelines:
- Prefer `--wait-until networkidle0` or `networkidle2` for SPA/JS-heavy pages.
- If a JS-heavy page times out, first raise `--timeout-ms` (for example `60000`), then consider falling back to `domcontentloaded` if full idle waiting is too slow.
- Use `--cache-ttl 0` when freshness matters more than speed.
- Use `--json` when you want full API output for debugging.
- Use raw JSON flags when you need advanced body fields without patching the script.

## Multi-page crawling with /crawl

Use `scripts/cf_crawl.py`.

Examples:

```bash
python3 scripts/cf_crawl.py start --url https://developers.cloudflare.com/workers/ --depth 2 --limit 20 --format markdown
python3 scripts/cf_crawl.py wait --job-id <job_id> --poll-seconds 5
python3 scripts/cf_crawl.py results --job-id <job_id> --limit 20 --status completed
python3 scripts/cf_crawl.py run --url https://developers.cloudflare.com/workers/ --depth 2 --limit 20 --format markdown --wait
python3 scripts/cf_crawl.py run --url https://developers.cloudflare.com/workers/ --depth 2 --limit 20 --format markdown --wait --fetch-results --results-status completed --out-json out/crawl.json --out-markdown out/crawl.md
python3 scripts/cf_crawl.py start --url https://example.com --source links --goto-options-json '{"timeout":30000}'
```

Guidelines:
- Keep initial crawls small: low `depth` and modest `limit`.
- Use `run --wait` for one-shot jobs.
- Use `run --wait --fetch-results` when you want a full one-command workflow.
- Use `start` + `wait` + `results` when you want more control.
- Poll lightly; do not tight-loop.
- Prefer markdown format for downstream summarization or embeddings.
- Use `--out-json` and `--out-markdown` for large outputs instead of dumping everything into chat.

## Output handling

For large crawls:
- First inspect summary fields: job status, total, finished, browser seconds used.
- Then fetch filtered results, usually `status=completed`.
- Avoid dumping huge markdown blobs into chat; summarize and point to saved output if needed.

## Failure and fallback rules

- If `/markdown` returns incomplete content, retry with `--wait-until networkidle0`.
- If `/crawl` is overkill for the task, fall back to `/markdown` on key URLs.
- If the site requires interaction or login, stop using this skill and switch to `browser`.
- If the API is unavailable or credentials are missing, report that clearly and fall back to `web_fetch` when possible.

## Resources

- `scripts/cf_markdown.py` - rendered single-page Markdown extraction
- `scripts/cf_crawl.py` - async crawl job helper
- `references/decision-guide.md` - routing and fallback guidance
- `references/markdown-endpoint.md` - focused notes on `/markdown`
- `references/crawl-endpoint.md` - focused notes on `/crawl`