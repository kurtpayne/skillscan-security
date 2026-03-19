## 2026-03-19 — GlassWorm Chrome Extension RAT, OpenClaw gatewayUrl RCE, SnappyClient C2, AI Platform CVEs

**Sources:**
- [Aikido Security — GlassWorm Hides a RAT Inside a Malicious Chrome Extension](https://www.aikido.dev/blog/glassworm-chrome-extension-rat)
- [Socket.dev — GlassWorm Sleeper Extensions Activate on Open VSX, Shift to GitHub-Hosted VSIX Malware](https://socket.dev/blog/glassworm-sleeper-extensions-activated-on-open-vsx)
- [ProArch — OpenClaw One-Click RCE Vulnerability (CVE-2026-25253)](https://www.proarch.com/blog/threats-vulnerabilities/openclaw-rce-vulnerability-cve-2026-25253)
- [Zscaler ThreatLabz — Technical Analysis of SnappyClient](https://www.zscaler.com/blogs/security-research/technical-analysis-snappyclient)
- [SC Media — Significant Security Flaws Flagged in LangSmith, SGLang](https://www.scworld.com/brief/significant-security-flaws-flagged-in-langsmith-sglang)
- [VPNCentral — ForceMemo Attacks GitHub Accounts and Quietly Backdoors Python Repositories](https://vpncentral.com/forcememo-attacks-github-accounts-and-quietly-backdoors-python-repositories-with-force-pushed-malware/)

**Event Summary:** Two new detection rules and significant IOC/vulnerability enrichment were added. Aikido Security published a full analysis of the GlassWorm Chrome extension RAT, revealing a multi-stage attack that force-installs a malicious Chrome extension masquerading as Google Docs Offline (version 1.95.1). The extension functions as a full RAT with commands including `startkeylogger`, `domsnapshot`, `localstoragedump`, and `capture_clipboard`, using Solana blockchain memos as a C2 dead-drop channel. C2 infrastructure operates at 45.32.150.251, 217.69.3.152, 217.69.0.159, and 45.150.34.158. Socket.dev reported that GlassWorm sleeper extensions on Open VSX have shifted to delivering payloads from GitHub-hosted VSIX files, moving outside the Eclipse Foundation's takedown reach. ProArch detailed the CVE-2026-25253 OpenClaw one-click RCE attack chain, where a malicious `gatewayUrl` parameter steals auth tokens via WebSocket and then disables execution approval prompts (`exec.approvals.set: off`) for full remote code execution. Zscaler ThreatLabz disclosed SnappyClient, a new C2 framework implant delivered via HijackLoader targeting cryptocurrency wallets, with C2 at 151.242.122.227 and 179.43.167.210. SC Media reported critical vulnerabilities in LangSmith (CVE-2026-25750, account takeover) and SGLang (CVE-2026-3060, CVE-2026-3059, CVE-2026-3989, unpatched RCE). VPNCentral covered the ForceMemo campaign linking GlassWorm credential theft to force-pushed Python repository backdoors using Solana blockchain memos for C2.

**New Patterns Added:**

### MAL-034: GlassWorm Chrome extension force-install RAT
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.90
- **Pattern:** Detects `--install-extension --force` extension sideloading, Google Docs Offline 1.95 masquerade, `jucku/manifest.json` extension directory, `chrome.storage.local` agent_id persistence, `/api/register`, `/api/commands?agent_id`, `/api/exfil`, `/api/webhook/auth-detected` C2 endpoints, and RAT commands (`startkeylogger`, `getkeyloggerdata`, `domsnapshot`, `localstoragedump`, `capture_clipboard`).
- **Justification:** Direct detection of the GlassWorm Chrome extension RAT documented by Aikido Security. The malware deploys a persistent browser-based RAT with keylogging, cookie theft, session surveillance (targeting Bybit), and screenshot capabilities, using Solana wallet memos as a C2 dead-drop.

### MAL-035: OpenClaw gatewayUrl parameter injection and approval bypass
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Detects `gatewayUrl` parameter injection, `exec.approvals.set` / `exec.approval.set` disabling patterns, `approvals.disable` / `approvals.bypass` / `approvals.override` calls, and `confirmation_prompts` disabling.
- **Justification:** Direct detection of the CVE-2026-25253 attack chain. The OpenClaw Control UI blindly trusts the `gatewayUrl` URL parameter, leaking auth tokens to attacker-controlled servers. Combined with approval bypass, this enables full one-click RCE on 40,000+ exposed instances.

**IOC Updates:**
- Added IP: `151.242.122.227` (SnappyClient C2 control session)
- Added IP: `179.43.167.210` (SnappyClient C2 control session)
- Added IP: `217.69.3.152` (GlassWorm Stage 2/3 exfiltration server)
- Added IP: `217.69.0.159` (GlassWorm DHT bootstrap node)
- Added IP: `45.150.34.158` (GlassWorm Ledger/Trezor seed phrase exfiltration)
- Added domain: `webhook.site` (ClawHavoc data exfiltration endpoint)

**Vulnerability Updates:**
- Added CVE-2026-25750 for `langsmith` Python package (account takeover, fixed in 0.12.71)
- Added CVE-2026-3060 for `sglang` Python package (unauthenticated RCE, unpatched)
- Added CVE-2026-3059 for `sglang` Python package (unauthenticated RCE, unpatched)
- Added CVE-2026-3989 for `sglang` Python package (insecure deserialization, unpatched)

**Corpus Updates:**
- Added `corpus/malicious/a31_glassworm_chrome_rat.md`
- Added `corpus/malicious/a32_openclaw_gatewayurl.md`

---

## 2026-03-19 — SnappyClient C2 Implant, Click-Fix WebDAV Variant

**Sources:**
- [The Hacker News — Investigating New Click-Fix Variant with WebDAV](https://thehackernews.com/2026/03/investigating-new-click-fix-variant.html)
- [Dark Reading — New C2 Implant SnappyClient Targets Crypto Wallets](https://www.darkreading.com/cyberattacks-data-breaches/new-c2-implant-snappyclient-targets-crypto-wallets)

**Event Summary:** Two related malware campaigns were identified. A new Click-Fix variant uses `net use` to map attacker-controlled WebDAV shares and execute malicious batch scripts, bypassing browser download protections and SmartScreen checks. The trojanized WorkFlowy desktop application (Electron-based) hides a C2 beacon inside the `app.asar` archive. Separately, the SnappyClient C2 implant (C++ based, delivered via HijackLoader) targets cryptocurrency wallets using ChaCha20-Poly1305 encrypted communications. Both campaigns share infrastructure at `cloudflare.report` and `happyglamper.ro`.

**New Patterns Added:**

### MAL-034: Click-Fix WebDAV share mount and execute pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects `net use` commands mapping WebDAV shares (`DavWWWRoot`, `\webdav`) followed by execution of batch/command/executable files.
- **Justification:** Captures a new Click-Fix delivery variant that stages payloads on attacker-controlled WebDAV servers. Unlike browser-based downloads, WebDAV-mounted files bypass SmartScreen and download protection checks, making this a high-signal evasion technique.
- **Mitigation:** Do not map WebDAV shares via `net use` and execute remote scripts. Block WebDAV mount commands in skill files and treat any `net use` + execute chain as suspicious.

### MAL-035: Trojanized Electron app.asar C2 payload injection
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects `app.asar` references combined with execution primitives (`exec`, `spawn`, `fetch`, `request`, `net.request`) indicating a trojanized Electron application with injected C2 functionality.
- **Justification:** Captures the SnappyClient/Click-Fix campaign technique of hiding C2 beacons inside Electron `app.asar` archives. Legitimate Electron apps do not typically combine asar manipulation with direct execution or network calls in the same context.
- **Mitigation:** Verify the integrity of Electron application packages and reject modified asar files that contain unexpected network or execution calls.

**IOC Updates:**
- Added domain: `cloudflare.report` (SnappyClient/Click-Fix C2)
- Added IP: `94.156.170.255` (SnappyClient C2)
- Added IP: `144.31.165.173` (Click-Fix WebDAV staging)
- Added URL: `https://cloudflare.report/forever/e/` (SnappyClient payload endpoint)

**Version:** Rules updated from 2026.03.18.2 to 2026.03.19.1
**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_19` and `tests/test_showcase_examples.py` with showcase fixtures `examples/showcase/89_clickfix_webdav_share_exec` and `examples/showcase/90_electron_asar_c2_injection`.
---
## 2026-03-18 — BlokTrooper VSX Extension Compromise, ClawHavoc Agent Memory Harvesting
**Sources:**
- [Aikido Security — fast-draft Open VSX Extension Compromised by BlokTrooper (RAT & Infostealer)](https://www.aikido.dev/blog/fast-draft-open-vsx-bloktrooper)
- [ClawSecure — ClawHavoc Malware Found in 539 OpenClaw Skills](https://www.clawsecure.ai/blog/clawhavoc-explained)
- [Towards AI — NVIDIA NemoClaw Explained: How It Secures OpenClaw AI Agents](https://pub.towardsai.net/nvidia-nemoclaw-explained-how-it-secures-openclaw-ai-agents-for-enterprise-deployment-6a606c2ddc33)

**Event Summary:** Two new threat categories were identified. Aikido Security disclosed the BlokTrooper compromise of the `fast-draft` Open VSX extension (26,000+ downloads), where malicious versions (0.10.89, 0.10.105, 0.10.106, 0.10.112) fetch a GitHub-hosted payload from `BlokTrooper/extension` and pipe it into a shell, deploying a four-module attack framework: a Socket.IO RAT with full desktop control, a browser and crypto wallet stealer targeting 25+ wallet extensions, a recursive file exfiltration module, and a clipboard surveillance module. The C2 infrastructure operates at 195.201.104.53 on ports 6931, 6936, and 6939. Separately, ClawSecure reported the ClawHavoc campaign affecting 539 OpenClaw skills (18.7% of the most popular), which harvests agent memory and identity files (`MEMORY.md`, `SOUL.md`) for impersonation and lateral movement, with C2 callbacks to 91.92.242.30 and exfiltration via glot.io/api/ and webhook.site. CVE-2026-25253 was assigned for the related OpenClaw RCE vulnerability.

**New Patterns Added:**

### MAL-033: BlokTrooper VSX extension GitHub-hosted downloader pattern
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.91
- **Pattern:** Detects `raw.githubusercontent.com/BlokTrooper` payload host, `fd.onlyOncePlease` one-time guard variable, `/cldbs` + `/upload` exfiltration routes, and `/api/service/makelog` clipboard logging endpoint.
- **Justification:** Direct detection of the BlokTrooper attack chain documented by Aikido Security. The compromised `fast-draft` extension alternates between clean and malicious versions, indicating a stolen publisher token. The four-module payload (RAT, stealer, file exfil, clipboard monitor) represents a full compromise toolkit.

### EXF-017: OpenClaw agent memory and identity file harvesting
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects access to `MEMORY.md`, `SOUL.md`, `.openclaw/memory`, `.openclaw/soul`, `.openclaw/identity`, and `agent-identity` or `agent-memory` files.
- **Justification:** Direct detection of the ClawHavoc campaign's agent file harvesting technique. Agent memory and identity files contain sensitive context, personality data, and conversation history that can be weaponized for impersonation, social engineering, or lateral movement across agent networks.

**IOC Updates:**
- Added IP: `195.201.104.53` (BlokTrooper C2)
- Added domain: `pastefy.app` (DRILLAPP C2 staging)

**Vulnerability Updates:**
- Added CVE-2026-25253 for `openclaw` npm package (RCE via malicious webpage, CVSS 8.8)

**Corpus Updates:**
- Added `corpus/malicious/a29_bloktrooper_vsx.md`
- Added `corpus/malicious/a30_clawhavoc_memory.md`

---

## 2026-03-18 — CursorJack Deeplinks, LeakNet Deno BYOR, GlassWorm Wave 6, MEDIA Directive Injection

**Sources:**
- [Infosecurity Magazine — CursorJack Attack Path Exposes Code Execution Risk](https://www.infosecurity-magazine.com/news/cursor-jack-attack-path-ai/)
- [BleepingComputer — LeakNet ransomware uses ClickFix and Deno runtime](https://www.bleepingcomputer.com/news/security/leaknet-ransomware-uses-clickfix-and-deno-runtime-for-stealthy-attacks/)
- [ReliaQuest — ClickFix, Deno, and LeakNet's Scaling Threat](https://reliaquest.com/blog/threat-spotlight-casting-a-wider-net-clickfix-deno-and-leaknets-scaling-threat/)
- [BleepingComputer — GlassWorm malware hits 400+ code repos](https://www.bleepingcomputer.com/news/security/glassworm-malware-hits-400-plus-code-repos-on-github-npm-vscode-openvsx/)
- [StepSecurity — bittensor-wallet 4.0.2 Compromised on PyPI](https://www.stepsecurity.io/blog/bittensor-wallet-4-0-2-compromised-on-pypi---backdoor-exfiltrates-private-keys)
- [SynScan — OpenClaw MEDIA: Directive Injection](https://synscan.net/vuln/openclaw-vulnerable-to-local-file-exfiltration-via-mcp-tool-result-media-directive-injection)

**Event Summary:** Four new threat categories were identified. Proofpoint disclosed the CursorJack attack path, where malicious `cursor://` deeplinks trick developers into installing rogue MCP servers that execute arbitrary commands. The LeakNet ransomware gang adopted a "bring your own runtime" (BYOR) technique using the legitimate Deno binary to decode and execute base64 JavaScript payloads from `data:` URLs, minimizing forensic artifacts. GlassWorm Wave 6 expanded to 433 compromised components across GitHub, npm, and VSCode/OpenVSX, with the `lzcdrtfxyqiplpd` marker variable and `~/init.json` persistence file as key indicators. A `MEDIA:` directive injection vulnerability in OpenClaw allows malicious MCP tool servers to exfiltrate local files through the media processing pipeline. Additionally, the `bittensor-wallet` 4.0.2 PyPI package was found backdoored with a 3-layer C2 exfiltration system.

**New Patterns Added:**

### MAL-030: IDE deeplink MCP server install abuse
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects `cursor://`, `vscode://`, or `vscode-insiders://` deeplinks containing MCP server install parameters.
- **Justification:** Direct detection of the CursorJack attack path documented by Proofpoint. Malicious deeplinks embed harmful server configurations that execute commands upon user approval.

### MAL-031: Deno bring-your-own-runtime execution pattern
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Detects Deno executing remote URLs, `data:` URI payloads, or `eval` with string arguments.
- **Justification:** Direct detection of the LeakNet BYOR technique. The legitimate Deno runtime is abused to execute malicious JavaScript in memory, bypassing binary blocklists.

### MAL-032: GlassWorm persistence marker variable
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.85
- **Pattern:** Detects the `lzcdrtfxyqiplpd` marker variable, `~/init.json` persistence config, or `~/node-v22` bundled runtime.
- **Justification:** Direct detection of GlassWorm Wave 6 persistence indicators. StepSecurity recommends searching for this marker variable as the primary indicator of compromise.

### PINJ-002: MCP tool result MEDIA directive injection
- **Category:** instruction_abuse
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects `MEDIA:` directives followed by absolute file paths, `file://` URIs, or Windows drive paths in tool result content.
- **Justification:** Direct detection of the OpenClaw file exfiltration vulnerability (GHSA-jjgj-cpp9-cvpv). Malicious MCP tool servers inject `MEDIA:` directives to exfiltrate local files.

**IOC Updates:**
- **Domains added:** `finney.opentensor-metrics.com`, `finney.metagraph-stats.com`, `finney.subtensor-telemetry.com`, `opentensor-cdn.com`, `t.opentensor-cdn.com` (bittensor-wallet C2), `serialmenot.com`, `crahdhduf.com`, `weaplink.com` (LeakNet C2)
- **IPs added:** `144.31.224.98` (LeakNet C2)
- **URLs added:** `https://fastdlvrss.s3.us-east-1.amazonaws.com`, `https://backupdailyawss.s3.us-east-1.amazonaws.com` (LeakNet S3 staging)

**Vulnerability DB Updates:**
- **PYPI-BACKDOOR-2026-0317:** `bittensor-wallet` 4.0.2 backdoor (private key exfiltration via 3-layer C2, severity: critical, safe version: 4.0.1)

**Corpus Updates:**
- `corpus/malicious/a26_cursorjack_deeplink.md` — CursorJack IDE deeplink abuse sample
- `corpus/malicious/a27_deno_byor.md` — Deno BYOR loader sample
- `corpus/malicious/a28_glassworm_persistence.md` — GlassWorm persistence marker sample
- `corpus/prompt_injection/pi43_media_directive_injection.md` — MEDIA directive injection sample

---

## 2026-03-17 — v0.3.1: Skill Graph Analysis, ML Pipeline, and Distribution Channels

**Summary:** v0.3.1 ships three new structural detection rules (`PINJ-GRAPH-001/002/003`) for skill graph analysis, ML-based prompt injection detection via a DeBERTa-v3-base LoRA adapter (ONNX INT8, 111-example corpus), `skillscan model` and `skillscan rule` command groups, a reusable GitHub Actions workflow, pre-commit hook, and VS Code extension scaffold. The signature-as-data architecture is now fully operational: rules, IOCs, and the ONNX model are versioned data artifacts updated independently of the scanner binary.

**New Rules:**
- `PINJ-GRAPH-001` — Skill loads a remote `.md` file at runtime (dead-drop instruction injection, HIGH)
- `PINJ-GRAPH-002` — Skill grants `Bash`/`Computer`/`Shell` tool without a declared purpose section (MEDIUM)
- `PINJ-GRAPH-003` — Skill instructs agent to write memory files (`SOUL.md`, `MEMORY.md`, `AGENTS.md`, `.claude/settings.json`) (CRITICAL)

**ML Model:** `kurtpayne/skillscan-deberta-adapter` on HuggingFace — DeBERTa-v3-base LoRA, ONNX INT8, trained on 111 labeled examples (54 benign / 57 injection). Enable with `skillscan scan --ml-detect` after `skillscan model sync`.

**Version:** Rules updated from 2026.03.17.2 to 2026.03.17.3

---

## 2026-03-17 (1): MCP Attack Patterns, Social Engineering Chains, and Container Escape Rules

## 2026-03-17 — GlassWorm Wave 5, PylangGhost RAT, CVE-2026-4270

**Sources:**
- [Koi Security — GlassWorm Hits MCP: 5th Wave with New Delivery Techniques](https://www.koi.ai/blog/glassworm-hits-mcp-5th-wave-with-new-delivery-techniques)
- [Aikido — GlassWorm Strikes React Native Packages](https://www.aikido.dev/blog/glassworm-strikes-react-packages-phone-numbers)
- [CyberPress — PylangGhost RAT Hits npm Supply Chain](https://cyberpress.org/pylangghost-hits-npm-supplychain/)
- [NVD — CVE-2026-4270](https://nvd.nist.gov/vuln/detail/CVE-2026-4270)

**Event Summary:** The GlassWorm campaign expanded into the MCP ecosystem (Wave 5, reported 2026-03-16). Typosquatted npm packages such as `@iflow-mcp/watercrawl-watercrawl-mcp` and backdoored React Native packages (`react-native-country-select@0.3.91`, `react-native-international-phone-number@0.11.8`) use a novel Solana blockchain RPC dead-drop technique: the malware calls `getSignaturesForAddress` to read on-chain transaction memos containing encoded C2 URLs, then fetches and executes the decoded payload. Separately, a DPRK-linked campaign delivers PylangGhost RAT via npm packages (`react-refresh-update`, `@jaime9008/math-service`) with C2 at `173.211.46.22:8080` and staging domain `malicanbur.pro`. Additionally, CVE-2026-4270 was published for `@awslabs/aws-api-mcp-server` (path traversal, CVSS 6.8, fixed in 1.3.9).

**New Patterns Added:**

### MAL-029: Solana RPC blockchain C2 resolution marker
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.90
- **Pattern:** Detects `getSignaturesForAddress` / `getConfirmedSignaturesForAddress2` Solana RPC calls combined with `memo`/`logMessages` field access and subsequent execution sinks (`eval`, `exec`, `spawn`, `fetch`, etc.), or `@solana/web3` imports combined with the same RPC+memo pattern.
- **Justification:** Direct detection of the blockchain-based C2 dead-drop technique documented in GlassWorm Wave 5. The attacker stores encoded C2 URLs in Solana transaction memos and resolves them at install time, making the C2 infrastructure immutable and censorship-resistant.

**IOC Updates:**
- **IPs added:** `45.32.150.251`, `45.32.151.157`, `70.34.242.255` (GlassWorm staging servers), `173.211.46.22` (PylangGhost C2)
- **Domains added:** `malicanbur.pro` (PylangGhost staging domain)

**Vulnerability DB Updates:**
- **CVE-2026-4270:** `@awslabs/aws-api-mcp-server` path traversal (affected >= 0.2.14, fixed in 1.3.9, severity: medium)

---

## 2026-03-17 — MCP Tool Poisoning, Container Escape Techniques

**Sources:**
- [Invariant Labs - MCP Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [Invariant Labs - WhatsApp MCP Cross-Server Exploit](https://invariantlabs.ai/blog/whatsapp-mcp-exploited)
- [OWASP Agentic Top 10 in Practice (Amine Raji)](https://aminrj.com/posts/owasp-agentic-top-10-in-practice/)
- [Unit 42 - Container Escape Techniques](https://unit42.paloaltonetworks.com/container-escape-techniques/)
- [Red Canary - Container Escape Detection](https://redcanary.com/threat-detection-report/techniques/container-escapes/)

**Event Summary:** Multiple documented attack patterns targeting MCP-based agent systems and containerized AI workloads have emerged in early 2026. Invariant Labs demonstrated tool description poisoning via hidden `<IMPORTANT>` instruction blocks, cross-server tool invocation attacks exploiting MCP's flat namespace, and rug-pull attacks where server behavior mutates after initial approval. Separately, container escape techniques combining privileged execution with host path mounts and Docker socket access continue to be exploited in CI/CD environments. This update adds 10 new rules (6 static, 4 chain) across three categories.

**New Patterns Added:**

### MAL-025: MCP tool description poisoning via hidden instruction block
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.92
- **Pattern:** Detects `<IMPORTANT>` tags containing action verbs (read, access, send, exfil, forward, upload, post) in tool descriptions.
- **Justification:** Direct detection of the canonical MCP tool poisoning attack documented by Invariant Labs. The `<IMPORTANT>` block pattern is the primary vector for embedding hidden instructions in tool descriptions.

### ABU-006: Stealth instruction concealment from user
- **Category:** instruction_abuse
- **Severity:** high
- **Confidence:** 0.88
- **Pattern:** Detects phrases that instruct the agent to hide actions from the user ("do not mention", "hide this step", "background telemetry", "don't let the user see").
- **Justification:** Core social engineering technique observed in all three documented MCP attacks. The attacker instructs the LLM to conceal malicious operations from the human operator.

### ABU-007: Cross-server MCP tool invocation instruction
- **Category:** instruction_abuse
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects instructions that reference tools from named MCP servers (whatsapp-mcp, slack-mcp, github-mcp, etc.) in a cross-invocation context.
- **Justification:** Directly targets the cross-server poisoning attack where a malicious server's tool description instructs the LLM to call tools from other connected servers.

### MAL-026: Docker socket mount or access pattern
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.90
- **Pattern:** Detects Docker socket mount patterns (`docker.sock`, `-v /var/run/docker.sock`).
- **Justification:** Docker socket access from within a container provides full control over the Docker daemon and enables container escape to the host.

### MAL-027: Privileged container execution or dangerous capability grant
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Detects `--privileged`, `--cap-add=ALL/SYS_ADMIN/SYS_PTRACE/NET_ADMIN`, and disabled security profiles.
- **Justification:** Privileged containers have unrestricted access to host devices and kernel capabilities, enabling full host compromise.

### MAL-028: Host network infrastructure manipulation
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.85
- **Pattern:** Detects writes to `/etc/hosts` and `/etc/resolv.conf`, iptables rule manipulation, and IP route changes.
- **Justification:** Network infrastructure modification enables DNS hijacking, traffic interception, and man-in-the-middle attacks from within a skill.

### CHN-011: MCP tool poisoning with credential exfiltration chain
- **Category:** exfiltration
- **Severity:** critical
- **Confidence:** 0.93
- **Chain:** mcp_tool_poison + secret_access
- **Justification:** Combines the tool poisoning vector with credential file access, matching the full Invariant Labs attack chain.

### CHN-012: Stealth concealment with network exfiltration chain
- **Category:** exfiltration
- **Severity:** critical
- **Confidence:** 0.91
- **Chain:** stealth_conceal + network
- **Justification:** Detects the combination of user-concealment instructions with outbound network activity, indicating covert data exfiltration.

### CHN-013: Container escape with host path mount chain
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.92
- **Chain:** container_escape + host_path_mount
- **Justification:** Privileged container execution combined with sensitive host path mounts enables full host filesystem compromise.

### CHN-014: Container escape with secret access chain
- **Category:** malware_pattern
- **Severity:** critical
- **Confidence:** 0.90
- **Chain:** container_escape + secret_access
- **Justification:** Privileged container access combined with credential harvesting enables host credential theft via container breakout.

**Version:** Rules updated from 2026.03.17.1 to 2026.03.17.2

**Testing:** Added coverage in `tests/test_showcase_examples.py` and fixtures `examples/showcase/72_mcp_tool_description_poisoning` through `examples/showcase/81_container_escape_secret_access_chain`.

---

## 2026-03-15 (1): CloudFormation Admin-Role Bootstrap Marker via CAPABILITY_IAM

**Sources:**
- [Google Cloud - Cloud Threat Horizons Report H1 2026](https://cloud.google.com/security/report/resources/cloud-threat-horizons-report-h1-2026)
- [The Hacker News - UNC6426 Exploits nx npm Supply-Chain Attack to Gain AWS Admin Access in 72 Hours](https://thehackernews.com/2026/03/unc6426-exploits-nx-npm-supply-chain.html)

**Event Summary:** Recent cloud incident reporting describes rapid escalation from stolen CI/CD credentials to full AWS administration by deploying CloudFormation stacks with IAM-creation capabilities and attaching `AdministratorAccess` to attacker-created roles. Existing SkillScan rules covered PR/workflow abuse and secret theft primitives, but did not include a focused static marker for this CloudFormation privilege-escalation bootstrap shape.

**New Pattern Added:**

### MAL-024: CloudFormation admin-role bootstrap marker via CAPABILITY_IAM
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects co-occurrence of `CAPABILITY_IAM`/`CAPABILITY_NAMED_IAM` and `arn:aws:iam::aws:policy/AdministratorAccess` within a short window.
- **Justification:** High-signal indicator for CI/cloud privilege-escalation templates and commands observed in current incident reporting; scoped to a specific dangerous capability+policy combination to keep false positives low.
- **Mitigation:** Require explicit approval and least-privilege review for any CloudFormation deployment that can create IAM principals and attach broad managed-admin policies.

**Version:** Rules updated from 2026.03.14.1 to 2026.03.15.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_15`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/69_cloudformation_adminrole_bootstrap`.

---

## 2026-03-11 (2): Bash Parameter-Expansion Command Smuggling Marker

**Sources:**
- [GitHub Advisory Database - GHSA-g8r9-g2v8-jv6f (CVE-2026-29783)](https://github.com/advisories/GHSA-g8r9-g2v8-jv6f)
- [GitLab Advisory DB - CVE-2026-29783](https://advisories.gitlab.com/pkg/npm/@github/copilot/CVE-2026-29783/)

**Event Summary:** March 2026 advisory reporting for CVE-2026-29783 documents that crafted bash parameter expansion syntax can hide executable payloads inside commands that may be misclassified as read-only in AI CLI workflows. The disclosed dangerous forms include `${var@P}` prompt expansion and default/assignment expansions that embed command substitutions like `${HOME:-$(whoami)}`. Existing SkillScan rules covered broad download/exec and eval behavior but did not include a focused marker for this bash expansion smuggling shape.

**New Pattern Added:**

### MAL-022: Bash parameter-expansion command smuggling marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects `@P` prompt-expansion usage and default/assignment parameter expansions that contain embedded command/process substitutions (for example `$(...)` or `<(...)`) within `${...}` blocks.
- **Justification:** High-signal marker tied directly to a recent GHSA/CVE affecting AI shell-tool safety classification; scoped to rare bash expansion forms to keep noise low.
- **Mitigation:** Treat these expansion forms as unsafe in AI-generated shell commands. Require explicit review and block auto-execution for matching commands.

**Version:** Rules updated from 2026.03.11.1 to 2026.03.11.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_11_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/67_bash_param_expansion_smuggling`.

---

## 2026-03-09 (2): Multi-Target Developer Credential Harvest List Marker

**Sources:**
- [JFrog - GhostClaw Unmasked: A Malicious npm Package Impersonating OpenClaw to Steal Everything](https://research.jfrog.com/post/ghostclaw-unmasked/)
- [The Hacker News - Malicious npm Package Posing as OpenClaw Installer Deploys RAT, Steals macOS Credentials](https://thehackernews.com/2026/03/malicious-npm-package-posing-as.html)

**Event Summary:** March 2026 reporting on the GhostClaw npm campaign shows bundled credential-harvest lists that collect multiple developer auth stores in one pass (for example `~/.npmrc`, `~/.git-credentials`, and GitHub CLI `~/.config/gh/hosts.yml`) before upload/exfiltration. Existing SkillScan coverage flagged individual secret files, but did not include a focused marker for this specific multi-target developer-token harvest pattern.

**New Pattern Added:**

### EXF-015: Multi-target developer credential file harvest list marker
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects co-occurrence of `.npmrc`, `.git-credentials`, and GitHub CLI `hosts.yml` path markers within a short content window.
- **Justification:** The combined path-set is a high-signal token-harvest indicator from current malware reporting and produces lower noise than matching any single path alone.
- **Mitigation:** Treat combined developer credential file collection as credential theft behavior, remove unauthorized collection logic, and rotate exposed tokens.

**Version:** Rules updated from 2026.03.09.1 to 2026.03.09.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_09_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/65_dev_credential_harvest_list`.

---

## 2026-03-06 (3): VS Code Hidden-Whitespace Task Command Marker

**Sources:**
- [Socket - StegaBin: 26 Malicious npm Packages Use Pastebin Steganography](https://socket.dev/blog/stegabin-26-malicious-npm-packages-use-pastebin-steganography)
- [The Hacker News - North Korean Hackers Publish 26 npm Packages Hiding Pastebin C2 for Cross-Platform RAT](https://thehackernews.com/2026/03/north-korean-hackers-publish-26-npm.html)

**Event Summary:** Recent campaign reporting describes VS Code persistence where malicious `tasks.json` entries hide shell/bootstrap commands behind very large leading whitespace, making payloads hard to spot in task viewers and quick reviews. Existing SkillScan coverage already flagged `runOn: "folderOpen"` and StegaBin dead-drop indicators, but lacked a focused static marker for the off-screen whitespace concealment technique itself.

**New Pattern Added:**

### MAL-020: VS Code task off-screen whitespace command padding marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects `tasks.json` command fields containing extreme leading whitespace followed by shell/bootstrap downloader primitives (`curl`, `wget`, `iwr`, `powershell`, `cmd /c`, `bash -c`, `sh -c`).
- **Justification:** High-signal stealth marker tied to a concrete 2026 campaign TTP; scoped to suspicious task-command shape to keep false positives low.
- **Mitigation:** Treat repo-supplied VS Code tasks as untrusted. Remove concealed command padding and require explicit review before enabling task automation.

**Version:** Rules updated from 2026.03.06.2 to 2026.03.06.3

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_06_patch3`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/63_vscode_hidden_whitespace_task`.

---

## 2026-03-06 (2): StegaBin Shared npm Payload-Path Marker

**Sources:**
- [Socket - StegaBin: 26 Malicious npm Packages Use Pastebin Steganography](https://socket.dev/blog/stegabin-26-malicious-npm-packages-use-pastebin-steganography)
- [The Hacker News - North Korean Hackers Publish 26 npm Packages Hiding Pastebin C2 for Cross-Platform RAT](https://thehackernews.com/2026/03/north-korean-hackers-publish-26-npm.html)

**Event Summary:** Socket’s March 2026 write-up documents 26 typosquat npm packages that shared a common malicious loader component at `vendor/scrypt-js/version.js`, executed through install-hook chains. Existing SkillScan rules covered generalized install-hook abuse and steganographic dead-drop behavior but did not include a focused static marker for this concrete, campaign-linked payload path.

**New Pattern Added:**

### MAL-019: StegaBin npm shared payload path marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.86
- **Pattern:** Detects references to `vendor/scrypt-js/version.js` in repository/package artifacts.
- **Justification:** High-signal and low-noise campaign marker tied to recent public reporting; suitable as an explicit static signature alongside broader behavioral patterns.
- **Mitigation:** Remove package content referencing this path, verify package provenance, and avoid installing typosquat dependencies from untrusted publishers.

**Version:** Rules updated from 2026.03.06.1 to 2026.03.06.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_06_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/62_stegabin_shared_payload_path`.

---

## 2026-03-06 (1): Bracket-Glob Sensitive Path Obfuscation Marker

**Sources:**
- [GitHub Advisory Database - GHSA-5wp8-q9mx-8jx8](https://github.com/advisories/GHSA-5wp8-q9mx-8jx8)
- [zeptoclaw Advisory - Shell allowlist/blocklist bypass](https://github.com/qhkm/zeptoclaw/security/advisories/GHSA-5wp8-q9mx-8jx8)

**Event Summary:** GHSA-5wp8-q9mx-8jx8 documents bypasses in shell guard logic where literal path blocklists can be evaded by bracket-glob obfuscation (for example `/etc/pass[w]d`). Existing SkillScan rules matched direct sensitive paths but did not include this evasive variant.

**New Pattern Added:**

### EXF-014: Bracket-glob obfuscated sensitive path marker
- **Category:** exfiltration
- **Severity:** high
- **Confidence:** 0.85
- **Pattern:** Detects bracket-glob variants of high-risk secret paths (`/etc/pass[w]d`, `/etc/shad[o]w`, `~/.ssh/id_r[s]a`) commonly used to evade literal denylist checks.
- **Justification:** High-signal marker tied to a concrete, recent advisory and narrowly scoped to sensitive-path obfuscation behavior with low expected false positives.
- **Mitigation:** Normalize/resolve glob metacharacters before path denylist checks and reject obfuscated sensitive path access attempts.

**Version:** Rules updated from 2026.03.05.2 to 2026.03.06.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_06`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/61_bracket_glob_secret_path_bypass`.

---

## 2026-03-05 (2): node-glob CLI `-c/--cmd` Shell Injection Sink Marker

**Sources:**
- [GitHub Advisory Database - CVE-2025-64756 (GHSA-5j98-mcp5-4vw2)](https://github.com/advisories/GHSA-5j98-mcp5-4vw2)
- [node-glob Security Advisory - GHSA-5j98-mcp5-4vw2](https://github.com/isaacs/node-glob/security/advisories/GHSA-5j98-mcp5-4vw2)

**Event Summary:** The `glob` CLI advisory describes command injection when `glob -c/--cmd` executes matched file names with shell semantics (`shell: true`). In untrusted repos/archives, attacker-controlled file names containing shell metacharacters can trigger arbitrary command execution in developer or CI environments.

**New Pattern Added:**

### MAL-018: node-glob CLI --cmd shell execution sink marker
- **Category:** malware_pattern
- **Severity:** high
- **Confidence:** 0.84
- **Pattern:** Detects `glob` CLI invocations that enable command mode via `-c` or `--cmd`, including common `npx glob -c ...` forms.
- **Justification:** High-signal, low-noise command-shape marker directly tied to a recent disclosed exploit path in tool/setup scripts.
- **Mitigation:** Avoid `glob -c/--cmd` on untrusted file sets; upgrade to patched versions and prefer non-shell argument passing (`--cmd-arg/-g`).

**Version:** Rules updated from 2026.03.05.1 to 2026.03.05.2

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_03_05_patch2`, showcase validation in `tests/test_showcase_examples.py`, and fixture `examples/showcase/60_glob_cmd_shell_injection`.

---

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

---

## 2026-03-16: Unicode PUA/Variation-Selector Obfuscation Near Dynamic Execution Sink

**Sources:**
- https://www.unicode.org/reports/tr51/#Emoji_and_Presentation_Sequences
- https://www.unicode.org/charts/PDF/UFE00.pdf

**Event Summary:** Recent malware/obfuscation campaigns continue to hide malicious intent using invisible or hard-to-spot Unicode code points. A practical high-signal variant is clustering Unicode variation-selector/PUA-style code points adjacent to dynamic execution sinks (`eval`, `exec`, `Function`) to evade quick visual review while preserving executable behavior.

**New Pattern Added:**

### OBF-003: Unicode PUA obfuscation near dynamic execution sink
- **Category:** instruction_abuse
- **Severity:** high
- **Confidence:** 0.87
- **Pattern:** Detects variation-selector/PUA-range clusters (`U+FE00..U+FE0F`, `U+E0100..U+E01EF`) within close proximity to `eval(` / `exec(` / `Function(` markers.
- **Justification:** Balances signal and noise by requiring adjacency/proximity to dynamic execution surfaces rather than flagging all Unicode variation selectors.
- **Mitigation:** Normalize Unicode before policy evaluation, treat hidden-control/presentation-codepoint clusters near execution sinks as suspicious, and reject unsafe dynamic execution paths.

**Version:** Rules updated from 2026.03.14.1 to 2026.03.14.1+2026.03.16.1

**Testing:** Added coverage in `tests/test_rules.py::test_new_patterns_2026_02_09` and `tests/test_showcase_examples.py` with showcase fixture `examples/showcase/70_pua_eval_obfuscation`.
