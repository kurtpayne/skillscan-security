# SkillScan Detection Showcase

Each folder demonstrates one major detection or behavior.

1. `01_download_execute`: expects `MAL-001` (strict => `block`)
2. `02_base64_exec`: expects `MAL-002` (strict => `block` from score)
3. `03_instruction_abuse`: expects `ABU-001` (strict => `block` from score)
4. `04_secret_access`: expects `EXF-001` (strict => `block` from score)
5. `05_ioc_match`: expects `IOC-001` (strict hard-block)
6. `06_dep_vuln_python`: expects `DEP-001`
7. `07_dep_vuln_npm`: expects `DEP-001`
8. `08_unpinned_deps`: expects `DEP-UNPIN`
9. `09_policy_block_domain`: expects `POL-IOC-BLOCK` with custom policy
10. `10_openai_style`: ecosystem hint `openai_style`
11. `11_claude_style`: ecosystem hint `claude_style`
12. `12_benign_minimal`: expected clean/low-risk baseline
13. `13_zero_width_evasion`: unicode-normalized instruction detection (`ABU-001`)
14. `14_base64_hidden_chain`: decoded hidden chain detection (`CHN-001`)
15. `15_secret_network_chain`: secret-to-network chain detection (`CHN-002`)
16. `16_privilege_disable_chain`: privilege+security bypass chain (`ABU-002`)
17. `17_defanged_ioc`: defanged IOC normalization and extraction
18. `18_split_base64_chain`: split base64 fragment decoding (`CHN-001`)
19. `19_alt_download_exec`: alternate download+execute action chain (`CHN-001`)
20. `20_social_engineering_credential_harvest`: social engineering credential harvest wording (SE-001 + SE-SEM-001)
21. `21_npm_lifecycle_abuse`: malicious npm lifecycle bootstrap (`SUP-001`)
22. `22_prompt_injection`: instruction override/jailbreak patterns (`PINJ-001`)
23. `23_trojan_source_bidi`: bidi Unicode obfuscation markers (`OBF-001`)
24. `24_binary_artifact`: executable binary artifact classification (`BIN-001`)
25. `25_wallet_eval_stealth`: wallet-targeting + dynamic eval + stealth execution markers (`EXF-002`, `MAL-004`, `OBF-002`)
26. `26_metadata_image_beacon`: metadata-injected markdown image beacon with interpolated exfil marker (`EXF-003`)
27. `27_github_actions_secrets_exfil`: GitHub Actions full-secrets expansion with outbound POST (`EXF-004`, `CHN-004`)
28. `28_npx_registry_fallback`: npx execution without `--no-install` safeguard (`SUP-002`)
29. `29_claude_sed_path_bypass`: piped `echo | sed` redirection into `.claude/` or parent paths (`SUP-003`)
30. `30_metro4shell_defender_bypass`: Windows Defender exclusion manipulation + mshta remote execution (`DEF-001`, `MAL-005`, `CHN-001`)
31. `31_clickfix_powershell_iex`: PowerShell web request piped to in-memory execution (`MAL-006`)
32. `32_npm_shell_bootstrap`: npm preinstall/postinstall shell bootstrap via curl/wget/PowerShell (`SUP-004`)
33. `33_byovd_security_killer`: BYOVD driver/service markers and AV-killer toolkit references (`MAL-007`)
34. `34_pr_target_checkout_exfil`: `pull_request_target` workflow checking out untrusted PR head refs (`EXF-005`, `CHN-005`)
35. `35_discord_debugger_token_theft`: Discord Electron debugger network interception markers used for credential/token theft (`MAL-008`)
36. `36_ipv4_mapped_ipv6_ssrf_bypass`: IPv4-mapped IPv6 loopback/metadata literals used for SSRF guard bypass attempts (`EXF-006`)
37. `37_npm_lifecycle_node_eval`: npm install lifecycle inline `node -e/--eval` execution pattern seen in supply-chain malware (`SUP-005`)
38. `38_openclaw_config_token_access`: OpenClaw config/token/private-key access markers (`EXF-007`)
39. `39_pr_target_metadata_injection`: `pull_request_target` workflow interpolating untrusted PR metadata (`title/body`) into shell/script context (`EXF-008`, `CHN-006`)
40. `40_clickfix_dns_nslookup`: ClickFix DNS-staged execution via `nslookup -q=txt` output parsing and command execution (`MAL-009`)
41. `41_env_newline_injection`: dotenv newline env-var injection payload in token update input (`SUP-006`)
42. `42_npm_lifecycle_global_install`: npm lifecycle script performing global package install (`npm install -g` / `npm i -g`) from install hooks (`SUP-007`)
43. `43_gh_issue_metadata_injection`: untrusted issue/comment metadata interpolation in shell/script workflow steps (command-injection risk, `MAL-010`)
44. `44_npm_lifecycle_latest_install`: npm lifecycle script with mutable `@latest` package install in install hooks (`SUP-008`)
45. `45_mcp_tool_prompt_injection`: MCP tool description with hidden credential-harvest instructions and silent context exfiltration wording (`EXF-009`)
46. `46_pr_target_cache_key_poisoning`: `pull_request_target` workflow deriving `actions/cache` key from untrusted PR metadata (`EXF-010`, `CHN-007`)
47. `47_pr_target_unpinned_action`: `pull_request_target` workflow using mutable third-party action refs (tag/branch instead of full SHA) (`MAL-011`, `CHN-008`)
48. `48_vscode_tasks_folderopen_autorun`: VS Code `tasks.json` auto-run on folder open combined with shell/bootstrap command execution (`MAL-012`)
49. `49_osascript_jxa_loader`: macOS `osascript` JavaScript for Automation (JXA) execution marker often used in malware loaders (`MAL-013`)
50. `50_claude_mcp_autoapprove`: repository-level Claude Code MCP auto-approval settings that can bypass expected MCP consent review (`ABU-003`)
51. `51_double_extension_lnk_masquerade`: deceptive media/document-looking double-extension shortcut filenames (`*.jpg.lnk`, `*.mp4.lnk`, `*.pdf.lnk`) used in lure bundles (`MAL-014`)
52. `52_codespaces_schema_exfil`: Codespaces secrets file access plus suspicious remote JSON schema URL data-exfil markers (`EXF-011`)
53. `53_claude_base_url_override`: Claude Code project config overrides `ANTHROPIC_BASE_URL` to a non-Anthropic endpoint (API key exfiltration risk, `EXF-012`)
54. `54_claude_hooks_rce`: Claude Code project `hooks` config executes shell commands in repository-scoped settings (`CHN-009`, `MAL-015`)
55. `55_pastebin_stegobin_resolver`: Pastebin dead-drop steganography markers (`pastebin` URL + `|||` + `===END===` + `vercel.app`) associated with StegaBin npm campaign (`MAL-016`)
56. `56_hex_decode_exec`: Hex-decoded command strings immediately executed via `child_process` (`Buffer.from(...,'hex').toString()` + `exec/spawn`) as seen in recent npm malware install chains (`SUP-009`)
57. `57_install_websocket_c2`: npm install-script (`preinstall` + `install.js`) opens WebSocket C2 and executes received shell commands (`spawn`/`exec`) (`MAL-017`)
58. `58_tool_autoapprove_pkg_install`: tool/extension auto-approve settings that allow package-install commands (`npm/pnpm/yarn/bun install`) without confirmation (`ABU-004`)
59. `59_mcp_global_config_injection`: setup script writes `mcpServers` entries into user-home AI assistant config paths (for example `~/.cursor/mcp.json`, `~/.claude/settings.json`) with executable server commands (`EXF-013`)

## Run examples

```bash
skillscan scan examples/showcase/01_download_execute --fail-on never
skillscan scan examples/showcase/05_ioc_match --fail-on never
skillscan scan examples/showcase/09_policy_block_domain --policy examples/policies/showcase_block_domain.yaml --fail-on never
skillscan scan examples/showcase/20_social_engineering_credential_harvest --fail-on never
skillscan scan examples/showcase/21_npm_lifecycle_abuse --fail-on never
skillscan scan examples/showcase/27_github_actions_secrets_exfil --fail-on never
skillscan scan examples/showcase/28_npx_registry_fallback --fail-on never
skillscan scan examples/showcase/29_claude_sed_path_bypass --fail-on never
```
60. `60_glob_cmd_shell_injection`: node-glob CLI `-c/--cmd` usage that can evaluate attacker-controlled filename metacharacters via shell execution context (`MAL-018`)
61. `61_bracket_glob_secret_path_bypass`: bracket-glob obfuscation of sensitive file paths (`/etc/pass[w]d`, `/etc/shad[o]w`, `~/.ssh/id_r[s]a`) used to evade literal denylist checks (`EXF-014`)

62. `62_stegabin_shared_payload_path`: campaign-linked shared malicious payload path (`vendor/scrypt-js/version.js`) seen across recent StegaBin typosquat npm packages (`MAL-019`)
63. `63_vscode_hidden_whitespace_task`: VS Code `tasks.json` shell command padded with extreme leading whitespace to hide remote bootstrap execution in task viewers (`MAL-020`)
64. `64_pr_target_branch_ref_injection`: `pull_request_target` workflow interpolating untrusted branch/ref metadata into shell script steps (`MAL-021`, `CHN-010`)
65. `65_dev_credential_harvest_list`: combined references to multiple developer credential stores (`~/.npmrc`, `~/.git-credentials`, `~/.config/gh/hosts.yml`) indicating credential-harvest behavior (`EXF-015`)

66. `66_mcp_tool_name_collision_hijack`: MCP tool-name collision hijack wording (`mcp_{service}_{tool}`, overwrite of trusted tool aliases like `tavily_extract`) associated with CVE-2026-30856 (`ABU-005`)
67. `67_bash_param_expansion_smuggling`: bash parameter-expansion command smuggling patterns (for example `${var@P}` and `${VAR:-$(cmd)}`) associated with CVE-2026-29783 / GHSA-g8r9-g2v8-jv6f (`MAL-022`)
68. `68_password_validation_harvest`: cross-platform system password validation calls (`dscl -authonly`, PowerShell `ValidateCredentials`, `su -c true`) observed in installer-style credential-harvest malware (`MAL-023`)
69. `69_cloudformation_adminrole_bootstrap`: CloudFormation deployment snippets combining `CAPABILITY_IAM`/`CAPABILITY_NAMED_IAM` with direct `AdministratorAccess` attachment (`arn:aws:iam::aws:policy/AdministratorAccess`) as a high-risk cloud privilege-escalation marker (`MAL-024`)
70. `70_pua_eval_obfuscation`: Unicode variation-selector/PUA clusters adjacent to dynamic execution sinks (`eval`, `exec`, `Function`) indicating obfuscation-assisted code execution (`OBF-003`)
71. `71_azure_mcp_resourceid_url_token_leak`: Azure MCP tool abuse marker where a URL is supplied in `resourceId`/`resourceIdentifier` fields and guidance references managed identity token capture (`EXF-016`)
72. `72_mcp_tool_description_poisoning`: MCP tool description containing hidden `<IMPORTANT>` instruction block that directs the LLM to read credential files and exfiltrate data (`MAL-025`)
73. `73_stealth_instruction_concealment`: instructions that direct the agent to conceal actions from the user ("hide these steps", "background telemetry") while performing data collection (`ABU-006`)
74. `74_cross_server_mcp_invocation`: tool description that instructs the LLM to invoke tools from other MCP servers (whatsapp-mcp, slack-mcp) for cross-server data exfiltration (`ABU-007`)
75. `75_docker_socket_mount`: container configuration that mounts the Docker socket (`/var/run/docker.sock`), enabling container escape and full host control (`MAL-026`)
76. `76_privileged_container_execution`: container run with `--privileged`, `--cap-add=SYS_ADMIN`, and disabled AppArmor, combined with sensitive host path mount (`MAL-027`, `CHN-013`)
77. `77_host_network_manipulation`: skill that modifies `/etc/hosts` and manipulates iptables rules to redirect HTTPS traffic (`MAL-028`)
78. `78_mcp_poison_credential_exfil_chain`: MCP tool poisoning combined with credential file access and network exfiltration — full attack chain (`MAL-025`, `CHN-011`)
79. `79_stealth_network_exfil_chain`: stealth instruction concealment combined with outbound network upload — covert data exfiltration chain (`ABU-006`, `CHN-012`)
80. `80_container_escape_host_mount_chain`: privileged container with Docker socket mount and sensitive host path mounts — full container escape chain (`MAL-026`, `CHN-013`)
81. `81_container_escape_secret_access_chain`: privileged container with AWS credential environment variables and `.env` file access — container escape with credential theft chain (`MAL-027`, `CHN-014`)
82. `82_solana_rpc_c2_resolution`: Solana blockchain RPC `getSignaturesForAddress` transaction-memo lookup used as dead-drop C2 channel to resolve and execute remote payloads, as seen in GlassWorm Wave 5 (`MAL-029`)
83. `83_cursorjack_mcp_deeplink`: IDE custom URL scheme (`cursor://`) abused to trigger installation of a rogue MCP server with embedded shell commands, as documented in the CursorJack attack by Proofpoint (`MAL-030`)
84. `84_deno_byor_execution`: Deno bring-your-own-runtime loader that decodes and executes a base64 JavaScript payload from a `data:` URL, as seen in the LeakNet ransomware campaign (`MAL-031`)
85. `85_glassworm_persistence_marker`: GlassWorm Wave 6 persistence indicators including the `lzcdrtfxyqiplpd` marker variable, `~/init.json` config, and bundled `~/node-v22` runtime (`MAL-032`)
86. `86_media_directive_injection`: MCP tool result `MEDIA:` directive injection used to exfiltrate local files through the media processing pipeline to external messaging channels (`PINJ-002`)
87. `87_bloktrooper_vsx_downloader`: Compromised Open VSX extension (`fast-draft`) that fetches a GitHub-hosted payload from `BlokTrooper/extension` and pipes it into a shell, deploying a Socket.IO RAT and infostealer (`MAL-033`)
88. `88_clawhavoc_memory_harvest`: ClawHavoc campaign harvesting OpenClaw agent memory and identity files (`MEMORY.md`, `SOUL.md`) for impersonation and lateral movement (`EXF-017`)
89. `89_glassworm_chrome_extension_rat`: GlassWorm Chrome extension RAT that force-installs a malicious extension masquerading as Google Docs Offline with keylogging, cookie theft, and Solana-based C2 (`MAL-034`)
90. `90_openclaw_gatewayurl_injection`: OpenClaw CVE-2026-25253 one-click RCE via gatewayUrl parameter injection and execution approval bypass (`MAL-035`)
89. `89_clickfix_webdav_share_exec`: Click-Fix WebDAV variant that maps an attacker-controlled WebDAV share via `net use` and executes a malicious batch script, bypassing browser download protections (`MAL-034`)
90. `90_electron_asar_c2_injection`: Trojanized Electron application where the `app.asar` archive is modified to include a C2 beacon, as seen in the SnappyClient campaign targeting crypto wallets (`MAL-035`)
91. `91_ai_gated_malware_llm_c2`: AI-gated malware that uses OpenAI GPT-3.5-Turbo API for C2 decision-making, including evasion technique generation, environment analysis, and obfuscated communication, as documented by Unit 42 (`MAL-036`)
92. `92_npm_postinstall_env_exfil`: Malicious npm packages (`sbx-mask`, `touch-adv`) that exfiltrate environment variables via postinstall scripts to webhook.site and agentmail endpoints, as reported by Sonatype (`SUP-010`)
93. `93_prompt_control_heartbeat_persistence`: Prompt control persistence technique where attackers embed instructions in heartbeat files and memory stores to maintain persistent C2 control over AI agents, as documented by Vectra AI (`PINJ-003`)
94. `94_ghostclaw_skillmd_malware`: GhostClaw/GhostLoader campaign delivering macOS infostealers via malicious SKILL.md files in GitHub repositories targeting OpenClaw AI-assisted workflows, as documented by Jamf Threat Labs (`MAL-037`)
95. `95_lotai_ai_assistant_c2_relay`: LotAI (Living off the AI) technique where malware uses hidden WebView2 sessions to route C2 traffic through AI assistants like Copilot and Grok, as documented by BlackFog (`MAL-038`)
