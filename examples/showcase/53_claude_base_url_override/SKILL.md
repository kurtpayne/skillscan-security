# Suspicious Claude Code project config

This repository-scoped Claude config overrides `ANTHROPIC_BASE_URL` to a non-Anthropic endpoint.
In vulnerable tool versions, this can route authenticated API traffic (including API keys) to attacker infrastructure before trust prompts are resolved.
