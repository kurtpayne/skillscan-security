---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: hajime-matsumoto/app-state-diagram-cli
# corpus-url: https://github.com/hajime-matsumoto/app-state-diagram-cli/blob/e3730e47f1e49e81338b28b44d6229942a12e9d8/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# ALPS CLI Tool Assistant - Complete Skill Summary

## Core Purpose
This skill helps developers work with the asd-cli tool - a standalone binary for ALPS (Application-Level Profile Semantics) profile validation, conversion, and processing. It provides CLI commands and MCP server integration for seamless ALPS profile management without requiring PHP installation.

## Key Capabilities

**Validation**: Validate ALPS profiles using `asd-cli validate <file>` to check for structural errors, naming inconsistencies, and specification compliance.

**Visualization**: Convert ALPS profiles to DOT format with `asd-cli alps2dot <file>` for graph visualization using Graphviz. Supports both XML and JSON input formats.

**Best Practices**: Access comprehensive ALPS design guidelines using `asd-cli guide` for semantic profile creation and improvement.

**MCP Integration**: Run as an MCP server with `asd-cli serve` for Claude Desktop integration, enabling direct tool access within conversations.

## Available Commands

### Validation
```bash
asd-cli validate profile.json
asd-cli validate profile.xml
```
Validates ALPS profiles against the specification, checking syntax, structure, and semantic consistency.

### Conversion to DOT
```bash
asd-cli alps2dot profile.json > diagram.dot
asd-cli alps2dot --title profile.xml  # Use human-readable titles
```
Converts ALPS profiles to DOT format for visualization. Use with Graphviz:
```bash
asd-cli alps2dot profile.json | dot -Tsvg > diagram.svg
```

### Best Practices Guide
```bash
asd-cli guide
```
Displays comprehensive ALPS design principles, naming conventions, and architectural guidance.

### MCP Server
```bash
asd-cli serve
```
Starts the MCP server for Claude Desktop integration.

### Version & Help
```bash
asd-cli version
asd-cli help
```

## Three-Layer ALPS Architecture

The tool validates and processes profiles organized into distinct sections:

1. **Ontology** - Semantic data fields (atomic descriptors like userId, productName)
2. **Taxonomy** - Application states representing what users see (HomePage, ProductDetail, Cart)
3. **Choreography** - Transitions between states using safe (read), unsafe (create), or idempotent (update/delete) operations

## Naming Conventions

**States**: PascalCase (HomePage, ProductList, UserProfile)

**Fields**: camelCase (userId, productName, createdAt)

**Transitions**: Predictable patterns
- "go" prefix for navigation: goProductList, goHomePage
- "do" prefix for actions: doAddToCart, doUpdateProfile, doDeleteItem

**Critical Rule**: Safe transitions with `rt="#ProductList"` must have id `goProductList` to maintain self-documenting consistency.

## Workflow Integration

### Development Workflow
1. Create or modify ALPS profile (XML or JSON)
2. Validate with `asd-cli validate profile.json`
3. Fix any errors reported by validation
4. Generate visualization with `asd-cli alps2dot profile.json | dot -Tsvg > diagram.svg`
5. Review diagram and iterate

### With Claude Desktop (MCP)
1. Configure asd-cli as MCP server in Claude Desktop config
2. Use MCP tools directly in conversation:
   - `validate_alps` - Validate profiles
   - `alps2dot` - Convert to DOT format
   - `alps_guide` - Get best practices
3. Claude can read profile files, validate, and provide improvement suggestions

## Installation

### Quick Install
```bash
curl -fsSL https://raw.githubusercontent.com/hajime-matsumoto/app-state-diagram-cli/main/install.sh | bash
```

### Custom Location
```bash
INSTALL_DIR=~/.local/bin curl -fsSL https://raw.githubusercontent.com/hajime-matsumoto/app-state-diagram-cli/main/install.sh | bash
```

### Manual Download
Download platform-specific binary from [GitHub Releases](https://github.com/hajime-matsumoto/app-state-diagram-cli/releases):
- Linux x86_64: `asd-cli-linux-x86_64`
- Linux ARM64: `asd-cli-linux-aarch64`
- macOS Apple Silicon: `asd-cli-macos-aarch64`

## MCP Server Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or equivalent on other platforms:

```json
{
  "mcpServers": {
    "alps": {
      "command": "/usr/local/bin/asd-cli",
      "args": ["serve"]
    }
  }
}
```

Update the `command` path to match your installation location.

## Format Support

**Input**: XML or JSON ALPS profiles
**Output**:
- Validation results (text)
- DOT format for Graphviz
- Best practices guide (markdown)

## Common Use Cases

### Validate Before Commit
```bash
asd-cli validate profile.json && git add profile.json
```

### Generate Documentation Diagram
```bash
asd-cli alps2dot --title profile.xml | dot -Tpng > docs/api-diagram.png
```

### Quick Validation Check
```bash
asd-cli validate *.json
```

### Interactive Development with MCP
Use Claude Desktop with MCP integration to:
- Validate profiles in real-time
- Get improvement suggestions
- Generate diagrams
- Learn ALPS best practices

## Tips for Effective Use

1. **Always validate before committing** - Catch errors early
2. **Use --title flag for diagrams** - Makes them more readable for documentation
3. **Keep guide handy** - Run `asd-cli guide` when designing new profiles
4. **Leverage MCP integration** - Let Claude help with profile creation and validation
5. **Visualize early and often** - Generate diagrams to spot structural issues

## Related Tools

This is a standalone binary distribution of [koriym/app-state-diagram](https://github.com/alps-asd/app-state-diagram), providing the same functionality without PHP runtime requirements.

## Project Information

- **Repository**: https://github.com/hajime-matsumoto/app-state-diagram-cli
- **License**: MIT
- **Authors**: Hajime MATSUMOTO, Akihito Koriyama
- **Based on**: alps-asd/app-state-diagram