---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Lawliet2004/Speech-emotion-Detector
# corpus-url: https://github.com/Lawliet2004/Speech-emotion-Detector/blob/ead480653e8788aaac423ef44769abedaa9f7cc6/skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Project Skill

This repository is for building a speech emotion recognition system from the local `AudioWAV/` dataset.

## Required First Step For Any Future Agent
- Read `context.md` before making plans, writing code, or changing files.
- Treat `context.md` as the current project handoff document.

## Working Rules
- Keep the raw dataset in `AudioWAV/` untouched.
- Use manifest-driven workflows instead of moving audio files into new folders.
- Preserve speaker-disjoint train/validation/test splits.
- Use the six V1 emotion labels only: `angry`, `disgust`, `fear`, `happy`, `neutral`, `sad`.
- Treat filename intensity as metadata, not as the V1 prediction target, unless the user explicitly changes that decision.
- Prefer reproducible scripts and versioned artifacts over manual steps.

## Current Repo Conventions
- Dataset manifests live in `manifests/`.
- Utility scripts live in `scripts/`.
- The current manifest generator is `scripts/create_audio_manifest.py`.

## Update Contract
- Any time code, data-processing logic, file structure, training setup, model behavior, or project decisions change, update `context.md` in the same work session.
- Update `skill.md` too if the workflow rules, repo conventions, or standing instructions change.
- When updating `context.md`, refresh:
  - current status
  - key decisions
  - important files
  - recent changes
  - next recommended step

## Preferred Agent Behavior
- Before changing anything, inspect the current manifests, scripts, and `context.md`.
- After changing anything, leave the repo in a state where another agent can continue without re-discovering the project.
- Be explicit about assumptions when the user has not decided something yet.