---
name: summarise-granola
description: This skill should be used when the user asks to "summarise my call", "summarise my meeting", "summarise my last call", "get granola transcript", "call summary", "meeting summary", or mentions Granola transcripts or summaries. Extracts raw transcripts from Granola and creates custom summaries. (user)
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: HartreeWorks/skill--summarise-granola
# corpus-url: https://github.com/HartreeWorks/skill--summarise-granola/blob/981dc217547c0a085c5e113367c0076725428886/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Granola transcript summarisation

This skill extracts raw meeting transcripts from the Granola app, creates tidied transcripts and structured summaries, files them to the relevant project, and optionally adds summaries to a shared Google Doc, sends call notes via email, or sends them as a Slack DM.

**Update check:** Before starting, run `bash ~/.claude/skills/summarise-granola/scripts/check-update.sh`. If it prints output, show the message and ask the user which action to take:
- **Update now** — run `bash ~/.claude/skills/summarise-granola/scripts/update-skill.sh`, then re-read this SKILL.md before continuing
- **Remind me tomorrow** — run `bash ~/.claude/skills/summarise-granola/scripts/check-update.sh --snooze`, then continue
- **Never ask again** — run `bash ~/.claude/skills/summarise-granola/scripts/check-update.sh --disable`, then continue
If no output, continue silently.

## Workflow

### Step 1: Check for recent calls

Always start by running the check command:

```bash
python3 ~/.claude/skills/summarise-granola/scripts/granola.py check
```

This returns JSON with one of two modes:

**Auto mode** (call ended within 30 minutes):
```json
{"mode": "auto", "id": "...", "title": "Meeting Title", "minutes_ago": 15.2}
```
→ Proceed directly to extract and summarise this meeting.

**Select mode** (no recent call):
```json
{"mode": "select", "meetings": [
  {"number": 1, "id": "...", "title": "Meeting A", "date": "2026-01-05"},
  {"number": 2, "id": "...", "title": "Meeting B", "date": "2026-01-04"},
  ...
]}
```
→ Present the numbered list to the user and ask which one to summarise. User can reply with just "1", "2", etc.

### Step 2: Extract the transcript

Once you have the meeting ID (from auto mode or user selection), extract the transcript:

```bash
python3 ~/.claude/skills/summarise-granola/scripts/granola.py get <document_id>
```

Or by number if user selected from the list:

```bash
python3 ~/.claude/skills/summarise-granola/scripts/granola.py recent <n>
```

The transcript is automatically saved to `data/transcripts/`.

### Step 2.5: Confirm participant names

Before creating the tidied transcript and summary, confirm the names of all participants.

**Check the meeting title first:**

If the meeting title contains clear participant names (e.g., "Jane Smith & Your Name", "Call with Sarah Chen"), extract those names.

**If names are unclear:**

If the meeting title is generic (e.g., "Weekly sync", "Project check-in", "Team meeting") or doesn't contain recognisable names, ask the user using AskUserQuestion:

```
"Who were the participants in this call? (I'll use these names in the transcript and summary)"
```

Provide a free-text input option since participant names can't be predicted.

**Important:** Never guess participant names. The Granola transcript only shows "Me" and "Other" as speaker labels, which doesn't identify the other person. If in doubt, ask.

**Store the confirmed names** and use them consistently throughout the tidied transcript and summary.

### Step 3: Create tidied transcript

Create a cleaned-up version of the transcript and save it to `data/tidied-transcripts/` using the same filename.

**Tidying guidelines:**

- Remove filler words (um, uh, you know) and false starts
- Fix obvious transcription errors and grammar
- Keep speaker labels clear and consistent
- Add section headings for major topic shifts
- Do not invent or infer facts not present in the transcript

**Preserve exact wording (in quotation marks) for:**

- Expressions of certainty/uncertainty:
  - Confidence levels ("very confident", "somewhat unsure", "fairly certain")
  - Probabilistic language ("probably", "definitely", "might", "possibly")
  - Percentage estimates ("70% sure", "almost certain", "50/50")
  - Hedging language ("I think", "it seems like", "my sense is")
- Commitments and decisions ("I will", "we've decided", "I promise")
- Memorable or distinctive phrasing
- Technical specifications, numbers, or data points
- Emotional or emphatic statements

**For everything else:**

- Lightly paraphrase for clarity and concision
- Combine fragmented thoughts into coherent points
- Group related back-and-forth exchanges

**Tidied transcript format:**

- Use "**Speaker Name**:" format for attribution (bold name). If there are only two participants, use first names only.
- Separate each conversation turn with a new paragraph (not just a line break)
- Put direct quotes in "quotation marks"
- Use bullet points for lists or multiple related points

### Step 4: Create and save the summary

Create a comprehensive summary and save it to `data/summaries/` using the same filename as the transcript.

### Step 5: Associate with project

Immediately after creating the summary, determine if this call should be associated with a project.

**Step 5a: Check the people registry**

1. Extract the other participant's name from the meeting title (the person who isn't the user)
2. Convert to registry key format: lowercase, hyphenated (e.g., "Jane Smith" → "jane-smith")
3. Read the registry file:
   ```bash
   cat ~/.agents/data/people.json
   ```
4. Check if the key exists in `people` and has a `default_project` value

**Step 5b: If person is registered → auto-associate**

If found in the registry:
1. Get the `default_project` value
2. Silently associate with that project (no confirmation needed)
3. Note the auto-association for the final output (Step 6)

**Step 5c: If person is NOT registered → show project list**

If not found in the registry, fall back to the full project selection:

```bash
python3 "/Users/ph/Documents/www/Claude Plugins/plugins/plugin--project-management/scripts/list_projects.py" --format json
```

Filter to only `status: "active"` projects and present options using AskUserQuestion:
- List each active project as an option (e.g., "80000 Hours advisory")
- Include a "None" option for calls not associated with any project

**Step 5d: Copy files to project**

For both auto-associated and manually selected projects:

1. Get the project's `folder` value (from registry's `default_project` or selected project's JSON)
2. The project directory is: `~/Documents/Projects/{folder}/`
3. Create the subdirectories if they don't exist: `{project_dir}/calls/summaries/` and `{project_dir}/calls/transcripts/`
4. Copy files to the project:
   - Summary: `{project_dir}/calls/summaries/{slug}--summary.md`
   - Tidied transcript: `{project_dir}/calls/transcripts/{slug}--transcript.md`

Example:
```bash
mkdir -p ~/Documents/Projects/2026-01-80000-hours-advisory/calls/summaries
mkdir -p ~/Documents/Projects/2026-01-80000-hours-advisory/calls/transcripts
cp ~/.claude/skills/summarise-granola/data/summaries/2026-01-06-meeting--summary.md ~/Documents/Projects/2026-01-80000-hours-advisory/calls/summaries/
cp ~/.claude/skills/summarise-granola/data/tidied-transcripts/2026-01-06-meeting--transcript.md ~/Documents/Projects/2026-01-80000-hours-advisory/calls/transcripts/
```

**Step 5e: Offer to register unregistered people**

If the user selected a project for someone NOT in the registry, offer to add them:

> "Would you like me to register [Name] with [Project] for future calls?"

If yes, update `people.json` to add or update the entry with the `default_project` value.

**If user selects "None":** No additional action needed, and don't offer registration.

### Step 6: Report saved files and open them

When reporting the files saved, always use **full expanded paths** (not relative paths or paths with `~`). This allows the user to control-click/command-click on the path in their terminal to open the file.

**Indicate auto-association when applicable:**

If the project was auto-associated via the person-project registry, include this in the output:
```
Auto-associated with **Acme Consulting** (Jane Smith is registered to this project)
```

**Good:**
```
Files saved:
- /Users/username/Documents/Projects/acme-consulting/context/calls/2026-01-09-meeting--summary.md
- /Users/username/Documents/Projects/acme-consulting/context/calls/2026-01-09-meeting--transcript.md

Auto-associated with **Acme Consulting** (Jane Smith is registered to this project)
```

**Bad:**
```
Files saved:
- context/calls/2026-01-09-meeting--summary.md
- ~/Documents/Projects/acme-consulting/context/calls/2026-01-09-meeting--transcript.md
```

**Open the summary file automatically:**

After copying files to a project, open the summary file:

```bash
open "/Users/username/Documents/Projects/acme-consulting/calls/summaries/2026-01-09-meeting--summary.md"
```

### Step 7: Offer to add summary to meeting doc and/or send call notes

**Skip this step for:**
- Group meetings (more than 2 participants)
- Meetings without a clear person name
- Internal meetings or solo sessions

**Step 7a: Ask what the user wants to do**

Use AskUserQuestion with `multiSelect: true`:

- **"Add summary to meeting doc"** — always show for 1:1 calls
- **"Send call notes email to [Person Name]"** — always show for 1:1 calls
- **"Send call notes Slack DM to [Person Name]"** — always show for 1:1 calls
- **"Skip"** — always show

If the user selects neither (just "Skip"), stop here.

**Step 7b: Add summary to Google Doc** (if selected)

1. **Look up the meeting doc:**
   - Extract the other participant's initials from their name (e.g., "Matt Brooks" → "mb")
   - Look up the person in `~/.agents/data/people.json` by initials and check for a `meeting_doc` entry
   - If not found, try `gdoc find "ph-{initials}" --title` to search Google Drive
     (IMPORTANT: always use `--title` — without it, short queries trigger full-text content search which can hang)
   - If a doc is found via search, save it to the person's `meeting_doc` field in `people.json` (create the person entry if needed)
   - If no doc is found at all, tell the user and skip this action

2. **Read the current "Call summaries" tab** to find the anchor text:
   ```bash
   gdoc cat <doc_id> --tab "Call summaries" > /tmp/gdoc-tab-content.txt
   ```
   Read the output (ignoring any `gdoc` status lines at the top) and identify the **first line of real content**. This is the **anchor text** — typically a heading like `# Meeting summary: ...` or `# 2026-02-06`.

3. **Create `/tmp/gdoc-old.txt`** — write ONLY the anchor text (a single line, no trailing newline):
   ```bash
   echo -n "Meeting summary: Matt Brooks & Peter Hartree" > /tmp/gdoc-old.txt
   ```
   The anchor must exactly match text in the tab. Do NOT include the full tab content.

4. **Create `/tmp/gdoc-new.txt`** — the new summary followed by the anchor:
   - Read the local summary markdown file (the one saved in Step 4)
   - Strip all `---` horizontal rule lines and collapse surrounding blank lines so there is only one blank line before each heading (Google Docs API cannot render horizontal rules; double blank lines produce unwanted spacing)
   - **Replace the heading block** with just the date as H1. The local markdown file has:
     ```
     # Meeting summary: [title]

     **Date:** YYYY-MM-DD

     **Participants:** [names]
     ```
     Replace all of that with just:
     ```
     # YYYY-MM-DD
     ```
     Everything else (Summary, Parts, Appendices) stays the same.
   - **No blank lines between headings and body text.** Every `##` heading should be immediately followed by the body text on the next line (no blank line in between). Blank lines should only appear *before* headings (to separate sections).
   - **Keep all other markdown formatting intact**: `##` headings, `**bold**`, `- bullet` lists, `1.` numbered lists, `| table |` rows. `gdoc edit` parses the new-file as markdown and converts it to Google Docs formatting (heading styles, bold, bullets, tables with bold headers). If the markdown syntax is missing, the content will appear as unformatted plain text.
   - Append the anchor text as the final line (so the new summary appears above existing content)
   - Write to `/tmp/gdoc-new.txt`

   - **No blank line between `# YYYY-MM-DD` and the first `## Summary` heading.** The date heading and first section heading should be immediately adjacent.

   Example structure of `/tmp/gdoc-new.txt`:
   ```
   # 2026-02-24
   ## Summary
   Peter and JP discussed...

   ## Part 1: [topic]
   [body text...]

   ## Appendix 2: Key quotes
   | Speaker | Quote | Context |
   |---------|-------|---------|
   | JP | "quote" | context |

   # 2026-02-19
   ```

5. **Push the edit:**
   ```bash
   gdoc edit <doc_id> --tab "Call summaries" --old-file /tmp/gdoc-old.txt --new-file /tmp/gdoc-new.txt
   ```

6. Report success or failure to the user.

**Critical `gdoc` rules (these prevent data loss and formatting bugs):**

- **Never use `gdoc pull`/`gdoc push`/`gdoc write` on multi-tab docs.** They flatten all tabs into a single document, destroying the tab structure. Always use `gdoc edit --tab`.
- **The old-file must match a unique string in the tab.** Use the first line of existing content as the anchor — not the full tab content.
- **The new-file MUST contain proper markdown syntax.** `gdoc edit` parses the new-file as markdown and applies formatting via the Google Docs API. If you write plain text without `#`, `**`, etc., the content will appear unformatted in the doc.
- **Strip `---` lines from the summary.** Google Docs API has no horizontal rule support; these render as literal text or cause issues.
- **The summary content should otherwise be identical to the local markdown file** — same section headings, same body text, same appendices. The only differences are: removal of `---` dividers, and replacing the title/date/participants heading block with just `## YYYY-MM-DD`.

**Step 7c: Send call notes email** (if selected)

**IMPORTANT:** Always use the `send-email` skill (Node.js script) for sending emails.

**If the user wants to send the email:**

**a) Find the meeting doc and get the Call summaries tab URL:**

Meeting docs follow the naming pattern `ph-${initials}` (e.g., `ph-js` for Jane Smith).

1. Extract person initials: first letter of each word in their name, lowercase (e.g., "Jane Smith" → "js")
2. Check `people.json` first: look up the person by initials and check for a `meeting_doc` entry. If found, use the cached URL.
3. If not cached, search Google Drive:
   ```bash
   gdoc find "ph-${initials}" --title
   ```
4. Cache any new result in `people.json` under the person's `meeting_doc` field.

5. **Get the "Call summaries" tab URL:**
   Extract the doc ID from the meeting doc URL, then get tab info:
   ```bash
   gdoc tabs <doc_id> --json
   ```
   Find the tab with `"title": "Call summaries"` and extract its `id` field. Construct the tab URL:
   ```
   https://docs.google.com/document/d/<doc_id>/edit?tab=<tab_id>
   ```
   **Always link to the "Call summaries" tab**, not the base doc URL.

**b) Find the attendee's email address:**

1. Check `people.json` for an `email` field on the person's entry. If found, use it.
2. If not found, search Gmail using the **claude.ai Gmail MCP**:
   ```
   mcp__claude_ai_Gmail__gmail_search_messages
     q: "from:<person name> OR to:<person name>"
     maxResults: 3
   ```
   Then read the most recent message to extract the attendee's email from the headers:
   ```
   mcp__claude_ai_Gmail__gmail_read_message
     messageId: "<message_id>"
   ```
3. If Gmail search doesn't find a match, ask the user for the email address.
4. Once an email is obtained (from Gmail or the user), save it to the person's `email` field in `people.json` for future use.

**c) Ask if the user wants to add a comment:**

> "Would you like to add a comment to the call notes email?"

- Provide a "No comment" option and a free-text "Add a comment" option

**d) Send the email using the send-email skill:**

Use the send-email skill's Node.js script directly:

```bash
cd ~/.agents/skills/send-email && node send-email.js "<to>" "Call notes" "<message>"
```

- **To:** the attendee's email address
- **Subject:** `Call notes`
- **Message (without comment):**
  ```
  Hi <first name>,

  Summary of our call here:
  <call_summaries_tab_url>

  All the best,
  Peter
  ```
- **Message (with comment):**
  ```
  Hi <first name>,

  Summary of our call here:
  <call_summaries_tab_url>

  <user's comment>

  All the best,
  Peter
  ```

Show the user a preview of the email and ask for confirmation before sending.

**Step 7d: Send call notes via Slack DM** (if selected)

1. **Find the person's Slack DM channel:**
   - Check `people.json` for a `slack_dm_channel` field on the person's entry
   - The field is an object: `{"channel_id": "D...", "workspace": "type3ltd", "slack_connect": true}`
   - If not found, use the Slack skill's `slack_client.py` to find the DM channel:
     - Try each workspace: `python3 ~/.agents/skills/slack/scripts/slack_client.py --workspace <ws> channels "im"`
     - Match by user ID against known Slack search results
   - Cache the full object in `people.json` under the person's `slack_dm_channel` field for future use

2. **Compose message** using Slack mrkdwn formatting — keep it brief (no greeting or sign-off):
   - **Without comment:**
     ```
     Summary of our call here:
     <call_summaries_tab_url>
     ```
   - **With comment:**
     ```
     Summary of our call here:
     <call_summaries_tab_url>

     <user's comment>
     ```

3. **Show preview and ask for confirmation** before sending (same pattern as the email step).

4. **Send via Slack** (always pass `--workspace` from the cached entry):
   ```bash
   python3 ~/.agents/skills/slack/scripts/slack_client.py --workspace <workspace> send "<channel_id>" "<message>"
   ```

5. Report success or failure to the user.

## File locations

- **Raw transcripts:** `~/.claude/skills/summarise-granola/data/transcripts/`
- **Tidied transcripts:** `~/.claude/skills/summarise-granola/data/tidied-transcripts/`
- **Summaries:** `~/.claude/skills/summarise-granola/data/summaries/`

Files use the pattern:
- Raw transcripts: `YYYY-MM-DD-meeting-title-slug.md`
- Tidied transcripts: `YYYY-MM-DD-meeting-title-slug--transcript.md`
- Summaries: `YYYY-MM-DD-meeting-title-slug--summary.md`

## Summary format

Create comprehensive, chronological summaries that help the user re-envision and remember the conversation. The chronological structure is key—it allows details not explicitly in the summary to be recalled by following the flow.

### Document structure

```markdown
# Meeting summary: [Title]

**Date:** YYYY-MM-DD

**Participants:** [Full names with roles if relevant]

---

## Summary

[3-5 sentence overview of what the call was about and what was concluded. If listing items, use a numbered list with each item on its own line.]

---

## Part 1: [Opening topic/context]

[Chronological narrative of this phase of the conversation...]

---

## Part 2: [Next major topic]

[Continue chronologically...]

---

## Part N: The path forward / Next steps

[Clear statement of decisions and actions decided upon]

**Specific actions agreed:**
1. First action
2. Second action
3. ...

**[Person]'s next step:**
[Immediate action to take]

---

## Appendix 1: Open questions

- Question 1
- Question 2

---

## Appendix 2: Key quotes

| Speaker | Quote | Context |
|---------|-------|---------|
| Name | "Quote text" | Brief context |

---

## Appendix 3: Underlying dynamics

[Optional—include when there are important subtext, emotional dynamics, or strategic considerations worth noting. Skip if not applicable.]

**[Dynamic 1]:** Explanation...

**[Dynamic 2]:** Explanation...
```

### Formatting guidelines

**Lists:**
- Use **numbered lists** when items might be referred to later (options, action items, decisions)
- Use **lettered lists (a, b, c)** when you don't want to imply prioritisation
- Use **bullet lists** only for items that won't need to be referenced
- Always put each list item on its own line (no inline numbered lists)

**Quotations:**
- Use inline "quotation marks" for short, key phrases within prose
- Use block quotes (>) for longer or particularly important statements
- Preserve exact wording for:
  - Expressions of certainty/uncertainty
  - Commitments and decisions
  - Memorable or distinctive phrasing
  - Insights and realisations

**Structure:**
- Use `---` horizontal rules to separate major sections
- Bold speaker names when attributing quotes or positions
- Use tables for structured comparisons (e.g., concept assessments)

### Content guidelines

**Depth:** Match depth to the richness of the conversation. A substantive 45-minute strategy discussion warrants 150-200+ lines; a brief check-in might need only 50.

**Chronological narrative:** Tell the story of how the conversation unfolded and how conclusions were reached. This helps the user mentally reconstruct the call.

**Capture insights:** Don't just list decisions—capture the reasoning, realisations, and shifts in thinking that led to them.

**Appendices:**
- **Open questions** (Appendix 1): Almost always include; usually first appendix
- **Key quotes** (Appendix 2): Include when there are memorable or important phrasings
- **Underlying dynamics** (Appendix 3): Include when there's important subtext (emotional state, strategic considerations, relationship dynamics); skip when not applicable

### Example part structure

```markdown
## Part 2: Diagnosing the problem

Alex asked a pivotal question: "Is this a brief issue or an execution of the brief issue?"

This opened up a crucial realisation. Alex introduced the "new aesthetics" framing—an emerging visual language for the project.

The user's reaction was immediate recognition:
> "We should be at the front of that. In my dream world, if I was leading this, I would have put a lot into trying to be at the front of that."

**The diagnosis crystallised:** The brief hadn't communicated this ambition. The user admitted: "It definitely wasn't pitched that ambitiously."

This explained the expectation gap: The user was unconsciously hoping for something revolutionary while the agency was delivering competent-but-safe work as briefed.
```

## Transcript format

- `**Me**:` - User's microphone (the person running Granola)
- `**Other**:` - System audio (other participants)

## User info

Replace "YOUR_NAME" with the user's actual name. Always use their preferred name format in summaries.

## Script reference

| Command | Description |
|---------|-------------|
| `check` | Check for recent call or list 5 most recent for selection |
| `list` | List all meetings with transcripts |
| `get <id>` | Get transcript by document ID |
| `recent [n]` | Get nth most recent transcript (default: 1) |

## Tips

- For long meetings, consider summarising in sections
- Ask what the user wants to focus on if the meeting covered multiple topics
- Include participant names from the meeting title when relevant

## People registry

The registry at `~/.agents/data/people.json` stores per-person metadata: default project associations and meeting doc references.

**Format:**
```json
{
  "people": {
    "jane-smith": {
      "full_name": "Jane Smith",
      "initials": "js",
      "default_project": "coaching-jane",
      "meeting_doc": {
        "url": "https://docs.google.com/document/d/...",
        "title": "ph-js Peter Hartree & Jane Smith meetings",
        "cached_at": "2026-01-20"
      }
    }
  }
}
```

**Key format:** Lowercase, hyphenated full name (e.g., "Rob Long" → "rob-long")

**Fields:**
- `full_name` — display name
- `initials` — lowercase initials for meeting doc lookup (e.g., "mb", "jho")
- `email` — email address for sending call notes (Step 7c), or `null`
- `slack_dm_channel` — Slack DM details for sending call notes (Step 7d), or `null`. Object with `channel_id`, `workspace` (e.g. "type3ltd", "80000hours"), and `slack_connect` (boolean)
- `default_project` — project folder name for auto-association (Step 5), or `null`
- `meeting_doc` — Google Doc reference for call summaries (Step 7b), or `null`

**Lookups:**
- **By name** (Step 5a): convert name to hyphenated key, check `people`
- **By initials** (Step 7b): scan `people` for matching `initials` field; if not found, search with `gdoc find "ph-{initials}" --title` and save the result

**Adding entries:**
- Automatically when a meeting doc is found via search
- When the user accepts the offer to register a person with a project (Step 5e)
- Manual edits