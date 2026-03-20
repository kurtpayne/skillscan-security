---
name: creating-npm-packages
description: 'Scaffold new TypeScript npm packages with ESM + CJS dual output, Biome linting, Bun testing, tsdown bundling, release-it publishing, and GitHub Actions CI. Use when asked to create, scaffold, or set up a new npm package.'
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: mrmartineau/npm-package
# corpus-url: https://github.com/mrmartineau/npm-package/blob/d5701389569cc92d665b89f39dd952485336493c/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Creating npm Packages

Scaffold production-ready TypeScript npm packages with a consistent stack:
**Bun** (runtime/test), **tsdown** (bundler), **Biome** (lint/format), **release-it** (publishing), **GitHub Actions** (CI).

## Workflow

1. Create the project directory and initialise git
2. Generate all config files using the templates below
3. Replace placeholder values (`PACKAGE_NAME`, `PACKAGE_DESCRIPTION`, `GITHUB_OWNER`, `GITHUB_REPO`) with user-provided values
4. Write initial source code in `src/index.ts` and a starter test in `src/index.test.ts`
5. Run `bun install`
6. Run `bun run build` to verify the setup works
7. Run `bun test` to verify tests pass

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── index.ts
│   └── index.test.ts
├── .gitignore
├── .release-it.json
├── biome.json
├── LICENSE
├── package.json
├── README.md
└── tsconfig.json
```

## File Templates

### package.json

"~/.config/agents/skills/creating-npm-packages/SKILL.md" 336L, 7852B