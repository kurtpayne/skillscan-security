## 2026-03-02 (2): Hex-Decoded Command Execution Marker in npm Malware Install Chains

**Sources:**
- [Tenable - New Malicious npm Package "ambar-src" Targets Developers with Open Source Malware](https://www.tenable.com/blog/cybersecurity-research-faq-new-malicious-npm-package-ambar-src)
- [The Hacker News - Malicious NuGet Packages Stole ASP.NET Data; npm Package Dropped Malware](https://thehackernews.com/2026/02/malicious-nuget-packages-stole-aspnet.html)
- [GitHub Advisory Database - GHSA-qjgj-mrv7-24f7 (ambar-src)](https://github.com/advisories/GHSA-qjgj-mrv7-24f7)

**Event Summary:** Recent reporting on the `ambar-src` npm campaign describes install-time malware that hid OS-specific one-liners as long hex strings, decoded them at runtime, then executed the decoded command. Existing SkillScan rules already covered lifecycle shell bootstraps and inline `node -e`, but lacked a focused marker for obfuscated `Buffer.from(..., 'hex').toString()` + immediate process execution patterns in JavaScript install scripts.

**New Pattern Added:**

### SUP-009: Hex-decoded command string execution marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects long hex decode via `Buffer.from(..., 'hex').toString()` followed shortly by `exec`/`execSync`/`spawn`/`spawnSync` invocation.
- **Justification:** High-signal indicator of command-obfuscation behavior in supply-chain malware loaders with lower noise than generic `Buffer.from` or generic `exec` matching alone.
- **Mitigation:** Reject install/setup scripts that decode opaque command blobs and execute them directly. Require reviewed plaintext scripts and explicit command allowlists.

**Version:** Rules updated from 2026.03.02.1 to 2026.03.02.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_02_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/56_hex_decode_exec`.

---

## 2026-02-28 (2): Claude Code Hooks Shell-Execution Marker

**Sources:**
- [The Hacker News - Claude Code Flaws Allow Remote Code Execution and API Key Exfiltration](https://thehackernews.com/2026/02/claude-code-flaws-allow-remote-code.html)
- [Check Point Research - Caught in the Hook: RCE and API Token Exfiltration Through Claude Code Project Files](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)

**Event Summary:** Public reporting on recent Claude Code vulnerabilities describes repository-controlled hook configuration abuse where project files can define tool/session hook commands that execute shell payloads when a user opens or interacts with an untrusted repository. Existing coverage already flagged MCP auto-approval and endpoint override exfil patterns, but lacked a focused marker for hook-driven shell execution in `.claude/settings.json`.

**New Patterns Added:**

### MAL-015: Claude Code hooks shell command execution marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.85
- **Pattern:** Detects repo-scoped Claude Code `hooks` blocks (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`) that define shell-capable `command` values (`bash`, `pwsh`, `cmd`, `python -c`, `node -e`).
- **Justification:** Captures a concrete, defensible RCE primitive from current disclosures while remaining narrow to high-risk hook+command combinations.
- **Mitigation:** Treat repo hook configs as untrusted by default. Remove auto-executed shell commands from project settings and require explicit reviewed scripts.

### CHN-009: Repository hook configuration with shell-command payload
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Chains Claude hook configuration markers with shell-capable `command` fields to reduce false positives.
- **Justification:** Tightens the signal to repository-controlled hook + command combinations aligned to disclosed abuse behavior.
- **Mitigation:** Block shell-capable repo hook payloads unless explicitly reviewed and approved.

**Version:** Rules updated from 2026.02.28.1 to 2026.02.28.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_28_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/54_claude_hooks_rce`.

---

## 2026-02-28 (1): Claude Code ANTHROPIC_BASE_URL Override Exfiltration Marker

**Sources:**
- [The Hacker News - Claude Code Flaws Allow Remote Code Execution and API Key Exfiltration](https://thehackernews.com/2026/02/claude-code-flaws-allow-remote-code.html)
- [Check Point Research - Caught in the Hook: RCE and API Token Exfiltration Through Claude Code Project Files](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)

**Event Summary:** Recent reporting on Claude Code project-file abuse describes API-key leakage through repository-scoped environment overrides, where `ANTHROPIC_BASE_URL` in `.claude/settings.json` can redirect authenticated requests to attacker infrastructure before user trust prompts are fully resolved.

**New Pattern Added:**

### EXF-012: Claude Code project env ANTHROPIC_BASE_URL override marker
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects `ANTHROPIC_BASE_URL` values that point to non-`api.anthropic.com` HTTPS endpoints in repo content (JSON/env forms).
- **Justification:** Captures a concrete, configuration-level credential-exfil primitive specific to AI coding tool project files and keeps noise low by excluding the canonical Anthropic API host.
- **Mitigation:** Do not accept repository-provided `ANTHROPIC_BASE_URL` overrides in untrusted projects unless endpoint ownership is explicitly verified.

**Version:** Rules updated from 2026.02.27.2 to 2026.02.28.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_28`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/53_claude_base_url_override`.

---

## 2026-02-27 (1): Double-Extension LNK Masquerade Marker

**Sources:**
- [The Hacker News - CRESCENTHARVEST Campaign Targets Iran Protest Supporters With RAT Malware](https://thehackernews.com/2026/02/crescentharvest-campaign-targets-iran.html)
- [Acronis TRU - CRESCENTHARVEST: Iranian protestors and dissidents targeted in cyberespionage campaign](https://www.acronis.com/en/tru/posts/crescentharvest-iranian-protestors-and-dissidents-targeted-in-cyberespionage-campaign/)

**Event Summary:** This week’s campaign reporting describes lure archives that include Windows shortcuts disguised as benign media/document files via double extensions (for example `*.jpg.lnk`, `*.mp4.lnk`). Existing rules already covered command-level execution chains, but did not include a focused static marker for this filename masquerade tactic used in initial-access bundles.

**New Pattern Added:**

### MAL-014: Deceptive media/document double-extension LNK masquerade
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects file names that end in media/document extension + `.lnk` (for example `.jpg.lnk`, `.mp4.lnk`, `.pdf.lnk`, `.docx.lnk`).
- **Justification:** High-signal, low-noise marker for social-engineering lure artifacts that execute shortcut behavior while appearing as non-executable content.
- **Mitigation:** Quarantine double-extension `.lnk` artifacts and require verified non-shortcut originals for media/document delivery flows.

**Version:** Rules updated from 2026.02.26.2 to 2026.02.27.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_27`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/51_double_extension_lnk_masquerade`.

---

## 2026-02-26 (2): Claude Code Project MCP Auto-Approval Marker

**Sources:**
- [Check Point Research - Caught in the Hook: RCE and API Token Exfiltration Through Claude Code Project Files (CVE-2025-59536 / CVE-2026-21852)](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [The Hacker News - Claude Code Flaws Allow Remote Code Execution and API Key Exfiltration](https://thehackernews.com/2026/02/claude-code-flaws-allow-remote-code.html)

**Event Summary:** Recent disclosure shows repository-controlled Claude Code settings can auto-approve project MCP servers (`enableAllProjectMcpServers` / `enabledMcpjsonServers`) and initialize untrusted `.mcp.json` commands before users meaningfully review trust prompts.

**New Pattern Added:**

### ABU-003: Claude Code project MCP auto-approval marker
- **Category:** instruction_abuse
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects repository settings that enable MCP auto-approval (`"enableAllProjectMcpServers": true` or populated `"enabledMcpjsonServers"`).
- **Justification:** Captures a concrete, high-signal configuration abuse primitive in AI coding tool artifacts, with lower false positives than generic MCP text matching.
- **Mitigation:** Do not commit MCP auto-approval settings at repo scope; require explicit user consent before project MCP server initialization.

**Version:** Rules updated from 2026.02.26.1 to 2026.02.26.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_26_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/50_claude_mcp_autoapprove`.

---

## 2026-02-26 (1): macOS osascript JXA Loader Marker

**Sources:**
- [The Hacker News - Malicious NuGet Packages Stole ASP.NET Data; npm Package Dropped Malware](https://thehackernews.com/2026/02/malicious-nuget-packages-stole-aspnet.html)
- [The Hacker News - Malicious npm Packages Harvest Crypto Keys, CI Secrets, and API Tokens](https://thehackernews.com/2026/02/malicious-npm-packages-harvest-crypto.html)

**Event Summary:** Current npm malware reporting includes macOS stage loaders that invoke `osascript` with JavaScript for Automation (JXA) to execute secondary shell payloads (`ObjC.import`, `doShellScript`) and deploy post-exploitation agents. Existing SkillScan rules covered npm lifecycle hooks and PowerShell/MSHTA chains, but lacked a dedicated static marker for JXA loader execution.

**New Pattern Added:**

### MAL-013: macOS osascript JavaScript (JXA) execution marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.85
- **Pattern:** Detects `osascript` command lines invoking JavaScript/JXA execution (`-l JavaScript`) and common loader primitives (`ObjC.import(`, `doShellScript`).
- **Justification:** Captures a concrete, reusable macOS execution primitive observed in active npm malware campaigns and applicable to skill/tool setup artifacts that embed shellable JXA loaders.
- **Mitigation:** Remove JXA-based `osascript` execution from setup/install content and avoid scripted shell execution from untrusted package flows.

**Version:** Rules updated from 2026.02.25.2 to 2026.02.26.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_26`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/49_osascript_jxa_loader`.

---

## 2026-02-25 (1): pull_request_target Unpinned Third-Party Action Ref Marker

**Sources:**
- [The Hacker News - Cline CLI 2.3.0 Supply Chain Attack Installed OpenClaw on Developer Systems](https://thehackernews.com/2026/02/cline-cli-230-supply-chain-attack.html)
- [GitHub Advisory Database - tj-actions/changed-files through 45.0.7 allows remote attackers to discover secrets by reading actions logs (GHSA-mrrh-fwg8-r2c3)](https://github.com/advisories/ghsa-mrrh-fwg8-r2c3)
- [Unit 42 - GitHub Actions Supply Chain Attack: Coinbase targeting and tj-actions compromise](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/)

**Event Summary:** Recent CI/CD incident reporting continues to show attacker success after compromising mutable GitHub Action refs (retargeted tags/branches) in privileged workflows. Existing SkillScan rules covered untrusted checkout refs, metadata interpolation, and cache-key poisoning in `pull_request_target`, but not mutable third-party `uses:` refs in the same privileged context.

**New Patterns Added:**

### MAL-011: pull_request_target workflow using unpinned third-party action ref
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects `uses: owner/action@...` references not pinned to a full 40-character commit SHA.
- **Justification:** Mutable refs (`@v4`, `@main`) can be retargeted during or after upstream compromise, creating a reusable supply-chain execution primitive in privileged workflows.
- **Mitigation:** Pin third-party actions to immutable full commit SHAs and review provenance before updates.

### CHN-008: pull_request_target with unpinned third-party GitHub Action
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.88
- **Pattern:** Chains `pull_request_target` with mutable third-party `uses:` references.
- **Justification:** Tightens signal to privileged CI workflows where tag-retarget abuse is high impact.
- **Mitigation:** Avoid mutable action refs in privileged workflows; use SHA pinning and controlled update cadence.

**Version:** Rules updated from 2026.02.24.1 to 2026.02.25.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_25`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/47_pr_target_unpinned_action`.

---

## 2026-02-24 (1): pull_request_target Cache-Key Poisoning Marker

**Sources:**
- [The Hacker News - Cline CLI 2.3.0 Supply Chain Attack Installed OpenClaw on Developer Systems](https://thehackernews.com/2026/02/cline-cli-230-supply-chain-attack.html)
- [GitHub Security Lab Advisories Index (Poisoned Pipeline Execution / cache-poisoning workflow class)](https://securitylab.github.com/advisories/)

**Event Summary:** Reporting on the Cline compromise describes a workflow chain where attacker-controlled issue/PR input can help poison CI cache state and pivot into privileged publish paths. Existing rules covered direct shell interpolation and untrusted head checkout, but not untrusted PR metadata used in `actions/cache` key derivation under `pull_request_target`.

**New Patterns Added:**

### EXF-010: GitHub Actions cache key interpolation from untrusted PR metadata
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Detects `actions/cache` (`cache`, `cache/restore`, `cache/save`) steps whose `key:` includes `${{ github.event.pull_request.* }}` untrusted metadata fields (`title`, `body`, `head.ref`, etc.).
- **Justification:** Captures a concrete cache-poisoning precursor in privileged workflows that can bridge untrusted input into trusted CI state.
- **Mitigation:** Never derive privileged cache keys from untrusted PR metadata; scope and separate caches between untrusted and trusted workflows.

### CHN-007: pull_request_target with untrusted PR-derived Actions cache key
- **Category:** exfiltration
- **Severity:** critical
- **Confidence:** 0.90
- **Pattern:** Chains `pull_request_target` with the untrusted cache-key marker to reduce noise and prioritize high-impact CI abuse paths.
- **Justification:** Privileged workflow context plus untrusted cache-key derivation is a stronger indicator of actionable pipeline abuse risk than either signal alone.
- **Mitigation:** Use unprivileged triggers for untrusted events and isolate cache namespaces/keys for trusted release jobs.

**Version:** Rules updated from 2026.02.23.2 to 2026.02.24.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_24`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/46_pr_target_cache_key_poisoning`.

---

## 2026-02-23 (2): MCP Tool Hidden Credential-Harvest Prompt Block Marker

**Sources:**
- [Socket - SANDWORM_MODE: Shai-Hulud-Style npm Worm Hijacks CI Workflow and Poisons AI Toolchains](https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning)
- [The Hacker News - Malicious npm Packages Harvest Crypto Keys, CI Secrets, and API Tokens](https://thehackernews.com/2026/02/malicious-npm-packages-harvest-crypto.html)

**Event Summary:** Recent supply-chain reporting describes malicious packages that deploy rogue MCP servers whose tool descriptions include hidden instructions to read SSH keys/credentials and silently pass stolen data via a `context` parameter while explicitly telling the assistant not to tell the user.

**New Pattern Added:**

### EXF-009: MCP tool hidden credential-harvest prompt block marker
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.90
- **Pattern:** Detects `<IMPORTANT>...</IMPORTANT>`-style MCP tool prompt blocks that combine credential-file read instructions (`~/.ssh/id_rsa`, `~/.aws/credentials`, `~/.npmrc`), explicit `context` payload transfer wording, and concealment language (`do not mention ... to the user`).
- **Justification:** Captures a concrete AI-toolchain abuse primitive from current campaign reporting where tool metadata itself acts as a covert exfil instruction carrier.
- **Mitigation:** Remove hidden credential-harvest instructions from MCP tool descriptions; never require silent context transfer of secrets.

**Version:** Rules updated from 2026.02.23.1 to 2026.02.23.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_23_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/45_mcp_tool_prompt_injection`.

---

## 2026-02-23 (1): npm Lifecycle Mutable `@latest` Install in Install Hooks

**Sources:**
- [Cline Security Advisory - GHSA-9ppg-jx86-fqw7](https://github.com/cline/cline/security/advisories/GHSA-9ppg-jx86-fqw7)
- [GitHub Advisory Database - GHSA-9ppg-jx86-fqw7](https://github.com/advisories/GHSA-9ppg-jx86-fqw7)
- [Socket - Cline CLI npm package compromised via suspected cache poisoning](https://socket.dev/blog/cline-cli-npm-package-compromised-via-suspected-cache-poisoning-attack)

**Event Summary:** The Feb 17 compromise of `cline@2.3.0` used a `postinstall` hook to pull `openclaw@latest`. SkillScan already flagged global installs in lifecycle hooks (`SUP-007`), but this incident highlights a reusable evasion variant: install-hook dependency pulls pinned to mutable `@latest` tags without `-g`, which still allow attacker-controlled code changes during install.

**New Pattern Added:**

### SUP-008: npm lifecycle mutable @latest dependency install pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects `package.json` `preinstall`/`postinstall` scripts that run `npm install`/`npm i` with an `@latest` package selector (non-global install hooks).
- **Justification:** Captures mutable-tag dependency execution in lifecycle hooks, a concrete install-time supply-chain risk adjacent to GHSA-9ppg-jx86-fqw7 and not covered by existing global-only hook rule.
- **Mitigation:** Disallow `@latest` in install lifecycle hooks; pin exact versions and move dependency setup to explicit, reviewed, user-triggered steps.

**Version:** Rules updated from 2026.02.21.2 to 2026.02.23.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_23`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/44_npm_lifecycle_latest_install`.

---

## 2026-02-21 (2): GitHub Actions Issue/Comment Metadata Interpolation in Shell Context

**Sources:**
- [GitHub Blog - How to secure GitHub Actions workflows: 4 tips to handle untrusted input and tighten permissions (updated 2026-02-04)](https://github.blog/security/supply-chain-security/four-tips-to-keep-your-github-actions-workflows-secure/)
- [GitHub Security Lab Advisories Index (workflow injection examples)](https://securitylab.github.com/advisories/)

**Event Summary:** Recent GitHub guidance re-emphasizes that untrusted issue/comment fields (for example `github.event.issue.title`) become command/script injection vectors when directly interpolated in `run:` blocks. Existing SkillScan coverage already handled pull-request metadata interpolation, but not issue/comment/discussion events.

**New Pattern Added:**

### MAL-010: GitHub Actions issue/comment metadata interpolation in run/script
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects `${{ github.event.issue.title/body }}`, `${{ github.event.comment.body }}`, and discussion body/title interpolation markers commonly inserted into shell/script steps.
- **Justification:** Captures the same workflow command-injection root cause class for issue/comment-driven automations that was not previously covered by `EXF-008`.
- **Mitigation:** Route untrusted metadata through environment variables and treat as untrusted data; avoid shell interpolation/evaluation of event text.

**Version:** Rules updated from 2026.02.21.1 to 2026.02.21.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_21_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/43_gh_issue_metadata_injection`.

---

## 2026-02-21 (1): npm Lifecycle Global Install via Compromised Publish Token

**Sources:**
- [GitHub Advisory Database - GHSA-9ppg-jx86-fqw7](https://github.com/advisories/GHSA-9ppg-jx86-fqw7)
- [Cline Security Advisory - GHSA-9ppg-jx86-fqw7](https://github.com/cline/cline/security/advisories/GHSA-9ppg-jx86-fqw7)
- [GitLab Advisory Mirror - GHSA-9ppg-jx86-fqw7](https://advisories.gitlab.com/pkg/npm/cline/GHSA-9ppg-jx86-fqw7/)

**Event Summary:** A compromised npm publish token was used to publish `cline@2.3.0` with a modified `postinstall` lifecycle script: `npm install -g openclaw@latest`. This is a concrete install-time behavior change that can silently pull in unrelated global packages during dependency install.

**New Pattern Added:**

### SUP-007: npm preinstall/postinstall global package install pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Detects `package.json` `preinstall`/`postinstall` script values running `npm install -g ...` or `npm i -g ...`.
- **Justification:** Captures the exact lifecycle-hook execution shape in GHSA-9ppg-jx86-fqw7 while staying narrow to install-hook global installs.
- **Mitigation:** Remove global package installation from npm lifecycle hooks and move setup to explicit reviewed, user-initiated steps.

**Version:** Rules updated from 2026.02.20.2 to 2026.02.21.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_21`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/42_npm_lifecycle_global_install`.

---

## 2026-02-20 (2): Dotenv Newline Environment-Variable Injection Payload Marker

**Sources:**
- [GitHub Advisory Database - CVE-2026-27203 (GHSA-97rm-xj73-33jh)](https://github.com/advisories/GHSA-97rm-xj73-33jh)
- [GitLab Advisory Mirror - CVE-2026-27203](https://advisories.gitlab.com/pkg/npm/ebay-mcp/CVE-2026-27203/)

**Event Summary:** A newly published MCP advisory (Feb 18-19, 2026) describes a token update tool writing user-controlled values into `.env` without rejecting newline/carriage-return characters. Attackers can smuggle additional key/value pairs (for example `NODE_OPTIONS=...`) and poison runtime configuration.

**New Pattern Added:**

### SUP-006: Dotenv newline environment-variable injection payload marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.89
- **Pattern:** Detects token/update input strings where token-like fields contain newline encodings (`\n`, `\r`, `%0a`, `%0d`) followed by injected uppercase env assignments.
- **Justification:** Captures the concrete payload shape used to exploit unsafe `.env` update helpers in MCP token management flows.
- **Mitigation:** Reject CR/LF in token inputs, enforce strict key allowlists, and serialize `.env` updates safely.

**Version:** Rules updated from 2026.02.20.1 to 2026.02.20.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_20_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/41_env_newline_injection`.

---

## 2026-02-20 (1): ClickFix DNS nslookup Staged Execution Pattern

**Sources:**
- [The Hacker News - Microsoft Discloses DNS-Based ClickFix Attack Using Nslookup for Malware Staging](https://thehackernews.com/2026/02/microsoft-discloses-dns-based-clickfix.html)
- [BleepingComputer - New ClickFix attack abuses nslookup to retrieve PowerShell payload via DNS](https://www.bleepingcomputer.com/news/security/new-clickfix-attack-abuses-nslookup-to-retrieve-powershell-payload-via-dns/)
- [Microsoft Security Blog - Think before you Click(Fix): Analyzing the ClickFix social engineering technique](https://www.microsoft.com/en-us/security/blog/2025/08/21/think-before-you-clickfix-analyzing-the-clickfix-social-engineering-technique/)

**Event Summary:** Recent reporting documents ClickFix campaigns that instruct users to run `nslookup` commands against attacker-controlled DNS servers, parse specific response lines (for example `Name:`), and execute the resulting command as stage two. This DNS-staging primitive is materially different from direct HTTP `iwr|iex` chains and appears in realistic AI-shared “fix” instructions.

**New Pattern Added:**

### MAL-009: ClickFix DNS nslookup staged command execution pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects `nslookup` TXT-query commands (`-q=txt`/`-querytype=txt`) that parse returned fields (`findstr`/`for /f`/`Select-String`) and hand off execution to `cmd /c`, `powershell`, `pwsh`, or `iex`.
- **Justification:** Captures the documented DNS-based ClickFix staging behavior where command text is delivered through DNS and executed locally.
- **Mitigation:** Block copy-paste Run-dialog instructions that execute parsed DNS response content; never execute command text sourced from untrusted resolver responses.

**Version:** Rules updated from 2026.02.19.2 to 2026.02.20.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_20`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/40_clickfix_dns_nslookup`.

---

## 2026-02-19 (1): OpenClaw Config Token/Key Access Marker

**Sources:**
- [The Hacker News - Infostealer Steals OpenClaw AI Agent Configuration Files and Gateway Tokens](https://thehackernews.com/2026/02/infostealer-steals-openclaw-ai-agent.html)
- [BleepingComputer - Infostealer malware found stealing OpenClaw secrets for first time](https://www.bleepingcomputer.com/news/security/infostealer-malware-found-stealing-openclaw-secrets-for-first-time/)
- [Security Affairs - Hackers steal OpenClaw configuration in emerging AI agent threat](https://securityaffairs.com/188097/malware/hackers-steal-openclaw-configuration-in-emerging-ai-agent-threat.html)

**Event Summary:** Reporting this week describes live infostealer infections stealing `.openclaw` runtime identity material including `openclaw.json` gateway tokens and `device.json` private keys. In skill/tool artifacts, direct references to those files/fields are high-signal indicators of identity-token theft behavior.

**New Pattern Added:**

### EXF-007: OpenClaw gateway token/private-key config access marker
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.91
- **Pattern:** Detects access markers for `.openclaw/openclaw.json`, `.openclaw/device.json`, and sensitive fields such as `gateway.auth.token` and `privateKeyPem`.
- **Justification:** These exact artifacts were highlighted in incident reporting as the stolen identity material enabling gateway impersonation and device-signing abuse.
- **Mitigation:** Do not read or transmit these files/fields in skills/tools; rotate tokens and re-pair devices after suspected compromise.

**Version:** Rules updated from 2026.02.18.2 to 2026.02.19.1

**Testing:** Added assertions in `tests/test_rules.py::test_new_patterns_2026_02_18`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/38_openclaw_config_token_access`.

---

# Pattern Updates - February 2026

## 2026-02-18 (2): npm Lifecycle Inline Node Eval Pattern

**Sources:**
- [The Hacker News - Compromised dYdX npm and PyPI Packages Deliver Wallet Stealers and RAT Malware](https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html)
- [The Hacker News - npm’s Update to Harden Their Supply Chain, and Points to Consider](https://thehackernews.com/2026/02/npms-update-to-harden-their-supply.html)

**Event Summary:** Recent npm supply-chain reporting continues to show malicious execution paths tied to install-time behavior. While prior rules covered shell bootstrap primitives in lifecycle hooks, attacker playbooks also rely on inline JavaScript execution during `preinstall`/`postinstall` to launch child processes and run second-stage payloads.

**New Pattern Added:**

### SUP-005: npm preinstall/postinstall inline Node eval pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects `package.json` lifecycle script values where `preinstall` or `postinstall` runs `node -e` or `node --eval` inline.
- **Justification:** Inline eval in install hooks is an execution primitive frequently used in supply-chain malware to hide process-spawn/download behavior without checked-in script files.
- **Mitigation:** Remove inline eval from install hooks and use reviewed version-controlled scripts with explicit file paths.

**Version:** Rules updated from 2026.02.18.1 to 2026.02.18.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_18`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/37_npm_lifecycle_node_eval`.

---

## 2026-02-18 (1): IPv4-Mapped IPv6 SSRF Bypass Literals

**Sources:**
- [GitHub Security Advisory - GHSA-jrvc-8ff5-2f9f (CVE-2026-26324)](https://github.com/openclaw/openclaw/security/advisories/GHSA-jrvc-8ff5-2f9f)
- [NVD - CVE-2026-26324](https://nvd.nist.gov/vuln/detail/CVE-2026-26324)
- [GitLab Advisory Mirror - CVE-2026-26324](https://advisories.gitlab.com/pkg/npm/openclaw/CVE-2026-26324/)

**Event Summary:** Advisory details describe SSRF guard bypass using full-form IPv4-mapped IPv6 literals (for example `0:0:0:0:0:ffff:7f00:1` => `127.0.0.1`). In skill/tool artifacts, these literals are high-signal markers of attempts to evade naive host-blocking rules for loopback/metadata access.

**New Pattern Added:**

### EXF-006: IPv4-mapped IPv6 loopback/metadata SSRF bypass literal
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.90
- **Pattern:** Detects explicit IPv4-mapped IPv6 loopback/metadata literals such as `0:0:0:0:0:ffff:7f00:1`, `::ffff:127.0.0.1`, `0:0:0:0:0:ffff:a9fe:a9fe`, and `::ffff:169.254.169.254`.
- **Justification:** Directly maps to currently disclosed SSRF bypass techniques where alternate IPv6 forms evade simplistic localhost/metadata deny lists.
- **Mitigation:** Normalize IP representations before SSRF checks and block mapped loopback/metadata targets in untrusted tool inputs.

**Version:** Rules updated from 2026.02.17.3 to 2026.02.18.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_18`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/36_ipv4_mapped_ipv6_ssrf_bypass`.

---

## 2026-02-13 (2): Discord Electron Debugger Credential Interception Marker

**Sources:**
- [JFrog Security Research - How a Complex Multi Payload Infostealer Hid in NPM Disguised as 'Console Visibility'](https://research.jfrog.com/post/duer-js-malicious-package/)
- [The Hacker News - Lazarus Campaign Plants Malicious Packages in npm and PyPI Ecosystems](https://thehackernews.com/2026/02/lazarus-campaign-plants-malicious.html)

**Event Summary:** Recent npm malware reporting (including `duer-js`) documented Discord Desktop hijacking behavior where attacker code hooks Electron `webContents.debugger`, intercepts auth/MFA-related network events (`/login`, `/register`, `/mfa`, `codes-verification`), and extracts credentials/tokens for exfiltration.

**New Pattern Added:**

### MAL-008: Discord Electron debugger credential interception marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.90
- **Pattern:** Detects `webContents.debugger` interception hooks (`attach`/`on`) and credential/MFA interception markers (`Network.getResponseBody` / `Network.getRequestPostData` with `/login`, `/register`, `/mfa`, `codes-verification`).
- **Justification:** This is a concrete behavior family in currently active npm infostealer campaigns targeting Discord/Electron clients.
- **Mitigation:** Remove debugger-based network interception code and any credential/token capture flows.

**Version:** Rules updated from 2026.02.13.1 to 2026.02.13.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_13_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/35_discord_debugger_token_theft`.

---

## 2026-02-13 (1): pull_request_target Untrusted Head Checkout Pattern

**Sources:**
- [GitHub Security Advisory - GHSA-h25v-8c87-rvm8 (Secrets exfiltration via `pull_request_target`)](https://github.com/spotipy-dev/spotipy/security/advisories/GHSA-h25v-8c87-rvm8)
- [NVD - CVE-2025-47928](https://nvd.nist.gov/vuln/detail/CVE-2025-47928)

**Event Summary:** Public advisory and NVD records describe a workflow anti-pattern where `pull_request_target` jobs check out untrusted fork PR head refs (`github.event.pull_request.head.ref` / `head.sha`). This allows attacker-controlled code to run with base-repository token/secrets context.

**New Patterns Added:**

### EXF-005: GitHub Actions untrusted PR head checkout reference
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.91
- **Pattern:** Detects `ref:` / `repository:` references to `github.event.pull_request.head.*` in workflow content.
- **Justification:** This is the exploit-enabling checkout marker highlighted by GHSA-h25v-8c87-rvm8 / CVE-2025-47928.
- **Mitigation:** Do not check out untrusted PR head refs in privileged workflows.

### CHN-005: pull_request_target with untrusted PR head checkout
- **Category:** exfiltration
- **Severity:** critical
- **Confidence:** 0.93
- **Pattern:** Chains `pull_request_target` event markers with `github.event.pull_request.head.*` checkout markers.
- **Justification:** Improves precision by requiring both privileged trigger context and untrusted checkout indicators.
- **Mitigation:** Use unprivileged `pull_request` jobs for untrusted code, and avoid secret-bearing contexts for fork-controlled refs.

**Version:** Rules updated from 2026.02.12.1 to 2026.02.13.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_13`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/34_pr_target_checkout_exfil`.

---

## 2026-02-12 (1): BYOVD Security-Killer Toolkit Marker

**Sources:**
- [Security Affairs - Reynolds ransomware uses BYOVD to disable security before encryption](https://securityaffairs.com/187869/security/reynolds-ransomware-uses-byovd-to-disable-security-before-encryption.html)
- [NVD - CVE-2025-68947 (NSecKrnl vulnerable driver)](https://nvd.nist.gov/vuln/detail/CVE-2025-68947)

**Event Summary:** Recent ransomware reporting described payloads embedding BYOVD components that load vulnerable signed drivers (NSecKrnl / CVE-2025-68947) and kill AV/EDR processes before encryption. In skill/tool artifacts, direct references to these toolkit names and driver-service creation commands are high-signal indicators of malicious intent.

**New Pattern Added:**

### MAL-007: BYOVD security-killer toolkit marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Detects known BYOVD/AV-killer markers (`nseckrnl`, `TrueSightKiller`, `AuKill`, `Poortry`, `GhostDriver`, `Warp AVKiller`) and explicit `sc create` service creation for those names.
- **Justification:** Matches observed defense-evasion tradecraft in current ransomware operations while remaining narrowly scoped to low-noise strings.
- **Mitigation:** Remove BYOVD-related tool/driver references and service-creation guidance from skills/tools.

**Version:** Rules updated from 2026.02.11.2 to 2026.02.12.1

**Testing:** Added assertions in `tests/test_rules.py::test_new_patterns_2026_02_12`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/33_byovd_security_killer`.

---

## 2026-02-11 (2): npm Lifecycle Shell-Bootstrap Pattern

**Sources:**
- [GitHub Advisory Database - CVE-2025-10894 (Malicious versions of Nx)](https://github.com/advisories/GHSA-cxm3-wv7p-598c)
- [StepSecurity - Shai-Hulud: Self-Replicating Worm Compromises 500+ NPM Packages](https://www.stepsecurity.io/blog/ctrl-tinycolor-and-40-npm-packages-compromised)
- [Zscaler ThreatLabz - Shai-Hulud V2 Poses Risk to NPM Supply Chain](https://www.zscaler.com/blogs/security-research/shai-hulud-v2-poses-risk-npm-supply-chain)

**Event Summary:** Recent npm supply-chain incidents repeatedly use `preinstall`/`postinstall` hooks as execution pivots for shell/bootstrap commands (`curl`, `wget`, `iwr`, `powershell`) to fetch or launch second-stage payloads during dependency install.

**New Pattern Added:**

### SUP-004: npm preinstall/postinstall shell bootstrap pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.89
- **Pattern:** Detects `package.json` `preinstall`/`postinstall` script values containing shell/bootstrap primitives such as `curl`, `wget`, `iwr/irm`, `powershell`, `cmd /c`, `bash -c`, or `sh -c`.
- **Justification:** Aligns to observed lifecycle-hook abuse in both targeted package compromises and broad worm-like npm propagation campaigns.
- **Mitigation:** Remove shell/bootstrap execution from install lifecycle hooks; move setup to explicit, reviewed commands.

**Version:** Rules updated from 2026.02.11.1 to 2026.02.11.2

**Testing:** Added assertions in `tests/test_rules.py::test_new_patterns_2026_02_11`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/32_npm_shell_bootstrap`.

---

## 2026-02-10 (2): Windows Defender Exclusion + mshta Remote Execution Patterns

**Sources:**
- [VulnCheck - Metro4Shell: CVE-2025-11953 Exploitation in the Wild](https://www.vulncheck.com/blog/metro4shell_eitw)
- [The Hacker News - Hackers Exploit Metro4Shell RCE Flaw in React Native CLI npm Package](https://thehackernews.com/2026/02/hackers-exploit-metro4shell-rce-flaw-in.html)
- [CISA KEV - CVE-2025-11953](https://www.cisa.gov/known-exploited-vulnerabilities-catalog?field_cve=CVE-2025-11953)
- [Malwarebytes - Fake CAPTCHA websites hijack your clipboard to install information stealers](https://www.malwarebytes.com/blog/news/2025/03/fake-captcha-websites-hijack-your-clipboard-to-install-information-stealers)

**Event Summary:** Active exploitation of CVE-2025-11953 (Metro4Shell) observed since December 2025, added to CISA KEV catalog Feb 5, 2026. Attackers deliver Base64-encoded PowerShell that disables Windows Defender via `Add-MpPreference -ExclusionPath` and `Set-MpPreference -DisableRealtimeMonitoring`. Separate campaign uses CAPTCHA-based clipboard hijacking to trick users into running `mshta.exe` commands fetching remote HTA/VBScript payloads.

**New Patterns Added:**

### DEF-001: Windows Defender Exclusion Manipulation
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.95
- **Pattern:** Detects PowerShell `Add-MpPreference`/`Set-MpPreference` with `-Exclusion*` or `-DisableRealtimeMonitoring` flags.
- **Justification:** Core anti-analysis technique in Metro4Shell payloads and other Windows malware campaigns; programmatic security control disablement is never legitimate in skill/tool contexts.
- **Mitigation:** Remove all commands that disable or weaken Windows Defender protections.

### MAL-005: mshta.exe Remote Execution Pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.92
- **Pattern:** Detects `mshta` or `mshta.exe` invocations with `http://`, `https://`, or `\\` (UNC) paths.
- **Justification:** Widespread in clipboard hijacking campaigns; mshta is a Living-off-the-Land Binary (LOLBin) frequently abused to execute remote scripts without traditional download steps.
- **Mitigation:** Remove mshta.exe invocations that fetch remote HTA/VBScript payloads.

**Version:** Rules updated from 2026.02.10.1 to 2026.02.10.2

**Testing:** Added assertions in `tests/test_rules.py` (test_new_patterns_2026_02_10), showcase example `30_metro4shell_defender_bypass`.

---

## 2026-02-10 (1): Piped `echo|sed` Scoped-Write Bypass Pattern

**Sources:**
- [GitHub Advisory Database - CVE-2026-25723](https://github.com/advisories/GHSA-mhg7-666j-cqg4)
- [NVD - CVE-2026-25723](https://nvd.nist.gov/vuln/detail/CVE-2026-25723)

**Event Summary:** GitHub and NVD documented a command-injection/write-scope bypass in Claude Code where piped `echo | sed` operations could bypass intended write restrictions and redirect output into sensitive paths such as `.claude/` or outside the project root.

**New Pattern Added:**

### SUP-003: Piped sed write to out-of-scope or agent config path
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects `echo ... | sed ... >` redirection targeting `.claude/` and `../` style out-of-scope paths.
- **Justification:** Directly aligned to CVE-2026-25723 described behavior (piped sed with redirected write bypass).
- **Mitigation:** Replace shell rewrite/redirection primitives with scoped file APIs and path allowlists.

**Version:** Rules updated from 2026.02.09.5 to 2026.02.10.1

**Testing:** Added coverage in `tests/test_rules.py`, `tests/test_scan.py`, and showcase validation in `tests/test_showcase_examples.py`.

## 2026-02-09: npx Phantom Package / Registry Fallback Pattern

**Sources:**
- [Aikido - npx Confusion: Packages That Forgot to Claim Their Own Name](https://www.aikido.dev/blog/npx-confusion-unclaimed-package-names)
- [The Hacker News - Compromised dYdX npm and PyPI Packages Deliver Wallet Stealers and RAT Malware](https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html)

**Event Summary:** Recent supply-chain reporting highlighted widespread abuse potential when `npx` commands reference package names that were never claimed. In that case, npm registry fallback can fetch and execute attacker-published code.

**New Pattern Added:**

### SUP-002: npx Registry Fallback Execution Without `--no-install`
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects `npx <package>` usage that lacks the `--no-install` safeguard on the same command line.
- **Justification:** Aikido reported large-scale real-world execution volume of phantom `npx` package names, and The Hacker News linked the same abuse class in ongoing package compromise reporting.
- **Mitigation:** Prefer explicit installs and use `npx --no-install` to prevent implicit registry fallback execution.

**Version:** Rules updated from 2026.02.09.4 to 2026.02.09.5

**Testing:** Added assertions in `tests/test_rules.py`, `tests/test_scan.py`, and showcase coverage in `tests/test_showcase_examples.py`.

---

## 2026-02-09: GitHub Actions Secrets-Dump Exfil Pattern

**Sources:**
- [StepSecurity - Shai-Hulud: Self-Replicating Worm Compromises 500+ NPM Packages](https://www.stepsecurity.io/blog/ctrl-tinycolor-and-40-npm-packages-compromised)
- [The Hacker News - Shai-Hulud v2 Spreads From npm to Maven, as Campaign Exposes Thousands of Secrets](https://thehackernews.com/2025/11/shai-hulud-v2-campaign-spreads-from-npm.html)

**Event Summary:** Supply-chain malware campaigns documented malicious GitHub Actions workflow persistence that serializes CI/CD secrets context and transmits it to attacker-controlled endpoints.

**New Patterns Added:**

### EXF-004: GitHub Actions Full Secrets Context Dump
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.93
- **Pattern:** Detects `${{ toJSON(secrets) }}` expansion, a high-risk full-secret serialization marker.
- **Justification:** Incident reports show `${{ toJSON(secrets) }}` used inside malicious workflows to dump all repository/org secrets.
- **Mitigation:** Never serialize the full secrets context; pass only minimally scoped secret values to specific steps.

### CHN-004: GitHub Actions Secrets Context with Outbound Network
- **Category:** exfiltration
- **Severity:** critical
- **Confidence:** 0.94
- **Pattern:** Chains GitHub Actions secrets-context markers with outbound network/exfil indicators.
- **Justification:** Improves precision by requiring both secret-context expansion and transfer behavior.
- **Mitigation:** Remove broad secrets context references and block outbound transfer of CI/CD secrets.

**Version:** Rules updated from 2026.02.09.3 to 2026.02.09.4

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_09` and showcase validation in `tests/test_showcase_examples.py`.

---

## 2026-02-09: dYdX Supply Chain Attack Patterns

**Source:** [The Hacker News - Compromised dYdX npm and PyPI Packages](https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html)

**Event Summary:** Legitimate dYdX cryptocurrency packages on npm and PyPI were compromised to deliver wallet stealers and RAT malware. The attack targeted wallet credentials and included stealth remote command execution capabilities.

**New Patterns Added:**

### EXF-002: Cryptocurrency Wallet File Access
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects access to crypto wallet files (wallet.dat, .keystore, mnemonic, private keys)
- **Justification:** dYdX attack specifically targeted wallet seed phrases and credentials
- **Mitigation:** Do not access wallet files or seed phrases; crypto operations should use secure key management

### MAL-004: Dynamic Code Evaluation Pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.85
- **Pattern:** Detects eval(), exec(), Function() constructor, and vm.run* patterns
- **Justification:** Python RAT component in dYdX attack used exec() for remote command execution
- **Mitigation:** Avoid eval/exec flows that execute arbitrary code strings; use explicit functions

### OBF-002: Stealth Execution Pattern
- **Category:** instruction_abuse
- **Severity:** medium
- **Confidence:** 0.8
- **Pattern:** Detects CREATE_NO_WINDOW, nohup with output redirection, hidden process execution
- **Justification:** dYdX RAT used CREATE_NO_WINDOW flag to execute without console window on Windows
- **Mitigation:** Remove hidden/stealth execution flags that obscure command behavior

**Version:** Rules updated from 2026.02.09.1 to 2026.02.09.2

**Testing:** All patterns validated with unit tests in `tests/test_rules.py::test_new_patterns_2026_02_09`

---

## 2026-02-09: DockerDash Meta-Context Injection Pattern

**Sources:**
- [Noma Security - DockerDash: Two Attack Paths, One AI Supply Chain Crisis](https://noma.security/blog/dockerdash-two-attack-paths-one-ai-supply-chain-crisis/)
- [The Hacker News - Docker Fixes Critical Ask Gordon AI Flaw Allowing Code Execution via Image Metadata](https://thehackernews.com/2026/02/docker-fixes-critical-ask-gordon-ai.html)

**Event Summary:** Researchers documented a meta-context injection path where malicious instructions embedded in Docker image metadata are interpreted by AI assistants and used to trigger MCP tool actions, including data exfiltration through markdown image beacons with interpolated data placeholders.

**New Pattern Added:**

### EXF-003: Markdown Image Beacon Exfiltration Pattern
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects markdown image URLs containing likely exfil query keys (`data`, `dump`, `exfil`, `token`, `key`) with variable placeholders.
- **Justification:** DockerDash examples include image-beacon style exfiltration payloads embedded in metadata context.
- **Mitigation:** Block instruction-driven external image beacons with interpolated placeholders and treat all metadata/context as untrusted.

**Version:** Rules updated from 2026.02.09.2 to 2026.02.09.3

---

## 2026-02-19: pull_request_target Metadata Interpolation Injection Pattern

**Sources:**
- https://github.com/RooCodeInc/Roo-Code/security/advisories/GHSA-xr6r-vj48-29f6
- https://github.blog/security/supply-chain-security/four-tips-to-keep-your-github-actions-workflows-secure/

**Event Summary:** A recent advisory documented command injection in a privileged GitHub Actions workflow where untrusted pull-request metadata was interpolated in shell execution context. This is especially risky when combined with `pull_request_target`, which runs with elevated repository privileges.

**New Patterns Added:**

### EXF-008: GitHub Actions untrusted PR metadata interpolation in run/script
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects `${{ github.event.pull_request.title/body/head.label/user.login }}` interpolation in `run:` / `script:` blocks.
- **Justification:** Mirrors the root cause class from recent workflow command-injection disclosures.
- **Mitigation:** Never interpolate PR metadata directly into shell/script execution. Prefer safe non-shell actions or strict quoting and input validation.

### CHN-006: pull_request_target with untrusted PR metadata in shell/script
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.91
- **Pattern:** Chains `pull_request_target` with untrusted PR metadata interpolation markers.
- **Justification:** Reduces false positives by requiring the privileged workflow context plus untrusted metadata usage.
- **Mitigation:** Avoid privileged `pull_request_target` execution paths that evaluate untrusted PR metadata in shell commands.

**Version:** Rules updated from 2026.02.19.1 to 2026.02.19.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_19_patch2` and `tests/test_showcase_examples.py`.

---

## 2026-03-04: Tool Auto-Approve Package-Install Command Pattern

**Sources:**
- https://github.com/RooCodeInc/Roo-Code/security/advisories/GHSA-c292-qxq4-4p2v
- https://docs.roocode.com/update-notes/v3.26.0

**Event Summary:** A disclosed Roo Code issue shows that enabling auto-approval for terminal commands can permit `npm install` execution without an explicit approval step. Because package installs can execute lifecycle scripts (`preinstall`/`postinstall`), this creates a realistic arbitrary-code-execution path when opening untrusted repositories.

**New Pattern Added:**

### ABU-004: Tool auto-approve allowlist includes package-install command
- **Category:** instruction_abuse
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects package-install commands (`npm/pnpm/yarn/bun install`) in proximity to auto-approve/command-allowlist markers.
- **Justification:** Captures high-signal tool settings that lower consent barriers before install-time script execution.
- **Mitigation:** Remove package-install commands from auto-approved command lists; require explicit human confirmation for install actions.

**Version:** Rules updated from 2026.03.03.1 to 2026.03.04.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_04` and `tests/test_showcase_examples.py` with showcase fixture `examples/showcase/58_tool_autoapprove_pkg_install`.
