---
name: qwen-tts
description: Generate speech locally on Apple Silicon using Qwen3-TTS via MLX. Supports custom voices, voice design (describe a voice), and voice cloning. 100% offline, no server needed. Use when the user asks to generate audio, speech, TTS, text-to-speech, voice synthesis, or voice cloning.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sunny-ng-citadel/openclaw-mlx-qwen-tts-skill
# corpus-url: https://github.com/sunny-ng-citadel/openclaw-mlx-qwen-tts-skill/blob/30f6a0154ee7af0f9a069d82aa6eea59b6771c49/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Qwen-TTS

Local text-to-speech using Qwen3-TTS on Apple Silicon via MLX. No server, no API keys, completely offline.

## Requirements

- Apple Silicon Mac (M1 or later)
- Python 3.10+
- macOS 13.5+
- RAM: ~3GB (0.6B models), ~6GB (1.7B models)
- ffmpeg (for voice cloning with non-WAV files): `brew install ffmpeg`

## Installation

```bash
cd /Users/openclaw/.gemini/antigravity/playground/distant-schrodinger
pip install -e .
```

Models auto-download on first use (~3-6GB, cached in `~/.cache/huggingface/hub/`).

## CLI Commands

### Generate with Preset Voice

```bash
qwen-tts-generate \
  --text "Hello world" \
  --output hello.wav \
  --voice Vivian \
  --instruct "Calm and warm" \
  --speed 1.0

# From text file
qwen-tts-generate --text-file speech.txt --output speech.wav

# Fast, lite model
qwen-tts-generate --text "Quick test" --model-size 0.6B --no-play
```

### Generate with Voice Design

```bash
qwen-tts-design \
  --text "Breaking news from the capital" \
  --voice-description "Deep British narrator" \
  --output narrator.wav

qwen-tts-design \
  --text "Once upon a time" \
  --voice-description "Calm bedtime storyteller" \
  --speed 0.8 \
  --output story.wav
```

### Voice Cloning

```bash
qwen-tts-clone \
  --text "Hello, this is a cloned voice" \
  --ref-audio ~/voices/sample.wav \
  --ref-text "the words spoken in the sample" \
  --output cloned.wav
```

## Python API

### Custom Voice (Default)

```python
from qwen_tts import QwenTTS

tts = QwenTTS()  # loads 1.7B custom-voice model
tts.generate(
    text="Hello world",
    output="hello.wav",
    voice="Vivian",
    instruct="Calm and warm",
    speed=1.0,
)
```

### Voice Design

```python
from qwen_tts import QwenTTS

tts = QwenTTS(mode="design")
tts.design(
    text="Welcome to the show",
    output="narrator.wav",
    voice_description="Deep British narrator",
)
```

### Voice Cloning

```python
from qwen_tts import QwenTTS

tts = QwenTTS(mode="base")
tts.clone(
    text="Hello in a cloned voice",
    output="cloned.wav",
    ref_audio="~/voices/sample.wav",
    ref_text="transcript of the sample audio",
)
```

### Lite Model (0.6B, Faster)

```python
tts = QwenTTS(model_size="0.6B")
tts.generate(text="Quick test", output="test.wav", auto_play=False)
```

## Parameters

### CLI Parameters (all commands)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--text` | str | required* | Text to synthesize |
| `--text-file` | str | required* | Path to .txt file with text |
| `--output` / `-o` | str | `output.wav` | Output WAV file path |
| `--model-size` | str | `1.7B` | `1.7B` (best) or `0.6B` (faster) |
| `--speed` | float | `1.0` | Speech speed (0.5-2.0) |
| `--no-play` | flag | false | Skip auto-playing generated audio |
| `--model-path` | str | None | Explicit local model path |

*One of `--text` or `--text-file` is required.

### qwen-tts-generate extras

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--voice` | `Vivian` | Speaker name |
| `--instruct` | `Normal tone` | Emotion/style instruction |

### qwen-tts-design extras

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--voice-description` | required | Natural language voice description |

### qwen-tts-clone extras

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--ref-audio` | required | Path to reference audio (5-10s WAV) |
| `--ref-text` | `""` | Transcript of reference audio |

## Available Voices

| Language | Speakers |
|----------|----------|
| English | Ryan, Aiden, Ethan, Chelsie, Serena, Vivian |
| Chinese | Vivian, Serena, Uncle_Fu, Dylan, Eric |
| Japanese | Ono_Anna |
| Korean | Sohee |

## Models

| Size | RAM | Speed | Quality | HuggingFace Repo |
|------|-----|-------|---------|-------------------|
| 1.7B | ~6GB | Standard | ⭐⭐⭐⭐⭐ | `mlx-community/Qwen3-TTS-12Hz-1.7B-*-8bit` |
| 0.6B | ~3GB | Faster | ⭐⭐⭐⭐ | `mlx-community/Qwen3-TTS-12Hz-0.6B-*-8bit` |

Models download automatically on first use. Cached at `~/.cache/huggingface/hub/`.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `mlx_audio not found` | Package not installed | `pip install -e .` in project dir |
| `Model not found` | First run / download issue | Check internet, re-run (auto-downloads) |
| `ffmpeg not found` | Voice cloning with non-WAV | `brew install ffmpeg` |
| `OutOfMemoryError` | Not enough RAM | Use `--model-size 0.6B` |