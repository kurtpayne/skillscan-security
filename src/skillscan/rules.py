from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

import yaml  # type: ignore[import-untyped]
from pydantic import BaseModel, Field

from skillscan.models import Severity


class RuleTechnique(BaseModel):
    id: str
    name: str | None = None


class RuleMetadata(BaseModel):
    version: str | None = None
    status: str | None = None
    techniques: list[RuleTechnique] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    applies_to: dict[str, list[str]] = Field(default_factory=dict)
    lifecycle: dict[str, str | list[str]] = Field(default_factory=dict)
    quality: dict[str, str | float] = Field(default_factory=dict)
    references: list[str] = Field(default_factory=list)


class StaticRule(BaseModel):
    id: str
    category: str
    severity: Severity
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    title: str
    pattern: str
    mitigation: str | None = None
    metadata: RuleMetadata | None = None


class ChainRule(BaseModel):
    id: str
    category: str
    severity: Severity
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    title: str
    all_of: list[str]
    snippet: str = ""
    mitigation: str | None = None


class RulePack(BaseModel):
    version: str
    static_rules: list[StaticRule] = Field(default_factory=list)
    action_patterns: dict[str, str] = Field(default_factory=dict)
    chain_rules: list[ChainRule] = Field(default_factory=list)
    capability_patterns: dict[str, str] = Field(default_factory=dict)


@dataclass
class CompiledStaticRule:
    id: str
    category: str
    severity: Severity
    confidence: float
    title: str
    pattern: re.Pattern[str]
    mitigation: str | None


@dataclass
class CompiledChainRule:
    id: str
    category: str
    severity: Severity
    confidence: float
    title: str
    all_of: set[str]
    snippet: str
    mitigation: str | None


@dataclass
class CompiledRulePack:
    version: str
    static_rules: list[CompiledStaticRule]
    action_patterns: dict[str, re.Pattern[str]]
    chain_rules: list[CompiledChainRule]
    capability_patterns: list[tuple[str, re.Pattern[str]]]


def _merge_rulepacks(rulepacks: list[RulePack]) -> RulePack:
    static_rules: list[StaticRule] = []
    chain_rules: list[ChainRule] = []
    action_patterns: dict[str, str] = {}
    capability_patterns: dict[str, str] = {}
    versions: list[str] = []

    for rp in rulepacks:
        versions.append(rp.version)
        static_rules.extend(rp.static_rules)
        chain_rules.extend(rp.chain_rules)
        action_patterns.update(rp.action_patterns)
        capability_patterns.update(rp.capability_patterns)

    return RulePack(
        version="+".join(versions),
        static_rules=static_rules,
        action_patterns=action_patterns,
        chain_rules=chain_rules,
        capability_patterns=capability_patterns,
    )


def _load_yaml_rule_file(raw: str) -> RulePack:
    parsed = yaml.safe_load(raw)
    return RulePack.model_validate(parsed)


def _filter_rule_files_for_channel(files: list, channel: str) -> list:
    # stable: base rules + stable-tagged overlays
    # preview: stable + preview overlays
    # labs: stable + preview + labs overlays
    if channel not in {"stable", "preview", "labs"}:
        raise ValueError(f"Unknown rulepack channel: {channel}")

    def include(name: str) -> bool:
        if not name.endswith(".yaml"):
            return False
        if name.endswith(".labs.yaml"):
            return channel == "labs"
        if name.endswith(".preview.yaml"):
            return channel in {"preview", "labs"}
        if name.endswith(".stable.yaml"):
            return channel in {"stable", "preview", "labs"}
        # channel-agnostic/base file
        return True

    return [p for p in files if include(p.name)]


def load_builtin_rulepack(channel: str = "stable") -> RulePack:
    rules_dir = resources.files("skillscan.data.rules")
    files = sorted([p for p in rules_dir.iterdir() if p.name.endswith(".yaml")], key=lambda p: p.name)
    files = _filter_rule_files_for_channel(files, channel)
    rulepacks = [_load_yaml_rule_file(p.read_text(encoding="utf-8")) for p in files]

    # Merge user-local rules on top of bundled rules (signature-as-data layer).
    # User-local rules are downloaded by `skillscan rules sync` and live in
    # ~/.skillscan/rules/. They extend the bundled set; rule IDs in both use
    # the user-local (newer) version because _merge_rulepacks appends them last
    # and analysis picks the last match for duplicate IDs.
    try:
        from skillscan.rules_sync import get_user_rules_dir  # avoid circular at module level

        user_dir = get_user_rules_dir()
        if user_dir is not None:
            user_files = sorted(user_dir.glob("*.yaml"), key=lambda p: p.name)
            user_files = _filter_rule_files_for_channel(list(user_files), channel)
            if user_files:
                user_rulepacks = [_load_yaml_rule_file(p.read_text(encoding="utf-8")) for p in user_files]
                rulepacks = rulepacks + user_rulepacks
    except Exception:  # pragma: no cover — network/fs errors must never block scan
        pass

    return _merge_rulepacks(rulepacks)


@lru_cache(maxsize=3)
def load_compiled_builtin_rulepack(channel: str = "stable") -> CompiledRulePack:
    rp = load_builtin_rulepack(channel=channel)
    static_rules = [
        CompiledStaticRule(
            id=r.id,
            category=r.category,
            severity=r.severity,
            confidence=r.confidence,
            title=r.title,
            pattern=re.compile(r.pattern, re.IGNORECASE),
            mitigation=r.mitigation,
        )
        for r in rp.static_rules
    ]
    action_patterns = {
        name: re.compile(pattern, re.IGNORECASE) for name, pattern in rp.action_patterns.items()
    }
    chain_rules = [
        CompiledChainRule(
            id=r.id,
            category=r.category,
            severity=r.severity,
            confidence=r.confidence,
            title=r.title,
            all_of=set(r.all_of),
            snippet=r.snippet,
            mitigation=r.mitigation,
        )
        for r in rp.chain_rules
    ]
    capability_patterns = [
        (name, re.compile(pattern, re.IGNORECASE)) for name, pattern in rp.capability_patterns.items()
    ]
    return CompiledRulePack(
        version=rp.version,
        static_rules=static_rules,
        action_patterns=action_patterns,
        chain_rules=chain_rules,
        capability_patterns=capability_patterns,
    )
