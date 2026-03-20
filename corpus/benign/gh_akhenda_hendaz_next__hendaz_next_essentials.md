---
name: hendaz-next-essentials
description: "Scaffold a newly created Next.js project with Hendaz defaults: commitizen + commitlint + cz-git, .commitsage, markdownlint config, bunfig.toml, Biome + Ultracite (and ESLint removal), lefthook + lint-staged (and Husky removal), VS Code workspace files, shared src/types utilities, and a production-ready logger. Use when a user asks to bootstrap, standardize, or initialize a Next.js project with these recurring essentials."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: akhenda/hendaz-next-essentials
# corpus-url: https://github.com/akhenda/hendaz-next-essentials/blob/b5b44b95ddac9cad348d5ef98f6fa29cef00d356/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Hendaz Next Essentials

## Workflow

1. Confirm target directory is a Next.js project root and normalize it to `src/` layout if it is still using root-level source directories.
2. Ask the user whether Convex should be set up too. If yes, run the setup with `--with-convex`.
3. Run `scripts/apply-templates.sh [--no-overwrite] [--backup] [--with-convex] <project-path>` from this skill.
4. Verify created files, removed files, and any moved source directories now live under `src/`.
5. Verify `package.json` scripts and `config.commitizen.path` are updated to the Hendaz defaults, including Vitest + Playwright test commands.
6. Verify root `AGENTS.md`/`CLAUDE.md` include enforced strict rules block.
7. Verify the API foundation under `src/modules/core/api` was added, including Axios config, React Query setup, resource folders, and the top-level `APIProvider`.
8. If Convex was enabled, verify `convex/` examples, `src/modules/core/api/convex/`, Convex-backed resource hooks under `src/modules/core/api/resources/`, and the unified Vitest configuration were added.
9. Run quality checks (`bun run lint`, `bun run typecheck`) when available.

## Agent Instruction Enforcement

This skill must update project instruction files with strict rules.

- It checks only root-level instruction files:
  - `<project-root>/AGENTS.md`
  - `<project-root>/CLAUDE.md`
- It upserts a managed block into each file with these rules:
  - prohibit `any`
  - allow `AnyType` or `AnyValue` only sparingly, and only when imported from `src/types/common`
  - stop and ask if typing intent is unclear
  - prohibit `console.*`
  - require custom logger usage
- If neither file exists, it creates `<project-root>/AGENTS.md` with the managed block.

Managed by script:

```bash
/Users/hendaz/.codex/skills/hendaz-next-essentials/scripts/enforce-agent-instructions.sh /path/to/project
```

## Apply Script

Use the script for deterministic setup:

```bash
/Users/hendaz/.codex/skills/hendaz-next-essentials/scripts/apply-templates.sh [--no-overwrite] [--backup] [--with-convex] /path/to/project
```

Options:

- `--no-overwrite`: skip files that already exist.
- `--backup`: create timestamped backups before overwriting existing files.
- `--with-convex`: add optional Convex backend examples, Convex API foundation files, and Convex-backed resource hooks.

The script will:

1. Ensure the project uses `src/` layout. If root-level Next.js source directories/files such as `app`, `pages`, `components`, `lib`, `utils`, `hooks`, `styles`, `types`, `middleware.ts`, or `instrumentation.ts` exist and `src/` does not, the script moves them into `src/` first.
2. Copy templates from `assets/templates` into the target project, including the standard `.gitignore`.
3. Upsert `package.json` to enforce the Hendaz script set and `config.commitizen.path = "cz-git"`.
4. Enforce strict rules in root `AGENTS.md`/`CLAUDE.md`.
5. Remove ESLint config files if present.
6. Remove `.husky/` if present.
7. Install all required packages with Bun.
8. Run `bun install` to refresh lockfile state.
9. Run `bunx playwright install` so e2e browsers are available.
10. Add the API foundation under `src/modules/core/api`, including Axios config, React Query config/provider, resource examples, and `APIProvider`.
11. If `--with-convex` is enabled, add Convex example files under `convex/`, extend `src/modules/core/api` with Convex support plus Convex-backed resources, and install the Convex testing/runtime packages.

## Templates Included

- Root configs: `.commitsage`, `.commitlintrc.mjs`, `.gitignore`, `lefthook.yml`, `.markdownlint.json`, `.lintstagedrc.cjs`, `bunfig.toml`, `biome.jsonc`
- Test configs: `playwright.config.ts`, `vitest.config.ts`
- Editor configs: `.vscode/extensions.json`, `.vscode/settings.json`, `.vscode/tailwind.json`
- Test scaffold: `tests/e2e/home.spec.ts`
- Types: `src/types/common.ts`, `src/types/components.ts`, `src/types/domain.ts`, `src/types/helpers.ts`, `src/types/navigation.ts`, `src/types/index.ts`
- Logger: `src/utils/logger/index.ts`, `src/utils/logger/types.ts`
- API foundation:
  - `src/modules/core/api/config/*`
  - `src/modules/core/api/react-query/*`
  - `src/modules/core/api/resources/countries/*`
  - `src/modules/core/api/provider.tsx`
  - `src/modules/core/api/index.ts`

If Convex is enabled, also include:

- Convex backend: `convex/test.setup.ts`, `convex/schema.ts`, `convex/queries.ts`, `convex/mutations.ts`, `convex/actions.ts`
- Convex tests: `convex/schema.test.ts`, `convex/queries.test.ts`, `convex/mutations.test.ts`, `convex/actions.test.ts`
- Convex API layer: `src/modules/core/api/convex/index.ts`, `src/modules/core/api/convex/provider.tsx`
- Convex-backed resources:
  - `src/modules/core/api/resources/settings/*`
  - `src/modules/core/api/resources/users/*`
- Convex-aware API provider/index variants that overwrite the base API provider barrels

## Package.json Enforcement

This skill must verify and upsert these `package.json` scripts:

- `lint`: `biome check . --error-on-warnings`
- `format`: `biome check . --write`
- `typecheck`: `tsc --noEmit`
- `commit`: `git-cz`
- `commitlint`: `commitlint --edit`
- `prepare`: `lefthook install`
- `test`: `bun run test:unit && bun run test:e2e`
- `test:unit`: `vitest run --coverage`
- `test:unit:watch`: `vitest`
- `test:e2e`: `playwright test --grep-invert @visual`
- `test:e2e:headed`: `playwright test --headed`
- `test:e2e:debug`: `playwright test --debug`
- `test:e2e:update`: `playwright test --update-snapshots`
- `test:e2e:visual`: `playwright test --grep @visual`
- `validate`: `bun run format && bun run lint && bun run typecheck && bun run test`

This skill must also enforce:

- `config.commitizen.path = "cz-git"`
- Vitest coverage thresholds of `statements: 95`, `functions: 95`, `branches: 90`, and `lines: 95`
- The skill uses one root `vitest.config.ts` with Vitest projects for app and Convex tests, inlines `convex-test` for the Convex project, and enforces the same 95/95/90/95 coverage thresholds across included app and Convex source files
- The Convex API layer should expose the shared hook surface, including `useQueryWithCache`, `useQueriesWithCache`, `useQueryWithStatus`, and `useQueryWithStatusAndCache`, and resource examples should prefer the cached/status-based query hooks over plain `useQuery`

## Package Installation Rules

Use Bun only.

Dev dependencies installed by the script:

- `@testing-library/react`
- `@playwright/test`
- `@vitest/coverage-v8`
- `@biomejs/biome`
- `@commitlint/cli`
- `@commitlint/config-conventional`
- `commitizen`
- `cz-git`
- `jsdom`
- `lefthook`
- `lint-staged`
- `playwright`
- `vitest`
- `ultracite`

Runtime dependencies installed by the script:

- `@tanstack/react-query`
- `@logtail/next`
- `@sentry/nextjs`
- `axios`
- `consola`
- `sonner`

Additional dependencies installed only when Convex is enabled:

- Dev: `@edge-runtime/vm`, `convex-test`
- Runtime: `convex`, `convex-helpers`

## Notes

- The user corrected lockfile intent to `bunfig.toml`; do not add lockfile-specific templates.
- If template updates are requested, update files in `assets/templates/` first, then re-run the apply script.
- A provided template labeled as `src/types/common.ts` (barrel exports) is intentionally stored as `src/types/index.ts`.
- The `src/` normalization step runs before template copying so all generated Hendaz defaults land in a consistent Next.js source layout.
- Playwright browser installation is part of setup, so the script should leave the project ready to run `bun run test:e2e` without a separate manual install step.
- The skill should add or overwrite `.gitignore` with the managed Next.js/React/macOS/Vim/Node template unless `--no-overwrite` is used.
- The skill should always scaffold `src/modules/core/api` as the shared foundation for third-party APIs and app-wide data providers.
- The old `src/hooks/convex` example path is deprecated and should not be generated anymore.
- Convex setup is opt-in. The skill should explicitly ask the user before enabling it, then use `--with-convex` for deterministic setup if the user agrees.
- After Convex setup, the user will still need to run `bunx convex dev` or another Convex codegen flow in their app to generate `convex/_generated/*` and connect a deployment.