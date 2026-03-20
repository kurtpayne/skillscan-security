---
name: heroku-cli-investigator
description: Step-by-step guidance for using the Heroku CLI (~>10.17.0) to inspect dynos, logs, releases, builds, CI runs, and Postgres health during operational incidents without creating or modifying resources. Trigger the skill when investigating failed deploys, stuck dynos, long-running queries, or anomalous build/CI results on a particular Heroku app.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: dgmdan/heroku-cli-investigator-skill
# corpus-url: https://github.com/dgmdan/heroku-cli-investigator-skill/blob/1bd63513715393b6483f3ff69fd38c78d4be07a8/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Heroku CLI Investigator

## Overview
Use the Heroku CLI as a forensic console that reports what is currently happening inside an app. Favor commands that only read state—release history, dyno status, realtime logs, builds, CI pipelines, and Postgres diagnostics—and treat this skill as the checklist you run before asking for write access. Look up exact syntax in `references/heroku-cli-commands.md` when you need the flags.

## Preparation & guardrails
- Verify the CLI version (`heroku --version`) and keep `~> 10.17.0` on your path so the documented flags remain valid. Authenticate once with `heroku login`, confirm the identity with `heroku whoami`, and export the target app via `HEROKU_APP` or add `--app <name>` to every command.
- Install the builds helper if it is not present: `heroku plugins:install @heroku-cli/heroku-builds`. Check `heroku plugins` to confirm it appears.
- Avoid running commands that create resources (`heroku apps:create`, `heroku addons:create`, `heroku pg:reset`, etc.) or alter infrastructure; ask for explicit permission before doing anything that writes. Immediately abort if a command prompts to change a pipeline, rotate credentials, or delete data.

## Runtime & dyno inspection
- List the live dynos and their states with `heroku ps --app <app>`. Use `heroku logs --app <app>` to stream output and filter by process (`--ps`, `--source`) when investigating a specific worker or web dyno. The same log stream shows real-time output from `heroku run:detached` jobs once you know their dyno name.
- Run short investigative commands inside a one-off dyno with `heroku run "<command>" --app <app>` when you need to inspect the filesystem, check environment variables, or run custom scripts. For longer tasks (database introspection, multi-step troubleshooting), use `heroku run:detached "<command>" --app <app>` so the output is recorded in the logs and you can view it later without keeping a shell open.
- When executing `heroku run`/`run:detached`, pass `--size` or `--type` if you need a specific dyno flavor and add `--exit-code` if you only care about success/failure. Always include `--app` to avoid running commands on the wrong app.

## Database investigation
- Use `heroku pg:info --app <app>` to verify which Postgres attachment powers the app, then run `heroku pg:psql --app <app> -c "<SQL>"` for read-only diagnostics. Keep queries short and only inspect information schema tables or low-load aggregates to avoid locking the database.
- Check `heroku pg:ps --app <app>` to surface connected clients and blocked sessions before adding load. For live long-running queries, run `heroku pg:diagnose --app <app>`—it summarizes recent slow SQL, waits, and disk usage unless the database is on Shield (the command is not supported there).
- Tail Postgres-specific logs via `heroku logs --postgres --app <app>` (or `--proc-type=postgres`) to catch errors or connection spikes. If a session is holding a lock, capture the stack trace quickly and plan a follow-up before killing the connection.

## Releases, builds, and CI checks
- Inspect the last few releases with `heroku releases --num 10 --app <app>` and dive into release-phase failures with `heroku releases:info <version> --app <app>` or `heroku releases:output <version> --app <app>` so you can see the exact deploy script that failed.
- Use the builds helper to review build history: `heroku builds --app <app>` lists each build, `heroku builds:info <build-id> --app <app>` shows the status, and `heroku builds:output <build-id> --app <app>` streams the build logs. Leave the commands that create/cancel builds alone unless you have approval—this skill only reads state.
- Query CI from the CLI: `heroku ci --app <app>` lists recent batches, `heroku ci:last --app <app>` summarizes the latest run, and `heroku ci:info <batch-number> --app <app>` or `heroku ci:debug <batch-number> --app <app>` surfaces failing tests (debug spawns an interactive rerun inside a dyno). When a test suite fails, `heroku ci:rerun` or `heroku ci:run` can be helpful but only execute them with explicit permission because they spin up new dynos.

## Safety for non-destructive investigations
- Always double-check the `--app` flag or `HEROKU_APP` environment variable before running anything with write implications (including `heroku run` if you plan to mutate data). Do not run any Papertrail commands—they no longer work, and the logs you need are already available via `heroku logs`.
- Never pipe a command directly into `heroku pg:psql` that drops or writes data. If a developer asks you to run something destructive, log it and request approval from the owner of the app.
- When you need to capture output for later, redirect CLI output to a file on your machine instead of rerunning high-impact operations. Document what you ran, why, and any follow-up steps inside the incident tracker.

## References & command cheatsheet
Keep `references/heroku-cli-commands.md` open for quick syntax, flag reminders, and the current list of investigative commands. Update that reference whenever Heroku adds new read-only flags or plugins that help you understand builds, CI, dynos, or Postgres state.