---
name: cyber-horn
description: Turn text into spoken Feishu (Lark) voice messages. Use when the agent should speak in a Feishu group, send voice alerts or announcements, or reply with a playable voice note instead of text.
metadata:
  {"openclaw": {"emoji": "🔊", "requires": {"env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET"], "bins": ["ffmpeg"]}, "primaryEnv": "FEISHU_APP_ID", "os": ["linux", "darwin", "win32"]}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Richerlv/cyber-horn
# corpus-url: https://github.com/Richerlv/cyber-horn/blob/4226a7e668035de4f567f148383c2c790642af61/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# CyberHorn (赛博小喇叭)

Let OpenClaw **speak** in Feishu: turn any text into a **native voice message** (not a file link) in a Feishu chat.

## When to use

- The user asks to "say something in Feishu" or "send a voice message to the group".
- The agent should announce or alert via voice in a Feishu room.
- You want replies as playable voice notes instead of text bubbles.

## How it works

1. **TTS** — Text is synthesized with **Edge TTS** (default, no API key) or **ElevenLabs** (custom voices). Set `TTS_PROVIDER=EDGE` or `ELEVEN` in `.env`.
2. **Encode** — Audio is converted to Opus (mono 16 kHz) via FFmpeg for Feishu’s voice message format.
3. **Send** — The file is uploaded to Feishu and sent as a voice message to the given chat.

## Setup

- **Required (all modes):** `FEISHU_APP_ID`, `FEISHU_APP_SECRET` in `.env` or OpenClaw config. **FFmpeg** must be on `PATH` or set `FFMPEG_PATH`.
- **Edge TTS (default):** No extra keys. Optional `EDGE_VOICE` (e.g. `zh-CN-XiaoxiaoNeural`).
- **ElevenLabs:** Set `TTS_PROVIDER=ELEVEN`, and add `ELEVEN_API_KEY`, `VOICE_ID`.

## Invocation

From the skill directory (or with `PYTHONPATH` set):

```bash
python main.py "<text to speak>" "<feishu_chat_id>" [receive_id_type]
```

- **Arg 1:** Text to speak.
- **Arg 2:** Feishu chat ID (or other `receive_id`).
- **Arg 3 (optional):** `receive_id_type`, default `chat_id` (can be `open_id` etc. per Feishu API).

OpenClaw can call this with env vars injected and the same two (or three) arguments.