---
name: fal-generate
description: Generate images and videos using fal.ai models. Use when the user asks to create, generate, or make images, pictures, videos, animations, or visual content. Supports text-to-image, text-to-video, and image-to-video generation with queue-based processing.
metadata:
  author: falagent
  version: "0.1.0"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: aleSheng/fal-agent
# corpus-url: https://github.com/aleSheng/fal-agent/blob/5e802a5f78a748756a181fcbc49cb7eb6d8a3213/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# fal.ai Image & Video Generation

Generate images and videos from text prompts using fal.ai's AI models.

## Setup

If FAL_KEY is not configured, run:
```bash
cd /Users/yzlabmac/agentspace/falagent && bun run setup
```

Or set directly:
```bash
export FAL_KEY=your_key_here
```

## Generate Images

```bash
cd /Users/yzlabmac/agentspace/falagent && bun run generate --prompt "DESCRIPTION" --model MODEL [--size square|portrait|landscape] [--num-images N]
```

**Recommended image models:**
- `fal-ai/nano-banana-pro` - Best quality, semantic-aware generation (default)
- `fal-ai/flux-pro/v1.1-ultra` - High quality, fast
- `fal-ai/recraft-v3` - Stylized images

## Generate Videos

```bash
cd /Users/yzlabmac/agentspace/falagent && bun run generate --prompt "DESCRIPTION" --model MODEL
```

**Recommended video models:**
- `fal-ai/veo3` - Highest quality text-to-video
- `fal-ai/kling-video/v2.1/standard` - Fast text-to-video
- `fal-ai/minimax-video/video-01-live` - Good for short clips

## Image-to-Video

First upload the image, then generate:

```bash
cd /Users/yzlabmac/agentspace/falagent && bun run upload --file /path/to/image.jpg
cd /Users/yzlabmac/agentspace/falagent && bun run generate --prompt "MOTION DESCRIPTION" --model fal-ai/kling-video/v2.1/pro/image-to-video --image-url IMAGE_URL
```

**Recommended image-to-video models:**
- `fal-ai/kling-video/v2.1/pro/image-to-video` - Best quality
- `fal-ai/wan/v2.1/image-to-video` - Good alternative

## Async Mode (for long videos)

For models that take a long time, use `--async` to get a request ID immediately:

```bash
cd /Users/yzlabmac/agentspace/falagent && bun run generate --prompt "..." --model fal-ai/veo3 --async
```

Then check status or get the result:
```bash
cd /Users/yzlabmac/agentspace/falagent && bun run generate --status REQUEST_ID --model fal-ai/veo3
cd /Users/yzlabmac/agentspace/falagent && bun run generate --result REQUEST_ID --model fal-ai/veo3
```

## Search Models

```bash
cd /Users/yzlabmac/agentspace/falagent && bun run search --query "flux"
cd /Users/yzlabmac/agentspace/falagent && bun run search --query "video" --category text-to-video
```

## Get Model Schema

```bash
cd /Users/yzlabmac/agentspace/falagent && bun run scripts/get-schema.ts --model fal-ai/flux/dev
```

## Output Format

All scripts output JSON to stdout and status messages to stderr. The JSON result from generate contains:
- For images: `{ "images": [{ "url": "https://...", "content_type": "image/jpeg" }] }`
- For videos: `{ "video": { "url": "https://..." } }`

Always show the user the URL(s) from the result so they can view the generated content.