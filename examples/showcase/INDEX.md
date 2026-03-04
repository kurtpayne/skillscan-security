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
20. `20_ai_semantic_risk`: semantic credential-harvest wording (detected via `--ai-assist`)
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

## Run examples

```bash
skillscan scan examples/showcase/01_download_execute --fail-on never
skillscan scan examples/showcase/05_ioc_match --fail-on never
skillscan scan examples/showcase/09_policy_block_domain --policy examples/policies/showcase_block_domain.yaml --fail-on never
skillscan scan examples/showcase/20_ai_semantic_risk --ai-assist --fail-on never
skillscan scan examples/showcase/21_npm_lifecycle_abuse --fail-on never
skillscan scan examples/showcase/27_github_actions_secrets_exfil --fail-on never
skillscan scan examples/showcase/28_npx_registry_fallback --fail-on never
skillscan scan examples/showcase/29_claude_sed_path_bypass --fail-on never
```
