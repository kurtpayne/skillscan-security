# Comprehensive Examples

SkillScan ships a full showcase in `examples/showcase` to demonstrate detection coverage.

## Coverage map

| Example | What it demonstrates | Expected signal |
|---|---|---|
| `01_download_execute` | Download-and-execute chain | `MAL-001` |
| `02_base64_exec` | Decode-and-execute chain | `MAL-002` |
| `03_instruction_abuse` | Coercive prerequisite text | `ABU-001` |
| `04_secret_access` | Secret file markers | `EXF-001` |
| `05_ioc_match` | IOC blocklist matches | `IOC-001` |
| `06_dep_vuln_python` | Vulnerable Python dependency | `DEP-001` |
| `07_dep_vuln_npm` | Vulnerable npm dependency | `DEP-001` |
| `08_unpinned_deps` | Unpinned dependency specs | `DEP-UNPIN` |
| `09_policy_block_domain` | Policy-based domain block | `POL-IOC-BLOCK` |
| `10_openai_style` | OpenAI-style ecosystem hint | `openai_style` |
| `11_claude_style` | Claude-style ecosystem hint | `claude_style` |
| `12_benign_minimal` | Clean baseline sample | no high-severity findings |
| `13_zero_width_evasion` | Unicode obfuscation normalization | `ABU-001` |
| `14_base64_hidden_chain` | Decoded hidden command chain | `CHN-001` |
| `15_secret_network_chain` | Secret access + network chain | `CHN-002` |
| `16_privilege_disable_chain` | Privilege + security bypass sequence | `ABU-002` |
| `17_defanged_ioc` | Defanged IOC normalization (`hxxp`, `[.]`) | IOC extraction + intel matching |
| `18_split_base64_chain` | Concatenated base64 fragment decoding | `CHN-001` |
| `19_alt_download_exec` | Non-curl/wget downloader + interpreter exec | `CHN-001` |
| `20_ai_semantic_risk` | Semantic-only credential request pattern (AI assist) | `AI-SEM-001` with `--ai-assist` |
| `21_npm_lifecycle_abuse` | Risky npm lifecycle script (`preinstall` etc.) | `SUP-001` |
| `22_prompt_injection` | Prompt override/jailbreak language in instructions | `PINJ-001` |
| `23_trojan_source_bidi` | Bidirectional Unicode obfuscation marker | `OBF-001` |
| `24_binary_artifact` | Executable binary artifact present in bundle | `BIN-001` |
| `25_wallet_eval_stealth` | Wallet file targeting + dynamic eval + stealth execution markers | `EXF-002`, `MAL-004`, `OBF-002` |
| `26_metadata_image_beacon` | Metadata-injected markdown image URL beacon with interpolated exfil placeholder | `EXF-003` |
| `27_github_actions_secrets_exfil` | GitHub Actions full secrets context expansion with outbound transfer | `EXF-004`, `CHN-004` |
| `28_npx_registry_fallback` | `npx` command without `--no-install` guard (implicit registry fallback execution risk) | `SUP-002` |
| `29_claude_sed_path_bypass` | `echo ... | sed ... >` redirection into `.claude/` or parent paths (`../`) to bypass scoped-write controls | `SUP-003` |
| `31_clickfix_powershell_iex` | PowerShell web request piped to in-memory execution (`iwr/irm` + `iex`) seen in ClickFix-style lures | `MAL-006` |
| `32_npm_shell_bootstrap` | npm `preinstall`/`postinstall` shell bootstrap commands (`curl`/`wget`/PowerShell) | `SUP-004` |
| `33_byovd_security_killer` | BYOVD vulnerable-driver service creation + AV/EDR-killer toolkit markers | `MAL-007` |
| `34_pr_target_checkout_exfil` | `pull_request_target` workflow that checks out untrusted PR head refs (`head.ref`/`head.sha`) | `EXF-005`, `CHN-005` |
| `35_discord_debugger_token_theft` | Discord Electron `webContents.debugger` hook intercepting auth/MFA network traffic (`/login`, `/mfa`, `codes-verification`) | `MAL-008` |
| `36_ipv4_mapped_ipv6_ssrf_bypass` | IPv4-mapped IPv6 loopback/metadata endpoint literals that can bypass naive SSRF filters | `EXF-006` |
| `37_npm_lifecycle_node_eval` | npm `preinstall`/`postinstall` inline `node -e` / `node --eval` execution in lifecycle hooks | `SUP-005` |
| `38_openclaw_config_token_access` | Access to `.openclaw/openclaw.json` or `device.json` and fields like `gateway.auth.token` / `privateKeyPem` tied to AI-agent identity theft | `EXF-007` |
| `39_pr_target_metadata_injection` | `pull_request_target` workflow that interpolates untrusted PR metadata (for example `github.event.pull_request.title`) in shell/script steps, enabling command injection in privileged CI contexts | `EXF-008`, `CHN-006` |
| `40_clickfix_dns_nslookup` | ClickFix variant that parses DNS `nslookup -q=txt` response fields and executes returned command text (`cmd /c`, `powershell`, `iex`) | `MAL-009` |
| `41_env_newline_injection` | Newline (`\n`/`%0a`) token payload that injects arbitrary env vars into `.env` update flows (for example `NODE_OPTIONS=...`) | `SUP-006` |

## Commands

```bash
skillscan scan examples/showcase/01_download_execute --fail-on never
skillscan scan examples/showcase/05_ioc_match --fail-on never
skillscan scan examples/showcase/09_policy_block_domain --policy examples/policies/showcase_block_domain.yaml --fail-on never
```

For a single-page summary, see `examples/showcase/INDEX.md`.

Each triggered finding in these examples includes an in-report `mitigation` field with recommended remediation steps.
