---
name: ctf-plat-skills
description: "Use when: detecting target CTF platform type, collecting user credentials, and routing actions to the correct script under scripts/ by platform."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ZianTT/ctf-plat-skills
# corpus-url: https://github.com/ZianTT/ctf-plat-skills/blob/9f3baed5dea66462dce835926407f2492d9db06d/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# CTF Platform Workflow Skill

## Outcome
Produce a reusable automation flow that can:
- Detect target CTF platform type from the target URL/domain using the repository detection script only
- Collect credentials from the user safely
- Route commands to the correct script in `scripts/` based on platform type

## Inputs
- Required:
  - target URL or domain
  - platform credential(s) from the user
- Optional:
  - desired action (`metadata`, `list`, `fetch`, `download`, `start`, `stop`, `renew`, `submit`)
  - action arguments (`challenge_id`, `instance_id`, `flag`)

## Script Routing Map
- `gzctf` -> `python scripts/gzctf.py ...`
- `zerosecone` -> `python scripts/zerosecone.py ...`
- More platforms can be added later by creating new scripts in `scripts/` and extending the routing map.

## Core Workflow
Run from the workspace root.

1. Detect platform type using the repository detection script only. Fix to url format if needed.
```bash
python scripts/detect_platorm.py --url <target_url>
```
Do not infer platform type from manual HTML inspection, browser checks, ad-hoc HTTP probing, or branding heuristics when this script is available.
2. Ask user for required credentials after detection.

3. Save base_url and token (or other credentials) in environment variables or pass as arguments to platform scripts.

4. Route to the matched platform script.
- If detected platform is `gzctf`, call:
```bash
python scripts/gzctf.py list
```
- If detected platform is `zerosecone`, call:
```bash
python scripts/zerosecone.py list
```

5. Execute user-requested action with routed script.
```bash
python scripts/gzctf.py metadata
python scripts/gzctf.py list
python scripts/gzctf.py fetch <challenge_id>
python scripts/gzctf.py download <challenge_id>
python scripts/gzctf.py start <challenge_id>
python scripts/gzctf.py renew <instance_id>
python scripts/gzctf.py stop <instance_id>
python scripts/gzctf.py submit <challenge_id> <flag>
```
```bash
python scripts/zerosecone.py fetch <challenge_id>
python scripts/zerosecone.py download <challenge_id>
python scripts/zerosecone.py start <challenge_id>
python scripts/zerosecone.py renew <instance_id>
python scripts/zerosecone.py submit <challenge_id> <flag>
```

## Environment Variable

- GZCTF_URL: Base URL of the GZCTF platform (e.g. https://target/api/game/1 or https://target/games/1)
- GZCTF_TOKEN: Authentication token for GZCTF API access
- ZEROSECONE_URL: Base URL of the Zerosecone CTF platform (e.g., https://www.aliyunctf.com)
- ZEROSECONE_TOKEN: Authentication token for API access

## Tool Prerequisites

- For websocket challenge environments, `websocat` is required before interaction.
- Install by OS:
  - macOS:
```zsh
brew install websocat
```

or

```zsh
sudo port install websocat
```

  - Linux:

Go https://github.com/vi/websocat/releases Download Pre-built Binary and add to PATH

  - Windows 

Go https://github.com/vi/websocat/releases Download Pre-built Binary and add to PATH

- If installation fails (network/repo/permission issues), stop automated installation and ask the user to install manually from:
```text
https://github.com/vi/websocat
```
- Resume challenge interaction only after `websocat` is available in `PATH`.

## Decision Points
- If platform detection script returns no match:
  - stop and report detection failure
- If challenge environment indicates websocket access:
  - check `websocat` availability first (`command -v websocat`)
  - try installing `websocat` automatically when missing
  - if installation fails, ask user to download/install manually from `https://github.com/vi/websocat`
  - for GZCTF `api/proxy/<uuid>` endpoints, try direct websocket connection first without adding Cookie auth headers
  - in that case, bind the ws/wss endpoint to a local TCP port with `websocat` and probe it with normal TCP/HTTP tools such as `curl` or `nc`
  - continue exploitation through the local bound port once protocol type is identified
- If detected platform has no mapped script:
  - stop and report unsupported platform
- If credentials are missing:
  - prompt user for required fields before running platform script
- If action fails:
  - return API JSON/error details and ask whether to retry, switch action, or stop

## Completion Checks
- Platform type is identified by `scripts/detect_platorm.py`
- For websocket environments, ws/wss endpoint is successfully bound to a local TCP port via `websocat` before exploitation/interaction
- For GZCTF websocket proxy endpoints, direct no-cookie connection is attempted before adding extra headers
- Required credentials are explicitly collected from the user
- Correct script path is selected based on platform type
- Routed command executes and returns parseable output
- On failures, the response includes next-step options (retry/change action/stop)

## Command Patterns
Detection:
```bash
python scripts/detect_platorm.py --url <target_url>
```

GZCTF with env token:
```bash
python scripts/gzctf.py list
```

GZCTF with explicit credentials:
```bash
python scripts/gzctf.py <action> [args]
```

Zerosecone with env token:
```bash
python scripts/zerosecone.py list
```

Zerosecone with explicit credentials:
```bash
python scripts/zerosecone.py --url <target_url> --token "$ZEROSECONE_TOKEN" <action> [args]
```

Websocket environment port binding (required before interaction):
```bash
command -v websocat || <install-websocat-by-os>

websocat tcp-l:127.0.0.1:<local_port> ws://<target_ws_endpoint>
# or
websocat -k tcp-l:127.0.0.1:<local_port> wss://<target_ws_endpoint>
```

Direct GZCTF websocket proxy probe without Cookie:
```bash
printf 'help\n' | websocat -v -k -t -E 'wss://<domain>/api/proxy/<instance_uuid>'
```

If installation fails, ask user to install manually from `https://github.com/vi/websocat` and rerun the binding command.