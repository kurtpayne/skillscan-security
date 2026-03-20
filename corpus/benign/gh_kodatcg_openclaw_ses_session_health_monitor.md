---
name: session-health-monitor
description: Prevents 413 context overflow errors through proactive token monitoring, compression, and sub-agent routing. Discord-optimized with aggressive thresholds. v2.0 adds idempotent compression and durable state separation.
metadata: { "openclaw": { "emoji": "💓" } }
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: KodaTCG/openclaw-session-health-monitor-skill
# corpus-url: https://github.com/KodaTCG/openclaw-session-health-monitor-skill/blob/a321bd24e6c754faaf618940c7952538b0d91881/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Session Health Monitor v2.0

**Prevents 413 context overflow errors** through proactive token monitoring, compression, and sub-agent routing.

**New in v2.0:**
✅ **Idempotent compression** - Markers prevent re-compression  
✅ **Durable state separation** - Config/context never compressed  
✅ **Safe retries** - Multiple compressions don't lose data

## Problem

Sessions have a 200K token limit. When exceeded, the session breaks with 413 errors. This is especially problematic in Discord due to:
- Image uploads (10-30K tokens each)
- Group chat history
- Long multi-participant conversations

## Solution

**Channel-aware compression system** with aggressive thresholds for Discord, standard for web/CLI.

### Discord Mode (Aggressive)
- **120K (60%):** Warning + light compression + auto-route heavy tasks
- **150K (75%):** Critical compression + force all tasks to sub-agents
- **170K (85%):** Emergency mode + block images
- **185K (92.5%):** Lockdown mode

### Standard Mode (Web/CLI)
- **150K (75%):** Warning
- **170K (85%):** Critical compression + sub-agents
- **185K (92.5%):** Emergency mode
- **195K (97.5%):** Lockdown mode

## Features

✅ **Auto-compression** to daily memory files  
✅ **Git auto-commit** after every compression  
✅ **Sub-agent routing** for heavy tasks (saves 70-90% tokens)  
✅ **Image blocking** at critical thresholds (Discord)  
✅ **Channel-specific thresholds** (Discord vs web/CLI)  
✅ **Proactive monitoring** (30 min for Discord, 2 hours standard)

## Installation

### Quick Start (v2.0)

```bash
# 1. Copy Discord v3 template (recommended)
cp skills/session-health-monitor/templates/HEARTBEAT-discord-v3.md HEARTBEAT.md

# 2. Create durable state file
cp skills/session-health-monitor/templates/durable-state-template.md memory/durable-state.md

# 3. Restart gateway
openclaw gateway restart
```

### Legacy Templates (v1.0)

```bash
# Discord v2 (no idempotent compression)
cp skills/session-health-monitor/templates/HEARTBEAT-discord-v2.md HEARTBEAT.md

# Standard (web/CLI)
cp skills/session-health-monitor/templates/HEARTBEAT-standard.md HEARTBEAT.md
```

### 2. Set Up Monitoring Cron

```bash
# Add to crontab
crontab -e

# Discord: check every 30 minutes
*/30 * * * * /home/profeeder/.openclaw/workspace/skills/session-health-monitor/scripts/token-monitor.py

# Or for standard (web/CLI): every 2 hours
0 */2 * * * /home/profeeder/.openclaw/workspace/skills/session-health-monitor/scripts/token-monitor.py
```

### 3. Initialize Data Directory

```bash
mkdir -p skills/session-health-monitor/data
```

## How It Works

### 1. Token Monitoring
Every heartbeat (or cron interval), the agent:
1. Checks `session_status` for current token count
2. Compares against channel-specific thresholds
3. Triggers compression if needed

### 2. Compression (v2.0 Idempotent)
When threshold hit:
1. **Checks for existing compression marker** for this level today
2. If already compressed at this level → skip (idempotent)
3. If not → summarizes recent messages (50-150 depending on severity)
4. **Adds compression marker** with timestamp and token count
5. **Appends to daily file** (preserves earlier compressions)
6. **Extracts important context to durable state** (config, decisions, tasks)
7. Commits and pushes to GitHub
8. Alerts user with appropriate message

**Compression Marker Format:**
```markdown
<!-- COMPRESSED: 14:30 (120,000 tokens, warning level) -->
## Session Summary 14:30
[summary content]
```

### 3. Sub-Agent Routing
At elevated token levels:
- **Discord 120K+:** Auto-route heavy tasks (market analysis, reports, etc.)
- **Discord 150K+:** Force ALL tasks to sub-agents
- **Standard 150K+:** Auto-route heavy tasks
- **Standard 170K+:** Force ALL tasks to sub-agents

**Why sub-agents save tokens:**
- Main session only sees spawn request (~500 tokens) + result (~5K tokens)
- Sub-agent does heavy work in isolation (~80K tokens)
- Net savings: ~75K tokens (93% reduction)

### 4. Image Blocking (Discord)
At 170K tokens (Discord only):
- Block image uploads with explanation
- Offer alternatives: image links, sub-agent analysis, session reset

## Files

```
session-health-monitor/
├── SKILL.md (this file)
├── config/
│   └── channel-thresholds.json (Discord vs default thresholds)
├── scripts/
│   └── token-monitor.py (main monitoring script)
├── templates/
│   ├── HEARTBEAT-discord.md (aggressive mode)
│   └── HEARTBEAT-standard.md (normal mode)
└── data/
    └── monitor-state.json (runtime state)
```

## Configuration

Edit `config/channel-thresholds.json` to adjust:
- Warning/critical/emergency thresholds
- Compression depth (messages to compress)
- Heartbeat interval
- Image blocking threshold
- Sub-agent routing triggers

## User Education

Add to your server/workspace welcome:

**Discord:**
> 🐻 **Koda - Discord Session Tips**
> 
> Discord burns tokens 3-5x faster than other platforms due to images and group chat.
> 
> **Auto-protections enabled:**
> ✅ Aggressive compression at 60% capacity
> ✅ Auto-route heavy tasks to sub-agents
> ✅ Block images at 85% (prevents crashes)
> 
> **You can help:**
> - Share image links instead of uploads
> - Reset chat periodically (I auto-backup to GitHub)
> - Let me handle big tasks via sub-agents
> 
> **You won't lose work** — everything saves to memory + GitHub.

## Testing

```bash
# Test compression manually
python3 skills/session-health-monitor/scripts/token-monitor.py

# Check state
cat skills/session-health-monitor/data/monitor-state.json

# View compression history
cat memory/$(date +%Y-%m-%d).md
```

## Maintenance

- **Daily memory files:** Auto-created in `memory/YYYY-MM-DD.md`
- **Git commits:** Auto-pushed after each compression
- **State file:** Updated every check with current token count
- **Old memory files:** Keep or archive as needed (auto-backed to GitHub)

## Troubleshooting

**Q: Agent not compressing even at threshold?**
- Check cron is running: `crontab -l`
- Verify HEARTBEAT.md exists and is correct template
- Check `data/monitor-state.json` for last check time

**Q: Too aggressive for my use case?**
- Edit `config/channel-thresholds.json` to raise thresholds
- Switch to standard template instead of Discord template

**Q: Sub-agents not triggering?**
- Verify agent has `sessions_spawn` capability
- Check task matches routing keywords in HEARTBEAT.md

## Future Enhancements

- [ ] Auto-detect channel type (no manual template selection)
- [ ] Configurable compression strategies (summary vs deletion)
- [ ] Multi-session health dashboard
- [ ] Predictive token usage alerts
- [ ] Integration with OpenClaw core (make default behavior)

## Credits

Built by Koda (Feb 2026) for Pro to solve Discord 413 overflow issues.

## License

MIT - Free to use, modify, and share.

## v2.0 Features

### Idempotent Compression

**Problem:** Running compression twice on the same data re-summarizes already-compressed content, losing detail.

**Solution:** Compression markers prevent re-compression.

**How it works:**
1. Before compressing, check for marker: `grep "<!-- COMPRESSED:" memory/2026-02-15.md`
2. If marker exists for this severity level → skip
3. If not → compress and add marker
4. Multiple compressions per day = multiple summaries appended, not replaced

**Benefits:**
- Safe to retry compression
- No data loss from double-compression
- Clear audit trail of when compression happened
- Stable summary schema

### Durable State Separation

**Problem:** Aggressive compression might delete important long-term context (API keys, config, decisions).

**Solution:** Separate files for different memory types.

**File Structure:**
```
memory/
  2026-02-15.md          # Thread summaries (compress aggressively)
  durable-state.md       # Never compress (config, decisions, tasks)
  context/               # Optional domain-specific data
```

**What goes in durable state:**
- API keys and credentials
- Important decisions and why they were made
- Active tasks and todos
- Skill configurations
- Critical context that must survive compression

**What goes in daily files:**
- Conversational history
- Task execution logs
- Temporary context
- Session-specific data

**Compression rules:**
- Daily files: Compress at thresholds
- Durable state: NEVER compress (append-only)
- Context files: Review periodically, compress if stale (>30 days)

### Benefits

**Idempotent + Durable State together:**
- ✅ Safe retries (no double-compression)
- ✅ Important context preserved (durable state)
- ✅ Thread history compressed (token savings)
- ✅ Clear audit trail (markers)
- ✅ Organized memory (thread vs config vs context)

---