from __future__ import annotations

import base64
import binascii
import ipaddress
import json
import os
import re
import tarfile
import tempfile
import unicodedata
import zipfile
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import cast

from skillscan import __version__
from skillscan.ai import AIAssistError, AIConfig, run_ai_assist
from skillscan.clamav import scan_paths as clamav_scan_paths
from skillscan.detectors.ast_flows import detect_python_ast_flows
from skillscan.ecosystems import detect_ecosystems
from skillscan.intel import load_store
from skillscan.models import (
    IOC,
    AIAssessment,
    Capability,
    DependencyFinding,
    Finding,
    Policy,
    ScanMetadata,
    ScanReport,
    Severity,
    Verdict,
    is_archive,
)
from skillscan.remote import RemoteFetchError, fetch_remote_target, is_url_target
from skillscan.rules import CompiledRulePack, load_compiled_builtin_rulepack

URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN_RE = re.compile(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
ZERO_WIDTH_RE = re.compile(r"[\u200b-\u200f\u2060\ufeff]")
B64_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9+/_-])[A-Za-z0-9+/_-]{16,}={0,2}(?![A-Za-z0-9+/_=-])")
QUOTED_B64_FRAGMENT_RE = re.compile(r"[\"']([A-Za-z0-9+/_-]{8,}={0,2})[\"']")
RISKY_NPM_SCRIPT_RE = re.compile(
    r"\b(curl|wget|invoke-webrequest|powershell|pwsh|bash|sh|cmd\.exe|certutil|bitsadmin|nc|ncat|netcat)\b|"
    r"https?://",
    re.IGNORECASE,
)
KNOWN_TLDS = {
    "ai",
    "app",
    "biz",
    "co",
    "com",
    "dev",
    "edu",
    "fr",
    "gov",
    "info",
    "io",
    "jp",
    "net",
    "org",
    "ru",
    "uk",
    "us",
    "xyz",
}

SEVERITY_SCORE = {
    Severity.LOW: 5,
    Severity.MEDIUM: 15,
    Severity.HIGH: 35,
    Severity.CRITICAL: 60,
}

IOCDB = dict[str, list[str]]
VulnRecord = dict[str, str]
VulnVersionMap = dict[str, VulnRecord]
VulnPackageMap = dict[str, VulnVersionMap]
VulnDB = dict[str, VulnPackageMap]

BYTECODE_SUFFIXES = {".pyc", ".pyo"}
LIBRARY_SUFFIXES = {".so", ".dll", ".dylib", ".a"}
EXECUTABLE_SUFFIXES = {".exe", ".msi", ".com"}
KNOWN_BINARY_SUFFIXES = {
    ".bin",
    ".o",
    ".obj",
    ".class",
    ".jar",
    ".wasm",
    ".pyz",
    ".whl",
}
MACHO_MAGICS = (
    b"\xfe\xed\xfa\xce",
    b"\xce\xfa\xed\xfe",
    b"\xfe\xed\xfa\xcf",
    b"\xcf\xfa\xed\xfe",
    b"\xca\xfe\xba\xbe",
    b"\xbe\xba\xfe\xca",
)


@dataclass
class PreparedTarget:
    root: Path
    target_type: str
    cleanup_dir: tempfile.TemporaryDirectory[str] | None
    read_warnings: list[str]
    policy_warnings: list[str]


@dataclass
class BinaryArtifact:
    path: Path
    kind: str
    detail: str


@dataclass
class FileInventory:
    text_files: list[Path]
    binary_artifacts: list[BinaryArtifact]


class ScanError(Exception):
    pass


def _safe_extract_zip(src: Path, dst: Path, max_files: int, max_bytes: int) -> None:
    total = 0
    with zipfile.ZipFile(src) as zf:
        infos = zf.infolist()
        if len(infos) > max_files:
            raise ScanError(f"Archive has too many files: {len(infos)}")
        for info in infos:
            name = info.filename
            if name.startswith("/") or ".." in Path(name).parts:
                raise ScanError(f"Unsafe archive path: {name}")
            total += info.file_size
            if total > max_bytes:
                raise ScanError("Archive exceeds max bytes limit")
            zf.extract(info, dst)


def _safe_extract_tar(src: Path, dst: Path, max_files: int, max_bytes: int) -> None:
    total = 0
    with tarfile.open(src) as tf:
        members = tf.getmembers()
        if len(members) > max_files:
            raise ScanError(f"Archive has too many files: {len(members)}")
        for member in members:
            p = Path(member.name)
            if p.is_absolute() or ".." in p.parts:
                raise ScanError(f"Unsafe archive path: {member.name}")
            if member.issym() or member.islnk():
                raise ScanError(f"Symlink/hardlink not allowed in archive: {member.name}")
            total += member.size
            if total > max_bytes:
                raise ScanError("Archive exceeds max bytes limit")
        tf.extractall(dst, filter="data")


def prepare_target(
    target: Path | str,
    policy: Policy,
    url_max_links: int = 25,
    url_timeout_seconds: int = 12,
    url_same_origin_only: bool = True,
) -> PreparedTarget:
    if isinstance(target, str) and is_url_target(target):
        try:
            fetched = fetch_remote_target(
                target,
                max_links=url_max_links,
                timeout_seconds=url_timeout_seconds,
                same_origin_only=url_same_origin_only,
            )
        except RemoteFetchError as exc:
            raise ScanError(str(exc)) from exc
        return PreparedTarget(
            root=fetched.root,
            target_type="url",
            cleanup_dir=fetched.cleanup_dir,
            read_warnings=fetched.unreadable_urls,
            policy_warnings=fetched.skipped_urls,
        )

    if isinstance(target, str):
        target = Path(target)

    if not target.exists():
        raise ScanError(f"Target does not exist: {target}")
    if target.is_dir():
        return PreparedTarget(
            root=target,
            target_type="directory",
            cleanup_dir=None,
            read_warnings=[],
            policy_warnings=[],
        )
    if target.is_file() and not is_archive(target):
        tmp = tempfile.TemporaryDirectory(prefix="skillscan-")
        dst = Path(tmp.name)
        (dst / target.name).write_bytes(target.read_bytes())
        return PreparedTarget(
            root=dst,
            target_type="file",
            cleanup_dir=tmp,
            read_warnings=[],
            policy_warnings=[],
        )
    if target.is_file() and is_archive(target):
        tmp = tempfile.TemporaryDirectory(prefix="skillscan-")
        dst = Path(tmp.name)
        if target.suffix.lower() == ".zip":
            _safe_extract_zip(target, dst, policy.limits["max_files"], policy.limits["max_bytes"])
        else:
            _safe_extract_tar(target, dst, policy.limits["max_files"], policy.limits["max_bytes"])
        return PreparedTarget(
            root=dst,
            target_type="archive",
            cleanup_dir=tmp,
            read_warnings=[],
            policy_warnings=[],
        )
    raise ScanError("Unsupported target type")


def _read_head(path: Path, limit: int = 4096) -> bytes:
    try:
        with path.open("rb") as fh:
            return fh.read(limit)
    except OSError:
        return b""


def _classify_non_text(path: Path) -> BinaryArtifact | None:
    suffix = path.suffix.lower()
    if "__pycache__" in path.parts or suffix in BYTECODE_SUFFIXES:
        return BinaryArtifact(path=path, kind="python_bytecode", detail="compiled python bytecode artifact")
    if suffix in LIBRARY_SUFFIXES:
        return BinaryArtifact(path=path, kind="binary_library", detail="compiled library artifact")
    if suffix in EXECUTABLE_SUFFIXES:
        return BinaryArtifact(path=path, kind="executable_binary", detail="known executable extension")

    head = _read_head(path)
    if not head:
        return None
    if head.startswith(b"\x7fELF") or head.startswith(b"MZ") or head.startswith(MACHO_MAGICS):
        return BinaryArtifact(path=path, kind="executable_binary", detail="executable binary header")
    if suffix in KNOWN_BINARY_SUFFIXES:
        return BinaryArtifact(path=path, kind="binary_blob", detail="binary extension")
    if b"\x00" in head:
        return BinaryArtifact(path=path, kind="binary_blob", detail="contains NUL bytes")
    return None


def iter_text_files(
    root: Path,
    max_files: int,
    max_bytes: int,
    max_binary_artifacts: int,
    max_binary_bytes: int,
) -> FileInventory:
    files: list[Path] = []
    binary_artifacts: list[BinaryArtifact] = []
    total_bytes = 0
    total_files = 0
    total_binary_bytes = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        total_files += 1
        total_bytes += size
        if total_bytes > max_bytes:
            raise ScanError("Scan size exceeded max_bytes policy limit")
        if total_files > max_files:
            raise ScanError("Scan file count exceeded max_files policy limit")
        classification = _classify_non_text(path)
        if classification is not None:
            binary_artifacts.append(classification)
            total_binary_bytes += size
            if len(binary_artifacts) > max_binary_artifacts:
                raise ScanError("Binary artifact count exceeded max_binary_artifacts policy limit")
            if total_binary_bytes > max_binary_bytes:
                raise ScanError("Binary artifact bytes exceeded max_binary_bytes policy limit")
            continue
        files.append(path)
    return FileInventory(text_files=files, binary_artifacts=binary_artifacts)


def _safe_read_text(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError:
        return ""
    if b"\x00" in raw:
        return ""
    return raw.decode("utf-8", errors="ignore")


def _normalize_text(text: str) -> str:
    norm = unicodedata.normalize("NFKC", text)
    norm = ZERO_WIDTH_RE.sub("", norm)
    # Recover common defanged URL/domain forms.
    norm = re.sub(r"\bhxxps://", "https://", norm, flags=re.IGNORECASE)
    norm = re.sub(r"\bhxxp://", "http://", norm, flags=re.IGNORECASE)
    norm = norm.replace("[.]", ".").replace("(.)", ".").replace("{.}", ".")
    return norm


def _try_decode_b64(token: str) -> str | None:
    value = token.strip()
    if len(value) < 16:
        return None
    # Normalize urlsafe base64 and missing padding.
    value = value.replace("-", "+").replace("_", "/")
    padding = (-len(value)) % 4
    if padding:
        value += "=" * padding
    try:
        blob = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError):
        return None
    if not blob:
        return None
    candidate = blob.decode("utf-8", errors="ignore").strip()
    if not candidate:
        return None
    printable_ratio = sum(ch.isprintable() for ch in candidate) / max(len(candidate), 1)
    if printable_ratio < 0.9:
        return None
    return candidate


def _decode_base64_fragments(text: str, max_decodes: int = 6) -> list[str]:
    decoded: list[str] = []
    seen: set[str] = set()
    for token in B64_TOKEN_RE.findall(text):
        if token in seen:
            continue
        seen.add(token)
        if len(decoded) >= max_decodes:
            break
        candidate = _try_decode_b64(token)
        if candidate:
            decoded.append(candidate)

    # Also try concatenated quoted fragments often used to bypass token scanners.
    for line in text.splitlines():
        fragments = QUOTED_B64_FRAGMENT_RE.findall(line)
        if len(fragments) < 2:
            continue
        joined = "".join(fragments)
        if joined in seen:
            continue
        seen.add(joined)
        if len(decoded) >= max_decodes:
            break
        candidate = _try_decode_b64(joined)
        if candidate:
            decoded.append(candidate)
    return decoded


def _prepare_analysis_text(text: str) -> str:
    norm = _normalize_text(text)
    decoded = _decode_base64_fragments(norm)
    if not decoded:
        return norm
    return f"{norm}\n\n# decoded_fragments\n" + "\n".join(decoded)


def _extract_actions(text: str, action_patterns: dict[str, re.Pattern[str]]) -> set[str]:
    actions: set[str] = set()
    for action, pattern in action_patterns.items():
        if pattern.search(text):
            actions.add(action)
    return actions


def _normalize_domain(value: str) -> str:
    return value.lower().strip().strip(".,;)")


def _parse_requirements(text: str) -> list[tuple[str, str]]:
    deps: list[tuple[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            name, version = line.split("==", 1)
            deps.append((name.strip().lower(), version.strip()))
    return deps


def _find_unpinned_requirements(text: str) -> list[tuple[str, str]]:
    unpinned: list[tuple[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            continue
        if any(op in line for op in (">=", "<=", "~=", ">", "<")):
            unpinned.append((line.split()[0], line))
    return unpinned


def _parse_package_json(text: str) -> list[tuple[str, str]]:
    deps: list[tuple[str, str]] = []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return deps
    for section in ("dependencies", "devDependencies"):
        values = data.get(section, {})
        if isinstance(values, dict):
            for name, version in values.items():
                deps.append((name.lower(), str(version)))
    return deps


def _parse_package_scripts(text: str) -> dict[str, str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return {}
    parsed: dict[str, str] = {}
    for name, cmd in scripts.items():
        if isinstance(name, str) and isinstance(cmd, str):
            parsed[name.lower()] = cmd
    return parsed


def _is_unpinned_npm(version: str) -> bool:
    v = version.strip().lower()
    if not v or v == "latest":
        return True
    return v.startswith("^") or v.startswith("~") or "*" in v or "x" in v


def _extract_iocs(path: Path, text: str) -> list[IOC]:
    iocs: list[IOC] = []
    seen: set[tuple[str, str]] = set()
    for url in URL_RE.findall(text):
        key = ("url", url)
        if key not in seen:
            seen.add(key)
            iocs.append(IOC(value=url, kind="url", source_path=str(path)))
    for token in IP_RE.findall(text):
        try:
            ipaddress.ip_address(token)
        except ValueError:
            continue
        key = ("ip", token)
        if key not in seen:
            seen.add(key)
            iocs.append(IOC(value=token, kind="ip", source_path=str(path)))
    for domain in DOMAIN_RE.findall(text):
        norm = _normalize_domain(domain)
        if norm.startswith("http"):
            continue
        tld = norm.rsplit(".", 1)[-1]
        if tld not in KNOWN_TLDS:
            continue
        key = ("domain", norm)
        if key not in seen:
            seen.add(key)
            iocs.append(IOC(value=norm, kind="domain", source_path=str(path)))
    return iocs


def _load_builtin_vuln_db() -> VulnDB:
    raw = resources.files("skillscan.data.intel").joinpath("vuln_db.json").read_text(encoding="utf-8")
    return cast(VulnDB, json.loads(raw))


def _load_builtin_ioc_db() -> IOCDB:
    raw = resources.files("skillscan.data.intel").joinpath("ioc_db.json").read_text(encoding="utf-8")
    return cast(IOCDB, json.loads(raw))


def _merge_user_intel(ioc_db: IOCDB, vuln_db: VulnDB) -> tuple[IOCDB, VulnDB, list[str]]:
    store = load_store()
    sources = ["builtin:ioc_db", "builtin:vuln_db"]
    for source in store.sources:
        if not source.enabled:
            continue
        path = Path(source.path)
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if source.kind == "ioc" and isinstance(payload, dict):
            for key in ("domains", "ips", "urls", "cidrs"):
                values = payload.get(key, [])
                if isinstance(values, list):
                    ioc_db.setdefault(key, []).extend([str(v).lower() for v in values])
        if source.kind == "vuln" and isinstance(payload, dict):
            for ecosystem, values in payload.items():
                eco = vuln_db.setdefault(ecosystem, {})
                if isinstance(values, dict):
                    eco.update(values)
        sources.append(f"user:{source.name}")
    for key in ("domains", "ips", "urls", "cidrs"):
        deduped = sorted(set(ioc_db.get(key, [])))
        ioc_db[key] = deduped
    return ioc_db, vuln_db, sources


def _binary_kind_template(kind: str) -> tuple[str, Severity, str, str]:
    if kind == "executable_binary":
        return (
            "BIN-001",
            Severity.HIGH,
            "Executable binary artifact present",
            "Review and verify binary provenance and signatures before trust or execution.",
        )
    if kind == "binary_library":
        return (
            "BIN-002",
            Severity.MEDIUM,
            "Compiled library artifact present",
            "Verify shared/static library provenance and hash against trusted release artifacts.",
        )
    if kind == "binary_blob":
        return (
            "BIN-003",
            Severity.MEDIUM,
            "Binary blob artifact present",
            "Inspect binary payload purpose and source; prefer transparent source artifacts when possible.",
        )
    return (
        "BIN-004",
        Severity.LOW,
        "Compiled Python bytecode artifact present",
        (
            "Prefer scanning source files with bytecode provenance; "
            "review for hidden or mismatched source content."
        ),
    )


def _binary_artifact_findings(artifacts: list[BinaryArtifact]) -> list[Finding]:
    grouped: dict[str, list[BinaryArtifact]] = {}
    for item in artifacts:
        grouped.setdefault(item.kind, []).append(item)
    findings: list[Finding] = []
    for kind, items in grouped.items():
        rule_id, severity, title, mitigation = _binary_kind_template(kind)
        sample = ", ".join(str(item.path) for item in items[:3])
        findings.append(
            Finding(
                id=rule_id,
                category="binary_artifact",
                severity=severity,
                confidence=0.9,
                title=title,
                evidence_path=str(items[0].path),
                snippet=f"count={len(items)} sample={sample}",
                mitigation=mitigation,
            )
        )
    return findings


def _ip_in_cidrs(ip_value: str, cidrs: list[str]) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip_value)
    except ValueError:
        return False
    for cidr in cidrs:
        try:
            if ip_obj in ipaddress.ip_network(cidr, strict=False):
                return True
        except ValueError:
            continue
    return False


def scan(
    target: Path | str,
    policy: Policy,
    policy_source: str,
    *,
    url_max_links: int = 25,
    url_timeout_seconds: int = 12,
    url_same_origin_only: bool = True,
    ai_assist: bool = False,
    ai_provider: str = "auto",
    ai_model: str | None = None,
    ai_base_url: str | None = None,
    ai_timeout_seconds: int = 20,
    ai_required: bool = False,
    ai_non_blocking: bool = False,
    ai_report_out: Path | None = None,
    clamav: bool = False,
    clamav_timeout_seconds: int = 30,
    rulepack_channel: str = "stable",
) -> ScanReport:
    prepared = prepare_target(
        target,
        policy,
        url_max_links=url_max_links,
        url_timeout_seconds=url_timeout_seconds,
        url_same_origin_only=url_same_origin_only,
    )
    try:
        ruleset: CompiledRulePack = load_compiled_builtin_rulepack(channel=rulepack_channel)
        inventory = iter_text_files(
            prepared.root,
            policy.limits["max_files"],
            policy.limits["max_bytes"],
            policy.limits.get("max_binary_artifacts", 500),
            policy.limits.get("max_binary_bytes", 100_000_000),
        )
        files = inventory.text_files
        findings: list[Finding] = []
        iocs: list[IOC] = []
        capabilities: list[Capability] = []
        dependency_findings: list[DependencyFinding] = []
        ai_assessment: AIAssessment | None = None

        vuln_db = _load_builtin_vuln_db()
        ioc_db = _load_builtin_ioc_db()
        ioc_db, vuln_db, intel_sources = _merge_user_intel(ioc_db, vuln_db)
        findings.extend(_binary_artifact_findings(inventory.binary_artifacts))

        if clamav:
            clamav_result = clamav_scan_paths(prepared.root, timeout_seconds=clamav_timeout_seconds)
            if not clamav_result.available:
                findings.append(
                    Finding(
                        id="AV-UNAVAILABLE",
                        category="artifact_malware",
                        severity=Severity.LOW,
                        confidence=1.0,
                        title="ClamAV unavailable",
                        evidence_path=str(prepared.root),
                        snippet=(clamav_result.message or "ClamAV unavailable")[:220],
                        mitigation="Install ClamAV (`clamscan`) or disable --clamav for this run.",
                    )
                )
            else:
                for detection in clamav_result.detections:
                    findings.append(
                        Finding(
                            id="AV-001",
                            category="artifact_malware",
                            severity=Severity.HIGH,
                            confidence=0.9,
                            title="ClamAV malware detection",
                            evidence_path=detection.path,
                            snippet=detection.signature[:220],
                            mitigation=(
                                "Treat detected artifact as malicious and "
                                "remove/quarantine before execution."
                            ),
                        )
                    )

        for path in files:
            text = _safe_read_text(path)
            if not text:
                continue
            analysis_text = _prepare_analysis_text(text)

            for rule in ruleset.static_rules:
                for line_no, line in enumerate(analysis_text.splitlines(), 1):
                    if rule.pattern.search(line):
                        findings.append(
                            Finding(
                                id=rule.id,
                                category=rule.category,
                                severity=rule.severity,
                                confidence=rule.confidence,
                                title=rule.title,
                                evidence_path=str(path),
                                line=line_no,
                                snippet=line.strip()[:240],
                                mitigation=rule.mitigation,
                            )
                        )
                        break

            for capability_name, pattern in ruleset.capability_patterns:
                if pattern.search(analysis_text):
                    capabilities.append(
                        Capability(name=capability_name, evidence_path=str(path), detail="Pattern match")
                    )

            if path.suffix.lower() == ".py":
                for ast_finding in detect_python_ast_flows(analysis_text):
                    findings.append(
                        Finding(
                            id=ast_finding.id,
                            category=ast_finding.category,
                            severity=ast_finding.severity,
                            confidence=ast_finding.confidence,
                            title=ast_finding.title,
                            evidence_path=str(path),
                            line=ast_finding.line,
                            snippet=ast_finding.snippet,
                            mitigation=ast_finding.mitigation,
                        )
                    )

            iocs.extend(_extract_iocs(path, analysis_text))

            actions = _extract_actions(analysis_text, ruleset.action_patterns)
            for chain_rule in ruleset.chain_rules:
                if chain_rule.all_of.issubset(actions):
                    findings.append(
                        Finding(
                            id=chain_rule.id,
                            category=chain_rule.category,
                            severity=chain_rule.severity,
                            confidence=chain_rule.confidence,
                            title=chain_rule.title,
                            evidence_path=str(path),
                            snippet=chain_rule.snippet or " + ".join(sorted(chain_rule.all_of)),
                            mitigation=chain_rule.mitigation,
                        )
                    )

            lower = path.name.lower()
            if lower == "requirements.txt":
                for name, version in _parse_requirements(text):
                    if name in vuln_db.get("python", {}) and version in vuln_db["python"][name]:
                        entry = vuln_db["python"][name][version]
                        dependency_findings.append(
                            DependencyFinding(
                                ecosystem="python",
                                name=name,
                                version=version,
                                vulnerability_id=entry["id"],
                                severity=Severity(entry["severity"]),
                                fixed_version=entry.get("fixed"),
                            )
                        )
                for name, spec in _find_unpinned_requirements(text):
                    findings.append(
                        Finding(
                            id="DEP-UNPIN",
                            category="dependency_vulnerability",
                            severity=Severity.MEDIUM,
                            confidence=0.8,
                            title=f"Unpinned python dependency: {name}",
                            evidence_path=str(path),
                            snippet=spec,
                            mitigation=(
                                "Pin exact dependency versions to improve reproducibility "
                                "and reduce supply-chain risk."
                            ),
                        )
                    )
            if lower == "package.json":
                for name, version in _parse_package_json(text):
                    version_norm = version.lstrip("^~>=< ")
                    if name in vuln_db.get("npm", {}) and version_norm in vuln_db["npm"][name]:
                        entry = vuln_db["npm"][name][version_norm]
                        dependency_findings.append(
                            DependencyFinding(
                                ecosystem="npm",
                                name=name,
                                version=version,
                                vulnerability_id=entry["id"],
                                severity=Severity(entry["severity"]),
                                fixed_version=entry.get("fixed"),
                            )
                        )
                    if _is_unpinned_npm(version):
                        findings.append(
                            Finding(
                                id="DEP-UNPIN",
                                category="dependency_vulnerability",
                                severity=Severity.MEDIUM,
                                confidence=0.75,
                                title=f"Unpinned npm dependency: {name}",
                                evidence_path=str(path),
                                snippet=f"{name}: {version}",
                                mitigation=(
                                    "Pin exact dependency versions to improve reproducibility "
                                    "and reduce supply-chain risk."
                                ),
                            )
                        )

                scripts = _parse_package_scripts(text)
                lifecycle_hooks = ("preinstall", "install", "postinstall", "prepare")
                for hook in lifecycle_hooks:
                    cmd = scripts.get(hook)
                    if not cmd:
                        continue
                    if RISKY_NPM_SCRIPT_RE.search(cmd):
                        findings.append(
                            Finding(
                                id="SUP-001",
                                category="malware_pattern",
                                severity=Severity.HIGH,
                                confidence=0.88,
                                title=f"Risky npm lifecycle script: {hook}",
                                evidence_path=str(path),
                                snippet=f"{hook}: {cmd[:220]}",
                                mitigation=(
                                    "Remove network/bootstrap execution from lifecycle hooks. "
                                    "Use explicit reviewed setup commands instead."
                                ),
                            )
                        )

        dedup_iocs: dict[tuple[str, str, str], IOC] = {}
        allow_domains = {d.lower() for d in policy.allow_domains}
        for ioc in iocs:
            key = (ioc.kind, ioc.value.lower(), ioc.source_path)
            listed = False
            if ioc.kind == "domain" and ioc.value.lower() in ioc_db.get("domains", []):
                listed = True
            if ioc.kind == "ip" and ioc.value in ioc_db.get("ips", []):
                listed = True
            if ioc.kind == "ip" and _ip_in_cidrs(ioc.value, ioc_db.get("cidrs", [])):
                listed = True
            if ioc.kind == "url" and ioc.value.lower() in ioc_db.get("urls", []):
                listed = True
            if ioc.kind == "domain" and ioc.value.lower() in allow_domains:
                listed = False
            ioc.listed = listed
            dedup_iocs[key] = ioc
        iocs = list(dedup_iocs.values())

        block_domains = {d.lower() for d in policy.block_domains}
        for ioc in iocs:
            if ioc.kind == "domain" and ioc.value.lower() in block_domains:
                findings.append(
                    Finding(
                        id="POL-IOC-BLOCK",
                        category="threat_intel",
                        severity=Severity.HIGH,
                        confidence=1.0,
                        title="Domain blocked by local policy",
                        evidence_path=ioc.source_path,
                        snippet=ioc.value,
                        mitigation=(
                            "Replace blocked destination with an approved domain "
                            "or remove network dependency."
                        ),
                    )
                )

        for ioc in iocs:
            if ioc.listed:
                findings.append(
                    Finding(
                        id="IOC-001",
                        category="threat_intel",
                        severity=Severity.HIGH,
                        confidence=0.95,
                        title="IOC matched local blocklist",
                        evidence_path=ioc.source_path,
                        snippet=ioc.value,
                        mitigation=(
                            "Block install/use and investigate indicator reputation. "
                            "Remove all references to this IOC."
                        ),
                    )
                )

        for dep in dependency_findings:
            findings.append(
                Finding(
                    id="DEP-001",
                    category="dependency_vulnerability",
                    severity=dep.severity,
                    confidence=0.9,
                    title=f"Vulnerable dependency: {dep.name}@{dep.version}",
                    evidence_path=dep.name,
                    snippet=dep.vulnerability_id,
                    mitigation="Upgrade to a non-vulnerable dependency version and refresh lockfiles.",
                )
            )

        if prepared.read_warnings:
            findings.append(
                Finding(
                    id="SRC-READ-ERR",
                    category="source_access",
                    severity=Severity.LOW,
                    confidence=1.0,
                    title="Some linked sources could not be fetched",
                    evidence_path=str(target),
                    snippet=f"unreadable_links={len(prepared.read_warnings)}",
                    mitigation=(
                        "Verify linked source URLs are reachable and public. "
                        "Unreachable links are not treated as malicious by default."
                    ),
                )
            )

        if prepared.policy_warnings:
            findings.append(
                Finding(
                    id="URL-SKIP-POLICY",
                    category="source_access",
                    severity=Severity.LOW,
                    confidence=1.0,
                    title="Some linked sources were skipped by URL safety policy",
                    evidence_path=str(target),
                    snippet=f"skipped_links={len(prepared.policy_warnings)}",
                    mitigation=(
                        "Links skipped due to same-origin policy. "
                        "Use --url-same-origin-only false to include cross-origin links when needed."
                    ),
                )
            )

        if ai_assist:
            try:
                ai_result = run_ai_assist(
                    AIConfig(
                        provider=ai_provider,
                        model=ai_model,
                        base_url=ai_base_url,
                        timeout_seconds=ai_timeout_seconds,
                        required=ai_required,
                    ),
                    target=str(target),
                    root=prepared.root,
                    files=files,
                    findings=findings,
                )
                findings.extend(ai_result.findings)
                ai_assessment = ai_result.assessment
                if ai_report_out is not None:
                    ai_report_out.parent.mkdir(parents=True, exist_ok=True)
                    ai_report_out.write_text(ai_result.raw_response, encoding="utf-8")
            except AIAssistError as exc:
                if ai_required:
                    raise ScanError(f"AI assist failed: {exc}") from exc
                findings.append(
                    Finding(
                        id="AI-UNAVAILABLE",
                        category="source_access",
                        severity=Severity.LOW,
                        confidence=1.0,
                        title="AI assist unavailable",
                        evidence_path=str(target),
                        snippet=str(exc)[:220],
                        mitigation=(
                            "Configure AI provider settings/API key to enable semantic checks, "
                            "or use local-only scanning."
                        ),
                    )
                )

        score = 0
        block_score = 0
        for finding in findings:
            weight = policy.weights.get(finding.category, 1)
            contribution = SEVERITY_SCORE[finding.severity] * weight
            score += contribution
            if finding.confidence >= policy.block_min_confidence:
                if ai_non_blocking and finding.category == "ai_semantic_risk":
                    continue
                block_score += contribution

        ai_critical_block = (not ai_non_blocking) and any(
            f.category == "ai_semantic_risk"
            and f.severity == Severity.CRITICAL
            and f.confidence >= policy.ai_block_min_confidence
            for f in findings
        )

        if any(
            f.id in policy.hard_block_rules and f.confidence >= policy.block_min_confidence for f in findings
        ):
            verdict = Verdict.BLOCK
        elif policy.ai_block_on_critical and ai_critical_block:
            verdict = Verdict.BLOCK
        elif block_score >= policy.thresholds["block"]:
            verdict = Verdict.BLOCK
        elif score >= policy.thresholds["warn"]:
            verdict = Verdict.WARN
        else:
            verdict = Verdict.ALLOW

        metadata = ScanMetadata(
            scanner_version=__version__,
            target=str(target),
            target_type=prepared.target_type,
            ecosystem_hints=detect_ecosystems(prepared.root),
            rulepack_version=ruleset.version,
            policy_profile=policy.name,
            policy_source=policy_source,
            intel_sources=intel_sources,
        )

        return ScanReport(
            metadata=metadata,
            verdict=verdict,
            score=score,
            findings=findings,
            iocs=iocs,
            dependency_findings=dependency_findings,
            capabilities=capabilities,
            ai_assessment=ai_assessment,
        )
    finally:
        if prepared.cleanup_dir is not None:
            prepared.cleanup_dir.cleanup()
        os.environ.pop("PYTHONINSPECT", None)
