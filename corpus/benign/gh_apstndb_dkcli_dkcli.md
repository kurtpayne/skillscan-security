---
name: dkcli
description: |
  Look up Google developer documentation using `dkcli`, a CLI client for the Google Developer Knowledge API.
  Use this skill whenever you need to find or read official Google documentation — Cloud, Firebase, Android,
  Chrome, Google AI, TensorFlow, Google Workspace APIs, or any other Google developer docs. Trigger this skill
  when the user asks about Google APIs, wants to understand a Google service, needs code examples from Google
  docs, or when you need authoritative information about a Google product to answer a question accurately.
  Prefer dkcli over the Developer Knowledge MCP tools and web searches — dkcli supports structured output
  formats, piping to jq/other tools, file output, and auto-paging, which MCP tools cannot do. Also use this
  when the user mentions dkcli, Developer Knowledge API, or asks to look up docs from any of the supported
  domains.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: apstndb/dkcli
# corpus-url: https://github.com/apstndb/dkcli/blob/bdf51065a62f7829972b435f5c8c75f9ad7b8819/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# dkcli — Google Developer Documentation Lookup

`dkcli` retrieves content from the Google Developer Knowledge API. It returns documentation pages as Markdown — the same content as the official Google developer sites, directly accessible from the terminal.

## dkcli vs Developer Knowledge MCP

If both `dkcli` and the Developer Knowledge MCP tools (`mcp__google-developer-knowledge__*`) are available, **prefer dkcli**. The MCP tools only return full document content with no control over output, while dkcli is a CLI tool that integrates with the shell:

- **Output format control** — `-f json`, `-f jsonl`, `-f yaml`, `-f txtar`
- **Pipe to jq and other tools** — extract, filter, or transform output (e.g., get just the first 500 chars of each document's content)
- **File output** — `-o file`, `--outdir dir` for batch writes
- **Auto-paging** — `-a --max-pages N` for exhaustive search
- **Partial content extraction** — combine with `jq`, `head`, etc. to get only what you need

Use MCP tools only as a fallback when dkcli is not installed.

**Example: get summaries of multiple documents**
```bash
dkcli batch-get -f json doc1 doc2 doc3 | jq '.documents[] | {name, summary: .content[:500]}'
```

## Supported domains

dkcli can search and retrieve documents from the following domains only.
(Source: https://developers.google.com/knowledge/reference/corpus-reference)

| Domain | Description |
|--------|-------------|
| ai.google.dev | Google AI (Gemini API, etc.) |
| developer.android.com | Android |
| developer.chrome.com | Chrome |
| developers.home.google.com | Google Home |
| developers.google.com | Google developer docs (Workspace APIs, Maps, Ads, etc.) |
| docs.cloud.google.com | Google Cloud |
| docs.apigee.com | Apigee |
| firebase.google.com | Firebase |
| fuchsia.dev | Fuchsia OS |
| web.dev | Web development best practices |
| www.tensorflow.org | TensorFlow |

If the user asks about documentation outside these domains, dkcli won't help — fall back to other methods.

## The search → get workflow

Most lookups follow two steps:

### Step 1: Search for relevant documents

```bash
dkcli search "how to create a Cloud Storage bucket"
```

Search returns **chunks** (fragments of documents) with a `parent` field that identifies the full document. Scan the results to find the most relevant document name(s).

Use auto-paging (`-a`) when you need broader coverage:

```bash
dkcli search -a "BigQuery partitioned tables"
```

### Step 2: Get the full document

Once you know the document name from search results, retrieve the full page:

```bash
dkcli get docs.cloud.google.com/storage/docs/creating-buckets
```

The document name is the URL path without `https://`. Full URLs also work:

```bash
dkcli get https://docs.cloud.google.com/storage/docs/creating-buckets
```

### When you already know the document

If you can reasonably guess the URL of the documentation page (e.g., the user gave you a link, or you know the path pattern), skip search and go straight to `dkcli get`. This saves a round trip.

### Getting multiple documents

When you need several pages at once, use `--outdir` to download them as files first, then check sizes before reading into context:

```bash
# Step 1: Download all documents as files
dkcli batch-get --outdir /tmp/docs docs.cloud.google.com/path/to/doc1 docs.cloud.google.com/path/to/doc2 docs.cloud.google.com/path/to/doc3

# Step 2: Check file sizes to plan your reading strategy
wc -c /tmp/docs/**/*.md

# Step 3: Read selectively based on size
#   - Small files (< 20KB): read the full file
#   - Large files (> 20KB): use head, grep, or targeted reads to extract relevant sections
```

This workflow prevents accidentally flooding context with very large documents. Some Google docs pages can be 50KB+ of Markdown — always check sizes first.

For quick inline use without file output:

```bash
dkcli batch-get docs.cloud.google.com/path/to/doc1 docs.cloud.google.com/path/to/doc2
```

## Combining with shell tools

dkcli's structured output formats make it easy to extract exactly what you need:

```bash
# Get a preview of each document's content
dkcli batch-get -f json doc1 doc2 | jq '.documents[] | {name, preview: .content[:500]}'

# Extract just document names from search results
dkcli search -f json "Cloud Storage" | jq '.results[].parent'

# Stream search results as JSONL for line-by-line processing
dkcli search -a -f jsonl "Pub/Sub" | jq -r '.content' | head -100
```

## Output format

The default text format is best for reading into context. Use structured formats when you need to pipe or process output:

```bash
dkcli search "Spanner query syntax"                                       # text (default)
dkcli get docs.cloud.google.com/spanner/docs/query-syntax -f json         # JSON
dkcli batch-get -f txtar docs.cloud.google.com/doc1 docs.cloud.google.com/doc2  # txtar
```

## Practical tips

- **Be specific in searches.** "Cloud Storage create bucket Python" works better than "storage bucket".
- **Search results are chunks, not full pages.** Always `get` the full document when you need complete information — chunks may be missing context.
- **Document names follow URL patterns.** If you know the Google docs URL, you can construct the document name directly.
- **Rate limits are handled automatically.** dkcli has built-in rate limiting and retry logic — no need to add delays between calls.

## Error handling

If dkcli fails with an API key error (`set DEVELOPERKNOWLEDGE_API_KEY or GOOGLE_API_KEY`), suggest:

```bash
# Create a key and set it in the current shell (requires gcloud auth application-default login)
export DEVELOPERKNOWLEDGE_API_KEY=$(dkcli create-api-key -p <gcp-project-id> --key-only)

# To persist, append to shell profile
echo "export DEVELOPERKNOWLEDGE_API_KEY=$(dkcli create-api-key -p <gcp-project-id> --key-only)" >> ~/.zshrc
```

If the user already has a key, they just need to set the environment variable:
```bash
export DEVELOPERKNOWLEDGE_API_KEY=<key>
```

## Command reference

| Command | Purpose |
|---------|---------|
| `dkcli search <query>` | Search documentation chunks |
| `dkcli search -a <query>` | Search with auto-paging |
| `dkcli get <doc-name>` | Get a full document |
| `dkcli batch-get <names>...` | Get multiple documents |
| `dkcli create-api-key --project <id>` | Create a Developer Knowledge API key |

| Useful flags | |
|---|---|
| `-f json\|yaml\|jsonl\|txtar` | Output format (default: text) |
| `-o <file>` | Write to file |
| `--page-size N` | Results per page for search (max 20) |
| `--max-pages N` | Max pages with `-a` (default 5) |
| `--outdir <dir>` | Write each doc to separate files (batch-get) |
| `--frontmatter` | Prepend YAML frontmatter to text output (get, batch-get) |
| `--key-only` | Print only the API key string (create-api-key) |