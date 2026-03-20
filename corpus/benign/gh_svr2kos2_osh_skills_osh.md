---
name: osh
description: Control remote devices via OSH (OpenClaw Remote Bridge). Execute shell commands on remote Windows/Linux/macOS machines through WebSocket tunneling, bypassing NAT without port forwarding.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: svr2kos2/osh-skills
# corpus-url: https://github.com/svr2kos2/osh-skills/blob/4700ce87f513c2e03ac32b6cb5418e8fdaf05e7f/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Open Shell (OSH) - OpenClaw Remote Bridge

This skill enables remote command execution on devices behind NAT. The AI agent interacts only with **osh-cli** tools (`osh`, `osh-admin`).

## Scope for AI Agent

The agent **only uses** the CLI tools `osh` and `osh-admin` on the VPS. The relay and daemon must already be running, but are **not** operated by the agent.

## CLI Commands

### Remote Command Execution

```bash
# Execute a command on a remote device (non-PTY mode, recommended)
osh <device_id|alias> "<command>"

# Execute in PTY mode (for interactive programs)
osh <device_id|alias> "<command>" --pty

# Examples:
osh mypc "Get-Process"                    # Use device alias
osh mypc "Get-ChildItem C:\Users"         # List files on Windows
osh linuxsrv "ls -la /home"               # List files on Linux
osh 550e8400 "python --version"           # Use device_id prefix

# Interactive examples (PTY mode)
osh mypc "python" --pty                   # Interactive Python REPL
osh linuxsrv "vim file.txt" --pty         # Interactive editor
```

### Execution Modes

| Mode | Flag | Use Case |
|------|------|----------|
| **Non-PTY** | (default) | Simple commands, scripts, one-shot execution |
| **PTY** | `--pty` | Interactive programs (Python REPL, editors, shells) |

**Non-PTY mode** (default):
- Uses simple process execution with stdout/stderr capture
- Clean output without terminal control sequences
- Faster for simple commands
- No interactive input support

**PTY mode** (`--pty`):
- Creates a pseudo-terminal for the remote process
- Supports interactive programs (REPL, editors)
- Raw keyboard input (key-by-key transmission)
- Control sequences are escaped for visibility (debugging)

### Device Management (osh-admin)

```bash
# List all devices and their status
osh-admin list

# Approve a pending device
osh-admin approve <device_id|alias>

# Reject a device
osh-admin reject <device_id|alias>

# Set device alias
osh-admin alias <device_id> <alias>

# Remove a device
osh-admin remove <device_id|alias>

# Reload configuration (after approve/reject)
osh-admin reload
```

## Device Status

| Status | Description |
|--------|-------------|
| `pending` | Waiting for admin approval |
| `approved` | Can receive and execute commands |
| `rejected` | Blocked from connecting |

## Platform-Specific Commands

When executing commands, use platform-appropriate syntax:

### Windows (PowerShell)
```bash
osh mypc "Get-ChildItem"                    # List files
osh mypc "Get-Content file.txt"             # Read file
osh mypc "Set-Content -Path f.txt -Value 'hello'"  # Write file
osh mypc "Get-Process | Select-Object -First 10"   # Process list
```

### Linux/macOS (bash)
```bash
osh linuxsrv "ls -la"                       # List files
osh linuxsrv "cat /etc/hostname"            # Read file
osh linuxsrv "echo 'hello' > file.txt"      # Write file
osh linuxsrv "ps aux | head -10"            # Process list
```

## Workflow Example

1. **Check available devices:**
   ```bash
   osh-admin list
   ```

2. **Approve a new device (if pending):**
   ```bash
   osh-admin approve <device_id>
   osh-admin alias <device_id> mypc
   osh-admin reload
   ```

3. **Execute commands:**
   ```bash
   osh mypc "pwd"
   osh mypc "Get-ChildItem"
   ```

## Notes

- **Default mode**: Non-PTY execution for simple commands (clean output)
- **PTY mode** (`--pty`): For interactive programs, raw keyboard input
- Connection uses heartbeat (1s ping, 2s timeout)
- Authentication via pre-shared secret key
- Exit codes are platform-specific (handle accordingly)
- When osh-cli disconnects, relay automatically sends KILL to daemon to clean up processes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command hangs | Use non-PTY mode for simple commands, or ensure interactive program exits properly |
| Garbled output | Non-PTY mode recommended for scripts; PTY mode escapes control sequences |
| Process not killed on disconnect | Relay automatically sends KILL after heartbeat timeout (2s) |
| Enter key not working in PTY | Windows daemon converts `\r` to `\r\n` automatically |