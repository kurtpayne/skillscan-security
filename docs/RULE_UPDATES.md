# Rule Updates

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
