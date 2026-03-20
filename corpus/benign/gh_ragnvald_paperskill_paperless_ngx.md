---
name: paperless-ngx
description: "Search and retrieve documents from a Paperless-ngx archive via REST API. Use when the user wants to find, read, or update documents stored in Paperless-ngx (for example: search by keyword or tag, fetch document content, or update document metadata)."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ragnvald/paperskill
# corpus-url: https://github.com/ragnvald/paperskill/blob/491e89c4deae9a1791635ad70546f0f1f2a7c9f2/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Paperless-ngx

## Overview
Use this skill to query a Paperless-ngx instance and retrieve or update documents via its REST API using the bundled scripts.

## Prerequisites
- Set `PAPERLESS_URL` and `PAPERLESS_TOKEN` environment variables.
- Install Python 3.10+ and `requests`.

## Quick Start
```bash
python scripts/search.py --query "tax form" --limit 5
python scripts/fetch.py --id 123 --text
python scripts/update_meta.py --id 123 --add-tag important
```

## Tasks

### Search documents
Run `scripts/search.py` to find documents by keyword, tag, type, correspondent, or date.
`--query` performs server-side full-text search in Paperless-ngx (includes OCR/content when the server index has it). This skill never downloads document content for searching.

Filters:
- `--query` full-text search string (server-side; matches OCR/content when indexed)
- `--tag` tag name (repeatable)
- `--type` document type name
- `--correspondent` correspondent name
- `--after` created after (YYYY-MM-DD)
- `--before` created before (YYYY-MM-DD)
- `--limit` max results (default 10)
- `--json` output as JSON

Example:
```bash
python scripts/search.py --query "invoice" --tag receipts --after 2024-01-01 --limit 20
```

### Fetch documents
Run `scripts/fetch.py` to download files or print OCR/text content.

Options:
- `--id` document ID (required)
- `--out` output file path or directory
- `--text` print the document `content` field instead of downloading

Example:
```bash
python scripts/fetch.py --id 123 --out ./downloads/
```

### Update metadata
Run `scripts/update_meta.py` to change tags, title, or correspondent.

Options:
- `--add-tag` tag name to add (repeatable)
- `--remove-tag` tag name to remove (repeatable)
- `--title` new title
- `--correspondent` new correspondent name

Example:
```bash
python scripts/update_meta.py --id 123 --add-tag important --remove-tag inbox
```

## Output
- Search output is a table by default with columns `id`, `title`, `created`, `correspondent`, `tags`, `document_type`.
- Use `--json` for machine-readable search results.

## Notes
- Authentication uses `Authorization: Token {PAPERLESS_TOKEN}`.
- Pagination is handled automatically.
- If text output is missing, OCR may still be processing. Reprocess in Paperless-ngx and retry.
- Search uses Paperless-ngx server-side full-text search via the `query` parameter; no document contents are downloaded for searching.
- Full-text results depend on the server index (OCR/content availability is determined by Paperless-ngx settings and processing status).

## Resources
- `scripts/search.py` searches documents with optional filters.
- `scripts/fetch.py` downloads documents or prints text content.
- `scripts/update_meta.py` updates document metadata.