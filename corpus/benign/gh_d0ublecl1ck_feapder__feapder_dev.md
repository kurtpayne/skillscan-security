---
name: feapder-dev
description: Develop, debug, and structure Python crawlers built with the Feapder framework. Use when the user asks about Feapder/AirSpider/Spider/TaskSpider/BatchSpider development, project scaffolding, parser design (BaseParser/BatchParser), request/response handling, pipelines, settings/configuration, proxy/user pools, de-duplication, logging, scheduling/tasks, or troubleshooting Feapder runtime issues.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: d0ublecl1ck/feapder-dev
# corpus-url: https://github.com/d0ublecl1ck/feapder-dev/blob/40b50867388c52b6fb26b78be7368d76eecc5ea0/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Feapder Dev

## Quick Intake

Ask the user for the minimum information needed to produce a runnable crawler:

- Target site/app constraints (login, JS rendering, anti-bot, rate limits).
- Data schema (fields), uniqueness key, and storage target (file/DB/queue).
- Entry points (seed URLs, keywords, categories) and pagination strategy.
- Scale constraints (single machine vs distributed; incremental vs full; schedule).
- Environment constraints (OS, Python version, network/proxy availability).

## Workflow Decision Tree

Decide the crawler architecture before writing code:

- Choose crawler type:
  - Choose `AirSpider` for small jobs, no distributed scheduling, simple persistence.
  - Choose `Spider` for high-volume, distributed crawling, and persistent task queues.
  - Choose `TaskSpider` for explicit task tables/queues with retry/continuation semantics.
  - Choose `BatchSpider` for periodic batches with batch metadata and separation.

- Choose rendering:
  - Use HTTP-only requests when pages are static or the API is reachable.
  - Use browser rendering only when content is JS-rendered or requires complex interaction.

- Choose persistence and flow:
  - Use `Item` + pipeline for normalized storage.
  - Use explicit DB access helpers only when pipeline is insufficient.

- Choose anti-bot strategy:
  - Add rate limits/backoff/retries first.
  - Add proxy rotation/user pool only when needed and with observability.

## Build Steps

Implement the smallest runnable crawler first, then iterate:

### 1) Set up environment (prefer `uv`)

- Create a project venv with `uv` and pin a compatible Python version.
- Install `feapder` and any runtime dependencies (DB drivers, playwright/selenium if used).
- Verify import and basic CLI availability before writing spider code.

### 2) Scaffold a minimal project

- Create a clean module layout: `spiders/`, `parsers/`, `items/`, `pipelines/`, `settings.py`.
- Start with one spider, one parser, and one item type.

### 3) Implement a minimal spider + parser

Keep the first version minimal and end-to-end runnable:

```python
from feapder import AirSpider
from feapder.network.request import Request

class DemoSpider(AirSpider):
    def start_requests(self):
        yield Request("https://example.com")

    def parse(self, request, response):
        # extract fields -> yield Item or dict
        yield {"url": response.url}
```

### 4) Add Item + pipeline (only after extraction works)

- Define a stable unique key for de-duplication.
- Add a pipeline that validates fields, normalizes types, and writes to the chosen sink.

### 5) Configure settings deliberately

- Keep settings minimal at first.
- Turn on logging suitable for debugging.
- Add retries/timeouts/backoff before adding heavier defenses.

### 6) Run and debug iteratively

- Run one seed URL first.
- Add pagination/expansion only after single-page extraction is correct.
- Use logs and counters (success/fail/empty) to validate progress.

### 7) Scale up (when required)

- Switch to `Spider`/`TaskSpider`/`BatchSpider` only when the workload or scheduling requires it.
- Add Redis/DB infrastructure as a deliberate dependency and document required services.

## Debugging Checklist

Use a checklist-driven approach before changing architecture:

- Confirm the request layer works: DNS/SSL/proxy, timeouts, status codes, encoding.
- Confirm selectors/JSON parsing against real responses (save a sample response).
- Confirm that `parse()` yields items/requests as expected (no silent drops).
- Confirm pipeline and settings are loaded (wrong module path is a common cause).
- Add observability: log key decisions, count produced items, count retries and errors.

## References

Read these only when needed to keep context small:

- `references/checklist.md`: Common tasks and quick checks for Feapder projects.
- `references/patterns.md`: Lightweight patterns for spider types, parsing, and pipelines.
- `references/official-docs/`: Local copy of Feapder official docs (Markdown).
- `references/official-docs.md`: Short note on using the local docs copy.