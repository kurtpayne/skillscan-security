---
name: send-video-message
description: Send the user a video message with an AI avatar that speaks any text, using Runway Character API. For async updates, explanations, or anything better said than typed.
user-invocable: true
metadata: {"openclaw":{"emoji":"🎬","requires":{"env":["RUNWAY_API_SECRET"],"bins":["uv"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}],"primaryEnv":"RUNWAY_API_SECRET","source":"https://docs.dev.runwayml.com","repository":"https://github.com/runwayml/openclaw-skill-send-video-message"}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: runwayml/openclaw-skill-send-video-message
# corpus-url: https://github.com/runwayml/openclaw-skill-send-video-message/blob/078aa119d73755538c150e8086afe37aa5ab84bb/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Send Video Message

Send the user a video message where an AI avatar speaks your words — lip-synced with natural motion. Use this for async updates, code review walkthroughs, incident summaries, or anything that's better explained with a face than a wall of text.

## Privacy & Data Handling

- **Runway API**: Only data you explicitly pass (spoken text, avatar image) is sent to Runway ([dev.runwayml.com](https://dev.runwayml.com)). Nothing is uploaded automatically. Custom avatars can be deleted anytime via `DELETE /v1/avatars/{id}`.
- **Output**: Generated videos are saved to `/tmp` and sent via `MEDIA:` for OpenClaw to auto-attach.

## Setup

### Get a Runway API Key

1. Go to [dev.runwayml.com](https://dev.runwayml.com)
2. Create an account and get an API key
3. Set it: `export RUNWAY_API_SECRET=your_key`

## One-Time Setup: Create Your Avatar

Before generating videos, create an avatar. **You only need to do this once** — the avatar ID is saved and reused for all future videos.

What matters is the **face image** — pick a character image that matches your personality. The voice is chosen later when generating each video.

### Step 1: Pick a face image

Choose one of these character images (or provide your own). **Default recommendation: Openclaw Lobster 2.**

- **Openclaw Lobster 2 (recommended)**: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/openclaw-lobster2.jpg`
- Openclaw Lobster 1: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/openclaw-lobster1.jpg`
- Cat: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/cat.png`
- Alien man, candy texture: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/alien-man-candy-texture.jpg`
- Alien woman, candy texture: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/alien-woman-candy-texture.jpg`
- Old man, long beard, game style: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/old-man-long-beard-game-style.png`
- Blond guy, blue sweater: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/blond-guy-blue-sweater.png`
- Man, 3D animation: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/man-3d-animation-style.png`
- Girl in airport, 3D: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/3d-animated-girl-in-airport.png`
- White furry monster: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/white-furry-monster.png`
- Superstar young woman: `https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/woman-music-superstar.png`

Or generate one from a text description — the image should be **a character facing the camera directly, head and shoulders, centered**. Be bold and creative:
- **Warm / friendly** → soft 3D animation, Pixar-style, watercolor
- **Sharp / professional** → clean illustration, stylized portrait, low-poly
- **Chaotic / playful** → candy texture, claymation, puppet, pop art
- **Cute / wholesome** → chibi, plush toy, animal character, kawaii

### Step 2: Create the avatar

**With a preset image:**

```bash
uv run {baseDir}/scripts/setup_avatar.py \
  --name "Mochi" \
  --image-url "https://runway-static-assets.s3.us-east-1.amazonaws.com/calliope-demo/agent-avatars-presets/cat.png"
```

**With a text description (generates the image):**

```bash
uv run {baseDir}/scripts/setup_avatar.py \
  --name "Mochi" \
  --description "A cute fluffy white cartoon creature with large expressive eyes, looking directly at the viewer, 3D animation style, head and shoulders, neutral background"
```

**With your own image URL:**

```bash
uv run {baseDir}/scripts/setup_avatar.py \
  --name "Mochi" \
  --image-url "https://example.com/avatar.jpg"
```

The setup script prints the avatar ID and saves it to `~/.openclaw/runway-avatar.json`. Future `generate_video.py` calls use it automatically. **Save the avatar ID — reuse it for all videos. Do NOT create a new avatar each time.**

## Generate a Video Message

Write what you want to say, pick a voice that matches your avatar image, and the avatar will speak it with lip-synced animation. **Always pass `--voice`** — choose one that fits the character's appearance (e.g. a female avatar should use a female voice, an authoritative-looking character should use a deeper voice).

```bash
uv run {baseDir}/scripts/generate_video.py \
  --text "Hey Alex — quick update on the deploy. Everything went through, all tests passing. The memory fix from your PR cut p99 latency by 40 percent. Nice work." \
  --voice "Maya"
```

### Available TTS voices

Pass `--voice <name>` to `generate_video.py` (default: `Maya`):

| ID | Gender | Style | Pitch |
|----|--------|-------|-------|
| `Maya` | Woman | Upbeat | Higher |
| `Arjun` | Man | Clear | Middle |
| `Serene` | Woman | Calm | Middle |
| `Bernard` | Man | Authoritative | Lower |
| `Billy` | Man | Casual | Middle |
| `Mark` | Man | Neutral | Middle |
| `Clint` | Man | Gravelly | Lower |
| `Mabel` | Woman | Warm | Middle |
| `Chad` | Man | Energetic | Middle |
| `Leslie` | Woman | Friendly | Middle |
| `Eleanor` | Woman | Mature | Middle |
| `Elias` | Man | Smooth | Lower-middle |
| `Elliot` | Man | Even | Middle |
| `Noah` | Man | Relaxed | Lower-middle |
| `Rachel` | Woman | Clear | Middle |
| `James` | Man | Firm | Lower |
| `Katie` | Woman | Bright | Higher |
| `Tom` | Man | Casual | Middle |
| `Wanda` | Woman | Warm | Middle |
| `Benjamin` | Man | Professional | Lower-middle |

With a specific avatar ID (overrides saved default):

```bash
uv run {baseDir}/scripts/generate_video.py --text "Morning standup recap..." --avatar-id "550e8400-e29b-41d4-a716-446655440000"
```

**Fallback — preset avatar (no setup, but less fun):**

If you haven't created a custom avatar yet and need to send a video immediately, you can use a Runway preset:

```bash
uv run {baseDir}/scripts/generate_video.py \
  --text "Quick heads up about the deploy." \
  --preset-id "game-character"
```

Available preset IDs: `game-character`, `game-character-man`, `music-superstar`, `cat-character`, `influencer`, `tennis-coach`, `human-resource`, `fashion-designer`, `cooking-teacher`

### Script output

The script outputs:
1. Progress updates as it generates speech and video
2. `Video saved: /tmp/runway-avatar-YYYY-MM-DD-HH-MM-SS.mp4`
3. `MEDIA: /tmp/runway-avatar-...mp4` — OpenClaw auto-attaches this to the user's chat

**Do not read the video file back** — just report the path and let OpenClaw handle delivery.

## When to Use Video Messages

Use video messages for async communication that benefits from a face:

- **Deploy updates**: "Your deploy went through, here's what changed"
- **Code review feedback**: Walk through a PR with visual explanation
- **Incident summaries**: Recap what happened and what was fixed
- **Progress updates**: End-of-day or weekly recap
- **Onboarding**: Explain a codebase concept or architecture decision
- **Celebrations**: "Your PR just hit 1000 users — nice work!"

Use a **video call** (not a video message) for things that need real-time back-and-forth.

## Complete Example: Deploy Notification

1. Agent detects a successful deploy
2. Agent composes what to say: "Hey Alex — deploy went through. 3 PRs merged: the auth refactor, the cart fix, and your memory optimization. All tests green. P99 latency dropped 40 percent after your fix. Nice work."
3. Generates the video:
   ```
   uv run {baseDir}/scripts/generate_video.py --text "Hey Alex — deploy went through..." --preset-id "game-character" --voice "Maya"
   ```
4. Sends the video to the user with a text summary:
   > Your deploy just went through. Here's a quick video recap:
   > [attached video]

## Notes

- Video generation takes 10-60 seconds depending on text length.
- Maximum text length is ~300 seconds of speech (~5 minutes).
- The `MEDIA:` output line tells OpenClaw to auto-attach the video file.
- Videos are saved to `/tmp` — they persist until the system clears temp files.