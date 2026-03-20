---
name: notion-md-converter
description: Markdown and Notion format conversion skill. Converts Markdown to Notion blocks, handles bold/italic, tables as lists, and supports page creation and updates.
homepage: https://developers.notion.com
metadata:
  {
    "openclaw":
      { "emoji": "📝", "requires": { "env": ["NOTION_API_KEY"] }, "primaryEnv": "NOTION_API_KEY" }
  }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: maweis1981/notion-md-converter
# corpus-url: https://github.com/maweis1981/notion-md-converter/blob/dd72af35b1616454d0e4a819586c55249f0076ba/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# notion-md-converter

Markdown and Notion format conversion, with current support focused on Markdown -> Notion.

## Features

- Convert Markdown to Notion blocks
- Support for bold (`**text**`) using annotations
- Italic (`*text*`) support
- Tables converted to bullet lists
- Horizontal rules converted to dividers
- Code blocks with syntax highlighting
- Link detection
- Create pages or add to existing pages

## Setup

### 1. Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Name it (e.g., "OpenClaw Converter")
4. Copy the API key (starts with `ntn_`)

### 2. Store API Key

```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```

Or set environment variable:

```bash
export NOTION_API_KEY="ntn_your_key_here"
```

### 3. Share Pages with Integration

Open your Notion page -> Click "..." -> "Connect to" -> Select your integration

## Usage

### Basic Page Creation

```bash
# From file
notion-md-converter create --file README.md --title "My Page"

# From stdin
echo "# Hello" | notion-md-converter create --title "Test Page"

# To specific parent page
notion-md-converter create --file report.md --parent-page-id "abc123..."
```

### Add Content to Existing Page

```bash
notion-md-converter append --file notes.md --page-id "abc123..."
```

### Options

```
--file, -f     Input Markdown file (default: stdin)
--title, -t    Page title (required for create)
--parent-id    Parent page ID for nesting
--emoji        Page icon emoji (default: 📄)
```

Legacy command alias: `notion-sync` (kept for compatibility).

## Notion Block Mapping

| Markdown | Notion Block |
|----------|--------------|
| `# Title` | heading_1 |
| `## Title` | heading_2 |
| `### Title` | heading_3 |
| `**bold**` | paragraph with bold annotation |
| `*italic*` | paragraph with italic annotation |
| `***bold+italic***` | paragraph with both |
| `---` | divider |
| ````python code```` | code block with language |
| `[link](url)` | paragraph with link |
| `- item` | bulleted_list_item |
| `1. item` | numbered_list_item |
| `| table |` | paragraph (tables as text) |
| `> quote` | quote block |

## Examples

### Create a Page from File

```bash
notion-md-converter create \
  --file "/path/to/report.md" \
  --title "Weekly Report" \
  --emoji "📊"
```

### Append to Existing Page

```bash
notion-md-converter append \
  --file "new-section.md" \
  --page-id "550e8400-e29b-41d4-a716-446655440000"
```

### Pipeline Usage

```bash
cat notes.md | notion-md-converter create --title "Meeting Notes"
```

## Configuration

### Environment Variables

| Variable | Description |
|-----------|-------------|
| `NOTION_API_KEY` | Notion API key (recommended) |
| `~/.config/notion/api_key` | Alternative key storage |

### API Version

Uses Notion API version `2025-09-03`

## Notes

- Maximum 100 blocks per request (chunking for longer content)
- Bold/italic uses `annotations` in rich_text
- Tables are converted to formatted text lists
- Horizontal rules become divider blocks
- Code blocks support syntax highlighting