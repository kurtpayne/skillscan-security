---
name: termux-telephony
description: Send SMS and make phone calls via a Termux device. Use when the user wants to send text messages or initiate calls through their Android phone running Termux. Requires setting up the Termux HTTP server.
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["curl","jq"]}}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: zivyuan/termux-telephony
# corpus-url: https://github.com/zivyuan/termux-telephony/blob/e7f4540a126edfee108c002e1a6a3537ef2f6176/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Termux Telephony

Send SMS and make phone calls through an Android device running Termux.

## Architecture

```
OpenClaw  ──HTTP──>  Termux Device (Python server)  ──termux-api──>  Android
```

The skill works by running a small HTTP server on your Termux device. OpenClaw sends requests to this server, which then calls `termux-sms-send` or `termux-telephony-call`.

## Setup

### 1. Termux Device Setup

Install required packages on your Termux device:

```bash
pkg update && pkg install python termux-api
```

Grant Android permissions (required once):

```bash
# For SMS
termux-sms-send -h  # will prompt for SMS permission

# For phone calls
termux-telephony-call -h  # will prompt for phone permission
```

### 2. Copy Server to Termux

Copy `termux-server/server.py` to your Termux device:

```bash
# On your Termux device
mkdir -p ~/telephony-server
```

Then transfer the file (via scp, adb, or copy-paste).

### 3. Configure Connection

Create `~/.config/termux-telephony/config.json` on the OpenClaw machine:

```json
{
  "url": "http://192.168.1.100:8765",
  "token": "your-secret-token-here"
}
```

Replace the URL with your Termux device's IP address.

### 4. Start the Server (on Termux)

```bash
python ~/telephony-server/server.py
# Or with custom options:
python ~/telephony-server/server.py --port 8765 --token your-secret-token-here
```

## Usage

### Send SMS

```bash
termux-api.sh sms +1234567890 "Hello from OpenClaw!"
```

### Make a Call

```bash
termux-api.sh call +1234567890
```

### Check Server Status

```bash
termux-api.sh status
```

## CLI Reference

```bash
# Send SMS
termux-api.sh sms <phone_number> <message>

# Make phone call
termux-api.sh call <phone_number>

# Check server status
termux-api.sh status

# List recent SMS (if supported)
termux-api.sh list-sms [--limit 10]
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TERMUX_URL` | Termux server URL | From config file |
| `TERMUX_TOKEN` | Authentication token | From config file |
| `TERMUX_CONFIG` | Config file path | `~/.config/termux-telephony/config.json` |

## Troubleshooting

### Connection Refused

- Ensure the server is running on Termux
- Check the IP address and port
- Verify firewall allows the connection

### Permission Denied

- Run `termux-sms-send -h` and grant SMS permission
- Run `termux-telephony-call -h` and grant phone permission

### Token Authentication Failed

- Ensure the token matches between server and client
- Check for typos in config file

### Server Not Responding

- Check if Python server is running: `ps aux | grep python`
- Check server logs for errors
- Verify port is not in use: `netstat -tlnp | grep 8765`

## Security Notes

- The token is sent in cleartext over HTTP. Use only on trusted networks.
- For better security, consider using SSH tunneling or VPN.
- Keep your token secret and rotate it periodically.

## Termux Server Options

```bash
python server.py --help

Options:
  --port PORT      Server port (default: 8765)
  --token TOKEN    Authentication token (required)
  --host HOST      Bind address (default: 0.0.0.0)
  --log-level      Logging level: debug, info, warn (default: info)
```

## API Reference

See [references/api.md](references/api.md) for HTTP API details.