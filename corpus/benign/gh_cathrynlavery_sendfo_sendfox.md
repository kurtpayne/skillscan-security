---
name: sendfox
description: Email marketing automation with SendFox API via agent-first CLI. Use when managing contacts and lists, viewing campaigns, setting up automated sequences, generating signup forms, or integrating SendFox with landing pages. Triggers on tasks like "add contact to newsletter," "create email list," "set up welcome sequence," "generate signup form," or any SendFox-related email automation.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: cathrynlavery/sendfox-skill
# corpus-url: https://github.com/cathrynlavery/sendfox-skill/blob/3dedd8795f84c183db0675eb28474ad35736e803/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# SendFox Email Marketing

## Overview

This skill provides an agent-first CLI for SendFox email marketing automation. Use the `sendfox` command to manage contacts, lists, view campaigns, and generate ready-to-use signup forms that integrate with landing pages.

## Installation

Build and install the SendFox CLI:

```bash
cd scripts
./build.sh
./install.sh
```

Set your API token:

```bash
export SENDFOX_API_TOKEN='your_token_here'
```

Get a token at: https://sendfox.com/account/oauth

## Quick Start

Verify API connection:

```bash
sendfox health
```

View all available commands:

```bash
sendfox
```

## Core Commands

### Contact Management

**Create a contact:**
```bash
sendfox contact create --email="user@example.com" --first-name="John"
```

**Add contact to specific lists:**
```bash
sendfox contact create --email="user@example.com" --lists=123 --lists=456
```

**Get contact by email:**
```bash
sendfox contact get --email="user@example.com"
```

**Get contact by ID:**
```bash
sendfox contact get --id=789
```

**Unsubscribe a contact:**
```bash
sendfox contact unsubscribe --email="user@example.com"
```

### List Management

**Create a new list:**
```bash
sendfox list create --name="Newsletter Subscribers"
```

**Get all lists:**
```bash
sendfox list get
```

**Get specific list:**
```bash
sendfox list get --id=123
```

**Get all contacts in a list:**
```bash
sendfox list contacts --id=123
```

### Campaign Management

**Get all campaigns:**
```bash
sendfox campaign get
```

**Get specific campaign:**
```bash
sendfox campaign get --id=456
```

Note: Campaign creation is read-only via API limitations. Use the SendFox UI to create campaigns; the API only supports retrieving campaign information.

### Form Generation

**Generate basic subscribe form:**
```bash
sendfox form generate --type=basic-subscribe --list-id=123 --output=subscribe.html
```

**Generate landing page with form:**
```bash
sendfox form generate --type=landing-page --list-id=123 --output=landing.html
```

**Generate popup form:**
```bash
sendfox form generate --type=popup --list-id=123 --output=popup.html
```

Available form types:
- `basic-subscribe` - Simple email signup form
- `landing-page` - Full landing page with integrated form
- `popup` - Modal popup signup form

## Common Workflows

### Add New Subscriber to Welcome Sequence

```bash
# 1. Get your welcome sequence list ID
sendfox list get

# 2. Add contact to the list (triggers automation)
sendfox contact create \
  --email="newuser@example.com" \
  --first-name="Jane" \
  --lists=123
```

When added to a list with an automation, the contact automatically enters the email sequence.

### Create Signup Form for Landing Page

```bash
# 1. Create a list for the signup form
sendfox list create --name="Landing Page Signups"

# 2. Generate the form with the list ID
sendfox form generate \
  --type=landing-page \
  --list-id=124 \
  --output=signup.html
```

### Batch Import Contacts

```bash
#!/bin/bash
# Import contacts from a CSV
while IFS=, read -r email first_name; do
  sendfox contact create \
    --email="$email" \
    --first-name="$first_name" \
    --lists=123
done < contacts.csv
```

## Email Automation

SendFox automations (drip campaigns) are set up through the web UI. Once configured, adding contacts via the CLI automatically triggers the sequences.

### Setting Up Automations

1. Go to https://sendfox.com/automations
2. Create a new automation
3. Set trigger: "Contact added to list"
4. Add emails with delays
5. Activate the automation

Then use the CLI to add contacts to that list, triggering the automation.

### Email Sequence Templates

Ready-to-use email sequence templates are available in `assets/sequence-templates/`:

- **welcome-sequence.md** - 3-email welcome series (Immediate, +2d, +5d)
- **nurture-sequence.md** - 5-email lead nurture flow (Immediate, +3d, +5d, +7d, +10d)
- **onboarding-sequence.md** - 7-email product onboarding (Immediate, +1d, +3d, +5d, +7d, +10d, +14d)

Copy the email content from these templates when creating automations in the SendFox UI.

For detailed automation setup instructions, see `references/automation_guide.md`.

## API Reference

For complete API documentation including all endpoints, authentication, request/response formats, and error handling, see `references/api_reference.md`.

## CLI Design

The `sendfox` CLI follows agent-first design principles:

- **JSON responses** - All commands return structured JSON for easy parsing
- **HATEOAS pattern** - Responses include `next_actions` suggesting contextual commands
- **Error guidance** - Errors include a `fix` field with remediation steps
- **Self-documenting** - Run `sendfox` with no arguments to see all available commands

Example response:
```json
{
  "ok": true,
  "command": "sendfox contact create",
  "result": {
    "contact": {
      "id": 789,
      "email": "user@example.com"
    }
  },
  "next_actions": [
    {
      "command": "sendfox contact get --id=789",
      "description": "View this contact's details"
    }
  ]
}
```

## Resources

### scripts/cli/
TypeScript CLI source code built with @effect/cli and Bun. Compiles to a standalone binary.

### references/
- `api_reference.md` - Complete SendFox API documentation
- `automation_guide.md` - Email automation and sequence setup guide

### assets/
- `form-templates/` - HTML signup form templates
- `sequence-templates/` - Email sequence content templates