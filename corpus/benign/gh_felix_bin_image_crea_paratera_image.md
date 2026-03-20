---
name: paratera-image
description: Generate images via Paratera OpenAI-compatible API (model via env).
homepage: https://llmapi.paratera.com
metadata:
  {
    "openclaw":
      {
        "emoji": "IMG",
        "requires":
          {
            "bins": ["uv"],
            "env": ["OPENAI_API_KEY", "OPENAI_BASE_URL", "IMAGE_MODEL"],
          },
        "primaryEnv": "OPENAI_API_KEY",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Felix-bin/image-creation
# corpus-url: https://github.com/Felix-bin/image-creation/blob/8dd2380fbf348e34452d0de95f890f3c633e3f8a/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Paratera Image Generation

Setup

1. Copy `.env.example` to `.env`
2. Fill in:
   - `OPENAI_API_KEY`
   - `OPENAI_BASE_URL` (include `/v1`)
   - `IMAGE_MODEL`

Generate

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K
```

Notes

- Model is selected via `IMAGE_MODEL` in `.env` (no CLI flag).
- Resolutions: `1K` (default), `2K`, `4K`.
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`.
- The script prints a `MEDIA:` line for OpenClaw to auto-attach on supported chat providers.
- Do not read the image back; report the saved path only.