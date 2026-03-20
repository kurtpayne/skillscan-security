---
name: macos-gui-skill
description: Use when tasks require operating desktop applications on macOS and need screenshot-guided GUI actions.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: baibairui/macos-gui-skill
# corpus-url: https://github.com/baibairui/macos-gui-skill/blob/418ca7d1bf66f336a6c9bcbde4b23768cdb68c2f/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# macOS GUI Skill

When the user asks for desktop application operations, run the bundled script in this skill for local macOS execution.
Use the script path relative to this skill directory so any agent client that loads the skill can call it directly.

Workflow:
1. Start with `node ./scripts/macos-gui-skill.mjs observe` to collect visual evidence.
2. Build one `act` bundle with `2-5` small GUI actions only when the next steps are obvious from the screenshot.
3. Run `observe` again immediately after the bundle to confirm the result.
4. Use the loop `observe -> act -> observe` until the task is complete.
5. Do not start with `run-shell` or `run-applescript`; keep them only as escape hatches after repeated visual ambiguity or explicit user instruction.

Runtime:
- local macOS execution from the current workspace
- the host terminal needs Accessibility and Screen Recording permission
- AppleScript-based app activation may also prompt Automation permission
- screenshots are stored under `./.codex/artifacts/desktop/`

Examples:
- `node ./scripts/macos-gui-skill.mjs observe --label inbox --show-cursor true`
- `node ./scripts/macos-gui-skill.mjs observe --active-window true`
- `node ./scripts/macos-gui-skill.mjs observe --region 10,20,300,400`
- `node ./scripts/macos-gui-skill.mjs act --steps '[{"type":"activate-app","appName":"Finder"},{"type":"hotkey","keys":["Meta","n"]}]'`
- `node ./scripts/macos-gui-skill.mjs click --x 640 --y 420 --button left`
- `node ./scripts/macos-gui-skill.mjs screenshot --filename desktop-step.png --show-cursor true`
- `node ./scripts/macos-gui-skill.mjs doctor`
- `node ./scripts/macos-gui-skill.mjs list-windows`
- `node ./scripts/macos-gui-skill.mjs window-bounds --app-name Finder`
- `node ./scripts/macos-gui-skill.mjs locate-image --image ./button-template.png --active-window true`
- `node ./scripts/macos-gui-skill.mjs locate-image-center --image ./button-template.png --source-image ./capture.png`
- `node ./scripts/macos-gui-skill.mjs run-applescript --script 'tell application "Finder" to activate'`
- `node ./scripts/macos-gui-skill.mjs run-shell --command 'open -a "System Settings"'`

Rules:
- Operate the frontmost visible application only.
- Treat every `observe` result as visual evidence. Do not guess the UI state from stale memory.
- Prefer `observe --active-window true` or `observe --region ...` when full-screen captures include irrelevant context.
- Use `list-windows` or `window-bounds` to learn the current window layout before narrowing the capture area.
- Run `doctor` before deciding that `act` is unavailable or before switching to shell or AppleScript fallbacks.
- Do not claim the skill "lacks dependencies" unless `doctor` explicitly reports `actReady: false` and identifies the blocker.
- Do not switch to system-level UI scripts just to probe the environment. Use `doctor` as the single source of truth for dependency and permission readiness.
- Use `locate-image` or `locate-image-center` when the next action depends on finding a stable visual template in a PNG screenshot.
- Use `act` for the default path. Each bundle should stay inside one obvious focus chain and contain only GUI actions.
- If the host window steals focus between invocations, `observe` and `act` restore the remembered target app before continuing.
- Do not start with `run-shell` or `run-applescript`. If shell or AppleScript is required, use them only after repeated visual ambiguity or explicit user instruction.
- If a search box or command palette keeps focus, dismiss it with `press-key --key Esc`, verify it closed, and only then type into the main surface.
- If the next action is ambiguous, stop and ask for user direction.
- Before send/delete/submit/payment or other irreversible actions, request confirmation if the user did not state it explicitly.
- If an action fails twice, stop and report the current frontmost app and latest screenshot path.

Observation return fields:
- `path` and `local_image_path` for the captured image
- `frontmostApp`
- `screenSize`
- `captureRegion`
- `coordinateSpace`
- `permissions`

Doctor return fields:
- `actReady`
- `blockers`
- `fallbackPolicy`
- `permissions`
- `dependencies`

Template matching notes:
- `locate-image` returns `found`, `confidence`, `boundingBox`, and `center`.
- `locate-image-center` returns `found`, `confidence`, and `center`.
- Both commands accept `--source-image` for an existing PNG or will take a fresh screenshot if omitted.
- Both commands perform PNG template matching only. They do not read text from the UI.