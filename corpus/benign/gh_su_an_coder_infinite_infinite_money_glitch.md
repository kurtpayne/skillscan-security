---
name: Infinite Money Glitch
description: Self-sustaining autonomous agent on Sui blockchain
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npx
      env:
        - SUI_PRIVATE_KEY
        - BOUNTY_PACKAGE_ID
        - BOUNTY_BOARD_ID
        - SEAL_PACKAGE_ID
    os:
      - macos
      - linux
      - windows
    emoji: 💰
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: SU-AN-coder/Infinite-Money-Glitch
# corpus-url: https://github.com/SU-AN-coder/Infinite-Money-Glitch/blob/476228289f4c9022d5e3ced702944686da050438/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Infinite Money Glitch Agent

A self-sustaining agent that earns SUI through BountyBoard tasks,
spends SUI on Seal encryption and Walrus storage, and reports
profit/loss with on-chain proof.

## Usage

Run a single economic cycle: health-check → earn → spend → audit → verify → report.