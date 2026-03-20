---
name: azure-image-gen
description: Generate a single image via Azure OpenAI Images REST API and return it inline in OpenClaw.
homepage: https://learn.microsoft.com/azure/ai-services/openai/
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins: ["python3"]
      env:
        - AZURE_OPENAI_ENDPOINT
        - AZURE_OPENAI_API_KEY
        - AZURE_OPENAI_IMAGE_DEPLOYMENT
        - AZURE_OPENAI_API_VERSION
    primaryEnv: AZURE_OPENAI_API_KEY
    notes: |
      This skill uses Azure OpenAI REST (not OpenAI public API).
      It generates exactly ONE image per invocation and prints JSON to stdout:
        { "ok": true, "path": "/absolute/path/to/image.png" }
      OpenClaw should attach the file at `path` as an inline image response.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: neojarvis0704/azure-image-gen
# corpus-url: https://github.com/neojarvis0704/azure-image-gen/blob/9a0fda72b933bca729544cbb9df3e222451b832a/skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Azure Image Generation (OpenClaw)

This skill generates a **single image** using **Azure OpenAI Images API** and returns it for **inline display** in OpenClaw-supported channels.

## How it works

- OpenClaw executes the script:
  ```bash
  python3 scripts/gen.py "<prompt>"
  ```
- The script:
  - Calls Azure OpenAI Images REST API
  - Saves the image using a **timestamp-based filename**
  - Prints a JSON object containing the absolute file path

## Script location

```
skills/azure-image-gen/scripts/gen.py
```

## Required environment variables

These are loaded from `/home/thomas/.env.azure` by the script:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_IMAGE_DEPLOYMENT`
- `AZURE_OPENAI_API_VERSION`

Example:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=****
AZURE_OPENAI_IMAGE_DEPLOYMENT=gpt-image-1.5
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

## Output contract (important)

The script prints **exactly one JSON object** to stdout:

```json
{
  "ok": true,
  "path": "/home/thomas/.openclaw/workspace/skills/azure-image-gen/out/20260206_101753.png",
  "prompt": "a cyberpunk cat in Hong Kong at night"
}
```

OpenClaw should treat `path` as a media attachment and send it inline.

## Notes

- No batch generation
- No gallery / index.html
- No OpenAI public API usage
- Azure-only, REST-only