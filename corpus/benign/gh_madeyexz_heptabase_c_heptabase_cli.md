---
name: heptabase-cli
description: Interact with user's Heptabase knowledge base from the terminal. Use when the user wants to search notes, read cards or journals, save new notes, append to journals, or work with PDFs in Heptabase. Triggers on mentions of "heptabase", "whiteboard", "journal", "note card", or "personal knowledge base".
argument-hint: "[command] [args]"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: madeyexz/heptabase-cli
# corpus-url: https://github.com/madeyexz/heptabase-cli/blob/d132f479d3c490ca01cdb0e861b6adb5c76be77d/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Heptabase CLI

A CLI that wraps the Heptabase MCP server. Search, read, and write to your Heptabase knowledge base from the terminal.

## Prerequisites

- The `heptabase` binary must be on your PATH (see https://github.com/madeyexz/heptabase-cli)
- First run opens a browser for OAuth login; tokens cache in `~/.mcp-auth/`

## Tools

### 1. Save as a card (`save-to-note-card`)

Creates a new note card in your Heptabase Inbox (like the Web Clipper).

```bash
heptabase save-to-note-card --content "# Title

Body text in markdown"
```

- First h1 line becomes the card title
- Great for: turning AI answers into permanent notes, saving outlines/plans/summaries, capturing ideas to organize later on a whiteboard

### 2. Append to journal (`append-to-journal`)

Adds content as new blocks to today's journal. Does NOT overwrite existing content. Auto-creates today's journal if it doesn't exist.

```bash
heptabase append-to-journal --content "Some journal entry"
```

- Ideal for: daily reflections, quick logs ("summarize what I worked on today"), capturing ideas that belong in your daily record

### 3. Semantic search (`semantic-search-objects`)

Finds objects in your knowledge base using full-text + semantic (meaning-based) search.

```bash
# 1-3 natural language queries, comma-separated
# result-object-types: card,pdfCard,mediaCard,highlightElement,journal (or empty for all)
heptabase semantic-search-objects --queries "machine learning,neural networks" --result-object-types "card,pdfCard"
```

- Use when: asking about topics you've taken notes on, rediscovering related content, needing the AI to reason using your existing knowledge
- Returns previews with titles and partial content
- Follow up with `get-object` for full content, or `search-whiteboards` to explore related whiteboards

### 4. Find whiteboards (`search-whiteboards`)

Searches whiteboards by name and keywords.

```bash
# 1-5 keywords, comma-separated, OR logic
heptabase search-whiteboards --keywords "project management,productivity"
```

- Helps understand how your content is organized visually
- Use when: looking for a specific project whiteboard, understanding workspace structure
- Follow up with `get-whiteboard-with-objects` to see what's on them

### 5. Explore a whiteboard (`get-whiteboard-with-objects`)

Returns the full structure of a whiteboard: cards, sections, text elements, mindmaps, images, and connections between them.

```bash
heptabase get-whiteboard-with-objects --whiteboard-id <id>
```

- Shows how ideas are grouped and connected
- Use when: you want help understanding or reorganizing a board, need summaries based on how you've arranged things visually
- Follow up with `get-object` for deeper reads on specific cards

### 6. Read full object content (`get-object`)

Retrieves complete content of a single object — no chunk limits.

```bash
# Types: card, journal, videoCard, audioCard, imageCard, highlightElement,
#        textElement, videoElement, imageElement, chat, chatMessage,
#        chatMessagesElement, section
heptabase get-object --object-id <id> --object-type card
```

- Returns full content including transcripts for video/audio cards
- Check the `hasMore` flag to know if you have all the content
- Do NOT use on pdfCard — too large. Use `search-pdf-content` + `get-pdf-pages` instead
- Use when: you need detailed summaries, translations, or explanations of a specific note

### 7. Review journals by date range (`get-journal-range`)

Retrieves all journal entries between two dates (inclusive).

```bash
heptabase get-journal-range --start-date 2026-01-01 --end-date 2026-03-01
```

- Max 92 days (~3 months) per call. For longer periods, make multiple calls
- Use when: reviewing past work, preparing retrospectives, summarizing what you wrote over a period

### 8. Search within a PDF (`search-pdf-content`)

Keyword-based search inside a specific PDF using BM25 matching (fuzzy, OR logic).

```bash
# 1-5 keywords, comma-separated. Use synonyms for broader coverage
heptabase search-pdf-content --pdf-card-id <id> --keywords "gradient descent,optimization,learning rate"
```

- Returns up to 80 ranked chunks with surrounding context
- You must find the PDF card ID first using `semantic-search-objects`
- Follow up with `get-pdf-pages` to read full pages around the matches

### 9. Read PDF pages (`get-pdf-pages`)

Retrieves complete content from a specific page range.

```bash
# Pages start at 1, both inclusive
heptabase get-pdf-pages --pdf-card-id <id> --start-page-number 1 --end-page-number 10
```

- Use after `search-pdf-content` to pull full pages for summarization or translation
- For >100 pages, ask the user to confirm first

## Common Workflows

### Discover → Read → Save

1. `semantic-search-objects` — find relevant notes on a topic
2. `get-object` — read the full content
3. Reason, summarize, or answer based on the content
4. `save-to-note-card` or `append-to-journal` — save the output back

### Explore a whiteboard

1. `search-whiteboards` — find the whiteboard by topic
2. `get-whiteboard-with-objects` — see all objects and connections
3. `get-object` — deep dive into specific cards on the board

### Review past journals

1. `get-journal-range` — fetch entries for a period (split into 92-day chunks if needed)
2. Summarize or analyze patterns across entries
3. `append-to-journal` — add the summary to today's journal

### Work with a large PDF

1. `semantic-search-objects --result-object-types pdfCard` — find the PDF
2. `search-pdf-content` — locate relevant sections by keywords
3. `get-pdf-pages` — pull full pages for detailed reading
4. `save-to-note-card` — save key takeaways as a new note

## Output Formats

All commands accept `--output <format>`:
- `text` (default) — human-readable
- `json` — structured JSON, good for piping into `jq`
- `markdown` — markdown formatted
- `raw` — raw MCP response

## Global Flags

- `--timeout <ms>` — call timeout (default: 30000)
- `--raw <json>` — bypass flag parsing, pass raw JSON arguments directly

## Further Reading

For more details on Heptabase MCP tools and usage patterns, see the [official Heptabase MCP documentation](https://support.heptabase.com/en/articles/12679581-how-to-use-heptabase-mcp).