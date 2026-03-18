#!/usr/bin/env python3
"""scripts/seed_corpus.py — Seed the training corpus with synthetic benign skill files.

Generates a configurable number of realistic-looking benign SKILL.md files
to balance the corpus against the adversarial (injection/malicious) examples.

Usage
-----
    python scripts/seed_corpus.py [--count N] [--output-dir PATH]

Options
-------
    --count INT         Number of benign examples to generate (default: 50)
    --output-dir PATH   Where to write the files (default: corpus/benign/)
    --seed INT          Random seed for reproducibility (default: 42)
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# Skill templates — realistic benign skill file content
# ---------------------------------------------------------------------------

SKILL_TEMPLATES = [
    """\
---
name: {name}
version: "1.0"
description: >
  {description}
tags: [{tags}]
---

## Overview

{overview}

## Inputs

- `{input1}` ({input1_type}): {input1_desc}
- `{input2}` ({input2_type}): {input2_desc}

## Outputs

- `{output1}` ({output1_type}): {output1_desc}

## Examples

```yaml
{example}
```

## Notes

{notes}
""",
    """\
---
name: {name}
version: "0.9"
description: {description}
tags: [{tags}]
---

# {name}

{overview}

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| {input1} | {input1_type} | yes | {input1_desc} |
| {input2} | {input2_type} | no | {input2_desc} |

### Return value

{output1_desc}

### Example usage

```
{example}
```
""",
]

SKILL_DOMAINS = [
    ("fetch-webpage", "Fetches the content of a webpage and returns the HTML or extracted text.",
     "web, http, scraping", "url", "string", "The URL to fetch",
     "timeout", "integer", "Request timeout in seconds",
     "content", "string", "The fetched page content",
     "fetch-webpage url=https://example.com timeout=10",
     "Uses requests library. Respects robots.txt by default."),

    ("parse-json", "Parses a JSON string and returns a structured Python object.",
     "json, parsing, data", "json_string", "string", "The JSON string to parse",
     "strict", "boolean", "Whether to raise on duplicate keys",
     "parsed", "dict", "The parsed Python dictionary or list",
     "parse-json json_string='{\"key\": \"value\"}'",
     "Returns None on parse failure unless strict=true."),

    ("send-email", "Sends an email via SMTP using the configured mail server.",
     "email, smtp, notification", "recipient", "string", "Recipient email address",
     "subject", "string", "Email subject line",
     "message_id", "string", "The sent message ID",
     "send-email recipient=user@example.com subject='Hello'",
     "Requires SMTP credentials in environment variables."),

    ("query-database", "Executes a read-only SQL query against the configured database.",
     "database, sql, query", "query", "string", "The SQL SELECT statement to execute",
     "params", "list", "Optional query parameters for parameterised queries",
     "rows", "list", "List of result rows as dictionaries",
     "query-database query='SELECT * FROM users WHERE id = ?' params=[42]",
     "Only SELECT statements are permitted. INSERT/UPDATE/DELETE will raise an error."),

    ("resize-image", "Resizes an image to the specified dimensions.",
     "image, resize, media", "image_path", "string", "Path to the source image file",
     "width", "integer", "Target width in pixels",
     "output_path", "string", "Path to the resized image",
     "resize-image image_path=/tmp/photo.jpg width=800",
     "Maintains aspect ratio by default. Supports JPEG, PNG, and WebP."),

    ("read-csv", "Reads a CSV file and returns its contents as a list of dictionaries.",
     "csv, data, parsing", "file_path", "string", "Path to the CSV file",
     "delimiter", "string", "Column delimiter character (default: comma)",
     "rows", "list", "List of row dictionaries keyed by column header",
     "read-csv file_path=/data/report.csv delimiter=,",
     "Handles UTF-8 and Latin-1 encodings automatically."),

    ("list-directory", "Lists files and directories at the specified path.",
     "filesystem, directory, listing", "path", "string", "Directory path to list",
     "recursive", "boolean", "Whether to recurse into subdirectories",
     "entries", "list", "List of file/directory entry objects",
     "list-directory path=/home/user/documents recursive=false",
     "Returns entries sorted alphabetically. Symlinks are followed."),

    ("calculate-hash", "Computes a cryptographic hash of a file or string.",
     "security, hash, crypto", "input", "string", "File path or string to hash",
     "algorithm", "string", "Hash algorithm: sha256, sha512, md5",
     "hash", "string", "Hexadecimal hash digest",
     "calculate-hash input=/path/to/file algorithm=sha256",
     "MD5 is provided for compatibility only; prefer SHA-256 or SHA-512."),

    ("format-date", "Formats a date/time value according to a specified format string.",
     "datetime, formatting, utility", "date", "string", "ISO 8601 date string to format",
     "format", "string", "strftime format string",
     "formatted", "string", "The formatted date string",
     "format-date date=2026-03-17 format='%B %d, %Y'",
     "Timezone-aware inputs are converted to UTC before formatting."),

    ("validate-schema", "Validates a JSON document against a JSON Schema.",
     "validation, schema, json", "document", "dict", "The JSON document to validate",
     "schema", "dict", "The JSON Schema to validate against",
     "valid", "boolean", "True if the document is valid",
     "validate-schema document={...} schema={...}",
     "Returns detailed error messages on validation failure."),

    ("compress-files", "Compresses one or more files into a ZIP or tar.gz archive.",
     "compression, archive, files", "files", "list", "List of file paths to compress",
     "output_path", "string", "Path for the output archive",
     "archive_path", "string", "Path to the created archive",
     "compress-files files=[/tmp/a.txt, /tmp/b.txt] output_path=/tmp/archive.zip",
     "Supports ZIP and tar.gz formats based on output file extension."),

    ("translate-text", "Translates text from one language to another.",
     "translation, nlp, language", "text", "string", "The text to translate",
     "target_language", "string", "Target language code (e.g. 'es', 'fr', 'de')",
     "translated", "string", "The translated text",
     "translate-text text='Hello world' target_language=es",
     "Source language is auto-detected. Requires translation API credentials."),

    ("generate-uuid", "Generates a universally unique identifier (UUID).",
     "utility, uuid, id", "version", "integer", "UUID version: 1, 4, or 5",
     "namespace", "string", "Namespace for version 5 UUIDs",
     "uuid", "string", "The generated UUID string",
     "generate-uuid version=4",
     "Version 4 is recommended for most use cases."),

    ("check-url-status", "Checks the HTTP status code of a URL.",
     "http, monitoring, url", "url", "string", "The URL to check",
     "timeout", "integer", "Request timeout in seconds",
     "status_code", "integer", "The HTTP response status code",
     "check-url-status url=https://example.com timeout=5",
     "Returns 0 on connection failure. Does not follow redirects by default."),

    ("extract-text-from-pdf", "Extracts plain text content from a PDF file.",
     "pdf, text, extraction", "file_path", "string", "Path to the PDF file",
     "pages", "list", "Optional list of page numbers to extract (1-indexed)",
     "text", "string", "The extracted plain text",
     "extract-text-from-pdf file_path=/docs/report.pdf pages=[1,2,3]",
     "Requires pdfminer or pypdf2. Scanned PDFs may require OCR."),
]


def generate_skill(domain_data: tuple, index: int) -> str:
    (name, description, tags, input1, input1_type, input1_desc,
     input2, input2_type, input2_desc, output1, output1_type, output1_desc,
     example, notes) = domain_data

    template = SKILL_TEMPLATES[index % len(SKILL_TEMPLATES)]
    return template.format(
        name=name,
        description=description,
        tags=tags,
        overview=description,
        input1=input1, input1_type=input1_type, input1_desc=input1_desc,
        input2=input2, input2_type=input2_type, input2_desc=input2_desc,
        output1=output1, output1_type=output1_type, output1_desc=output1_desc,
        example=example,
        notes=notes,
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed corpus with synthetic benign skill files")
    p.add_argument("--count", type=int, default=50)
    p.add_argument("--output-dir", type=Path, default=REPO_ROOT / "corpus" / "benign")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    random.seed(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    for i in range(args.count):
        domain = SKILL_DOMAINS[i % len(SKILL_DOMAINS)]
        content = generate_skill(domain, i)
        filename = f"synthetic_{domain[0]}_{i:03d}.md"
        dest = args.output_dir / filename
        if not dest.exists():  # don't overwrite hand-crafted examples
            dest.write_text(content, encoding="utf-8")
            generated += 1

    print(f"Generated {generated} synthetic benign skill files in {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
