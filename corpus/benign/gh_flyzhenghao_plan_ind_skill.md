---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: flyzhenghao/plan-index-manager
# corpus-url: https://github.com/flyzhenghao/plan-index-manager/blob/ddd90a07d64193310c239777115e22ab7985606a/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Plan Index Manager

> Automatically maintain an organized index of your Claude Code planning files

## Overview

Plan Index Manager is a Claude Code hook that automatically scans your `~/.claude/plans/` directory and generates a searchable INDEX.md file. It extracts metadata from each plan file (date, title, priority, status) and organizes them in a clean, sortable table.

## Features

- 🔄 **Auto-sync on PlanModeEnd** - INDEX.md updates automatically when you exit Plan Mode
- 🌍 **Bilingual Support** - Switch between English and Chinese templates
- 📊 **Smart Metadata Extraction** - Automatically detects plan priority and status
- 🗂️ **Priority Grouping** - Plans organized by P0/P1/P2 priority levels
- 🔍 **Easy Search** - Quickly find plans by keywords
- ⚡ **Manual Trigger** - Run `bash ~/.claude/hooks/plans-sync.sh` anytime

## Installation

```bash
# Download and install
curl -fsSL https://raw.githubusercontent.com/flyzhenghao/plan-index-manager/main/install.sh | bash

# Or clone and install manually
git clone https://github.com/flyzhenghao/plan-index-manager.git
cd plan-index-manager
bash install.sh
```

## Usage

### Automatic (Recommended)

The INDEX.md will be automatically updated every time you exit Plan Mode in Claude Code.

### Manual

```bash
# Sync plans manually
bash ~/.claude/hooks/plans-sync.sh

# Switch language to Chinese
bash ~/.claude/hooks/plans-sync.sh --lang zh

# Switch language to English
bash ~/.claude/hooks/plans-sync.sh --lang en
```

### Querying Plans

Once installed, you can ask Claude Code:

- "查询 Plan: mobile UI" - Search for plans related to mobile UI
- "恢复 Plan: Authentication System" - Restore a specific plan by title

## Configuration

Language setting is stored in `~/.claude/hooks/plans-sync-config.sh`:

```bash
# Supported: en, zh
PLAN_INDEX_LANG="en"
```

## Metadata Detection

The script automatically extracts:

- **Date**: File modification time
- **Title**: First `# ` heading (strips "Peer Review Report:" prefix)
- **Priority**: Searches for P0/P1/P2 in content (defaults to P1)
- **Status**: Detects keywords like "completed", "in progress", "planning", "ongoing"

## Requirements

- Claude Code installed
- Bash 4.0+
- Plans directory at `~/.claude/plans/`

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by the Claude Code community