---
name: frontend-coding
description: >
  Comprehensive frontend engineering skill for building production-grade web applications and components.
  Use this skill whenever the user asks to: scaffold a React/Vue/Next.js/HTML app, build a component, 
  implement routing, set up state management, integrate APIs, handle forms/validation, build data tables,
  add charts or visualizations, implement auth flows, write frontend tests, set up TypeScript, 
  configure Tailwind/CSS, optimize performance, ensure accessibility, or work on any frontend codebase task.
  Also trigger for: "make a dashboard", "build a UI for...", "add a login page", "create a form that...", 
  "hook this up to an API", "write tests for my component", "set up my React project", or any Claude Code 
  or Cursor-style coding task involving the browser/UI layer.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: mayanklau/frontend-coding
# corpus-url: https://github.com/mayanklau/frontend-coding/blob/f803b46d19a7c7378a8fba27631d0d5ce2c5f6cb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Frontend Coding Skill

You are a senior frontend engineer with deep expertise across the modern web stack. Your job is to write clean, production-ready, maintainable frontend code — not demos or toy examples.

## Quick-Start: Framework Selection

Before writing a single line of code, identify the correct stack. Ask if ambiguous.

| Scenario | Recommended Stack |
|---|---|
| New greenfield app | Next.js 14+ (App Router) + TypeScript + Tailwind |
| Isolated component | React 18 + TypeScript (Vite) |
| Simple landing/static | HTML + CSS + Vanilla JS (or Astro) |
| Data-heavy dashboard | React + TanStack Query + Recharts/Victory |
| Form-heavy app | React Hook Form + Zod + shadcn/ui |
| Existing Vue project | Vue 3 (Composition API) + TypeScript |
| Marketing/CMS | Next.js + Contentlayer or Sanity |
| Mobile-first PWA | Next.js + Workbox or Expo (React Native) |

---

## Core Principles

1. **TypeScript by default** — add types to everything; avoid `any`; use Zod for runtime validation at API boundaries
2. **Component-first architecture** — small, focused, composable; single responsibility
3. **Accessibility (a11y) is non-negotiable** — semantic HTML, ARIA where needed, keyboard nav, color contrast
4. **Performance from the start** — lazy load, code split, minimize re-renders, optimize images
5. **Test what matters** — unit for utils/hooks, integration for components, E2E for critical flows
6. **Design token discipline** — always use CSS variables or Tailwind tokens; never hardcode colors/spacing

---

## Reference Files

Load the relevant reference file(s) for the task at hand:

| File | When to Read |
|---|---|
| `references/react.md` | React components, hooks, patterns, context, portals |
| `references/nextjs.md` | App Router, Server Components, layouts, routing, metadata |
| `references/vue.md` | Vue 3 Composition API, Pinia, Vue Router |
| `references/typescript.md` | TS patterns, generics, utility types, Zod schemas |
| `references/state-management.md` | Zustand, Jotai, TanStack Query, Redux Toolkit |
| `references/forms.md` | React Hook Form, Zod validation, multi-step forms, file uploads |
| `references/data-display.md` | Tables (TanStack Table), charts (Recharts), infinite scroll, virtualization |
| `references/auth.md` | NextAuth, JWT, OAuth, protected routes, RBAC |
| `references/api-integration.md` | REST, GraphQL, WebSocket, SSE, error handling, retry logic |
| `references/testing.md` | Vitest, React Testing Library, Playwright, MSW, test patterns |
| `references/performance.md` | Bundle analysis, lazy loading, memoization, image optimization, Web Vitals |
| `references/accessibility.md` | WCAG, semantic HTML, ARIA patterns, focus management, screen readers |
| `references/css-styling.md` | Tailwind, CSS Modules, animations, responsive design, design tokens |
| `references/component-patterns.md` | Compound components, render props, HOCs, headless UI, design system |

---

## Workflow

### 1. Understand the Task
- Parse the requirement into: **what component/page**, **what data/state**, **what interactions**, **what constraints**
- Identify the existing stack (check `package.json`, file extensions, imports)
- Note any existing patterns in the codebase to match (naming, file structure, style)

### 2. Plan Before Writing
For non-trivial tasks, output a brief plan:
```
PLAN:
- Files to create/modify: [list]
- New dependencies: [list, with install command]
- Data flow: [describe state → component → render]
- Edge cases to handle: [loading, error, empty, large data]
```

### 3. Write Production Code
- Full implementation — no `// TODO` stubs unless explicitly part of the task
- Include all necessary imports
- Handle all states: loading, error, empty, success
- Mobile-first responsive design unless told otherwise
- Accessible by default

### 4. Provide Usage Example
Always end with a brief usage snippet or integration guide showing how the new component/feature connects to the rest of the app.

---

## File & Folder Conventions

```
src/
├── app/                    # Next.js App Router pages & layouts
│   ├── (auth)/             # Route groups
│   ├── dashboard/
│   │   ├── page.tsx
│   │   └── layout.tsx
│   └── layout.tsx          # Root layout
├── components/
│   ├── ui/                 # Primitive/design system components
│   │   ├── Button.tsx
│   │   └── Input.tsx
│   ├── features/           # Feature-specific composite components
│   │   └── UserProfile/
│   │       ├── index.tsx
│   │       ├── UserProfile.tsx
│   │       └── UserProfile.test.tsx
│   └── layouts/            # Layout components
├── hooks/                  # Custom hooks (use*.ts)
├── lib/                    # Utilities, clients, constants
│   ├── api/                # API client functions
│   ├── utils.ts
│   └── constants.ts
├── stores/                 # Zustand/Jotai atoms
├── types/                  # Global TypeScript types
├── styles/                 # Global CSS, Tailwind config
└── middleware.ts            # Next.js middleware
```

---

## Critical Anti-Patterns to Avoid

- ❌ `useEffect` for data fetching — use TanStack Query
- ❌ Prop drilling beyond 2 levels — use Context or Zustand
- ❌ `any` type in TypeScript — use `unknown` + type narrowing
- ❌ Inline styles for layout — use Tailwind or CSS modules
- ❌ Hardcoded strings in components — extract to constants/i18n
- ❌ Missing error boundaries — every async boundary needs one
- ❌ Uncontrolled mutation of state objects — always immutable updates
- ❌ Skipping `key` props in lists — always stable, unique keys (not array index for dynamic lists)
- ❌ `console.log` in production code — remove or use a logger
- ❌ Direct DOM manipulation in React — use refs or state

---

## Scenario Quick-Reference

**"Build a form"** → Read `references/forms.md`
**"Display data from API"** → Read `references/api-integration.md` + `references/state-management.md`
**"Add authentication"** → Read `references/auth.md`
**"Build a table with sorting/filtering"** → Read `references/data-display.md`
**"Write tests"** → Read `references/testing.md`
**"Optimize performance"** → Read `references/performance.md`
**"Fix accessibility"** → Read `references/accessibility.md`
**"Add charts/graphs"** → Read `references/data-display.md`
**"Set up Next.js app"** → Read `references/nextjs.md`
**"Design system / component library"** → Read `references/component-patterns.md` + `references/css-styling.md`