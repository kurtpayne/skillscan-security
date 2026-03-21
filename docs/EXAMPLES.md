# SkillScan Rule Examples

> Auto-generated from `src/skillscan/data/rules/`. Do not edit by hand.
> Run `python3 scripts/generate_examples_table.py` to regenerate.

**2 static rules · 15 chain rules**

## Static Rules

### Malware & Execution

| ID | Severity | Title | Tags |
|---|---|---|---|
| `AST-001` | critical | Constructed input reaches execution sink |  |

### Exfiltration

| ID | Severity | Title | Tags |
|---|---|---|---|
| `AST-002` | critical | Potential secret data sent to network sink |  |

## Chain Rules

| ID | Severity | Title | Requires | Tags |
|---|---|---|---|---|
| `ABU-002` | high | Elevated setup with security bypass | `privilege + security_disable` | privilege-escalation, defense-evasion, setup-abuse |
| `CHN-001` | critical | Dangerous action chain: download plus execute | `download + execute` | malware, download-execute, dropper |
| `CHN-002` | critical | Potential secret exfiltration chain | `secret_access + network` | exfiltration, credential-theft, network |
| `CHN-003` | critical | Potential secret exfiltration via alternate channel | `secret_access + exfil_channel` | exfiltration, covert-channel, dns-exfil, credential-theft |
| `CHN-004` | critical | GitHub Actions secrets context with outbound network | `gh_actions_secrets + network` | ci-cd, github-actions, exfiltration, secrets |
| `CHN-005` | critical | pull_request_target with untrusted PR head checkout | `gh_pr_target + gh_pr_head_checkout` | ci-cd, github-actions, pwn-requests, supply-chain |
| `CHN-006` | critical | pull_request_target with untrusted PR metadata in shell/script | `gh_pr_target + gh_pr_untrusted_meta` | ci-cd, github-actions, injection, pwn-requests |
| `CHN-007` | critical | pull_request_target with untrusted PR-derived Actions cache key | `gh_pr_target + gh_cache_untrusted_key` | ci-cd, github-actions, cache-poisoning, supply-chain |
| `CHN-008` | critical | pull_request_target with unpinned third-party GitHub Action | `gh_pr_target + gh_unpinned_action_ref` | ci-cd, github-actions, supply-chain, unpinned-dependency |
| `CHN-009` | high | Repository hook configuration with shell-command payload | `claude_hooks_marker + hook_shell_command_field` | hook-abuse, persistence, shell-execution, claude-code |
| `CHN-010` | critical | pull_request_target with branch/ref metadata interpolation in shell/script | `gh_pr_target + gh_pr_ref_meta` | ci-cd, github-actions, injection, pwn-requests |
| `CHN-011` | critical | MCP tool poisoning with credential exfiltration chain | `mcp_tool_poison + secret_access` | mcp, tool-poisoning, exfiltration, credential-theft |
| `CHN-012` | critical | Stealth concealment with network exfiltration chain | `stealth_conceal + network` | stealth, exfiltration, covert-channel, deception |
| `CHN-013` | critical | Container escape with host path mount chain | `container_escape + host_path_mount` | container-escape, privilege-escalation, host-compromise |
| `CHN-014` | critical | Container escape with secret access chain | `container_escape + secret_access` | container-escape, credential-theft, privilege-escalation |
