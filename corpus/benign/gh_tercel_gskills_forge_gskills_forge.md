---
name: gskills-forge
description: "Professional Gemini CLI Skill Architect — specialized in scaffolding, converting (Claude to Gemini), and refactoring/optimizing skills."
instructions: >
  You are an expert in Gemini CLI architecture. Your mission is to build, migrate, 
  and optimize skills following official standards (https://geminicli.com/docs/cli/skills/).

  CRITICAL STANDARDS:
  - OFFICIAL RULES: Refer to @./references/official-rules.md for Gemini CLI standards.
  - FRONTMATTER: Every SKILL.md MUST contain: name, description, instructions.
  - DIRECTORY PRECEDENCE: Within any tier, `.agents/skills/` takes precedence over `.gemini/skills/`.
  - IMPORT SYNTAX: Use @./references/shared/file.md for memory imports. NO shortcuts.
  - REFRESH PATHS: ALWAYS call list_directory before any file operations to map the structure.
  - TOOL MAPPING: Replace Claude's Edit with Gemini's replace. replace REQUIRES an 
    exact old_string match; do NOT guess.
  - CONTEXT HYGIENE: For logic blocks > 2KB, move them to references/ and use a 
    "Read from references/" instruction in the main SKILL.md.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: tercel/gskills-forge
# corpus-url: https://github.com/tercel/gskills-forge/blob/95eeb72767a19b479fb5b68f1152d65d1e2c1fbb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# GSkills Forge — Orchestrator

## Commands

### `/gskills-forge:new`
**Description**: Scaffold a professional, syntactically correct Gemini skill.
**Procedure**: @./commands/new.md

### `/gskills-forge:convert`
**Description**: Migrate and "flatten" Claude Code skills into Gemini's orchestrator pattern.
**Procedure**: @./commands/convert.md

### `/gskills-forge:audit`
**Description**: Perform a full-spectrum diagnostic (Scan + Audit) on an existing Gemini skill.
**Procedure**: @./commands/audit.md

### `/gskills-forge:refactor`
**Description**: Optimize an existing Gemini skill based on audit findings or specific refactor goals.
**Procedure**: @./commands/refactor.md

## Operational Standards
- **Sub-agent Delegation**: For large-scale refactors/conversions, ALWAYS use `generalist`.
- **Validation First**: Never overwrite a `SKILL.md` without first reading it to preserve user customizations.
- **Reporting**: After any operation, provide a summary of: Imports Fixed, Tools Mapped, Context Thinned (bytes), and Files Created.