---
name: shadcn-app-shell
description: Build an authenticated Laravel + Inertia + Vue app shell with starter default pages, wrapper-based AppLayout pages, plain shadcn-vue table defaults for lists, and standardized form/feedback behavior.
metadata:
  tags:
    - laravel
    - inertia
    - vue
    - shadcn-vue
    - app-shell
    - dashboard
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: jamesulip/shadcn-app-shell
# corpus-url: https://github.com/jamesulip/shadcn-app-shell/blob/b5d0f6b503199a8f903356dba1b560027ace0c2f/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Shadcn App Shell

## Overview

Use this skill to build ERP-style internal dashboards where pages render inside a persistent shell and operators prioritize speed, clarity, and repeatability.
Prefer Vue 3 Composition API with `<script setup>` and TypeScript unless the project explicitly requires a different style.

## When To Use

- Scaffold a new internal Laravel + Inertia + Vue operations console.
- Refactor an existing back-office UI to use a persistent `AppLayout`.
- Standardize list tables, CRUD forms, keyboard UX, and feedback states across modules.

## Quick Start

1. Apply [shadcn-vue-prerequisites.md](shadcn-vue-prerequisites.md) before generating shell components.
2. Apply [Laravel Inertia Vue skill](../laravel-inertia-vue/SKILL.md) for Inertia routing, props, and form conventions.
3. Read [blank-app-default-pages.md](blank-app-default-pages.md) to scaffold default pages in a blank Laravel app.
4. Read [app-shell-architect.md](app-shell-architect.md) before generating any page layout.
5. Read [workspace-navigation.md](workspace-navigation.md) when defining routes, breadcrumbs, preserved state, and keyboard shortcuts.
6. Read [app-data-table-standard.md](app-data-table-standard.md) for any list or index screen.
7. Read [inertia-crud-form-standard.md](inertia-crud-form-standard.md) for create/edit forms.
8. Read [system-feedback-standard.md](system-feedback-standard.md) for toasts, loading states, and empty states.
9. Read [production-workflow-awareness.md](production-workflow-awareness.md) for printing and work-unit lifecycle interfaces.
10. Apply [final-behavior-rule.md](final-behavior-rule.md) to all generated UI.

## Non-Negotiables

- Keep `AppLayout` mounted across Inertia visits.
- Keep navigation and workspace context persistent.
- Standardize behavior across modules instead of creating one-off patterns.
- If `shadcn-vue` is not initialized, initialize it before generating components.
- Apply `laravel-inertia-vue` conventions for page contracts, navigation state, and forms.
- Optimize for operator throughput, not marketing presentation.

## Skill-Creator Defaults

- For blank app scaffolds, start from [blank-app-default-pages.md](blank-app-default-pages.md).
- For list pages, default to plain shadcn-vue table primitives (`components/ui/table`), not `DataTable.vue`.
- Use wrapper-based page structure with `Head` and `AppLayout :breadcrumbs`.
- Treat advanced shell/table behavior as explicit upgrades, not baseline output.