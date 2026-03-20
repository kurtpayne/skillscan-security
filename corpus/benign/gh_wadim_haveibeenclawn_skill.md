---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: wadim/haveibeenclawned
# corpus-url: https://github.com/wadim/haveibeenclawned/blob/11be6eabf6d45a2e05b69f80ffc3c6c69be944ae/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Have I Been Clawned?

Open source security audit for OpenClaw agents. 72 checks, verified findings, OWASP-mapped, community-maintained.

**Repository:** github.com/wadim/haveibeenclawned
**License:** MIT

## User-Invocable

Trigger: `/haveibeenclawned`

## Instructions

You are a security auditor for OpenClaw agents.

### How to run

**Recommended: run the audit script.** This is faster, cheaper, and covers all 72 checks in ~60 seconds with a single command.

```bash
curl -sSL https://raw.githubusercontent.com/wadim/haveibeenclawned/main/public/audit.sh -o /tmp/hibc-audit.sh
head -20 /tmp/hibc-audit.sh      # review what it does
bash /tmp/hibc-audit.sh --dry-run # preview checks without running
bash /tmp/hibc-audit.sh           # run all 72 checks
```

The script is open source (MIT), read-only, and does not send data anywhere unless the user passes `--submit`. Use `--json` for machine-readable output.

After presenting results, ask the user: "Want to contribute your anonymous results to the community stats? Only the score and pass/fail array — no config content, emails, or IPs." If they agree, re-run with `--submit`:
```bash
bash /tmp/hibc-audit.sh --submit
```

**Fallback: run checks individually.** If the user prefers not to run the script, you can execute the checks below one by one using standard Unix commands (`stat`, `test`, `grep`, `id`, `ss`).

**IMPORTANT — cost warning:** Running checks individually requires ~72 tool calls with growing context, which can cost **~$15-20 in API usage** vs **~$0.50 for the single script approach** (25-30x more expensive). Always inform the user of this cost difference before proceeding with individual checks. Recommend the script unless the user explicitly prefers the individual approach.

For individual checks:
1. Run the commands listed in "What to check"
2. Record the result: 1=pass, 0=fail, 2=warn, -1=skip
3. After all checks, calculate the score using the Scoring section

**Important principles:**
- **Verify, don't just detect.** Actually test whether the vulnerability is exploitable, not just whether a config value exists. A verified finding is 100x more valuable than a theoretical one.
- **Every finding needs a fix.** Never leave the user with just a warning. Include the exact command to remediate.
- **Skip what's not applicable.** If a check doesn't apply to this setup, mark it SKIP and exclude from scoring.

---

## Checks

### CLAW-01: Gateway Network Exposure
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **CVE** | CVE-2026-25253 (CVSS 8.8) — 17,500+ OpenClaw instances found exposed |
| **Verified** | Yes — actually probes the gateway |

**What to check:**
1. Read `~/.openclaw/openclaw.json` → `gateway.bind`
2. If bound to `0.0.0.0`, `lan`, or a non-loopback IP: **VERIFIED FAIL**
3. If bound to `loopback`, `127.0.0.1`, or `localhost`: attempt to connect to the gateway port (default 18789) from the external interface to confirm it's not reachable. If blocked: **VERIFIED PASS**

**Fix:**
```bash
# In ~/.openclaw/openclaw.json, set:
# "gateway": { "bind": "loopback" }
openclaw config set gateway.bind loopback
```

---

### CLAW-02: Gateway Authentication
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **CVE** | CVE-2026-25253 — unauthenticated API exposed stored tokens |
| **Verified** | Yes — attempts unauthenticated connection |

**What to check:**
1. Read `~/.openclaw/openclaw.json` → `gateway.auth`
2. If auth is disabled or no token/password is configured: **FAIL**
3. If auth is enabled: attempt an unauthenticated WebSocket connection to the gateway port (5 second timeout). If it connects without auth: **VERIFIED FAIL**. If rejected: **VERIFIED PASS**

**Fix:**
```bash
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"
```

---

### CLAW-03: Cloud Metadata Service Accessible
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | AWS IMDS credential theft, GCP/Azure equivalent |
| **Verified** | Yes — actually probes metadata endpoint |

**What to check:**
1. Run: `curl -s -m 2 http://169.254.169.254/latest/meta-data/`
2. If it returns data (HTTP 200): **VERIFIED FAIL** — the agent can steal cloud IAM credentials
3. If it times out or returns error: **PASS**
4. If not on a cloud VM (no route to 169.254.169.254): **SKIP**

**Fix:**
```bash
# AWS: Enable IMDSv2 (requires token)
aws ec2 modify-instance-metadata-options --instance-id <id> --http-tokens required
# Or block via iptables:
sudo iptables -A OUTPUT -d 169.254.169.254 -j DROP
```

---

### CLAW-04: Personal Email as Agent Identity
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Agent compromise → attacker sends as you |

**What to check:**
1. Read `~/.openclaw/openclaw.json` → email configuration
2. Match domain against personal email providers:
   `gmail.com, googlemail.com, yahoo.com, yahoo.co.uk, hotmail.com, outlook.com, live.com, msn.com, aol.com, icloud.com, me.com, mac.com, protonmail.com, proton.me, zoho.com, yandex.com, mail.com, gmx.com, tutanota.com, fastmail.com`
3. If match: **FAIL** — your personal identity is the agent's identity
4. If custom domain or no email: **PASS**

**Fix:**
Use a dedicated agent email on a domain you control, or a managed service that provides agent-specific email addresses.

---

### CLAW-05: Plaintext API Keys in Configuration
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **CVE** | CVE-2026-22038 (AutoGPT plaintext key logging) |
| **Ref** | OpenClaw Issues #9627, #4654 — `openclaw doctor --fix` writes env vars as plaintext |

**What to check:**
1. Scan these files for secret patterns:
   - `~/.openclaw/openclaw.json`
   - `~/.openclaw/.env`
   - `.env` and `openclaw.json` in current directory
2. Patterns to match:
   - `sk-` followed by 20+ alphanumeric chars (OpenAI)
   - `sk-ant-` (Anthropic)
   - `AKIA` followed by 16 uppercase alphanumeric chars (AWS)
   - `ghp_` followed by 36 alphanumeric chars (GitHub)
   - `xoxb-` or `xoxp-` (Slack)
   - `AIza` followed by 35 chars (Google)
   - Any line matching `(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*['"]?[a-zA-Z0-9_\-]{20,}`
3. **Critical:** Also check if `openclaw.json` contains resolved environment variable values (the `openclaw doctor --fix` bug writes `${VAR}` as its actual value)
4. If any match: **FAIL** — report which file and pattern type (never echo the actual key)

**Fix:**
```bash
# Move secrets to environment variables
# In openclaw.json, use: "${OPENAI_API_KEY}" not the actual key
# Set in .env (with 600 permissions):
chmod 600 ~/.openclaw/.env
# Or use system keychain:
openclaw config set auth.keychain true
```

---

### CLAW-06: Sensitive Files Accessible to Agent
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Every self-hosted agent runs as the user with full filesystem access |
| **Verified** | Yes — actually checks if files are readable |

**What to check:**
Test if the following sensitive files/directories exist AND are readable:
```
~/.ssh/id_rsa
~/.ssh/id_ed25519
~/.aws/credentials
~/.config/gcloud/application_default_credentials.json
~/.kube/config
~/.npmrc
~/.docker/config.json
~/.netrc
~/.gnupg/
```
For each, run `test -r <path>` (or equivalent stat check).
- If 3+ sensitive paths are readable: **VERIFIED FAIL**
- If 1-2 readable: **WARN** (partial exposure)
- If none readable: **VERIFIED PASS**

Report which specific files are exposed but never read their contents.

**Fix:**
```bash
# Enable sandbox to isolate agent from host filesystem
openclaw config set sandbox.mode all
# Or restrict with file permissions:
chmod 700 ~/.ssh ~/.aws ~/.gnupg
```

---

### CLAW-07: Secrets in Session Transcripts
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Snyk research: skills leak credentials into session JSONL files |
| **Verified** | Yes — scans actual session content |

**OPT-IN: Ask the user before running this check:**
> "Check 7 scans your recent session transcripts for accidentally leaked secrets (API keys, credit cards, SSNs). Everything stays local. Run this check? (y/n)"

If declined: **SKIP (-1)**

**What to check:**
1. Scan the 10 most recent files in `~/.openclaw/agents/*/sessions/*.jsonl`
2. Search for:
   - API key patterns (same as CLAW-05)
   - Credit card numbers: `\b[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4}\b`
   - SSN patterns: `\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b`
3. If found: **VERIFIED FAIL** — report count and type, never the actual values

**Fix:**
```bash
# Enable log redaction
openclaw config set logging.redactSensitive tools
# Add custom redaction patterns:
openclaw config set logging.redactPatterns '["sk-[a-zA-Z0-9]+", "AKIA[A-Z0-9]+"]'
# Purge compromised sessions:
rm ~/.openclaw/agents/*/sessions/<affected_session>.jsonl
# Rotate any exposed keys immediately
```

---

### CLAW-08: Docker Privileged Mode
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-05 Unexpected Code Running |
| **CVE** | CVE-2023-37273 (AutoGPT Docker escape) |
| **Verified** | Yes — inspects container runtime configuration |

**What to check:**
1. Detect if running inside Docker: check for `/.dockerenv` file or `cgroup` entries containing `docker`/`containerd`
2. If not in Docker: **SKIP**
3. If in Docker, inspect the container configuration for:
   - `--privileged` flag (check: `cat /proc/1/status | grep CapEff` — if all bits set `0000003fffffffff`, container is privileged)
   - Host network mode (check: `cat /proc/1/net/dev` and compare to host — if identical, host networking is active)
   - Dangerous volume mounts: `/` or `/home` or `/etc` mounted from host (check: `mount | grep -E "on / type|on /home type|on /etc type"` for bind mounts from host)
4. If `--privileged` or host root/home mounted: **VERIFIED FAIL** — any agent compromise is full host compromise
5. If host network only: **WARN**
6. If none of the above: **PASS**

**Fix:**
```bash
# Remove --privileged flag from docker run / docker-compose.yml
# Replace host volume mounts with specific directories:
#   BAD:  -v /:/host
#   GOOD: -v /path/to/project:/workspace:ro
# Use non-root user inside container:
#   USER 1000:1000 in Dockerfile
# Drop all capabilities and add only what's needed:
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE ...
```

---

### CLAW-09: Agent Running as Root
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) |
| **OWASP** | ASI-05 Unexpected Code Running |
| **Ref** | If UID=0, any agent compromise = full system compromise |
| **Verified** | Yes — checks process UID |

**What to check:**
1. Check the UID of the current process: run `id -u`
2. If UID is `0` (root): **VERIFIED FAIL** — the agent has unrestricted system access
3. Also check if the agent user has passwordless sudo: run `sudo -n true 2>/dev/null` — if it succeeds without prompting, the user effectively has root
4. If UID != 0 and no passwordless sudo: **VERIFIED PASS**
5. If UID != 0 but passwordless sudo exists: **WARN**

**Fix:**
```bash
# Create a dedicated non-root user for the agent:
sudo useradd -m -s /bin/bash openclaw-agent
# Run the agent as that user:
sudo -u openclaw-agent openclaw start
# Remove passwordless sudo if present:
sudo visudo  # Remove NOPASSWD entries for the agent user
# In Docker, add to Dockerfile:
RUN useradd -m agent
USER agent
```

---

### CLAW-10: Sandbox Configuration
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-05 Unexpected Code Running |
| **Ref** | OpenClaw sandbox is OFF by default (Issue #7827) |

**What to check:**
1. Read `~/.openclaw/openclaw.json` → `sandbox.mode`
2. If `off` or not set: **FAIL** — agent code runs directly on host
3. If `non-main`: **WARN** — only non-primary sessions sandboxed
4. If `all`: check `sandbox.scope`:
   - `shared`: **WARN** — cross-session data leakage possible
   - `session` or `agent`: **PASS**

**Fix:**
```bash
openclaw config set sandbox.mode all
openclaw config set sandbox.scope session
```

---

### CLAW-11: Elevated Mode Restrictions
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-05 Unexpected Code Running |
| **CVE** | CVE-2026-25253 kill chain used elevated mode to escape sandbox |

**What to check:**
1. Read `~/.openclaw/openclaw.json` → `tools.elevated`
2. If `tools.elevated.allowFrom` is set to `*` or `all`: **FAIL** — sandbox escape for any session
3. If `tools.elevated` exists but `allowFrom` is restricted to specific users/channels: **PASS**
4. If `tools.elevated` doesn't exist: **PASS** (not configured)

**Fix:**
```bash
# Restrict elevated mode to specific trusted users only
openclaw config set tools.elevated.allowFrom '["your-telegram-id"]'
# Or disable entirely:
openclaw config delete tools.elevated
```

---

### CLAW-12: Configuration File Permissions
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | CIS Benchmark: sensitive config should be 600 |
| **Verified** | Yes — checks actual file permissions |

**What to check:**
1. Check permissions on:
   - `~/.openclaw/openclaw.json`
   - `~/.openclaw/.env`
   - `~/.openclaw/credentials/` (all files)
   - `~/.openclaw/agents/*/agent/auth-profiles.json`
2. Any file readable by group or others (mode > 600 for files, > 700 for dirs): **FAIL**
3. All files owner-only: **PASS**

**Fix:**
```bash
chmod 600 ~/.openclaw/openclaw.json ~/.openclaw/.env
chmod -R 600 ~/.openclaw/credentials/
chmod 700 ~/.openclaw/ ~/.openclaw/credentials/
# Or let openclaw fix it:
openclaw doctor --fix
```

---

### CLAW-13: Installed Skills Against Threat Intel
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-04 Agentic Supply Chain |
| **Ref** | 341 malicious ClawHub skills found (12% of registry), Feb 2026 |

**What to check:**
1. List all skills in `~/.openclaw/skills/`
2. Check against known-malicious skills (case-insensitive):
   ```
   data-exfil, keylogger, reverse-shell, crypto-miner, credential-stealer,
   prompt-injector, shadow-agent, backdoor-tool, solana-wallet-tracker,
   polymarket-trader, token-sniper, atomic-stealer, openclaw-boost,
   free-credits, claw-premium, admin-tools
   ```
3. Flag skills that:
   - Have no `SKILL.md` file
   - Were modified in the last 24 hours (potential tampering)
   - Have npm packages with post-install scripts
4. If known-malicious found: **VERIFIED FAIL**
5. If 3+ unverified (no SKILL.md): **WARN**
6. If all clean: **PASS**

**Fix:**
```bash
# Remove malicious skills:
rm -rf ~/.openclaw/skills/<malicious-skill>
# Enable plugin allowlist (whitelist mode):
openclaw config set plugins.allow '["skill-a", "skill-b"]'
```

---

### CLAW-14: MCP Server Known Vulnerabilities
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-04 Agentic Supply Chain |
| **CVE** | CVE-2025-6514 (mcp-remote RCE, CVSS 9.6), CVE-2025-49596 (MCP Inspector RCE), CVE-2025-53109/53110 (Filesystem MCP escape) |

**What to check:**
1. Find installed MCP packages: check `package.json` files in agent config, `node_modules/` directories, or MCP config
2. Check versions against known-vulnerable:
   - `mcp-remote` < 1.1.0 → CVE-2025-6514 (CRITICAL)
   - `@anthropic/mcp-inspector` < 0.7.0 → CVE-2025-49596
   - `@anthropic/mcp-server-filesystem` < 2.1.0 → CVE-2025-53109
   - `@anthropic/mcp-server-git` < 2.1.0 → CVE-2025-68143/68144/68145
3. If any vulnerable version found: **FAIL** — report package and CVE
4. If no MCP packages found: **SKIP**
5. If all patched: **PASS**

**Fix:**
```bash
npm update mcp-remote @anthropic/mcp-inspector @anthropic/mcp-server-filesystem
# Or pin to safe versions in package.json
```

---

### CLAW-15: OpenClaw Version Security
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **CVE** | CVE-2026-25253 (CVSS 8.8) — patched in v2.6.1+ |

**What to check:**
1. Run `openclaw --version` or read `package.json`
2. Known-vulnerable versions:
   - < 2.6.1: CVE-2026-25253 (unauthenticated RCE)
   - < 2.5.0: Multiple path traversal issues
3. If vulnerable: **FAIL**
4. If current: **PASS**

**Fix:**
```bash
openclaw update
# Or:
npm install -g openclaw@latest
```

---

### CLAW-16: Session File Permissions
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Session files contain full conversation history in plaintext JSONL |
| **Verified** | Yes — checks actual permissions |

**What to check:**
1. Check permissions on `~/.openclaw/agents/*/sessions/` directories and files
2. If any session file is readable by group or others: **FAIL**
3. If all owner-only: **PASS**
4. Also check: are session files being synced to cloud (iCloud, Dropbox, Google Drive)? If `~/.openclaw/` is inside a synced folder: **WARN**

**Fix:**
```bash
chmod -R 700 ~/.openclaw/agents/*/sessions/
# Exclude from cloud sync:
# macOS: add to .nosync or move outside ~/Library/Mobile Documents
```

---

### CLAW-17: Default Credentials in Config
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Default/placeholder credentials are the first thing attackers try |

**What to check:**
1. Scan these files for default/placeholder values:
   - `~/.openclaw/openclaw.json`
   - `~/.openclaw/.env`
   - `.env` and `openclaw.json` in current directory
2. Patterns to match (case-insensitive):
   - `change_me`, `changeme`
   - `default`, `placeholder`
   - `example`, `sample`
   - `YOUR_` (e.g., `YOUR_API_KEY`, `YOUR_TOKEN`)
   - `xxx`, `TODO`, `FIXME`
   - `password123`, `admin`, `test`
   - Exact matches of documented default values from OpenClaw quickstart guides
3. Only flag values that appear in key-value contexts (not comments or descriptions)
4. If any default/placeholder values found in credential fields: **FAIL**
5. If none found: **PASS**

**Fix:**
```bash
# Replace all placeholder values with real credentials:
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"
# Audit your .env file:
grep -inE "change_me|default|placeholder|YOUR_|xxx" ~/.openclaw/.env
# Replace each match with actual values, then:
chmod 600 ~/.openclaw/.env
```

---

### CLAW-18: .env Not in .gitignore
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Wiz research: 65% of Forbes AI 50 companies leaked secrets on GitHub |
| **Verified** | Yes — checks .gitignore contents |

**What to check:**
1. Check if the current directory or `~/.openclaw/` is inside a git repository: run `git rev-parse --is-inside-work-tree 2>/dev/null`
2. If not a git repo: **SKIP**
3. If it is a git repo, check if `.env` is listed in `.gitignore`:
   - Run `git check-ignore .env` — if it returns `.env`, it's ignored: **PASS**
   - Also check for `.env*`, `.env.local`, `.env.production` patterns
4. If `.env` is NOT ignored: **FAIL** — secrets may be committed to version control
5. Bonus: check if `.env` is already tracked by git: `git ls-files --error-unmatch .env 2>/dev/null` — if tracked, it's already in history even if later added to .gitignore

**Fix:**
```bash
# Add .env to .gitignore:
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
# If .env was already committed, remove from tracking (file stays on disk):
git rm --cached .env
git commit -m "Remove .env from tracking"
# WARNING: The .env is still in git history — see CLAW-19
```

---

### CLAW-19: Secrets in Git History
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Keys committed even once persist in history forever; Wiz found secrets in deleted forks and gists |
| **Verified** | Yes — scans actual git log |

**OPT-IN: Ask the user before running this check:**
> "Check 20 scans your git history for accidentally committed secrets (API keys, tokens). This may take a moment on large repos. Run this check? (y/n)"

If declined: **SKIP (-1)**

**What to check:**
1. Check if current directory is a git repo: `git rev-parse --is-inside-work-tree 2>/dev/null`
2. If not a git repo: **SKIP**
3. Scan recent git history (last 100 commits) for secret patterns:
   ```bash
   git log --all -p -100 2>/dev/null
   ```
4. Search output for the same API key patterns as CLAW-05:
   - `sk-` followed by 20+ alphanumeric chars
   - `sk-ant-` (Anthropic)
   - `AKIA` followed by 16 uppercase alphanumeric chars (AWS)
   - `ghp_` followed by 36 alphanumeric chars (GitHub)
   - `xoxb-` or `xoxp-` (Slack)
   - Lines matching `(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*['"]?[a-zA-Z0-9_\-]{20,}`
5. If secrets found in history: **VERIFIED FAIL** — report count and commit range, never the actual values
6. If no secrets found: **PASS**

**Fix:**
```bash
# IMPORTANT: Rotate all exposed credentials FIRST — assume they are compromised
# Then remove from history using git-filter-repo (preferred over BFG):
pip install git-filter-repo
git filter-repo --invert-paths --path .env --force
# Or use BFG Repo Cleaner:
bfg --delete-files .env
git reflog expire --expire=now --all && git gc --prune=now --aggressive
# Force push the cleaned history (coordinate with team):
git push --force-with-lease
```

---

### CLAW-20: Browser Profiles Accessible
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Browser profiles contain saved passwords, cookies, and active session tokens for every logged-in service |
| **Verified** | Yes — checks if directories are readable |

**What to check:**
1. Check if any of the following browser profile directories exist AND are readable:
   ```
   # macOS
   ~/Library/Application Support/Google/Chrome/
   ~/Library/Application Support/Firefox/Profiles/
   ~/Library/Application Support/BraveSoftware/Brave-Browser/
   ~/Library/Application Support/Microsoft Edge/
   # Linux
   ~/.config/google-chrome/
   ~/.mozilla/firefox/
   ~/.config/BraveSoftware/Brave-Browser/
   ~/.config/microsoft-edge/
   ```
2. For each path, run `test -r <path>` (or equivalent stat check)
3. If 2+ browser profile directories are readable: **VERIFIED FAIL** — agent can access saved passwords, cookies, session tokens
4. If 1 readable: **WARN**
5. If none readable: **VERIFIED PASS**

Report which browser profiles are exposed but never read their contents.

**Fix:**
```bash
# Enable sandbox to isolate agent from browser profile directories
openclaw config set sandbox.mode all
# Or restrict permissions (will break browser for current user — use sandbox instead):
# The real fix is running the agent as a separate user:
sudo -u openclaw-agent openclaw start
```

---

### CLAW-21: Git Credentials Accessible
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Plaintext git credentials give push access to every repository the user has access to |
| **Verified** | Yes — checks if credential files are readable |

**What to check:**
1. Check if the following files exist AND are readable:
   ```
   ~/.git-credentials
   ~/.gitconfig
   ```
2. For `~/.git-credentials`: if it exists and is readable: **FAIL** — contains plaintext username:token pairs
3. For `~/.gitconfig`: check if it contains a `credential` section with `helper = store` (plaintext storage): if so, **FAIL**
4. Also check for credential helpers that cache tokens:
   - `git config --global credential.helper` — if set to `store`, credentials are in plaintext
   - If set to `cache`, credentials are temporarily in memory (less severe)
   - If set to `osxkeychain`, `wincred`, or `libsecret`: **PASS** (uses OS keychain)
5. If no plaintext credential storage found: **PASS**

**Fix:**
```bash
# Switch from plaintext to OS keychain:
# macOS:
git config --global credential.helper osxkeychain
# Linux:
git config --global credential.helper libsecret
# Remove plaintext credentials file:
rm ~/.git-credentials
# Enable agent sandbox to prevent access:
openclaw config set sandbox.mode all
```

---

### CLAW-22: Database Credentials Accessible
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Database credential files provide direct access to production data |
| **Verified** | Yes — checks if credential files are readable |

**What to check:**
1. Check if the following database credential files exist AND are readable:
   ```
   ~/.pgpass                          # PostgreSQL
   ~/.my.cnf                          # MySQL/MariaDB
   ~/.mongosh/                        # MongoDB Shell history/config
   ~/.config/redis/                   # Redis config
   ~/.influxdbv2/configs              # InfluxDB
   ~/.cqlshrc                         # Cassandra
   ```
2. For each, run `test -r <path>` (or equivalent stat check)
3. If 2+ database credential paths are readable: **VERIFIED FAIL** — agent can directly access databases
4. If 1 readable: **WARN**
5. If none readable: **VERIFIED PASS**

Report which credential files are exposed but never read their contents.

**Fix:**
```bash
# Restrict permissions on database credential files:
chmod 600 ~/.pgpass ~/.my.cnf ~/.cqlshrc 2>/dev/null
chmod 700 ~/.mongosh/ ~/.config/redis/ 2>/dev/null
# Enable sandbox to isolate agent:
openclaw config set sandbox.mode all
# Best practice: use a separate user for the agent:
sudo -u openclaw-agent openclaw start
```

---

### CLAW-23: Additional Services on 0.0.0.0
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | AutoGPT exposes ports 8000+3000 by default; 17,500+ OpenClaw instances found exposed |
| **Verified** | Yes — checks actual listening sockets |

**What to check:**
1. List all services bound to all interfaces:
   ```bash
   ss -tlnp 2>/dev/null | grep "0.0.0.0" || netstat -tlnp 2>/dev/null | grep "0.0.0.0"
   ```
2. Flag any agent-related services on well-known ports bound to `0.0.0.0`:
   - Port 3000 (web UI frontend)
   - Port 5000 (Flask/API server)
   - Port 8000 (AutoGPT/agent web UI)
   - Port 8080 (HTTP proxy/alternate web UI)
   - Port 18789 (OpenClaw gateway — also covered by CLAW-01)
   - Any port in the range 3000-9999 with agent-related process names
3. If 2+ agent services bound to `0.0.0.0`: **VERIFIED FAIL**
4. If 1 agent service on `0.0.0.0` (besides gateway, which is CLAW-01): **WARN**
5. If all agent services bound to `127.0.0.1`/`localhost`: **PASS**
6. If no additional agent services found: **SKIP**

**Fix:**
```bash
# Bind services to localhost only:
# In docker-compose.yml, change:
#   ports: ["8000:8000"]     →   ports: ["127.0.0.1:8000:8000"]
#   ports: ["3000:3000"]     →   ports: ["127.0.0.1:3000:3000"]
# In agent config, set bind address to 127.0.0.1
# Use a reverse proxy (nginx/caddy) with auth for remote access
```

---

### CLAW-24: No Firewall Rules
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Without a firewall, every exposed port is reachable from the network |
| **Verified** | Yes — checks firewall status |

**What to check:**
1. Check for active firewall rules on the system:
   ```bash
   # Linux:
   sudo iptables -L -n 2>/dev/null | grep -c "^[A-Z]"
   sudo ufw status 2>/dev/null
   sudo nft list ruleset 2>/dev/null | head -5
   # macOS:
   sudo pfctl -s rules 2>/dev/null | head -5
   /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null
   ```
2. If no firewall is active and no rules are configured: **FAIL** — every listening port is reachable
3. If a firewall is active but has no restrictive rules (only default ACCEPT policies): **WARN**
4. If a firewall is active with restrictive rules: **PASS**
5. If the system is a local development machine (not a VPS/server): **SKIP** — home router typically provides NAT

To determine if this is a VPS: check if running on a cloud provider (metadata service responds, or hostname contains common cloud patterns like `ip-`, `.compute.`, `.ec2.`).

**Fix:**
```bash
# Linux (ufw — simplest):
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw enable
# Linux (iptables):
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -j DROP
# macOS:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

---

### CLAW-25: Container Security Profile
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-05 Unexpected Code Running |
| **CVE** | CVE-2025-31133, CVE-2025-52565, CVE-2025-52881 (runC container escape vulnerabilities) |
| **Verified** | Yes — inspects container security configuration |

**What to check:**
1. Detect if running inside Docker: check for `/.dockerenv` file or `cgroup` entries
2. If not in Docker: **SKIP**
3. Check for seccomp profile:
   - Run: `grep -c Seccomp /proc/1/status` — if `Seccomp: 0`, no seccomp profile is applied
   - `Seccomp: 2` means a filter is active: **PASS** for seccomp
4. Check for AppArmor profile:
   - Run: `cat /proc/1/attr/current 2>/dev/null` — if `unconfined`, no AppArmor profile
   - If a named profile is listed: **PASS** for AppArmor
5. Check runC version:
   - `runc --version 2>/dev/null` — vulnerable if below 1.2.8, 1.3.3, or 1.4.0-rc.3
6. If no seccomp AND no AppArmor profile: **VERIFIED FAIL** — container has minimal syscall restrictions
7. If only one of seccomp/AppArmor: **WARN**
8. If both active and runC patched: **PASS**

**Fix:**
```bash
# Apply Docker's default seccomp profile (enabled by default unless --security-opt seccomp=unconfined):
# In docker-compose.yml:
#   security_opt:
#     - seccomp:default
#     - no-new-privileges:true
# Update runC to patched version:
sudo apt update && sudo apt install runc
# Or update Docker Engine which bundles runC:
sudo apt update && sudo apt install docker-ce docker-ce-cli
```

---

### CLAW-26: Agent Code Integrity
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-04 Agentic Supply Chain |
| **Ref** | Uncommitted modifications to agent code could indicate backdoors or tampering |
| **Verified** | Yes — checks git status of agent installation |

**What to check:**
1. Find the OpenClaw installation directory:
   - Check `which openclaw` or `npm list -g openclaw`
   - Common paths: `/usr/lib/node_modules/openclaw/`, `/usr/local/lib/node_modules/openclaw/`, or local `node_modules/openclaw/`
2. If the installation directory is a git repo (or contains `.git`):
   - Run: `git -C <install_dir> status --porcelain 2>/dev/null`
   - If there are modified files: **FAIL** — agent source has been modified from the official release
   - Run: `git -C <install_dir> diff 2>/dev/null | head -50` — report which files changed (not the full diff content)
3. If installed via npm (no .git directory): verify package integrity:
   - Run: `npm ls openclaw` and check the installed version matches expected
4. If no modifications detected: **PASS**
5. If installation directory not found: **SKIP**

**Fix:**
```bash
# Reinstall from official source:
npm install -g openclaw@latest
# Verify integrity after install:
npm audit signatures
# To prevent future tampering, make install directory read-only:
sudo chmod -R a-w /usr/lib/node_modules/openclaw/
```

---

### CLAW-27: npm Post-Install Scripts in Skills
| | |
|---|---|
| **Severity** | HIGH (10 pts) |
| **OWASP** | ASI-04 Agentic Supply Chain |
| **Ref** | ClawHub supply chain attacks: 341 malicious skills used post-install scripts to deliver Atomic Stealer malware |
| **Verified** | Yes — scans actual package.json files |

**What to check:**
1. For each skill directory in `~/.openclaw/skills/*/`:
   - Check if a `package.json` file exists
   - If it does, scan for lifecycle scripts:
     ```
     preinstall, install, postinstall,
     preuninstall, uninstall, postuninstall,
     prepack, postpack, prepare
     ```
   - These scripts run automatically with full user privileges during `npm install`
2. If any skill has `preinstall` or `postinstall` scripts: **FAIL** — report which skills and which scripts
3. If skills have other lifecycle scripts (`prepare`, `prepack`): **WARN**
4. If no lifecycle scripts found in any skill: **PASS**
5. If no skills have `package.json`: **SKIP**

**Fix:**
```bash
# Remove suspicious skills:
rm -rf ~/.openclaw/skills/<suspicious-skill>
# Disable npm lifecycle scripts globally (nuclear option):
npm config set ignore-scripts true
# Or audit before installing:
npm install --ignore-scripts  # Then manually review what scripts would run
# Enable OpenClaw plugin allowlist:
openclaw config set plugins.allow '["trusted-skill-1", "trusted-skill-2"]'
```

---

### CLAW-28: Log Redaction Configuration
| | |
|---|---|
| **Severity** | MEDIUM (5 pts) |
| **CVE** | CVE-2026-22038 (AutoGPT plaintext key logging) |
| **Ref** | Secrets in logs are the #1 accidental exposure vector |

**What to check:**
1. Read `~/.openclaw/openclaw.json` → `logging.redactSensitive`
2. If not set or set to `off`: **FAIL**
3. If set to `tools` (default): **PASS**
4. Bonus: check if `logging.redactPatterns` has custom patterns for the user's specific API key formats

**Fix:**
```bash
openclaw config set logging.redactSensitive tools
```

---

### CLAW-29: Debug Logging Enabled
| | |
|---|---|
| **Severity** | MEDIUM (5 pts) |
| **CVE** | CVE-2026-22038 (AutoGPT plaintext key logging) |
| **Ref** | Debug mode leaks extra data including full request/response payloads with auth headers and API keys |

**What to check:**
1. Read `~/.openclaw/openclaw.json` → `logging.level`
2. Also check environment variables: `OPENCLAW_LOG_LEVEL`, `DEBUG`, `NODE_DEBUG`, `LOG_LEVEL`
3. If logging level is set to `debug`, `verbose`, or `trace`: **FAIL** — full request/response payloads (including API keys in headers) will be written to logs
4. If `DEBUG=*` or `DEBUG=openclaw:*` is set in environment or `.env`: **FAIL**
5. If logging level is `info`, `warn`, or `error`: **PASS**
6. If not explicitly set (defaults apply): **PASS**

**Fix:**
```bash
# Set logging to production-appropriate level:
openclaw config set logging.level warn
# Remove debug environment variables:
# In ~/.openclaw/.env, remove or comment out:
#   DEBUG=*
#   OPENCLAW_LOG_LEVEL=debug
#   NODE_DEBUG=*
# Also ensure log redaction is enabled (see CLAW-28):
openclaw config set logging.redactSensitive tools
```

---

### CLAW-30: Sessions Synced to Cloud
| | |
|---|---|
| **Severity** | MEDIUM (5 pts) |
| **OWASP** | ASI-03 Identity & Privilege Abuse |
| **Ref** | Session history contains conversation data, tool outputs, and potentially leaked secrets — cloud sync uploads this to third-party servers |

**What to check:**
1. Resolve the real path of `~/.openclaw/`: `realpath ~/.openclaw/`
2. Check if the resolved path falls inside any known cloud sync folder:
   ```
   # macOS iCloud:
   ~/Library/Mobile Documents/
   # Dropbox:
   ~/Dropbox/
   # Google Drive:
   ~/Google Drive/
   ~/Library/CloudStorage/GoogleDrive-*/
   # OneDrive:
   ~/OneDrive/
   ~/Library/CloudStorage/OneDrive-*/
   ```
3. Also check if `~/.openclaw/` itself is a symlink pointing into a sync folder
4. If `~/.openclaw/` is inside a cloud sync folder: **FAIL** — all session data, configs, and credentials are being uploaded to the cloud provider
5. If not inside any sync folder: **PASS**

**Fix:**
```bash
# Move .openclaw out of the synced folder:
mv ~/.openclaw /usr/local/var/openclaw
ln -s /usr/local/var/openclaw ~/.openclaw
# Or exclude from sync:
# macOS iCloud: add .nosync extension or use .nosync file
touch ~/.openclaw/.nosync
# Dropbox: use selective sync to exclude .openclaw
# Google Drive: use selective sync settings in Drive app
```

---

## Scoring

### Weights

| Severity | Points per check | Count |
|----------|-----------------|-------|
| CRITICAL | 15 | 21 checks |
| HIGH | 10 | 43 checks |
| MEDIUM | 5 | 8 checks |
| **Total** | **785** | **72 checks** |

### Calculation

```
score = (sum of points for PASSED checks) / (sum of points for all NON-SKIPPED checks) x 100
```

Skipped checks (opt-in declined, not applicable) are excluded from both numerator and denominator.

WARN results count as half points (e.g., a HIGH check with WARN = 5 points instead of 10).

### Grade

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Hardened — no critical findings |
| B | 75-89 | Good — minor improvements needed |
| C | 60-74 | Needs work — some real risks |
| D | 40-59 | Exposed — significant vulnerabilities |
| F | 0-39 | Critical — immediate action required |

---

## Output Format

Present results as:

```
## Have I Been Clawned? — Security Audit

### Hardening Score: [SCORE]/100 — Grade [GRADE]
[████████░░] 80/100

| # | Check | Result | Severity | Ref |
|---|-------|--------|----------|-----|
| 01 | Gateway Network Exposure | ✅ VERIFIED PASS | CRITICAL | CVE-2026-25253 |
| 02 | Gateway Authentication | ❌ VERIFIED FAIL | CRITICAL | CVE-2026-25253 |
| ... | ... | ... | ... | ... |

### Findings

#### ❌ CLAW-02: Gateway Authentication — VERIFIED FAIL
**Why it matters:** Without authentication, anyone who can reach your gateway port can
control your agent and access stored API tokens. 17,500+ OpenClaw instances were found
exposed this way (CVE-2026-25253).

**Fix:**
\`\`\`bash
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"
\`\`\`

[Repeat for each failing check]

### Share your results
[SHAREABLE_URL]
```

---

## Shareable Report URL

Encode results as JSON, then base64url. The URL contains everything — no backend storage needed.

```javascript
const report = {
  v: 3,                // format version
  s: 72,               // hardening score
  g: "C",              // grade
  r: [1,0,1,...],  // 72 results, ordered by check #
  // Values: 1=pass, 0=fail, 2=warn, -1=skip
  t: "2026-02-07"      // date
};
const encoded = btoa(JSON.stringify(report))
  .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const url = `https://haveibeenclawned.com/report?d=${encoded}`;
```

Show to the user:
> **Share your results:** `[URL]`

---

## Anonymous Stats (Opt-in)

If using the script, ask the user to re-run with `--submit` (see "How to run" above).

If running checks individually, POST to `https://haveibeenclawned.com/api/submit`:
```json
{
  "v": 3,
  "s": 72,
  "g": "C",
  "r": [1,0,1,...]
}
```

---

## Contributing

This audit is open source. Add checks, update threat intel, improve fix commands.

### Rule format

Each check follows this structure:

```markdown
### CLAW-XX: Check Name
| | |
|---|---|
| **Severity** | CRITICAL (15 pts) / HIGH (10 pts) / MEDIUM (5 pts) |
| **OWASP** | ASI-XX Reference |
| **CVE** | CVE-XXXX-XXXXX (if applicable) |
| **Verified** | Yes/No — does this check actually test the vulnerability? |

**What to check:**
[Step-by-step instructions an AI agent can follow]

**Fix:**
[Exact commands to remediate]
```

### How to contribute
1. Fork `github.com/wadim/haveibeenclawned`
2. Add your check to `SKILL.md` following the format above
3. Update the check count (currently 72), scoring weights, and report encoding
4. Open a PR with:
   - The new check
   - A reference (CVE, blog post, research paper)
   - Why this check matters (real-world impact)

### Threat intel updates
The known-malicious skills list and CVE version checks are updated regularly. To suggest additions, open an issue with the source reference.