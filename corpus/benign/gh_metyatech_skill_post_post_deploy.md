---
name: post-deploy
description: Use when verifying deployment after code changes to globally linked packages (npm link), running services, daemons, or scheduled tasks. Triggers when code changes affect a globally installed CLI or a running service. Do not use for general development, CI setup, or initial deployments.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: metyatech/skill-post-deploy
# corpus-url: https://github.com/metyatech/skill-post-deploy/blob/4cb52e7a80c8b525692e3cb001dad580813ea2e8/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Post-change deployment procedures

## Detection

### Globally linked packages

- Check npm global links: run `npm ls -g --depth=0` and look for entries with `->` pointing to a local path.
- If the changed repo matches a globally linked package, proceed to rebuild.

### Running services and scheduled tasks

- Check for running processes associated with the repo (service names, PM2/systemd/Windows service entries).
- Check for scheduled tasks (cron, Windows Task Scheduler) referencing the repo.

## Rebuild and verify

### npm-linked packages

1. Run the repo's build command (e.g., `npm run build`, `tsc`).
2. Verify the rebuilt output: run the CLI's `--version` or a smoke command.
3. Report the verified version.

### Services and daemons

1. Rebuild the service component.
2. Restart using the service manager (PM2 restart, systemctl restart, etc.).
3. Verify with deterministic evidence:
   - New PID (compare before/after).
   - Port check (verify listening).
   - Service status query.
   - Log entry showing updated behavior/version.
4. Report the verification evidence.

## Completion gate

Do not claim completion until the running instance reflects the changes. Include verification evidence in the final response.