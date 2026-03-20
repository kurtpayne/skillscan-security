---
name: loopback4
description: Guides implementation and maintenance tasks for this Juzmatch LoopBack 4 API. Use when adding or changing controllers, authentication, boot and application configuration, datasources or repositories, OpenAPI behavior, and startup/runtime wiring.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: wadjakorn/agents-skills-loopback4
# corpus-url: https://github.com/wadjakorn/agents-skills-loopback4/blob/ce3b6ee1bed791982c552296f09dd6ecaba378c6/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# LoopBack4 Juzmatch API

## When To Use

Use this skill when the user asks for work involving:
- New or changed REST endpoints in `src/controllers`.
- API key or JWT auth behavior.
- Application boot, startup flow, or component/provider binding.
- Datasource/repository integration and data-access changes.
- LoopBack command usage, testing, linting, and local run verification.

## Repo Conventions To Follow

- Application class is `GettingStartedApplication` in `src/application.ts`.
- Controllers are boot-discovered from `controllers` with `.controller.js` extension and nested folders enabled.
- OpenAPI security scheme `apikey` is configured globally in `src/application.ts` and defaults to `x-api-key` header if `API_KEY_HEADER_NAME` is unset.
- Startup flow is in `src/index.ts`: `main()` creates app, calls `boot()`, then `start()`, then starts SQS consumer wiring.
- `src/index.ts` currently overwrites `options.rest`; preserve this behavior unless user explicitly asks to refactor it.
- Existing auth stack mounts `AuthenticationComponent`, `JWTAuthenticationComponent`, and custom `ApiKeyAuthenticationStrategy`.

## Common Tasks

### Add Or Update A Controller Endpoint

1. Follow existing controller style in `src/controllers`.
2. Use LoopBack decorators from `@loopback/rest` (`@get`, `@post`, `@param`, `@requestBody`) as needed.
3. Keep business logic in services/repositories where practical; keep controller methods thin.
4. If endpoint must be protected, apply `@authenticate('apikey')` or the strategy requested by the user.
5. Validate with:
   - `npm run build`
   - `npm run lint`
   - targeted test command when applicable (`npm test`, `npm run test:jest`, or a narrower suite).

### Change Authentication Behavior

1. Confirm which strategy is expected (`apikey`, JWT, or both).
2. For API key changes:
   - Keep strategy registration in `src/application.ts`.
   - Ensure OpenAPI `securitySchemes.apikey` matches runtime header name.
3. For JWT changes:
   - Keep component/binding flow consistent with current app setup.
4. Verify with protected endpoint smoke checks (for example `/health` if public and one protected route).

### Modify App Boot Or Configuration

1. Keep `BootMixin(ServiceMixin(RepositoryMixin(RestApplication)))` composition intact unless user requests architectural change.
2. Preserve `projectRoot` and `bootOptions.controllers` conventions.
3. If adding new providers/services, bind via application context (`this.bind(...).toProvider(...)`, `this.service(...)`) consistent with existing code.
4. If changing request/body limits or rest options, confirm impact on current startup behavior in `src/index.ts`.

## Fast Verification Commands

- Build: `npm run build`
- Lint: `npm run lint`
- Mocha pipeline: `npm test`
- Jest: `npm run test:jest`
- Dev run: `npm run start:watch`

## Guardrails

- Do not introduce new folder conventions for LoopBack artifacts unless asked.
- Avoid broad refactors while doing endpoint/auth fixes.
- Keep naming and decorators aligned with LoopBack 4 patterns already present in this repo.
- Prefer minimal, behavior-preserving changes.

## Additional Resources

- See curated references in [reference.md](reference.md).