---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?", "explain this code", "what does this code do", "walk me through this", "explain this file", "explain this function", "explain this class", "break down this code", or wants to understand code logic, architecture, or behavior. Includes Spring Boot equivalent mappings for non-Java code.
allowed-tools: Bash(*), Glob(*), Grep(*), Read(*), WebFetch(*), WebSearch(*), mcp__claude_ai_Context7__*, mcp__plugin_context7_context7__*
argument-hint: "[file, function, class, or directory to explain]"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: adityamparikh/explain-code-skill
# corpus-url: https://github.com/adityamparikh/explain-code-skill/blob/279c740ec7fc2dc85612c659357f829675e83e39/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Code Explanation Skill

When explaining code, always include these four elements:

1. **Start with an analogy**: Compare the code to something from everyday life to build intuition before diving into details.
2. **Draw a diagram**: Use ASCII art or Mermaid diagrams to show the flow, structure, or relationships between components. Prefer Mermaid for complex flows and class relationships; use ASCII art for simple, quick illustrations.
3. **Walk through the code**: Explain step-by-step what happens.
4. **Highlight a gotcha**: Call out a common mistake or misconception related to the code.

For complex concepts, use multiple analogies.

## Output Templates

Structure explanations using these sections as appropriate:

- **File/Class:** Purpose, Key Concepts, Structure, How It Works, Dependencies & Interactions, Notable Details
- **Function/Method:** Purpose, Parameters & Return Value, How It Works, Edge Cases & Error Handling, Usage
- **Directory/Module:** Purpose, Architecture, Key Files, External Interfaces, Data Flow

## Spring Boot Equivalents

When the code is not Java/Kotlin + Spring Boot, read `references/spring-boot-mapping.md` and include equivalent mappings in the explanation.

## Verify Library and Framework Usage

The model's training data has a knowledge cutoff. When explaining code that uses libraries or frameworks, **actively verify** that your explanations reflect current APIs and behavior:

1. **Identify versions** — Check `pom.xml`, `build.gradle.kts`, `package.json`, or other dependency files to determine the exact versions of libraries and frameworks in use.
2. **Look up current documentation** — Use Context7 (`mcp__claude_ai_Context7__resolve-library-id` then `mcp__claude_ai_Context7__query-docs`) to retrieve up-to-date documentation for any library or framework where:
   - The version is newer than what the model may have been trained on
   - You are unsure whether an API, configuration property, or pattern is still valid or has been deprecated/replaced
   - The code uses advanced or less common features of a library
3. **Search the web** — Use `WebSearch` and `WebFetch` to check for:
   - Breaking changes or migration guides for the specific version in use
   - Known behavioral changes between versions that affect how the code works
   - Deprecated APIs that have been replaced in newer versions
4. **Check GitHub** — Use `gh` CLI to check release notes, changelogs, or issues for dependencies when needed (e.g., `gh api repos/{owner}/{repo}/releases/latest`)

**Do not assume** that an API or pattern is correct based solely on model knowledge. When in doubt, look it up.

## Explanation Guidelines

- **Reference specific line numbers** using `file_path:line_number` format.
- **Call out design patterns** by name (e.g., "This uses the Strategy pattern to...").