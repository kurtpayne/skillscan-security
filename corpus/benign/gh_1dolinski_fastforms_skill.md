---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: 1dolinski/fastforms
# corpus-url: https://github.com/1dolinski/fastforms/blob/bd5a5a88e3e6faf52b482eec866faacfb428eefb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# fastforms

Fill any form fast using your personas.

## Triggers

Use this skill when the user says any of:
- "fill a form", "fill out this form", "fill out this application"
- "apply to X", "submit my info to X"
- "autofill form", "autofill with my persona"
- "fill this form with my persona"
- "use fastforms", "fastforms fill"
- "set up my personas", "init fastforms"
- "add a persona", "add a form persona"
- "import from twitter", "pull my twitter profile"

## What it does

`fastforms` is a CLI tool that:

1. Manages three types of personas locally in `.fastforms/`:
   - **User** — who you are (name, email, bio, skills)
   - **Business** — what you're building (company, product, traction)
   - **Form** — who's asking and why (org, purpose, form-specific answers)
2. Can import user personas from Twitter via x402 micropayment
3. Connects to Chrome via the DevTools Protocol
4. Lets you pick which user + business + form persona to use at fill time
5. Fills any form using label-matching — never submits

## Quick start

```bash
# 1. Create your first personas
npx @1dolinski/fastforms init

# Or import from Twitter ($0.01 USDC on Base)
export PRIVATE_KEY=0x...
npx @1dolinski/fastforms import twitter <your-handle>

# 2. Add form-specific context
npx @1dolinski/fastforms add form

# 3. Enable remote debugging in Chrome
#    Open chrome://inspect/#remote-debugging

# 4. Fill any form — pick from your personas
npx @1dolinski/fastforms fill https://example.com/apply
```

## Commands

### `npx @1dolinski/fastforms init`

Walks through creating a user + business persona (optionally a form persona too).

### `npx @1dolinski/fastforms import twitter <username>`

Imports a user persona from Twitter via x402 micropayment ($0.01 USDC on Base). Requires `PRIVATE_KEY` env var set to a Base wallet private key.

### `npx @1dolinski/fastforms add user|business|form`

Add another persona of any type.

### `npx @1dolinski/fastforms list`

Show all saved personas across all types.

### `npx @1dolinski/fastforms fill <url>`

Fills any form. If you have multiple personas, prompts you to pick. Form personas auto-match by URL.

Options:
- `--user <hint>` — pre-select a user persona by name
- `--business <hint>` — pre-select a business persona by name
- `--form <hint>` — pre-select a form persona by name
- `--web` — use web app personas (https://293-fastforms.vercel.app) instead of local files
- `--dir <path>` — custom path to persona directory
- `--port <port>` — Chrome debug port (auto-detected by default)

### `npx @1dolinski/fastforms edit`

Pick any persona to edit interactively.

### `npx @1dolinski/fastforms remove`

Pick any persona to delete.

## Persona types

### User persona
Who you are. Name, email, role, GitHub, LinkedIn, bio, custom facts.

### Business persona
What you're building. Company, product, one-liner, traction, business model.

### Form persona
Who's asking and why. The organization that owns the form, the form's purpose, and **form-specific answers** that override user/business data.

Form personas auto-match by URL. If your form persona has `urls: ["apply.ycombinator.com"]` and you fill that URL, it auto-selects.

## How it works

1. Reads all personas from `.fastforms/users/`, `.fastforms/businesses/`, and `.fastforms/forms/`
2. If multiple, prompts you to pick which user + business persona to use
3. Auto-matches form persona by URL (or prompts if multiple)
4. Auto-discovers Chrome's debug port from `DevToolsActivePort`
5. Opens (or reuses) the target form URL tab
6. Fills using label-matching. Form persona facts are checked first as overrides.
7. Shows what was filled, what was skipped. **Never submits.**

## Agent instructions

When the user asks you to fill a form:

1. Check if `.fastforms/` exists. If not, run `npx @1dolinski/fastforms init`
2. If the form is new, suggest `npx @1dolinski/fastforms add form` to capture form-specific context
3. Run `npx @1dolinski/fastforms fill <the-url>`
4. If Chrome debugging isn't enabled, tell the user to open `chrome://inspect/#remote-debugging`
5. After filling, tell the user to review in Chrome and submit manually

When the user wants to import from Twitter:

1. They need `PRIVATE_KEY` set (Base wallet with USDC)
2. Run `npx @1dolinski/fastforms import twitter <handle>`
3. The persona will be saved to `.fastforms/users/<handle>.json`

When the user wants to add a persona:

1. Run `npx @1dolinski/fastforms add user|business|form`

When the user wants to see their personas:

1. Run `npx @1dolinski/fastforms list`