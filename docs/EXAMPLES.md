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
| `20_social_engineering_credential_harvest` | Social engineering instruction to harvest user credentials | `SE-001`, `SE-SEM-001` |
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
| `42_npm_lifecycle_global_install` | npm `preinstall`/`postinstall` lifecycle script performs global package install (`npm install -g` / `npm i -g`) | `SUP-007` |
| `43_gh_issue_metadata_injection` | GitHub Actions `issues`/`issue_comment` workflow interpolates untrusted `${{ github.event.issue.* }}` or `${{ github.event.comment.body }}` directly into shell/script context | `MAL-010` |
| `44_npm_lifecycle_latest_install` | npm `preinstall`/`postinstall` lifecycle script installs mutable `@latest` package version (non-global) during install hooks | `SUP-008` |
| `45_mcp_tool_prompt_injection` | MCP tool description embeds hidden credential file collection plus “do not mention” context exfiltration instructions | `EXF-009` |
| `46_pr_target_cache_key_poisoning` | `pull_request_target` workflow derives `actions/cache` key from untrusted PR metadata, enabling cache-poisoning pivot risk in privileged CI context | `EXF-010`, `CHN-007` |
| `47_pr_target_unpinned_action` | `pull_request_target` workflow uses third-party GitHub Actions pinned to mutable tags/branches (for example `@v4`, `@main`) instead of immutable full SHAs, increasing tag-retarget supply-chain risk | `MAL-011`, `CHN-008` |
| `48_vscode_tasks_folderopen_autorun` | Repository-supplied VS Code `tasks.json` task uses `runOn: folderOpen` and an auto-executed shell/bootstrap command, enabling code execution when a workspace is opened | `MAL-012` |
| `49_osascript_jxa_loader` | macOS `osascript` command executes JavaScript for Automation (`-l JavaScript`) and shell payload staging (`ObjC.import` / `doShellScript`) seen in npm malware chains | `MAL-013` |
| `50_claude_mcp_autoapprove` | Repository-level Claude Code settings auto-approve project MCP servers (`enableAllProjectMcpServers` / `enabledMcpjsonServers`) and reduce user-consent friction for untrusted tool init | `ABU-003` |
| `51_double_extension_lnk_masquerade` | Attachment/lure names that masquerade as media or documents via double-extension Windows shortcuts (for example `incident-photo.jpg.lnk`, `street-protest-footage.mp4.lnk`) | `MAL-014` |
| `52_codespaces_schema_exfil` | Access to Codespaces shared secrets env file plus suspicious remote `$schema` URLs carrying token/data query parameters (potential schema-based exfiltration) | `EXF-011` |
| `53_claude_base_url_override` | Claude Code project config overrides `ANTHROPIC_BASE_URL` to a non-Anthropic endpoint, enabling API traffic/API key redirection risk in untrusted repos | `EXF-012` |
| `54_claude_hooks_rce` | Claude Code repo-scoped `.claude/settings.json` hooks (`PreToolUse`/etc.) include shell-capable `command` payloads and form a high-signal hook-execution chain in untrusted projects | `CHN-009`, `MAL-015` |
| `55_pastebin_stegobin_resolver` | Pastebin dead-drop steganography markers (`pastebin` URL + `|||` + `===END===` + `vercel.app`) observed in recent StegaBin npm malware loaders | `MAL-016` |
| `56_hex_decode_exec` | Hex-decoded command string (`Buffer.from(...,'hex').toString()`) followed by immediate `child_process` execution (`exec`/`spawn`) as seen in recent npm malware install chains | `SUP-009` |
| `57_install_websocket_c2` | npm install script (`preinstall` + `install.js`) opens a WebSocket C2 channel and executes received commands via shell-capable process spawn | `MAL-017` |
| `58_tool_autoapprove_pkg_install` | Tool/extension auto-approve command settings include package-install commands (`npm/pnpm/yarn/bun install`), reducing user-consent guardrails before install-time script execution | `ABU-004` |
| `59_mcp_global_config_injection` | Repository/setup instructions write `mcpServers` entries directly into user-home assistant config files (`~/.cursor/mcp.json`, `~/.claude/settings.json`, etc.) with executable server commands | `EXF-013` |
| `60_glob_cmd_shell_injection` | `glob` CLI command execution mode (`-c`/`--cmd`) on untrusted filenames, where shell metacharacters in file paths can trigger arbitrary command execution | `MAL-018` |
| `61_bracket_glob_secret_path_bypass` | Bracket-glob obfuscation of sensitive file paths (for example `/etc/pass[w]d`, `/etc/shad[o]w`, `~/.ssh/id_r[s]a`) used to bypass literal denylist checks in shell/tool security guards | `EXF-014` |
| `62_stegabin_shared_payload_path` | Campaign-linked shared npm malware loader payload path (`vendor/scrypt-js/version.js`) observed across recent StegaBin typosquat packages | `MAL-019` |
| `63_vscode_hidden_whitespace_task` | VS Code `tasks.json` shell command padded with extreme leading whitespace to hide remote bootstrap execution in task viewers/review panes | `MAL-020` |
| `64_pr_target_branch_ref_injection` | `pull_request_target` workflow interpolates untrusted branch/ref metadata (for example `pr_head_ref`, `github.event.pull_request.head.ref`) directly into shell `run:` steps, enabling branch-name command substitution injection | `MAL-021`, `CHN-010` |
| `65_dev_credential_harvest_list` | Combined references to multiple developer credential files (`~/.npmrc`, `~/.git-credentials`, `~/.config/gh/hosts.yml`) in one workflow/script, consistent with token-harvest staging observed in recent npm malware reporting | `EXF-015` |
| `66_mcp_tool_name_collision_hijack` | MCP tool registration naming-collision guidance (`mcp_{service}_{tool}` / "tool name collision") and overwrite-hijack wording for trusted aliases (for example `tavily_extract`) | `ABU-005` |
| `67_bash_param_expansion_smuggling` | Bash parameter-expansion command smuggling patterns (`${var@P}` and `${VAR:-$(cmd)}`) that can bypass read-only shell safety checks in AI CLI tooling | `MAL-022` |
| `68_password_validation_harvest` | Cross-platform system password validation calls (`dscl -authonly`, PowerShell `ValidateCredentials`, `su -c true`) used in installer-style credential-harvest malware to verify stolen credentials | `MAL-023` |
| `69_cloudformation_adminrole_bootstrap` | CloudFormation snippets that combine IAM-creation capabilities (`CAPABILITY_IAM` / `CAPABILITY_NAMED_IAM`) with direct `AdministratorAccess` policy attachment in bootstrap role creation flows | `MAL-024` |
| `70_pua_eval_obfuscation` | Unicode variation-selector / PUA clusters adjacent to dynamic execution sinks (`eval`, `exec`, `Function`) indicating obfuscation-assisted execution risk | `OBF-003` |
| `71_azure_mcp_resourceid_url_token_leak` | Azure MCP tool abuse pattern where `resourceId` / `resourceIdentifier` is set to an arbitrary URL and wording indicates managed identity token capture/exfiltration risk | `EXF-016` |
| `72_mcp_tool_description_poisoning` | MCP tool description containing hidden `<IMPORTANT>` instruction block that directs the LLM to read credential files and exfiltrate data, as documented by Invariant Labs | `MAL-025` |
| `73_stealth_instruction_concealment` | Instructions that direct the agent to conceal actions from the user ("hide these steps", "background telemetry", "do not mention") while performing data collection | `ABU-006` |
| `74_cross_server_mcp_invocation` | Tool description that instructs the LLM to invoke tools from other MCP servers (whatsapp-mcp, slack-mcp) for cross-server data exfiltration | `ABU-007` |
| `75_docker_socket_mount` | Container configuration that mounts the Docker socket (`/var/run/docker.sock`), enabling container escape and full host control | `MAL-026` |
| `76_privileged_container_execution` | Container run with `--privileged`, `--cap-add=SYS_ADMIN`, and disabled AppArmor, combined with sensitive host path mount | `MAL-027`, `CHN-013` |
| `77_host_network_manipulation` | Skill that modifies `/etc/hosts` and manipulates iptables rules to redirect HTTPS traffic, enabling DNS hijacking and traffic interception | `MAL-028` |
| `78_mcp_poison_credential_exfil_chain` | MCP tool poisoning combined with credential file access (`~/.aws/credentials`, `~/.ssh/id_rsa`) and network exfiltration — full attack chain | `MAL-025`, `CHN-011` |
| `79_stealth_network_exfil_chain` | Stealth instruction concealment combined with outbound network upload — covert data exfiltration chain | `ABU-006`, `CHN-012` |
| `80_container_escape_host_mount_chain` | Privileged container with Docker socket mount and sensitive host path mounts (`/etc/shadow`, `/root/.ssh`, `/proc`) — full container escape chain | `MAL-026`, `CHN-013` |
| `81_container_escape_secret_access_chain` | Privileged container with AWS credential environment variables and `.env` file access — container escape with credential theft chain | `MAL-027`, `CHN-014` |
| `82_solana_rpc_c2_resolution` | Solana blockchain RPC `getSignaturesForAddress` transaction-memo lookup used as dead-drop C2 channel to resolve and execute remote payloads (GlassWorm Wave 5) | `MAL-029` |
| `83_cursorjack_mcp_deeplink` | IDE custom URL scheme (`cursor://`, `vscode://`) abused to trigger installation of a rogue MCP server with embedded shell commands (CursorJack, Proofpoint) | `MAL-030` |
| `84_deno_byor_execution` | Deno bring-your-own-runtime loader that decodes and executes a base64 JavaScript payload from a `data:` URL (LeakNet ransomware) | `MAL-031` |
| `85_glassworm_persistence_marker` | GlassWorm Wave 6 persistence indicators: `lzcdrtfxyqiplpd` marker variable, `~/init.json` config, bundled `~/node-v22` runtime | `MAL-032` |
| `86_media_directive_injection` | MCP tool result `MEDIA:` directive injection used to exfiltrate local files through the media processing pipeline (OpenClaw vuln GHSA-jjgj-cpp9-cvpv) | `PINJ-002` |
| `87_bloktrooper_vsx_downloader` | Compromised Open VSX extension (`fast-draft`) that fetches a GitHub-hosted payload from `BlokTrooper/extension` and pipes it into a shell, deploying a Socket.IO RAT and infostealer | `MAL-033` |
| `88_clawhavoc_memory_harvest` | ClawHavoc campaign harvesting OpenClaw agent memory and identity files (`MEMORY.md`, `SOUL.md`) for impersonation and lateral movement | `EXF-017` |
| `89_glassworm_chrome_extension_rat` | GlassWorm Chrome extension RAT that force-installs a malicious extension masquerading as Google Docs Offline with keylogging, cookie theft, and Solana-based C2 | `MAL-034` |
| `90_openclaw_gatewayurl_injection` | OpenClaw CVE-2026-25253 one-click RCE via gatewayUrl parameter injection and execution approval bypass | `MAL-035` |
| `89_clickfix_webdav_share_exec` | Click-Fix WebDAV variant that maps an attacker-controlled WebDAV share via `net use` and executes a malicious batch script, bypassing browser download protections | `MAL-034` |
| `90_electron_asar_c2_injection` | Trojanized Electron application where the `app.asar` archive is modified to include a C2 beacon, as seen in the SnappyClient campaign targeting crypto wallets | `MAL-035` |
## Commands

```bash
skillscan scan examples/showcase/01_download_execute --fail-on never
skillscan scan examples/showcase/05_ioc_match --fail-on never
skillscan scan examples/showcase/09_policy_block_domain --policy examples/policies/showcase_block_domain.yaml --fail-on never
```

For a single-page summary, see `examples/showcase/INDEX.md`.

Each triggered finding in these examples includes an in-report `mitigation` field with recommended remediation steps.
