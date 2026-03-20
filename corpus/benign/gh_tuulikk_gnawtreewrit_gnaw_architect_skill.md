---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Tuulikk/GnawTreeWriter
# corpus-url: https://github.com/Tuulikk/GnawTreeWriter/blob/37d0a0084bcf23305e5e64fdb3f6e1ac8cb659db/GNAW_ARCHITECT_SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Skill: GnawTree Architect 🧠🏗️

Specialized skill for structural code engineering, semantic navigation, and autonomous self-healing using **GnawTreeWriter**.

## Core Mandates

1.  **Tool-First Policy**: ALWAYS prefer `./target/release/gnawtreewriter` over generic text tools (`sed`, `replace`, `write_file`) for modifying code. 
2.  **TCARV 1.0 Adherence**:
    *   **Hypothesis**: Define the architectural change in text before acting.
    *   **Blocks**: Break changes into atomic node-based edits.
    *   **Verification**: Run `cargo check` or language-specific linters after every block.
3.  **Anti-Lobotomy**: Never delete complex logic to "fix" a build error. Use **Git Surgery** to restore from history if a node becomes corrupted.
4.  **Surgical Precision**: Target the smallest possible AST node for any given change.

## Operation Workflow

### 1. Navigation & Discovery
*   **Satelite View**: Use `sense "<query>"` to find relevant files across the project.
*   **Zoom View**: Use `sense "<query>" <file>` to find specific nodes within a file.
*   **Skeleton**: Use `get_skeleton <file>` to understand the structural layout without consuming high tokens.
*   **Impact Analysis**: Always use the `--impact` flag (or check the `impact` field in MCP) before editing high-traffic functions.

### 2. Modification
*   **Verification-First**: Run `list <file>` to get the current AST path before every `edit` or `insert`.
*   **STDIN for Safety**: Use `-` as content and pipe the code via STDIN to avoid shell escaping nightmares.
*   **Relative Placement**: Use `sense-insert` for adding new logic near semantic landmarks.

### 3. The Duplex Loop (Self-Healing)
*   **Preview**: Use `edit --preview` to see the proposed change.
*   **Healing**: If a `SyntaxError` is reported, analyze the `line` and `column` provided and use the `Healer` logic to fix braces, colons, or semicolons before final application.

## Language Specifics

*   **Rust**: Target `impl_item`, `function_item`, and `struct_item`. Use `cargo check` for verification.
*   **Python**: Target `class_definition` and `function_definition`. Use `ruff` or `python -m py_compile`.
*   **QML**: Target `ui_object` and `ui_property`. Use `qmlformat` if available.

## Spirit of the Tool
"Gnaw through the noise, preserve the intent." The architect does not just write text; they manipulate the tree of thought.