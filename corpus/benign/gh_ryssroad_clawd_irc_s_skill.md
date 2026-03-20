---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: ryssroad/clawd-irc-skill
# corpus-url: https://github.com/ryssroad/clawd-irc-skill/blob/c43b21810f93130005d841d62e73b36a17d53757/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# IRC Client Skill

## Overview
This skill enables Claude to connect to IRC servers, join channels, send/receive messages, and coordinate with other AI agents over IRC protocol.

## When to Use
- Connecting to IRC servers for multi-agent communication
- Monitoring IRC channels for messages
- Sending messages to IRC channels or users
- Coordinating tasks between multiple AI agents
- Real-time chat-based collaboration

## Prerequisites
```bash
pip install irc --break-system-packages
```

## Core Concepts

### IRC Basics
- **Server**: IRC daemon (e.g., irc.libera.chat, or custom server)
- **Channel**: Chat rooms prefixed with # (e.g., #agents)
- **Nickname**: Your identity on the server (must be unique)
- **Messages**: Public (channel) or private (user-to-user)

## Implementation Patterns

### Pattern 1: Simple Message Send (One-shot)
Use when you just need to send a message and disconnect:

```python
#!/usr/bin/env python3
import socket
import time

def send_irc_message(server, port, channel, nickname, message):
    """Send a single message to IRC channel and disconnect"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    
    # IRC handshake
    sock.send(f"NICK {nickname}\r\n".encode())
    sock.send(f"USER {nickname} 0 * :{nickname}\r\n".encode())
    time.sleep(2)  # Wait for connection
    
    # Join channel and send message
    sock.send(f"JOIN {channel}\r\n".encode())
    time.sleep(1)
    sock.send(f"PRIVMSG {channel} :{message}\r\n".encode())
    time.sleep(1)
    
    sock.send(b"QUIT :Goodbye\r\n")
    sock.close()

# Example usage
send_irc_message(
    server="localhost",
    port=6667,
    channel="#agents",
    nickname="claude_bot",
    message="Hello from Claude!"
)
```

### Pattern 2: Persistent Connection (Background Process)
Use when you need to monitor channels and respond to messages:

```python
#!/usr/bin/env python3
import socket
import time
import sys
import select

class IRCBot:
    def __init__(self, server, port, nickname, channel):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.channel = channel
        self.sock = None
        
    def connect(self):
        """Connect to IRC server"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server, self.port))
        
        # IRC handshake
        self.send_raw(f"NICK {self.nickname}")
        self.send_raw(f"USER {self.nickname} 0 * :{self.nickname}")
        time.sleep(2)
        
        # Join channel
        self.send_raw(f"JOIN {self.channel}")
        print(f"[IRC] Connected to {self.server}:{self.port} as {self.nickname}")
        print(f"[IRC] Joined {self.channel}")
        
    def send_raw(self, message):
        """Send raw IRC command"""
        self.sock.send(f"{message}\r\n".encode())
        
    def send_message(self, target, message):
        """Send message to channel or user"""
        self.send_raw(f"PRIVMSG {target} :{message}")
        print(f"[IRC] -> {target}: {message}")
        
    def listen(self, callback=None):
        """Listen for IRC messages"""
        buffer = ""
        
        while True:
            # Check if socket has data (non-blocking)
            ready = select.select([self.sock], [], [], 1.0)
            if ready[0]:
                data = self.sock.recv(4096).decode('utf-8', errors='ignore')
                buffer += data
                
                while '\r\n' in buffer:
                    line, buffer = buffer.split('\r\n', 1)
                    self.handle_line(line, callback)
                    
    def handle_line(self, line, callback):
        """Handle incoming IRC line"""
        print(f"[IRC] <- {line}")
        
        # Respond to PING
        if line.startswith('PING'):
            pong = line.replace('PING', 'PONG')
            self.send_raw(pong)
            return
            
        # Parse messages
        if 'PRIVMSG' in line:
            # Format: :nick!user@host PRIVMSG #channel :message
            parts = line.split(' ', 3)
            if len(parts) >= 4:
                sender = parts[0][1:].split('!')[0]
                target = parts[2]
                message = parts[3][1:] if parts[3].startswith(':') else parts[3]
                
                print(f"[MSG] {sender} -> {target}: {message}")
                
                if callback:
                    callback(sender, target, message)
                    
    def quit(self):
        """Disconnect from IRC"""
        self.send_raw("QUIT :Goodbye")
        self.sock.close()

# Example usage
if __name__ == "__main__":
    bot = IRCBot(
        server="localhost",
        port=6667,
        nickname="claude_bot",
        channel="#agents"
    )
    
    bot.connect()
    
    # Send initial message
    bot.send_message("#agents", "Claude is now online!")
    
    # Optional: Define message handler
    def on_message(sender, target, message):
        # Respond to mentions
        if "claude" in message.lower():
            bot.send_message(target, f"Hello {sender}! You mentioned me.")
    
    # Listen for messages
    try:
        bot.listen(callback=on_message)
    except KeyboardInterrupt:
        bot.quit()
```

### Pattern 3: Background Daemon with File-based Control
Use when you need persistent connection that other processes can control:

```python
#!/usr/bin/env python3
import socket
import time
import json
import os
from pathlib import Path

CONTROL_DIR = Path("/tmp/irc_control")
CONTROL_DIR.mkdir(exist_ok=True)

class IRCDaemon:
    def __init__(self, server, port, nickname, channel):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.channel = channel
        self.sock = None
        self.running = True
        
        # Create control files
        self.inbox = CONTROL_DIR / "inbox.txt"
        self.outbox = CONTROL_DIR / "outbox.txt"
        self.commands = CONTROL_DIR / "commands.txt"
        
        self.inbox.touch()
        self.commands.touch()
        
    def connect(self):
        """Connect to IRC server"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1.0)
        self.sock.connect((self.server, self.port))
        
        self.send_raw(f"NICK {self.nickname}")
        self.send_raw(f"USER {self.nickname} 0 * :{self.nickname}")
        time.sleep(2)
        self.send_raw(f"JOIN {self.channel}")
        
    def send_raw(self, message):
        """Send raw IRC command"""
        self.sock.send(f"{message}\r\n".encode())
        
    def check_commands(self):
        """Check for commands in control file"""
        if self.commands.stat().st_size > 0:
            with open(self.commands, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("SEND "):
                        # Format: SEND #channel message text
                        parts = line.split(' ', 2)
                        if len(parts) >= 3:
                            target, message = parts[1], parts[2]
                            self.send_raw(f"PRIVMSG {target} :{message}")
                    elif line == "QUIT":
                        self.running = False
            
            # Clear commands file
            self.commands.write_text("")
            
    def run(self):
        """Main daemon loop"""
        buffer = ""
        
        while self.running:
            # Check for outgoing commands
            self.check_commands()
            
            # Check for incoming messages
            try:
                data = self.sock.recv(4096).decode('utf-8', errors='ignore')
                buffer += data
                
                while '\r\n' in buffer:
                    line, buffer = buffer.split('\r\n', 1)
                    
                    # Handle PING
                    if line.startswith('PING'):
                        self.send_raw(line.replace('PING', 'PONG'))
                        continue
                    
                    # Handle messages
                    if 'PRIVMSG' in line:
                        with open(self.inbox, 'a') as f:
                            f.write(f"{time.time()} {line}\n")
                            
            except socket.timeout:
                pass  # No data, continue
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)
                self.connect()  # Reconnect
                
        self.sock.send(b"QUIT :Daemon stopped\r\n")
        self.sock.close()

# Example usage
if __name__ == "__main__":
    import sys
    
    daemon = IRCDaemon(
        server=sys.argv[1] if len(sys.argv) > 1 else "localhost",
        port=int(sys.argv[2]) if len(sys.argv) > 2 else 6667,
        nickname=sys.argv[3] if len(sys.argv) > 3 else "claude_daemon",
        channel=sys.argv[4] if len(sys.argv) > 4 else "#agents"
    )
    
    daemon.connect()
    print(f"IRC Daemon running. Control files in {CONTROL_DIR}")
    print(f"  Send messages: echo 'SEND #agents Hello!' > {daemon.commands}")
    print(f"  View inbox: cat {daemon.inbox}")
    print(f"  Stop daemon: echo 'QUIT' > {daemon.commands}")
    
    daemon.run()
```

## Usage Instructions for Claude

### Quick Test (One Message)
1. Create a simple Python script using Pattern 1
2. Run it to send a test message
3. Check if message appears in IRC channel

### Monitoring Channel (Interactive)
1. Use Pattern 2 to create interactive bot
2. Run in foreground to see messages in real-time
3. Implement custom message handlers as needed

### Background Service (Production)
1. Use Pattern 3 to create daemon
2. Run in background: `python3 irc_daemon.py server port nick channel &`
3. Control via files:
   - Send: `echo "SEND #agents Hi!" >> /tmp/irc_control/commands.txt`
   - Read: `tail -f /tmp/irc_control/inbox.txt`
   - Stop: `echo "QUIT" >> /tmp/irc_control/commands.txt`

## Common IRC Commands

```python
# Join channel
bot.send_raw("JOIN #channel")

# Part channel
bot.send_raw("PART #channel")

# Send message
bot.send_raw("PRIVMSG #channel :message")

# Private message
bot.send_raw("PRIVMSG nickname :message")

# Set topic
bot.send_raw("TOPIC #channel :New topic")

# List users
bot.send_raw("NAMES #channel")

# Disconnect
bot.send_raw("QUIT :Goodbye")
```

## Troubleshooting

### Connection Issues
- Check firewall rules: `telnet server 6667`
- Verify server is running: `netstat -tuln | grep 6667`
- Check nickname conflicts (must be unique)

### Message Not Sending
- Wait for full connection (2-3 seconds after handshake)
- Ensure channel join completed before sending
- Check for PING/PONG responses

### Daemon Not Responding
- Check if process is running: `ps aux | grep irc_daemon`
- Verify control files: `ls -la /tmp/irc_control/`
- Check permissions on control directory

## Security Notes

- IRC traffic is **unencrypted** by default (use SSL/TLS if available)
- Do not send sensitive data over IRC
- Implement authentication if exposing publicly
- Rate limit messages to avoid flooding/bans

## Examples for Testing

### Test 1: Simple Hello
```bash
python3 -c "
import socket, time
s = socket.socket()
s.connect(('localhost', 6667))
s.send(b'NICK testbot\r\nUSER testbot 0 * :testbot\r\n')
time.sleep(2)
s.send(b'JOIN #agents\r\n')
time.sleep(1)
s.send(b'PRIVMSG #agents :Hello from Python!\r\n')
time.sleep(1)
s.send(b'QUIT\r\n')
s.close()
"
```

### Test 2: Read Last 10 Messages
```bash
# If using daemon
tail -10 /tmp/irc_control/inbox.txt
```

### Test 3: Send Message via Daemon
```bash
echo "SEND #agents Claude says hi!" >> /tmp/irc_control/commands.txt
```

## Integration with Other Agents

When coordinating with OpenClaw agents:
1. Establish naming convention (e.g., `claude_`, `claw_`)
2. Use channel topics for status/coordination
3. Implement command prefix system (e.g., `!task`, `!status`)
4. Store conversation history in files for context

## Next Steps

After testing basic connectivity:
- Implement command parsing for agent coordination
- Add message persistence/logging
- Create higher-level API for common operations
- Integrate with other skills (e.g., task management)