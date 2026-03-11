# Rule Updates

## 2026-03-11

- Added `ABU-005` (high): **MCP tool name-collision hijack marker**.
- Rationale: CVE-2026-30856 disclosures describe malicious remote MCP servers abusing ambiguous client naming conventions (`mcp_{service}_{tool}`) to overwrite trusted tool aliases (for example `tavily_extract`) and hijack tool execution flow.
- Rule scope intentionally targets explicit collision/hijack phrasing from advisory and incident writeups to keep false positives low.

Sources:
- GitLab Advisory DB (2026-03-06, updated 2026-03-09), *CVE-2026-30856*: https://advisories.gitlab.com/pkg/golang/github.com/tencent/weknora/CVE-2026-30856/
- GitHub Advisory DB, *GHSA-67q9-58vj-32qx*: https://github.com/advisories/GHSA-67q9-58vj-32qx
- NVD, *CVE-2026-30856*: https://nvd.nist.gov/vuln/detail/CVE-2026-30856

## 2026-03-09

- Added `MAL-021` (high): **GitHub Actions branch/ref metadata interpolation in run/script**.
- Added `CHN-010` (critical): **`pull_request_target` + branch/ref metadata interpolation chain**.
- Rationale: fresh incident reporting on the `hackerbot-claw` campaign documented branch-name command-substitution payloads executing in privileged workflows when branch refs were interpolated directly into `run:` shell steps.
- Rule scope is intentionally constrained to shell/script contexts (`run:`/`script:`) and high-signal branch/ref metadata fields (`github.head_ref`, `github.ref_name`, `github.event.pull_request.head.ref`, `steps.*.outputs.pr_head_ref`) to reduce false positives.

Sources:
- StepSecurity (2026-03-02), *hackerbot-claw: An AI-Powered Bot Actively Exploiting GitHub Actions*: https://www.stepsecurity.io/blog/hackerbot-claw-github-actions-exploitation
- Orca Security (2026-03-04), *HackerBot-Claw: An AI-Assisted Campaign Targeting GitHub Actions Pipelines*: https://orca.security/resources/blog/hackerbot-claw-github-actions-attack/

## 2026-03-05

- Added `EXF-013` (high): **AI assistant global MCP config injection marker**.
- Rationale: recent SANDWORM_MODE reporting shows malware writing `mcpServers` entries into user-home assistant config files (`~/.cursor/mcp.json`, `~/.claude/settings.json`, Claude Desktop config paths, etc.) so malicious local MCP servers persist outside the infected repository.
- Rule scope intentionally requires both a known assistant config path marker and `mcpServers` + executable `command` fields in the same artifact to keep false positives low.

Sources:
- Socket (2026-02-24), *SANDWORM_MODE: Shai-Hulud-Style npm Worm Hijacks CI Workflow...*: https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning
- The Hacker News (2026-02-24), *Malicious npm Packages Harvest Crypto Keys, CI Secrets, and API Tokens*: https://thehackernews.com/2026/02/malicious-npm-packages-harvest-crypto.html

## 2026-03-03

- Added `MAL-017` (high): **WebSocket C2 shell execution marker**.
- Rationale: newly reported npm malware clusters include install-time RAT behavior that opens persistent WebSocket channels and executes attacker-delivered shell commands in developer environments.
- Rule scope is intentionally constrained to install-script context (`preinstall`/`postinstall` or `install.js`-style loader markers) plus explicit WebSocket C2 and shell-exec indicators to keep false positives low.

Sources:
- The Hacker News (2026-03-02), *North Korean Hackers Publish 26 npm Packages Hiding Pastebin C2 for Cross-Platform RAT*: https://thehackernews.com/2026/03/north-korean-hackers-publish-26-npm.html
- Socket (2026-03-02), *StegaBin: 26 Malicious npm Packages Use Pastebin Steganography*: https://socket.dev/blog/stegabin-26-malicious-npm-packages-use-pastebin-steganography

## 2026-03-02

- Added `MAL-016` (high): **Pastebin steganographic dead-drop resolver marker**.
- Rationale: multiple newly reported npm packages (StegaBin cluster) used hardcoded Pastebin dead-drop URLs with `|||` + `===END===` decoding markers to reconstruct Vercel C2 domains before staging payload execution.
- Rule scope intentionally requires all core markers (`pastebin.com/<id>`, `|||`, `===END===`, and `vercel.app`) in the same artifact to keep false positives low.

Sources:
- Socket (2026-03-02), *StegaBin: 26 Malicious npm Packages Use Pastebin Steganography*: https://socket.dev/blog/stegabin-26-malicious-npm-packages-use-pastebin-steganography
- The Hacker News (2026-03-02), *North Korean Hackers Publish 26 npm Packages Hiding Pastebin C2 for Cross-Platform RAT*: https://thehackernews.com/2026/03/north-korean-hackers-publish-26-npm.html

## 2026-02-25

- Added `MAL-012` (high): **VS Code task autorun-on-folder-open marker**.
- Rationale: recent GitHub Codespaces research highlighted abuse of repository-supplied VS Code configuration files where tasks auto-run on folder open with no additional prompts, enabling command execution and token/secret theft chains.
- This rule flags explicit `runOn: folderOpen` task autorun markers so reviewers can block or gate repository-defined auto-execution behavior.

Sources:
- Infosecurity Magazine (2026-02-22), *Malicious Commands in GitHub Codespaces Enable RCE*: https://www.infosecurity-magazine.com/news/malicious-commands-in-github/
- Orca Security (2026-02), *Hacking GitHub Codespaces: RCE & Supply Chain Risks*: https://orca.security/resources/blog/hacking-github-codespaces-rce-supply-chain-attack/

## 2026-02-18

- Added `SUP-005` (high): **npm preinstall/postinstall inline Node eval pattern**.
- Rationale: recent npm supply-chain incident reporting continues to show install-time execution abuse, and lifecycle scripts using `node -e` / `node --eval` provide a compact way to hide malicious child-process execution without committed script files.
- This rule is scoped only to `preinstall`/`postinstall` keys to keep false positives lower than generic `node -e` matching.

Sources:
- The Hacker News (2026-02), *Compromised dYdX npm and PyPI Packages Deliver Wallet Stealers and RAT Malware*: https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html
- The Hacker News (2026-02), *npm’s Update to Harden Their Supply Chain, and Points to Consider*: https://thehackernews.com/2026/02/npms-update-to-harden-their-supply.html

## 2026-02-11

- Added `MAL-006` (high): **PowerShell web request piped to Invoke-Expression**.
- Rationale: recent ClickFix-style and infostealer campaigns continue to use copy/paste bootstrap commands that fetch remote PowerShell and execute in memory (`iwr|irm ... | iex`, `Invoke-Expression (irm ...)`).
- This rule targets high-signal static strings with low ambiguity and avoids broad PowerShell-only matching.

Sources:
- Microsoft Security Blog (2026-02-02), *Infostealers without borders: macOS, Python stealers, and platform abuse* — discusses ClickFix-style copy/paste command execution and in-memory script pipelines: https://www.microsoft.com/en-us/security/blog/2026/02/02/infostealers-without-borders-macos-python-stealers-and-platform-abuse/
- The Hacker News (2026-01), *CrashFix Chrome Extension Delivers ModeloRAT Using ClickFix-Style Browser Crash Lures* — reports clipboard-pasted Run dialog commands used to execute payloads: https://thehackernews.com/2026/01/crashfix-chrome-extension-delivers.html
