---
name: fish-tts
description: Text-to-speech using Fish Audio API. Use when user requests audio, voice, TTS, or wants text read aloud. Returns audio file path.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: YanChen0819/fish-tts-skill
# corpus-url: https://github.com/YanChen0819/fish-tts-skill/blob/73e446b36dd1861df3ba3ee149fe6969303fa8c9/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Fish Audio TTS

Generate speech from text using Fish Audio's TTS API.

## Quick Usage

```bash
./scripts/tts.sh "要轉換的文字" [output.mp3]
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FISH_API_KEY` | ✅ | - | Fish Audio API key |
| `FISH_REFERENCE_ID` | ❌ | `0bb80f15ff69492ea36f67174250cdb1` | Voice model ID |
| `FISH_MODEL` | ❌ | `s1` | 模型：`s1` (推薦) 或 `speech-1.6` (備用) |

## Examples

```bash
# 基本用法（使用 s1 模型）
./scripts/tts.sh "你好，我是勞大"

# 指定輸出檔案
./scripts/tts.sh "今天天氣很好" weather.mp3

# 使用舊模型 speech-1.6
FISH_MODEL="speech-1.6" ./scripts/tts.sh "用舊模型說話"

# 使用不同的聲音
FISH_REFERENCE_ID="your-model-id" ./scripts/tts.sh "換個聲音"
```

## Models

| Model | Description |
|-------|-------------|
| `s1` | 最新模型（預設，推薦） |
| `speech-1.6` | 舊版模型（備用，某些聲音效果較好） |

## Output

成功時輸出檔案路徑到 stdout：

```bash
OUTPUT=$(./scripts/tts.sh "測試")
echo "Audio saved to: $OUTPUT"
```

## Limitations

- 輸出格式為 MP3
- 需要有效的 FISH_API_KEY