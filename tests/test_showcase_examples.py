from pathlib import Path

from skillscan.ai import AIResult
from skillscan.analysis import scan
from skillscan.ecosystems import detect_ecosystems
from skillscan.models import AIAssessment, Finding, Policy, Severity
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


def test_showcase_ai_semantic_example_value_add(monkeypatch) -> None:
    base = scan(Path("examples/showcase/20_ai_semantic_risk"), STRICT, "builtin:strict")
    assert not any(f.id.startswith("AI-SEM-") for f in base.findings)

    def fake_ai(*_args, **_kwargs):
        return AIResult(
            assessment=AIAssessment(
                provider="openai",
                model="gpt-4o-mini",
                summary="Instruction asks for raw production credentials.",
                findings_added=1,
            ),
            findings=[
                Finding(
                    id="AI-SEM-001",
                    category="ai_semantic_risk",
                    severity=Severity.HIGH,
                    confidence=0.85,
                    title="Socially engineered credential request",
                    evidence_path="examples/showcase/20_ai_semantic_risk/SKILL.md",
                    snippet="paste their production API token into the chat",
                    mitigation="Never request raw credentials; use delegated, scoped authentication.",
                )
            ],
            raw_response='{"summary":"x","risks":[]}',
        )

    monkeypatch.setattr("skillscan.analysis.run_ai_assist", fake_ai)
    enriched = scan(Path("examples/showcase/20_ai_semantic_risk"), STRICT, "builtin:strict", ai_assist=True)
    assert any(f.id == "AI-SEM-001" for f in enriched.findings)
