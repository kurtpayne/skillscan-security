---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: bcharleson/openclaw-macmini-setup-guide
# corpus-url: https://github.com/bcharleson/openclaw-macmini-setup-guide/blob/ea7bff28034ca50d63513ec922fc3fa1a4d95b46/claude-skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# OpenClaw Mac Mini Setup - Claude Skill

## Description

Guide users through setting up an OpenClaw agent on a Mac Mini with a dedicated user account, Slack integration, and proper security configuration.

## When to Use This Skill

Invoke this skill when users ask about:
- Setting up OpenClaw on Mac Mini
- Creating isolated OpenClaw agent accounts
- Configuring OpenClaw with Slack
- OpenClaw security best practices
- Multiple agent setups on the same machine

## Instructions

When a user requests OpenClaw setup assistance:

1. **Understand their goal:**
   - Single agent or multiple agents?
   - What's the agent name and username?
   - Do they have Slack workspace access?
   - Do they have Anthropic API credentials?

2. **Guide them through the setup:**
   - Reference the [AGENT-SETUP.md](./AGENT-SETUP.md) guide
   - Help them fill in the variables section:
     - AGENT_NAME: Display name (e.g., "EVE", "WALL-E")
     - AGENT_USERNAME: Lowercase username
     - UNIQUE_ID: Auto-detect or specify (502, 503, etc.)
     - ADMIN_USERNAME: Their admin username
     - Slack tokens (obtained in Part 4)
     - Anthropic API key

3. **Walk through each part:**
   - Part 1: Create user account
   - Part 2: Set up environment
   - Part 3: Install Node.js and build
   - Part 4: Create Slack app (detailed OAuth flow)
   - Part 5: Configure OpenClaw
   - Part 6: Set up API key
   - Part 7: Start gateway
   - Part 8: Verify setup
   - Part 9: Test in Slack
   - Part 10: (Optional) Admin access

4. **Security reminders:**
   - Warn about secrets in shell history
   - Ensure `.env` files have proper permissions (chmod 600)
   - Explain Slack DM policy security implications
   - Recommend FileVault for disk encryption
   - Suggest strong passwords for user accounts

5. **LLM Configuration:**
   - Recommend Anthropic Opus 4.5 for best results
   - Mention OAuth support (Anthropic Pro/Max)
   - Note that any LLM can be configured (local or cloud)
   - Reference OpenClaw docs for model configuration

6. **Troubleshooting:**
   - "User already exists" → check/change UNIQUE_ID
   - "Permission denied" → re-run ownership commands
   - "Slack not connecting" → verify tokens and Socket Mode
   - "Node/pnpm not found" → ensure nvm is sourced

## Example Usage

**User:** "How do I set up OpenClaw on my Mac Mini?"

**Agent:** "I'll help you set up OpenClaw on your Mac Mini! This guide will create a dedicated user account for your agent with proper isolation and security.

First, let's gather some info:
1. What would you like to name your agent? (e.g., 'EVE', 'WALL-E')
2. Do you have a Slack workspace?
3. Do you have an Anthropic API key?

Once we have these, I'll walk you through the setup using a variable-driven guide that makes it easy to copy-paste commands..."

## Files

- `AGENT-SETUP.md`: Complete setup guide with all commands
- `README.md`: Quick overview and features
- `claude-skill.md`: This skill documentation

## Repository

https://github.com/bcharleson/openclaw-macmini-setup-guide