---
name: claude-code-spinner-tips
version: 1.0.0
description: |
  Community-curated bilingual spinner tips for Claude Code. 118 tips covering Claude Code shortcuts, slash commands, CLI flags, MCP, Git, Python, JS/TS, Shell, and programming wisdom. Non-intrusive, works in any terminal. Contribute tips via simple text files.
tags: ["spinner", "tips", "learning", "productivity", "bilingual", "claude-code"]
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: dongsheng123132/claude-code-spinner-tips
# corpus-url: https://github.com/dongsheng123132/claude-code-spinner-tips/blob/8b73528ec11e223ab0b2278de395ed21a8737ddb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Spinner Tips

Community-curated bilingual (zh/en) spinner tips for Claude Code. Learn while Claude thinks!

## When to use

When the user wants to:
- Install learning tips that show during Claude Code's thinking spinner
- Add custom tips to their Claude Code setup
- Contribute tips to the community collection

## How it works

1. Tips are organized by category in `tips/` directory (one per line, `中文 | English` format)
2. `build.sh` merges all tip files into `settings-snippet.json`
3. `install.sh` merges the snippet into `~/.claude/settings.json`
4. Uses `spinnerTipsOverride` with `excludeDefault: false` — official tips are preserved

## Install

```bash
bash install.sh
```

## Add Tips

Add one line per tip to the appropriate file in `tips/`:

```
中文描述 | English description
```

Categories: `claude-code.txt`, `git.txt`, `python.txt`, `javascript.txt`, `shell.txt`, `wisdom.txt`

Create new files for new categories (e.g. `rust.txt`, `docker.txt`).