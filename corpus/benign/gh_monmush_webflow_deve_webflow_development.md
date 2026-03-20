---
name: webflow-development
description: >
  Build and style websites in the Webflow Designer using the Webflow MCP Bridge and browser automation.
  Use when the user wants to: (1) create or style pages/sections/elements in Webflow, (2) transfer a local
  web project (React, HTML/CSS, Next.js, etc.) to Webflow, (3) implement a Figma design in Webflow,
  (4) fix styling or layout issues in Webflow, (5) create or manage Webflow components, variables, or
  CMS collections, (6) work with responsive breakpoints in Webflow, (7) add custom code (Code Embeds)
  for SVGs, animations, or complex layouts, or (8) publish and QA a Webflow site. Trigger when user
  mentions "Webflow", "webflow designer", "MCP bridge", or asks to build/style web pages with Webflow tools.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: monmush/webflow-development
# corpus-url: https://github.com/monmush/webflow-development/blob/afee538b6fdade83c7af91f3dc1ff48c8495cbb1/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Webflow Development

Build pixel-perfect websites in the Webflow Designer using MCP tools and browser automation.

## Prerequisites

- **Webflow MCP Bridge** Chrome extension connected (provides `mcp__webflow__*` tools)
- **Claude in Chrome** extension for browser automation (navigation, clicks, JS injection)
- Webflow Designer open in Chrome with the target site loaded

## Core Workflow

1. **Discover** — Use `element_tool` to explore the current page structure and find elements by style name
2. **Build** — Use `element_builder` to create new elements (DivBlock, Heading, Paragraph, LinkBlock, Image, etc.)
3. **Style** — Use `style_tool` to apply CSS properties at each breakpoint
4. **Content** — Use `set_text` (via `element_tool`) to set text content on Heading/Paragraph elements
5. **Components** — Use `element_builder` with `component` param to insert component instances
6. **Code Embeds** — Use browser automation to add Code Embed elements for SVGs, custom CSS, or complex patterns
7. **QA** — Use `element_snapshot_tool` to capture screenshots, resize browser for responsive checks
8. **Publish** — Use `data_sites_tool` to publish the site

## Tool Quick Reference

| Tool | Purpose |
|------|---------|
| `element_tool` | Select/find elements, get element tree, set text, move/delete elements |
| `element_builder` | Create new elements (type, parent, position, component instances) |
| `style_tool` | Read/write CSS properties on style classes at specific breakpoints |
| `element_snapshot_tool` | Capture visual screenshots of elements or pages |
| `variable_tool` | Manage design variables (colors, fonts, spacing) |
| `data_pages_tool` | List/manage pages |
| `data_sites_tool` | Publish site, get site info |
| `de_page_tool` | Page-level settings (title, slug, SEO) |
| `de_component_tool` | Manage components (create, rename, list instances) |
| `style_tool` with `get_styles` | List all existing style classes on the site |
| `webflow_guide_tool` | Ask Webflow-specific questions (documentation reference) |

## Breakpoint System (Critical)

Webflow uses a **desktop-first** cascade. Styles set on `main` inherit downward unless overridden.

| Breakpoint | Name | Width | Cascade |
|-----------|------|-------|---------|
| `main` | Desktop | ≥992px | Default — all screens inherit |
| `medium` | Tablet | ≤991px | Overrides main |
| `small` | Mobile landscape | ≤767px | Overrides medium |
| `tiny` | Mobile portrait | ≤478px | Overrides small |
| `xl` | Wide | ≥1440px | Extends main upward |

**When transferring from a local mobile-first codebase**, see [references/breakpoints-and-styles.md](references/breakpoints-and-styles.md) for the mapping table.

### Setting Styles at Breakpoints

```
style_tool → set_styles:
  styleName: "my-element"
  breakpoint: "main"          # or "medium", "small", "tiny", "xl"
  pseudo: "noPseudo"          # REQUIRED when updating existing properties on main
  properties:
    font-size: "18px"
    color: "#1A2332"
```

## Known Gotchas (Must-Know)

1. **`pseudo: "noPseudo"` is required** when updating existing properties on `main` breakpoint. Without it, the value silently fails to change.
2. **`overflow` is a shorthand** — use `overflow-x` and `overflow-y` separately.
3. **`TextBlock` type creates a DivBlock** that does NOT support `set_text`. Use `Heading` or `Paragraph` types for text elements.
4. **`element_builder` with `component: ""`** (empty string) causes timeouts. Always pass a valid component ID or omit the parameter.
5. **Large element trees** — `element_tool` with `get_elements` on complex pages can return 100K+ characters. Filter by style name or save to file and parse with jq/Python.
6. **Designer in preview mode** — URLs with `workflow=sitePreview` block style edits. Navigate to the designer URL without this parameter.
7. **MCP connection drops** — If you get "Unable to connect to Webflow Designer", navigate to the designer URL with the `?app=` parameter to reconnect the MCP Bridge.
8. **Inline styles override CSS** — Some Webflow interactions (e.g., animations) leave stuck inline styles like `transform: translate3d(...)`. Override with `!important` in a Code Embed.

For the complete gotchas reference with solutions, see [references/gotchas.md](references/gotchas.md).

## Section Container Pattern

Every page section should include container constraints to prevent content from touching viewport edges:

- **main:** `max-width: 1200px`, `margin-left: auto`, `margin-right: auto`
- **medium:** `padding-left: 40px`, `padding-right: 40px`
- **small:** `padding-left: 20px`, `padding-right: 20px`

## Workflow: Transferring a Local Project to Webflow

When the user has a local web project (React, Vue, HTML/CSS, etc.) and wants to replicate it in Webflow:

1. **Read the local component** (TSX/HTML + CSS) to understand structure, styles, and content
2. **Map CSS variables** to pixel values at each breakpoint (resolve `var(--x)` to actual values)
3. **Map local breakpoints** to Webflow breakpoints (see breakpoint mapping reference)
4. **Build the element tree** in Webflow using `element_builder`
5. **Apply styles** using `style_tool` with resolved pixel values at each Webflow breakpoint
6. **Set text content** using `element_tool` → `set_text`
7. **Handle SVGs/custom code** via Code Embed (see [references/code-embeds-and-svgs.md](references/code-embeds-and-svgs.md))
8. **QA** — screenshot and compare with local dev site

For the full detailed guide, see [references/local-to-webflow.md](references/local-to-webflow.md).

## Workflow: Building from Scratch (Figma or No Design)

1. **Establish design tokens** — Create Webflow variables for colors, fonts, spacing via `variable_tool`
2. **Build page structure** — Create sections, containers, grids via `element_builder`
3. **Style top-down** — Start with `main` breakpoint, then override for `medium`, `small`, `tiny`
4. **Componentize repeating patterns** — Use `de_component_tool` → `transform_element_to_component`
5. **Add interactions/animations** — Use Code Embeds for CSS animations, or Webflow's native interactions
6. **Responsive QA** — Check each breakpoint, screenshot at 1440px, 992px, 768px, 480px, 375px

## Workflow: Creating Reusable Components

1. Build and style the element as a regular element first
2. Select the root element via `element_tool`
3. Use `de_component_tool` → `transform_element_to_component` with a name
4. Insert instances on other pages via `element_builder` with `component: "<component-id>"`
5. Override text content on instances via `element_tool` → `set_text`

## Using Design Variables

Prefer Webflow variables over hardcoded values for consistency:

```
variable_tool → set_variable:
  collection_id: "<collection-id>"
  variable_id: "<variable-id>"
  value: "#FF4733"
```

Reference variables in styles:
```
style_tool → set_styles:
  properties:
    color: "var(--variable-id)"
```

Discover existing variables with `variable_tool` → `get_variables`.

## Reference Files

- **[references/breakpoints-and-styles.md](references/breakpoints-and-styles.md)** — Breakpoint mapping table, typography scale patterns, style_tool examples
- **[references/local-to-webflow.md](references/local-to-webflow.md)** — Detailed guide for transferring local web projects to Webflow
- **[references/code-embeds-and-svgs.md](references/code-embeds-and-svgs.md)** — Code Embed insertion, SVG conversion (JSX→HTML), CodeMirror injection, custom CSS patterns
- **[references/gotchas.md](references/gotchas.md)** — Complete list of known issues, error messages, and workarounds