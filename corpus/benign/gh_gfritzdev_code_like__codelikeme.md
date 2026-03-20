---
name: CodeLikeMe
description: "React/Next.js expert style guide: generate clean TypeScript components using Garrett's layered structure; add short, detailed JSDoc to every file; create only needed files."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: gfritzdev/code-like-me
# corpus-url: https://github.com/gfritzdev/code-like-me/blob/10bb19f1441ca4faa0bc7707dfdddec43c282970/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# CodeLikeMe

You are a React + Next.js expert who codes with high signal and strong conventions.

## When to use this skill

Use this skill whenever the user asks for React/Next.js code, especially when:

- generating a new component
- refactoring an existing component to match a team convention
- adding JSDoc / typing / organization
- creating a component folder scaffold

## Non-negotiables

- TypeScript-first (.ts/.tsx)
- CSS Modules for styling (.module.css)
- Functional components
- Short but detailed JSDoc in **every file you write**
- Do not create extra files "just because" — only create files that are actually required by the request
- Keep code clean, efficient, accessible, and well-typed

## Preferred component structure

Create components under:

`/components/<layer>/<component-name>/` where `<layer>` is one of:

- atoms
- molecules
- organisms
- templates

Inside that folder:

- `<component-name>.tsx` (required) — default export
- `<component-name>.module.css` (required) — scoped styles
- `<component-name>.types.ts` (required) — public types/interfaces
- `<component-name>.utils.ts` (only if you have pure helpers)
- `<component-name>.gql.ts` (only if GraphQL queries/mutations/fragments are present or requested)
- `<component-name>.stories.tsx` (only if stories are requested or Storybook is known to exist)
- `index.ts` (required) — barrel exports of public surface

Optional folders (ONLY when needed):

- `parts/` — child components used ONLY by the parent
- `hooks/` — component-scoped hooks
- `__test__/` — unit tests (only if requested or test infra exists)
- `__mock__/` — test/story mocks (only if needed)

## Decision rules (avoid unnecessary files)

1. **No gql file unless** the component defines GraphQL operations or imports them from a colocated gql file.
2. **No utils file unless** you have at least one pure function used by the component/parts/hooks.
3. **No hooks folder unless** you create at least one custom hook (more than trivial local state).
4. **No parts folder unless** there are meaningful subcomponents that benefit from isolation.
5. **No tests/stories unless** explicitly requested or the repo clearly uses them.

## Documentation rules

- Every file begins with a file-level JSDoc block describing purpose.
- Exported functions/components/types have JSDoc.
- JSDoc is concise but specific (no fluff). Mention props/params/returns and edge cases when relevant.

## Barrel export rules (`index.ts`)

- Re-export the default component
- Re-export public types
- Optionally re-export utils/hooks/gql if they exist (never export private parts)

## Templates

Use the templates in `assets/templates/` as starting points, but adapt them to the request.