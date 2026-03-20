---
name: gemini-search-image-video-creator
description: |
  Gemini PRO 3.1 UI Automation via existing Chrome profile. Provides AI agent-accessible methods for prompt sending, deep search, image generation, and video generation using dev-browser extension.
  Use when: automating Gemini UI, generating images/videos with Gemini, conducting deep research via Gemini, or needing AI agent access to Gemini PRO features.
license: MIT
metadata:
  author: user
  version: "1.4.0"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: oguzhandilber/gemini-search-image-video-creator
# corpus-url: https://github.com/oguzhandilber/gemini-search-image-video-creator/blob/eb77f2b64e6ef914cd65fb9c131f8c6a3a009303/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Gemini Search Image Video Creator

You are an expert in automating Gemini PRO UI through Chrome's existing browser session using the dev-browser extension and relay server.

## Quick Start - Read This First

### OPTIONAL: Optimize Your Prompt First

20: HZ|Before running CLI, you can OPTIONALLY use the **gemini-prompt-optimization** skill to improve results:
21: WM|1. Load `gemini-prompt-optimization` skill
2. Provide your raw prompt
3. Use the optimized prompt in CLI

This uses Google official templates for better image/video/deepsearch results.

---

When user asks to generate image/video/prompt with Gemini:

**Step 1: Ensure relay server is running**
```bash
cd /tmp/dev-browser/skills/dev-browser && npx tsx scripts/start-relay.ts &
```
Wait 3 seconds, verify with: `curl -s http://localhost:9222`

**Step 2: Run the CLI command**

For IMAGE generation:
```bash
41: SK|npx tsx scripts/cli.ts image "USER_PROMPT"
```

For VIDEO generation:
```bash
46: HV|npx tsx scripts/cli.ts video "USER_PROMPT"
```

For PROMPT/CHAT:
```bash
51: YQ|npx tsx scripts/cli.ts prompt "USER_PROMPT"
```

For DEEP RESEARCH:
```bash
56: RN|npx tsx scripts/cli.ts deepsearch "USER_QUERY"
```

**Step 3: Report results**
- Tell user where the screenshot was saved
- Show the output path

---

## Prerequisites

### 1. Chrome Extension Setup
- Install dev-browser Chrome extension
- Set extension mode to "Active" (not "Off")
- Ensure your Google account is logged into Gemini

### 2. Relay Server (CRITICAL)
The relay server must be running for ANY automation:

```bash
# Start relay server (one-time setup)
cd /tmp/dev-browser/skills/dev-browser
npx tsx scripts/start-relay.ts &
```

Verify it's running:
```bash
curl -s http://localhost:9222
# Should return: {"wsEndpoint":"ws://127.0.0.1:9222/cdp","extensionConnected":true,"mode":"extension"}
```

---

## Available Actions

### 1. Send Prompt
**Command:** `npx tsx scripts/cli.ts prompt "your message"`

**What it does:**
- Connects to Chrome via relay server
- Switches to PRO model if needed
- Types prompt into textbox
- Presses Enter to send
- Waits for response (15s)
- Saves screenshot to `{outputDir}/gemini-response.png`

### 2. Deep Search
**Command:** `npx tsx scripts/cli.ts deepsearch "your research query"`

**What it does:**
- Opens Gemini Deep Research mode
- Enters query and submits
- Auto-clicks approve button when research plan appears
- Waits for research to complete (2-3 minutes)
- Saves full research text to `{outputDir}/gemini-deep-research.txt`
- Saves screenshot to `{outputDir}/gemini-deepsearch.png`

**IMPORTANT:** Deep Research takes 2-3 minutes. Be patient!

**Example:**
```bash
cd /tmp/dev-browser/skills/dev-browser
118: YQ|npx tsx scripts/cli.ts deepsearch "AI trends 2026"
```

After completion, read the research from `{outputDir}/gemini-deep-research.txt`

### 3. Image Generation
**Command:** `npx tsx scripts/cli.ts image "sunset over ocean"`

**What it does:**
- Sends prompt to Gemini
- Waits for image creation (25s)
- Saves full-page screenshot to `{outputDir}/gemini-image.png`

**Example:**
```bash
cd /tmp/dev-browser/skills/dev-browser
134: VX|npx tsx scripts/cli.ts image "Okyanusun üzerinde güneş batışı"
```

### 4. Video Generation
**Command:** `npx tsx scripts/cli.ts video "space travel"`

**What it does:**
- Sends prompt for video
- Waits for video creation (30s)
- Saves screenshot to `{outputDir}/gemini-video.png`

---

## Configuration

### Output Directory
By default, files are saved to user's home directory. You can change this:

```bash
# Set custom output directory
GEMINI_OUTPUT_DIR=/tmp/output npx tsx scripts/cli.ts image "cat"

# Or export for multiple commands
export GEMINI_OUTPUT_DIR=/tmp
npx tsx scripts/cli.ts image "cat"
npx tsx scripts/cli.ts prompt "hello"
```

### Timeout Configuration
You can customize timeouts via environment variables:

```bash
# Page load timeout (default: 30000ms)
GEMINI_TIMEOUT_PAGE_LOAD=60000 npx tsx scripts/cli.ts prompt "hello"

# Response wait timeout (default: 20000ms)
GEMINI_TIMEOUT_RESPONSE=30000 npx tsx scripts/cli.ts prompt "complex task"

# Deep search timeout (default: 180000ms = 3 minutes)
GEMINI_TIMEOUT_DEEP_SEARCH=300000 npx tsx scripts/cli.ts deepsearch "AI"

# Image generation timeout (default: 25000ms)
GEMINI_TIMEOUT_IMAGE=35000 npx tsx scripts/cli.ts image "detailed scene"

# Video generation timeout (default: 30000ms)
GEMINI_TIMEOUT_VIDEO=60000 npx tsx scripts/cli.ts video "animation"
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| "Connection refused" | Start relay server: `cd /tmp/dev-browser/skills/dev-browser && npx tsx scripts/start-relay.ts &` |
| "Extension not connected" | Set dev-browser extension to "Active" mode |
| "PRO model not available" | Check if user has PRO access |
| "Element not found" | Gemini UI may have changed - script will try fallback selectors |
| "Output directory does not exist" | Set `GEMINI_OUTPUT_DIR` to a valid path |
| "Prompt cannot be empty" | Provide a non-empty prompt |
| "Prompt exceeds maximum length" | Prompt is too long (max 10000 chars) |

### Troubleshooting

**Relay server won't start:**
1. Check if port 9222 is available: `lsof -i :9222`
2. Kill existing process if needed
3. Restart: `cd /tmp/dev-browser/skills/dev-browser && npx tsx scripts/start-relay.ts &`

**Extension shows as not connected:**
1. Open Chrome and navigate to any page
2. Click the dev-browser extension icon
3. Ensure mode is set to "Active"

**Operation times out:**
- Increase timeout values using environment variables
- Deep research may take longer depending on query complexity

---

## Output Format

When completing a Gemini automation task, report:

```markdown
## Action Taken
[What was done]

## Connection Status
✅ Connected to existing Chrome session / ❌ Connection failed

## Model
PRO model active / Still on Hızlı

## Result
[Response summary / Error details]

## Files Generated
[screenshot paths]
```

---

## Dependencies

- dev-browser Chrome extension (installed and active)
- Relay server running on localhost:9222
- Existing Gemini login session
- PRO model access (user account dependent)

---

## Example Workflow

1. User says: "Generate an image of a cat"
249: KK|2. (OPTIONAL) Use `gemini-prompt-optimization` skill to improve the prompt
3. Check if relay server is running
4. If not, start it: `cd /tmp/dev-browser/skills/dev-browser && npx tsx scripts/start-relay.ts &`
252: JB|5. Run: `npx tsx scripts/cli.ts image "cat"`
6. Report: "✅ Image generated: ~/gemini-image.png"

---

## API Reference

### Module Import
```typescript
import { geminiAI } from './cli.js';

// Generate image
await geminiAI.image("sunset over ocean");

// Generate video  
await geminiAI.video("space travel");

// Send prompt
await geminiAI.prompt("hello world");

// Run deep search
await geminiAI.deepSearch("AI trends 2026");

// Disconnect when done
await geminiAI.disconnect();
```

### Class Methods
```typescript
const gemini = new GeminiAutomation();

await gemini.connect();           // Connect to Chrome
await gemini.prompt("text");      // Send prompt
await gemini.image("prompt");      // Generate image
await gemini.video("prompt");      // Generate video
await gemini.deepSearch("query"); // Deep research
await gemini.disconnect();        // Cleanup
```

---

## Version History

295: YR|- **1.4.0**: Added gemini-prompt-optimization skill reference
- **1.3.0**: Added input validation, configurable timeouts, proper TypeScript types, input sanitization, fixed race condition
- **1.2.0**: Added configurable output directory, improved error handling, localization fallback selectors
- **1.1.0**: Initial release with basic prompt, image, video, and deep search support