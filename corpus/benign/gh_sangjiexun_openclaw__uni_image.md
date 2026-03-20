---
name: uni-image
description: Unified multi-platform AI image generation. Supports Volcengine Seedream, Alibaba Qwen Image, and Google Gemini (Nano Banana). Switch between models with a dropdown selector.
homepage: https://github.com/sangjiexun/openclaw-skill-UniImage
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires":
          {
            "env":
              [
                "ARK_API_KEY",
                "DASHSCOPE_IMAGE_KEY",
                "GOOGLE_API_KEY",
              ],
          },
        "primaryEnv": "ARK_API_KEY",
      },
  }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sangjiexun/openclaw-skill-UniImage
# corpus-url: https://github.com/sangjiexun/openclaw-skill-UniImage/blob/30a40584ab2843a079d860a05683b7f64088c8b1/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# UniImage — 统一多平台 AI 图片生成

Multi-platform AI image generation skill for OpenClaw. Supports switching between providers via a dropdown model selector on the paint page.

## Supported Platforms

| Model ID | Display Name | Provider | Description |
|----------|-------------|----------|-------------|
| `doubao-seedream-5-0-260128` | Seedream 5.0 | Volcengine Ark | 多角色超强一致性，中文处理能力极强 |
| `qwen-image-plus` | Qwen Image | Alibaba DashScope | 单图一致性强，适合中文相关的多图处理场景 |
| `gemini-3-pro-image-preview` | 香蕉 Pro | Google Gemini | 最强修图模型，适合电商和专业设计 |
| `gemini-3.1-flash-image-preview` | 香蕉 V2 | Google Gemini | 最新香蕉模型，极致速度和超高性价比 |

## Architecture

```
Renderer (paint page)
  ↓  fetch(/v1/images/generations)
  ↓  [fetch interceptor rewrites URL + model]
UniImage Proxy (port 18800)
  ├── Volcengine Ark API (Seedream)
  ├── DashScope API (Qwen Image, async poll)
  └── Google Gemini API (Nano Banana)
```

## Files

- `uni-image-proxy.js` — HTTP proxy server with multi-provider routing
- `uni-image-inject.js` — Renderer injection script (fetch wrapper + model selector UI)
- `SKILL.md` — This skill manifest

## Configuration

Configure API keys via the 🔑 button on the paint page, or set environment variables:

```bash
# Volcengine Ark (Seedream)
ARK_API_KEY=your-volcengine-key

# Alibaba DashScope (Qwen Image)
DASHSCOPE_IMAGE_KEY=your-dashscope-key

# Google AI (Nano Banana / Gemini)
GOOGLE_API_KEY=your-google-api-key
```

Keys are stored in `~/.openclaw-dev/uni-image-config.json`.

## Usage

1. Navigate to the **绘画助手** (Paint) page
2. Select a model from the **模型平台** dropdown
3. Click **🔑** to configure the API key for the selected provider
4. Enter a prompt and generate images

## Run (CLI)

```bash
# Seedream (default)
node uni-image-proxy.js &
curl -X POST http://127.0.0.1:18800/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{"model":"doubao-seedream-5-0-260128","prompt":"a cute cat","size":"1024x1024"}'

# Qwen Image
curl -X POST http://127.0.0.1:18800/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen-image-plus","prompt":"a cute cat","size":"1024*1024"}'

# Google Gemini (Nano Banana)
curl -X POST http://127.0.0.1:18800/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini-3.1-flash-image-preview","prompt":"a cute cat"}'
```