---
name: inference-difference
description: "The Inference Difference is a transparent AI inference router that automatically selects the best model for each request based on complexity, domain, cost, and hardware constraints. Invoke when asked about routing decisions, model selection, inference costs, why a specific model was chosen, routing statistics, available models, or to inspect current routing state."
metadata: { "openclaw": { "emoji": "✂️", "requires": {} } }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: greatnorthernfishguy-hub/The-Inference-Difference
# corpus-url: https://github.com/greatnorthernfishguy-hub/The-Inference-Difference/blob/33adbce6a7910ac7613ea4bf8e3eff9aa5e1997a/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# The Inference Difference (TID)

## Overview

TID is a transparent OpenAI-compatible inference proxy running at `http://127.0.0.1:7437/v1`. All model calls route through it automatically — callers never know TID exists.

## Introspection Endpoints

Use these to inspect routing behavior without triggering a real inference call:

- `GET  http://127.0.0.1:7437/health` — Service health and NG-Lite status
- `GET  http://127.0.0.1:7437/stats`  — Routing performance and learning stats
- `GET  http://127.0.0.1:7437/models` — Available models and their capabilities
- `GET  http://127.0.0.1:7437/modules` — Registered ET modules (TrollGuard, etc.)
- `POST http://127.0.0.1:7437/route`  — Inspect routing decision for a given request without forwarding it

## Routing Pipeline

1. Pre-route hooks (TrollGuard security scan, OpenClaw compliance)
2. Request classification (domain, complexity, token estimate)
3. Model scoring (hardware constraints, 6-factor weighted score, NG-Lite learning)
4. Forward to winning provider (Ollama / OpenRouter / Anthropic / etc.)
5. Quality evaluation → NG-Lite outcome feedback loop