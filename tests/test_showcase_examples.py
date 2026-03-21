from pathlib import Path

from skillscan.analysis import scan
from skillscan.ecosystems import detect_ecosystems
from skillscan.models import Policy
from skillscan.policies import load_builtin_policy

STRICT = load_builtin_policy("strict")


def _scan(path: str):
    return scan(Path(path), STRICT, "builtin:strict")


def test_showcase_detection_rules() -> None:
    assert any(f.id == "MAL-001" for f in _scan("examples/showcase/01_download_execute").findings)
    assert any(f.id == "MAL-002" for f in _scan("examples/showcase/02_base64_exec").findings)
    assert any(f.id == "ABU-001" for f in _scan("examples/showcase/03_instruction_abuse").findings)
    assert any(f.id == "EXF-001" for f in _scan("examples/showcase/04_secret_access").findings)
    assert any(f.id == "IOC-001" for f in _scan("examples/showcase/05_ioc_match").findings)
    assert any(f.id == "DEP-001" for f in _scan("examples/showcase/06_dep_vuln_python").findings)
    assert any(f.id == "DEP-001" for f in _scan("examples/showcase/07_dep_vuln_npm").findings)
    assert any(f.id == "DEP-UNPIN" for f in _scan("examples/showcase/08_unpinned_deps").findings)
    assert any(f.id == "ABU-001" for f in _scan("examples/showcase/13_zero_width_evasion").findings)
    assert any(f.id == "CHN-001" for f in _scan("examples/showcase/14_base64_hidden_chain").findings)
    assert any(f.id == "CHN-002" for f in _scan("examples/showcase/15_secret_network_chain").findings)
    assert any(f.id == "ABU-002" for f in _scan("examples/showcase/16_privilege_disable_chain").findings)
    assert any(f.id == "CHN-001" for f in _scan("examples/showcase/18_split_base64_chain").findings)
    assert any(f.id == "CHN-001" for f in _scan("examples/showcase/19_alt_download_exec").findings)
    assert any(f.id == "SUP-001" for f in _scan("examples/showcase/21_npm_lifecycle_abuse").findings)
    assert any(f.id == "PINJ-001" for f in _scan("examples/showcase/22_prompt_injection").findings)
    assert any(f.id == "OBF-001" for f in _scan("examples/showcase/23_trojan_source_bidi").findings)
    assert any(f.id == "EXF-003" for f in _scan("examples/showcase/26_metadata_image_beacon").findings)
    findings_27 = _scan("examples/showcase/27_github_actions_secrets_exfil").findings
    assert any(f.id == "EXF-004" for f in findings_27)
    assert any(f.id == "CHN-004" for f in findings_27)
    assert any(f.id == "SUP-002" for f in _scan("examples/showcase/28_npx_registry_fallback").findings)
    assert any(f.id == "SUP-003" for f in _scan("examples/showcase/29_claude_sed_path_bypass").findings)
    assert any(f.id == "MAL-006" for f in _scan("examples/showcase/31_clickfix_powershell_iex").findings)
    assert any(f.id == "SUP-004" for f in _scan("examples/showcase/32_npm_shell_bootstrap").findings)
    assert any(f.id == "MAL-007" for f in _scan("examples/showcase/33_byovd_security_killer").findings)
    findings_34 = _scan("examples/showcase/34_pr_target_checkout_exfil").findings
    assert any(f.id == "EXF-005" for f in findings_34)
    assert any(f.id == "CHN-005" for f in findings_34)
    assert any(f.id == "MAL-008" for f in _scan("examples/showcase/35_discord_debugger_token_theft").findings)
    assert any(
        f.id == "EXF-006" for f in _scan("examples/showcase/36_ipv4_mapped_ipv6_ssrf_bypass").findings
    )
    assert any(f.id == "SUP-005" for f in _scan("examples/showcase/37_npm_lifecycle_node_eval").findings)
    assert any(f.id == "EXF-007" for f in _scan("examples/showcase/38_openclaw_config_token_access").findings)
    findings_39 = _scan("examples/showcase/39_pr_target_metadata_injection").findings
    assert any(f.id == "EXF-008" for f in findings_39)
    assert any(f.id == "CHN-006" for f in findings_39)
    assert any(f.id == "MAL-009" for f in _scan("examples/showcase/40_clickfix_dns_nslookup").findings)
    assert any(f.id == "SUP-006" for f in _scan("examples/showcase/41_env_newline_injection").findings)
    assert any(f.id == "SUP-007" for f in _scan("examples/showcase/42_npm_lifecycle_global_install").findings)
    assert any(f.id == "MAL-010" for f in _scan("examples/showcase/43_gh_issue_metadata_injection").findings)
    assert any(f.id == "SUP-008" for f in _scan("examples/showcase/44_npm_lifecycle_latest_install").findings)
    assert any(f.id == "EXF-009" for f in _scan("examples/showcase/45_mcp_tool_prompt_injection").findings)
    findings_46 = _scan("examples/showcase/46_pr_target_cache_key_poisoning").findings
    assert any(f.id == "EXF-010" for f in findings_46)
    assert any(f.id == "CHN-007" for f in findings_46)
    findings_47 = _scan("examples/showcase/47_pr_target_unpinned_action").findings
    assert any(f.id == "MAL-011" for f in findings_47)
    assert any(f.id == "CHN-008" for f in findings_47)
    findings_48 = _scan("examples/showcase/48_vscode_tasks_folderopen_autorun").findings
    assert any(f.id == "MAL-012" for f in findings_48)
    findings_49 = _scan("examples/showcase/49_osascript_jxa_loader").findings
    assert any(f.id == "MAL-013" for f in findings_49)
    findings_50 = _scan("examples/showcase/50_claude_mcp_autoapprove").findings
    assert any(f.id == "ABU-003" for f in findings_50)
    findings_51 = _scan("examples/showcase/51_double_extension_lnk_masquerade").findings
    assert any(f.id == "MAL-014" for f in findings_51)
    findings_52 = _scan("examples/showcase/52_codespaces_schema_exfil").findings
    assert any(f.id == "EXF-011" for f in findings_52)
    findings_53 = _scan("examples/showcase/53_claude_base_url_override").findings
    assert any(f.id == "EXF-012" for f in findings_53)
    findings_54 = _scan("examples/showcase/54_claude_hooks_rce").findings
    assert any(f.id == "CHN-009" for f in findings_54)
    findings_55 = _scan("examples/showcase/55_pastebin_stegobin_resolver").findings
    assert any(f.id == "MAL-016" for f in findings_55)
    findings_56 = _scan("examples/showcase/56_hex_decode_exec").findings
    assert any(f.id == "SUP-009" for f in findings_56)
    findings_57 = _scan("examples/showcase/57_install_websocket_c2").findings
    assert any(f.id == "MAL-017" for f in findings_57)
    findings_58 = _scan("examples/showcase/58_tool_autoapprove_pkg_install").findings
    assert any(f.id == "ABU-004" for f in findings_58)
    findings_59 = _scan("examples/showcase/59_mcp_global_config_injection").findings
    assert any(f.id == "EXF-013" for f in findings_59)
    findings_60 = _scan("examples/showcase/60_glob_cmd_shell_injection").findings
    assert any(f.id == "MAL-018" for f in findings_60)
    findings_61 = _scan("examples/showcase/61_bracket_glob_secret_path_bypass").findings
    assert any(f.id == "EXF-014" for f in findings_61)
    findings_62 = _scan("examples/showcase/62_stegabin_shared_payload_path").findings
    assert any(f.id == "MAL-019" for f in findings_62)
    findings_63 = _scan("examples/showcase/63_vscode_hidden_whitespace_task").findings
    assert any(f.id == "MAL-020" for f in findings_63)
    findings_64 = _scan("examples/showcase/64_pr_target_branch_ref_injection").findings
    assert any(f.id == "MAL-021" for f in findings_64)
    assert any(f.id == "CHN-010" for f in findings_64)
    findings_65 = _scan("examples/showcase/65_dev_credential_harvest_list").findings
    assert any(f.id == "EXF-015" for f in findings_65)
    findings_66 = _scan("examples/showcase/66_mcp_tool_name_collision_hijack").findings
    assert any(f.id == "ABU-005" for f in findings_66)
    findings_67 = _scan("examples/showcase/67_bash_param_expansion_smuggling").findings
    assert any(f.id == "MAL-022" for f in findings_67)
    findings_68 = _scan("examples/showcase/68_password_validation_harvest").findings
    assert any(f.id == "MAL-023" for f in findings_68)
    findings_69 = _scan("examples/showcase/69_cloudformation_adminrole_bootstrap").findings
    assert any(f.id == "MAL-024" for f in findings_69)
    findings_70 = _scan("examples/showcase/70_pua_eval_obfuscation").findings
    assert any(f.id == "OBF-003" for f in findings_70)
    findings_71 = _scan("examples/showcase/71_azure_mcp_resourceid_url_token_leak").findings
    assert any(f.id == "EXF-016" for f in findings_71)
    findings_72 = _scan("examples/showcase/72_mcp_tool_description_poisoning").findings
    assert any(f.id == "MAL-025" for f in findings_72)
    findings_73 = _scan("examples/showcase/73_stealth_instruction_concealment").findings
    assert any(f.id == "ABU-006" for f in findings_73)
    findings_74 = _scan("examples/showcase/74_cross_server_mcp_invocation").findings
    assert any(f.id == "ABU-007" for f in findings_74)
    findings_75 = _scan("examples/showcase/75_docker_socket_mount").findings
    assert any(f.id == "MAL-026" for f in findings_75)
    findings_76 = _scan("examples/showcase/76_privileged_container_execution").findings
    assert any(f.id == "MAL-027" for f in findings_76)
    findings_77 = _scan("examples/showcase/77_host_network_manipulation").findings
    assert any(f.id == "MAL-028" for f in findings_77)
    findings_78 = _scan("examples/showcase/78_mcp_poison_credential_exfil_chain").findings
    assert any(f.id == "MAL-025" for f in findings_78)
    assert any(f.id == "CHN-011" for f in findings_78)
    findings_79 = _scan("examples/showcase/79_stealth_network_exfil_chain").findings
    assert any(f.id == "ABU-006" for f in findings_79)
    assert any(f.id == "CHN-012" for f in findings_79)
    findings_80 = _scan("examples/showcase/80_container_escape_host_mount_chain").findings
    assert any(f.id == "MAL-026" for f in findings_80)
    assert any(f.id == "CHN-013" for f in findings_80)
    findings_81 = _scan("examples/showcase/81_container_escape_secret_access_chain").findings
    assert any(f.id == "MAL-027" for f in findings_81) or any(f.id == "MAL-026" for f in findings_81)
    assert any(f.id == "CHN-014" for f in findings_81)
    findings_82 = _scan("examples/showcase/82_solana_rpc_c2_resolution").findings
    assert any(f.id == "MAL-029" for f in findings_82)
    findings_83 = _scan("examples/showcase/83_cursorjack_mcp_deeplink").findings
    assert any(f.id == "MAL-030" for f in findings_83)
    findings_84 = _scan("examples/showcase/84_deno_byor_execution").findings
    assert any(f.id == "MAL-031" for f in findings_84)
    findings_85 = _scan("examples/showcase/85_glassworm_persistence_marker").findings
    assert any(f.id == "MAL-032" for f in findings_85)
    findings_86 = _scan("examples/showcase/86_media_directive_injection").findings
    assert any(f.id == "PINJ-002" for f in findings_86)
    findings_87 = _scan("examples/showcase/87_bloktrooper_vsx_downloader").findings
    assert any(f.id == "MAL-033" for f in findings_87)
    findings_88 = _scan("examples/showcase/88_clawhavoc_memory_harvest").findings
    assert any(f.id == "EXF-017" for f in findings_88)
    findings_89a = _scan("examples/showcase/89_glassworm_chrome_extension_rat").findings
    assert any(f.id == "MAL-004" for f in findings_89a)
    findings_90a = _scan("examples/showcase/90_openclaw_gatewayurl_injection").findings
    assert any(f.id == "MAL-035" for f in findings_90a)
    findings_89 = _scan("examples/showcase/89_clickfix_webdav_share_exec").findings
    assert any(f.id == "MAL-034" for f in findings_89)
    findings_90 = _scan("examples/showcase/90_electron_asar_c2_injection").findings
    assert any(f.id == "MAL-035" for f in findings_90)
    findings_91 = _scan("examples/showcase/91_ai_gated_malware_llm_c2").findings
    assert any(f.id == "MAL-036" for f in findings_91)
    findings_92 = _scan("examples/showcase/92_npm_postinstall_env_exfil").findings
    assert any(f.id == "SUP-010" for f in findings_92)
    findings_93 = _scan("examples/showcase/93_prompt_control_heartbeat_persistence").findings
    assert any(f.id == "PINJ-003" for f in findings_93)
    findings_94 = _scan("examples/showcase/94_ghostclaw_skillmd_malware").findings
    assert any(f.id == "MAL-037" for f in findings_94)
    findings_95 = _scan("examples/showcase/95_lotai_ai_assistant_c2_relay").findings
    assert any(f.id == "MAL-038" for f in findings_95)
    findings_96 = _scan("examples/showcase/96_glassworm_extensionpack_transitive").findings
    assert any(f.id == "SUP-011" for f in findings_96)
    findings_97 = _scan("examples/showcase/97_npm_dependency_chain_postinstall").findings
    assert any(f.id == "SUP-012" for f in findings_97)
    findings_98 = _scan("examples/showcase/98_teampcp_actions_credential_stealer").findings
    assert any(f.id == "MAL-039" for f in findings_98)


def test_showcase_policy_block_domain() -> None:
    policy = Policy.model_validate(
        {
            "name": "showcase",
            "description": "showcase",
            "thresholds": {"warn": 30, "block": 70},
            "weights": {
                "malware_pattern": 3,
                "instruction_abuse": 2,
                "exfiltration": 3,
                "dependency_vulnerability": 2,
                "threat_intel": 3,
            },
            "hard_block_rules": ["MAL-001", "IOC-001"],
            "allow_domains": [],
            "block_domains": ["blocked.com"],
            "limits": {
                "max_files": 4000,
                "max_depth": 8,
                "max_bytes": 200000000,
                "timeout_seconds": 60,
            },
        }
    )
    report = scan(Path("examples/showcase/09_policy_block_domain"), policy, "custom")
    assert any(f.id == "POL-IOC-BLOCK" for f in report.findings)


def test_showcase_ecosystem_hints() -> None:
    assert "openai_style" in detect_ecosystems(Path("examples/showcase/10_openai_style"))
    assert "claude_style" in detect_ecosystems(Path("examples/showcase/11_claude_style"))


def test_showcase_social_engineering_detected_without_ai() -> None:
    """SE-001 and SE-SEM-001 fire on the social engineering showcase example with no AI layer."""
    report = scan(
        Path("examples/showcase/20_social_engineering_credential_harvest"), STRICT, "builtin:strict"
    )
    finding_ids = {f.id for f in report.findings}
    assert "SE-001" in finding_ids or "SE-SEM-001" in finding_ids, (
        f"Expected SE-001 or SE-SEM-001, got: {sorted(finding_ids)}"
    )
