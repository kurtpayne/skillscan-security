---
name: youtube-scraper
description: Given a YouTube URL, verify login via OpenClaw browser, scrape full video metadata (title, video ID, thumbnail, publish date, view count, like count, channel name, subscriber count, channel country/region), then download subtitles using a fallback chain — creator-uploaded subtitles first, then auto-generated subtitles, then Whisper local transcription from downloaded audio if subtitles are disabled.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"bins": ["yt-dlp", "python3"], "anyBins": ["whisper", "whisper-ctranslate2"]}, "install": [{"id": "brew-yt-dlp", "kind": "brew", "formula": "yt-dlp", "bins": ["yt-dlp"], "label": "Install yt-dlp (brew)"}]}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: LUKELEE-OneOnOne/youtube-scraper-openclaw
# corpus-url: https://github.com/LUKELEE-OneOnOne/youtube-scraper-openclaw/blob/0af5e2e4ab9e68e3b4fe96aac426d17993ec551b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# YouTube Scraper & Subtitle Downloader

Scrape full YouTube video metadata and download subtitles. Verifies YouTube login via the OpenClaw browser before proceeding.

Supports two browser modes, detected automatically in priority order:
- **Mode A (preferred)**: OpenClaw managed Chromium (`--browser-profile openclaw`)
- **Mode B (fallback)**: Chrome Extension Relay using the user's existing Chrome (`--browser-profile chrome`)

## Prerequisites

- `yt-dlp`: `brew install yt-dlp`
- `youtube-transcript-api`: `pip install youtube-transcript-api`
- `whisper` (optional, last-resort fallback): `pip install openai-whisper` + `brew install ffmpeg`
- User must be logged into YouTube via one of the browser modes above

---

## Step 0 — Detect Available Browser Mode

Before doing anything, determine which browser mode is available:

```bash
# Check if the managed Chromium profile is available
openclaw browser --browser-profile openclaw status --json 2>/dev/null
```

- If response contains `"running": true` or the browser starts successfully → **use Mode A (`openclaw` profile)**
- If the command errors or returns unavailable → **use Mode B (`chrome` extension relay)**

Store the result as `BROWSER_MODE` (value: `openclaw` or `chrome`). Use this value for all subsequent `--browser-profile` flags.

---

## Step 1 — Start Browser and Verify YouTube Login

### Mode A: OpenClaw Managed Chromium

```bash
# Start the managed browser
openclaw browser --browser-profile openclaw start 2>/dev/null || true

# Navigate to YouTube
openclaw browser --browser-profile openclaw open "https://www.youtube.com"
```

Wait ~3 seconds for the page to load, then take a snapshot:

```bash
openclaw browser --browser-profile openclaw snapshot
```

### Mode B: Chrome Extension Relay

The extension relay does not attach to tabs automatically — the user must do this manually:

1. Open `https://www.youtube.com` in Chrome and make sure you are logged in
2. Click the **OpenClaw Browser Relay** extension icon in the toolbar and wait for the badge to show **ON**
3. Once the badge shows ON, tell the agent to continue

After the tab is attached, take a snapshot:

```bash
openclaw browser --browser-profile chrome snapshot
```

---

### Login Verification (both modes)

In the snapshot, look for any of the following signs of a logged-in session:
- Account avatar button (`#avatar-btn`)
- Account menu icon
- User channel link

**If no login indicator is found:**
- Mode A: Stop and tell the user to visit youtube.com in the OpenClaw managed browser and log in, then retry.
- Mode B: Stop and tell the user to log into YouTube in Chrome first, then click the extension icon to attach the tab, then retry.

---

## Step 2 — Parse Video ID and Set Working Directory

Extract the Video ID from the URL:

| URL format | Video ID location |
|-----------|------------------|
| `https://www.youtube.com/watch?v=VIDEO_ID` | `v=` query parameter |
| `https://youtu.be/VIDEO_ID` | path segment |
| `https://www.youtube.com/shorts/VIDEO_ID` | after `/shorts/` |

```bash
VIDEO_ID="<ID parsed from URL>"
OUTPUT_DIR="/tmp/youtube-${VIDEO_ID}"
mkdir -p "${OUTPUT_DIR}"
echo "Working directory: ${OUTPUT_DIR}"
```

---

## Step 3 — Obtain YouTube Cookies for yt-dlp

Cookie handling differs between the two browser modes.

---

### Mode A: OpenClaw Managed Chromium → Export via API

The managed Chromium runs in an isolated profile. `yt-dlp --cookies-from-browser` cannot read it directly. Export cookies manually and convert to Netscape format:

```bash
# Export YouTube-related cookies from the managed browser (JSON)
openclaw browser --browser-profile openclaw cookies --json > /tmp/yt-cookies-raw.json
```

Convert JSON to the Netscape format yt-dlp expects:

```bash
python3 - <<'PYEOF'
import json

with open('/tmp/yt-cookies-raw.json') as f:
    cookies = json.load(f)

yt_domains = ['.youtube.com', 'youtube.com', '.google.com', 'google.com']
yt_cookies = [c for c in cookies if any(
    c.get('domain','').endswith(d.lstrip('.')) or c.get('domain','') == d
    for d in yt_domains
)]

with open('/tmp/yt-cookies.txt', 'w') as f:
    f.write('# Netscape HTTP Cookie File\n')
    for c in yt_cookies:
        domain = c.get('domain', '')
        flag   = 'TRUE' if domain.startswith('.') else 'FALSE'
        path   = c.get('path', '/')
        secure = 'TRUE' if c.get('secure', False) else 'FALSE'
        expiry = str(int(c.get('expires', 0) or 0))
        name   = c.get('name', '')
        value  = c.get('value', '')
        f.write(f'{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n')

print(f'Exported {len(yt_cookies)} YouTube cookies → /tmp/yt-cookies.txt')
PYEOF
```

Verify the file has more than 1 line (header only = not logged in):

```bash
wc -l /tmp/yt-cookies.txt
```

If only 1 line, the session is missing or expired. Return to Step 1 and re-confirm login.

All subsequent yt-dlp commands use: `--cookies /tmp/yt-cookies.txt`

---

### Mode B: Chrome Extension Relay → yt-dlp reads system Chrome directly

The user is logged into YouTube via their normal Chrome. yt-dlp can read Chrome's local cookie database directly — no export step needed:

```bash
# Standard Chrome on macOS (most common)
yt-dlp --cookies-from-browser chrome ...

# Brave
yt-dlp --cookies-from-browser brave ...

# Edge
yt-dlp --cookies-from-browser edge ...
```

> yt-dlp handles Chrome Keychain encryption on macOS automatically. Chrome does not need to be closed.

All subsequent yt-dlp commands use: `--cookies-from-browser chrome` (or whichever browser applies)

If direct reading fails (permissions error or decryption issue), fall back to exporting via the extension relay:

```bash
# The extension relay also supports cookies --json (requires an attached tab)
openclaw browser --browser-profile chrome cookies --json > /tmp/yt-cookies-raw.json
# Then run the same Python conversion script as Mode A
```

---

## Step 4 — Scrape Video Metadata

Set the cookie argument based on `BROWSER_MODE` from Step 0:

```bash
# Mode A
COOKIE_ARG="--cookies /tmp/yt-cookies.txt"

# Mode B
COOKIE_ARG="--cookies-from-browser chrome"
```

```bash
yt-dlp \
  ${COOKIE_ARG} \
  --write-thumbnail \
  --convert-thumbnails jpg \
  --skip-download \
  --print-json \
  "https://www.youtube.com/watch?v=${VIDEO_ID}" \
  -o "${OUTPUT_DIR}/%(title)s.%(ext)s" \
  2>&1 | tee /tmp/yt-meta-${VIDEO_ID}.json | tail -1
```

Extract the following fields from the JSON output:

| Field | yt-dlp key | Notes |
|-------|-----------|-------|
| Video ID | `id` | |
| Title | `title` | |
| Publish date | `upload_date` | YYYYMMDD → reformat to YYYY-MM-DD |
| View count | `view_count` | |
| Like count | `like_count` | null if hidden |
| Channel name | `channel` | |
| Subscriber count | `channel_follower_count` | |
| Channel country/region | `uploader_country` | may be null, see below |
| Channel URL | `channel_url` | |
| Duration | `duration_string` | |
| Thumbnail URL | `thumbnail` | |
| Thumbnail local path | `.jpg` file in `OUTPUT_DIR` | |

### Supplemental: scrape channel country when `uploader_country` is null

Navigate to the channel's About page using the OpenClaw browser:

```bash
# Extract channel_id from the saved JSON
CHANNEL_ID=$(python3 -c "import json; d=json.load(open('/tmp/yt-meta-${VIDEO_ID}.json')); print(d.get('channel_id',''))")

openclaw browser --browser-profile ${BROWSER_MODE} open "https://www.youtube.com/channel/${CHANNEL_ID}/about"
```

After the page loads, take a snapshot. Look for the location field in the About section, or extract it via JavaScript:

```bash
openclaw browser --browser-profile ${BROWSER_MODE} evaluate \
  --fn "() => {
    const items = document.querySelectorAll('yt-description-preview-view-model, #details-container, .ytd-channel-about-metadata-renderer');
    for (const el of items) {
      const text = el.textContent;
      if (text && text.length < 50) return text.trim();
    }
    return null;
  }" \
  --target-id <TARGET_ID_FROM_SNAPSHOT>
```

---

## Step 5 — Download Subtitles (Three-Level Fallback Chain)

### Method A: youtube-transcript-api (preferred — fastest, no download required)

Fetches directly from YouTube's internal API without downloading the video:

```bash
# List available subtitle tracks
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
try:
    tl = YouTubeTranscriptApi.list_transcripts('${VIDEO_ID}')
    for t in tl:
        kind = 'auto' if t.is_generated else 'manual'
        print(f'{kind} | {t.language_code} | {t.language}')
except TranscriptsDisabled:
    print('DISABLED')
except Exception as e:
    print(f'ERROR: {e}')
"
```

If output is `DISABLED` → **skip directly to Method C (Whisper)**.

Otherwise, try creator-uploaded subtitles first, then fall back to auto-generated:

```bash
python3 - <<'PYEOF'
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import SRTFormatter
import os

video_id  = os.environ.get('VIDEO_ID', '')
output_dir = os.environ.get('OUTPUT_DIR', '/tmp')
prefer_langs = ['zh-Hans', 'zh-Hant', 'en', 'en-US', 'ja', 'ko']

try:
    tl = YouTubeTranscriptApi.list_transcripts(video_id)

    transcript = None
    source = ''

    # Prefer creator-uploaded subtitles
    for lang in prefer_langs:
        try:
            transcript = tl.find_manually_created_transcript([lang])
            source = f'creator-uploaded ({lang})'
            break
        except NoTranscriptFound:
            continue

    # Fall back to auto-generated subtitles
    if not transcript:
        for lang in prefer_langs:
            try:
                transcript = tl.find_generated_transcript([lang])
                source = f'auto-generated ({lang})'
                break
            except NoTranscriptFound:
                continue

    # Last resort: any available track
    if not transcript:
        transcript = next(iter(tl))
        source = f'available ({transcript.language_code})'

    data = transcript.fetch()
    srt_content = SRTFormatter().format_transcript(data)

    out_path = os.path.join(output_dir, f'subtitle_{video_id}.srt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    print(f'SUCCESS|{source}|{out_path}')

except TranscriptsDisabled:
    print('DISABLED')
except Exception as e:
    print(f'ERROR|{e}')
PYEOF
```

Run with environment variables:

```bash
VIDEO_ID="${VIDEO_ID}" OUTPUT_DIR="${OUTPUT_DIR}" python3 <above script>
```

- Output starts with `SUCCESS` → **go to Step 6**, note the source (creator-uploaded or auto-generated)
- Output is `DISABLED` → **go to Method C**
- Output starts with `ERROR` → **try Method B**

---

### Method B: yt-dlp subtitle download (fallback when transcript-api fails)

```bash
# Try creator-uploaded subtitles first (${COOKIE_ARG} set in Step 4)
yt-dlp \
  ${COOKIE_ARG} \
  --write-subs \
  --no-write-auto-subs \
  --sub-langs "zh-Hans,zh-Hant,en,en-US,ja,ko" \
  --sub-format "srt/vtt/best" \
  --skip-download \
  "https://www.youtube.com/watch?v=${VIDEO_ID}" \
  -o "${OUTPUT_DIR}/%(title)s.%(ext)s"

ls "${OUTPUT_DIR}"/*.srt "${OUTPUT_DIR}"/*.vtt 2>/dev/null && echo "MANUAL_SUCCESS" || echo "MANUAL_FAILED"
```

If `MANUAL_FAILED`, try auto-generated subtitles:

```bash
yt-dlp \
  ${COOKIE_ARG} \
  --write-auto-subs \
  --no-write-subs \
  --sub-langs "zh-Hans,zh-Hant,en,en-US,ja,ko" \
  --sub-format "srt/vtt/best" \
  --skip-download \
  "https://www.youtube.com/watch?v=${VIDEO_ID}" \
  -o "${OUTPUT_DIR}/%(title)s.%(ext)s"

ls "${OUTPUT_DIR}"/*.srt "${OUTPUT_DIR}"/*.vtt 2>/dev/null && echo "AUTO_SUCCESS" || echo "AUTO_FAILED"
```

If a file is produced → **go to Step 6**.
If still failing → **continue to Method C**.

---

### Method C: Whisper local transcription (last resort — subtitles fully disabled)

```bash
# 1. Download best available audio (prefer m4a)
yt-dlp \
  ${COOKIE_ARG} \
  -f "bestaudio[ext=m4a]/bestaudio/best" \
  "https://www.youtube.com/watch?v=${VIDEO_ID}" \
  -o "${OUTPUT_DIR}/audio.%(ext)s"

# 2. Locate the downloaded audio file
AUDIO_FILE=$(ls "${OUTPUT_DIR}"/audio.* 2>/dev/null | head -1)
echo "Audio file: ${AUDIO_FILE}"

# 3. Transcribe with Whisper
# Model size trade-off: tiny (fast) → base → small → medium → large (accurate)
# Use small for short videos; medium or large for long videos or when accuracy matters
whisper "${AUDIO_FILE}" \
  --model small \
  --language auto \
  --output_format srt \
  --output_dir "${OUTPUT_DIR}"
```

Check that the `.srt` file was produced:

```bash
ls "${OUTPUT_DIR}"/*.srt 2>/dev/null && echo "WHISPER_SUCCESS" || echo "WHISPER_FAILED"
```

---

## Step 6 — Compile and Return Results

Return a structured summary to the user:

```
════════════════════════════════════════
📹  Video Info
────────────────────────────────────────
Title          : [title]
Video ID       : [id]
Published      : [upload_date → YYYY-MM-DD]
Duration       : [duration_string]

📊  Stats
────────────────────────────────────────
Views          : [view_count]
Likes          : [like_count or "hidden"]

📺  Channel
────────────────────────────────────────
Channel name   : [channel]
Subscribers    : [channel_follower_count]
Country/Region : [uploader_country or scraped from About page]
Channel URL    : [channel_url]

📁  Local Files
────────────────────────────────────────
Thumbnail      : [OUTPUT_DIR]/[title].jpg
Subtitle file  : [OUTPUT_DIR]/subtitle_*.srt
Subtitle source: creator-uploaded / auto-generated / Whisper transcription
════════════════════════════════════════
```

---

## Troubleshooting

### Mode A: yt-dlp still reports not logged in after cookie export

Revisit YouTube in the OpenClaw managed browser to refresh the session, then re-run Step 3 to re-export cookies.

### Mode B: `--cookies-from-browser chrome` fails

Chrome's cookie database on macOS is encrypted with Keychain. If you see a permissions error:
1. Grant Chrome "Full Disk Access" in System Settings → Privacy & Security
2. Or fall back to the extension relay export: `openclaw browser --browser-profile chrome cookies --json > /tmp/yt-cookies-raw.json`, then run the same Python conversion script as Mode A

### Chrome extension badge shows `!`

The relay server is unreachable, meaning the OpenClaw Gateway is not running on this machine. Start the Gateway and the extension will reconnect automatically.

### youtube-transcript-api blocked when using a proxy

YouTube blocks known datacenter IPs. Running locally without a proxy is not affected. Disable the proxy temporarily and retry.

### Whisper is slow on first run

The model weights are downloaded automatically on first use (small ≈ 244 MB, medium ≈ 769 MB) and cached at `~/.cache/whisper/`. Subsequent runs use the cache.

### Video is members-only content

Ensure the account logged in via the browser holds the required membership. The exported cookies will carry the membership credentials to yt-dlp.