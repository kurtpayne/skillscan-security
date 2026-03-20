---
name: api-builder
description: Use when the user wants to build, scaffold, or create a backend API or REST endpoint. Launches an interactive wizard artifact inside the chat — collects project details through clickable option cards step by step — then sends the full config to Claude to generate the complete project directly in the conversation.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Omkar1634/Claude-API_Skills
# corpus-url: https://github.com/Omkar1634/Claude-API_Skills/blob/08a43aa5893babb8e42908f4bbdc050f665f5516/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# API Builder Skill

## Overview

API Builder scaffolds a backend API project through an interactive step-by-step wizard artifact that runs inside the Claude chat. It collects all project information via clickable option cards, shows a confirmation summary, then uses sendPrompt() to pass the full config to Claude — who generates the complete project inline in the conversation with real entity names and runnable code.

No new browser windows. No external API calls. Works identically in claude.ai browser, mobile app, and Claude Code terminal.

---

## Trigger Phrases

Activate when the user says any of the following (or close variations):

- "build an API"
- "create a backend"
- "scaffold my API"
- "help me build a REST API"
- "I want to create an API"
- "set up a backend project"

---

## Core Rules

1. **Launch the wizard artifact immediately** on trigger — do not ask questions conversationally.
2. **Never assume the framework** — framework options shown only after language is selected.
3. **No experience level question** — removed in v0.2.0.
4. **Back button always visible and clearly secondary** — ghost style, never competes with Continue.
5. **Continue button always bright and prominent** — purple with glow, impossible to miss.
6. **Generate button is the biggest element on the confirm screen** — green, full-width feel.
7. **Generation happens via sendPrompt()** — wizard sends the config to Claude in chat, Claude generates the project inline. No external API calls, no CORS issues, no new windows.
8. **Generated code uses real entity names** — never MyModel, YourEntity, or placeholders.
9. **Show folder structure first** — before any file content.
10. **Ask permission before reading existing code** — for Existing API flow only.

---

## Wizard Steps (10 steps)

### Step 1 — Project type
Single select: From scratch / Mid-project / Existing API

### Step 2 — Project description
Free text — what does it do, who is it for

### Step 3 — Entities
Free text — main resources (users, posts, orders) — become real names in generated code

### Step 4 — API consumers
Multi-select tags: Web frontend / Mobile app / Other services / Third-party clients

### Step 5 — Language
Single select: Python / JavaScript / TypeScript / C# / Java / Go / PHP / Ruby

### Step 6 — Framework
Single select — options change based on chosen language:

| Language | Options |
|---|---|
| Python | FastAPI (Recommended), Django REST, Flask |
| JavaScript | Express (Recommended), Fastify, NestJS |
| TypeScript | NestJS (Recommended), Fastify, Express |
| C# | ASP.NET Core Web API (Recommended), Minimal API |
| Java | Spring Boot (Recommended), Quarkus |
| Go | Gin (Recommended), Echo, Fiber |
| PHP | Laravel (Recommended), Slim |
| Ruby | Rails API (Recommended), Sinatra |

### Step 7 — Database
Single select: SQLite (Easiest) / PostgreSQL / MySQL / MongoDB

### Step 8 — Auth
Single select: JWT (Most common) / API Key / OAuth2 / Session / None

### Step 9 — Features
Multi-select — pre-selected based on context:
- OpenAPI / Swagger — always pre-selected
- CORS Config — always pre-selected
- Structured Logging — always pre-selected
- Rate Limiting
- Pagination
- Caching
- Unit Tests
- Docker

### Step 10 — Confirm + Generate
Full config recap shown. Generate button sends full spec to Claude via sendPrompt().

---

## Generation Prompt (sent via sendPrompt)

When user clicks Generate, the wizard sends this to Claude:

```
Generate a complete backend API project with these exact specifications:

Project: [desc]
Type: [type]
Entities: [entities]
API consumers: [consumers]
Language: [lang]
Framework: [fw]
Database: [db]
Auth: [auth]
Features: [features]

Please:
1. Show the full folder structure first
2. Then generate each file completely — no TODOs, no placeholders
3. Use real entity names from the entities list throughout
4. After all files, show how to run the project locally
```

---

## Claude's Response After sendPrompt

When Claude receives the generation prompt, it must:

1. Show the full folder structure as a tree
2. Generate every file completely with real entity names
3. Never use TODO comments or placeholder values
4. End with the exact commands to run the project locally

---

## Folder Structure to Generate (example — FastAPI + SQLite)

```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py              — FastAPI app entry, mounts routers, middleware
│   ├── config.py            — Settings via pydantic-settings, reads .env
│   ├── dependencies.py      — Shared DI: db session, current user
│   ├── api/
│   │   └── v1/
│   │       ├── router.py    — Aggregates all v1 sub-routers
│   │       └── endpoints/   — One file per entity
│   ├── core/
│   │   ├── security.py      — JWT / auth logic
│   │   ├── exceptions.py    — Global error handlers
│   │   ├── logging.py       — Structured logging
│   │   └── pagination.py    — Reusable pagination params
│   ├── db/
│   │   ├── session.py       — SQLAlchemy engine + SessionLocal
│   │   └── base.py          — DeclarativeBase
│   ├── models/              — ORM table definitions per entity
│   ├── schemas/             — Pydantic request/response models per entity
│   └── services/            — Business logic per entity
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Existing API Flow (Phase 1B)

If user picks "Existing API" in Step 1, after the wizard sends the generation prompt, Claude must:

1. Ask permission to read existing code before touching anything
2. Show an implementation plan after reading
3. Ask whether to edit files directly or provide code blocks to copy in
4. Wait for confirmation before making any changes

---

## Mid-project Flow

If user picks "Mid-project", Claude uses the existing context (frontend, DB etc.) when generating — references CORS for the frontend, matches existing data shapes. Does not ask for backend code since there is none.

---

## Follow-Up Loop (after generation)

After generating the project, offer in chat:
1. Add a new endpoint
2. Generate tests
3. Show the OpenAPI spec
4. Add Docker support
5. Something else

Loop until the user is done.

---

## Version

Current skill version: **v0.4.2**