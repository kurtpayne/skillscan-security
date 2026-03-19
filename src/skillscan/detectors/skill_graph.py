"""Skill graph analyzer — detects cross-skill invocation abuse, remote .md loading,
and memory-file poisoning patterns.

Rule IDs emitted:
  PINJ-GRAPH-001  Skill loads a remote Markdown file at runtime
  PINJ-GRAPH-002  Skill grants a high-risk tool without a declared purpose
  PINJ-GRAPH-003  Skill instructs the agent to write a memory/config file
  PINJ-GRAPH-004  Skill references another skill that grants higher-risk tools
                  (cross-skill tool escalation)

Supported skill formats:
  SKILL.md         Standard SkillScan / ClawHub format (YAML front-matter + Markdown body)
  CLAUDE.md        Claude Projects format (same Markdown schema as SKILL.md)
  gpt_actions.json OpenAI Actions manifest (JSON; tool names extracted from functions[].name)
"""
from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

import yaml  # type: ignore[import-untyped]

from skillscan.models import Finding, Severity

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Remote .md fetch: URL ending in .md (optionally with query/fragment)
_REMOTE_MD_RE = re.compile(
    r"https?://[^\s\"'<>)]+\.md(?:[?#][^\s\"'<>)]*)?",
    re.IGNORECASE,
)

# Tool calls that fetch remote content and could load a .md
_FETCH_TOOL_RE = re.compile(
    r"\b(?:fetch|curl|wget|http_get|url_fetch|web_fetch|read_url|get_url)\b",
    re.IGNORECASE,
)

# High-risk tools that grant code execution or full computer control
_HIGH_RISK_TOOLS = frozenset(
    {
        "bash",
        "computer",
        "computer_use",
        "shell",
        "terminal",
        "execute_code",
        "run_code",
        "code_execution",
        "exec",
    }
)

# Medium-risk tools: network access or arbitrary file write
_MEDIUM_RISK_TOOLS = frozenset(
    {
        "webfetch",
        "web_fetch",
        "url_fetch",
        "http_get",
        "fetch",
        "curl",
        "wget",
        "write",
        "write_file",
        "file_write",
        "create_file",
    }
)

# Risk tiers: higher number = higher risk
_TOOL_RISK: dict[str, int] = {
    **{t: 2 for t in _MEDIUM_RISK_TOOLS},
    **{t: 3 for t in _HIGH_RISK_TOOLS},
}


def _max_tool_risk(tools: Iterable[str]) -> int:
    """Return the highest risk tier among the given tool names (0 = no risk)."""
    return max((_TOOL_RISK.get(t.lower(), 0) for t in tools), default=0)


# Memory / config files that, if written, affect all future agent sessions
_MEMORY_FILES = frozenset(
    {
        "soul.md",
        "memory.md",
        "agents.md",
        "claude.md",
        ".claude/settings.json",
        "settings.json",
        "agent.md",
        "system.md",
        "context.md",
    }
)

# Patterns that indicate a write/modify instruction in prose
_WRITE_INSTRUCTION_RE = re.compile(
    r"\b(?:write|update|modify|append|overwrite|save|edit|create|patch)\b"
    r"[^.]{0,80}"
    r"(?:soul\.md|memory\.md|agents\.md|claude\.md|settings\.json|agent\.md|system\.md)",
    re.IGNORECASE,
)

# Skill reference: "use skill X", "invoke skill X", "load skill X", "/skill-name"
_SKILL_REF_RE = re.compile(
    r"(?:use|invoke|load|run|call|activate)\s+(?:skill\s+)?[\"']?([a-z0-9_-]{3,50})[\"']?"
    r"|/([a-z0-9_-]{3,50})\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class SkillNode:
    """Parsed representation of a single skill file (SKILL.md, CLAUDE.md, or gpt_actions.json)."""

    path: Path
    name: str
    description: str
    allowed_tools: list[str] = field(default_factory=list)
    context: str = ""
    body: str = ""
    raw_front_matter: dict = field(default_factory=dict)
    # Explicit sub-skill references declared in front-matter (name → relative path)
    declared_skills: dict[str, str] = field(default_factory=dict)
    format: str = "skill_md"  # "skill_md" | "claude_md" | "gpt_actions"


@dataclass
class SkillGraph:
    nodes: dict[str, SkillNode] = field(default_factory=dict)  # path-key → node
    # Edges: (source_name, target_name, edge_type)
    edges: list[tuple[str, str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def _parse_skill_md(path: Path, fmt: str = "skill_md") -> SkillNode | None:
    """Parse a SKILL.md or CLAUDE.md file into a SkillNode.  Returns None on failure."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    front_matter: dict = {}
    # Strip BOM and leading whitespace so front-matter detection is robust
    raw = raw.lstrip("\ufeff").lstrip()
    body = raw

    # Extract YAML front-matter (--- ... ---)
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            fm_text = raw[3:end].strip()
            body = raw[end + 4 :].strip()
            try:
                parsed = yaml.safe_load(fm_text)
                if isinstance(parsed, dict):
                    front_matter = parsed
            except yaml.YAMLError:
                pass

    name = str(front_matter.get("name", path.parent.name))
    description = str(front_matter.get("description", ""))
    raw_tools = front_matter.get("allowed-tools", front_matter.get("allowed_tools", []))
    if isinstance(raw_tools, str):
        allowed_tools = [t.strip() for t in raw_tools.split(",") if t.strip()]
    elif isinstance(raw_tools, list):
        allowed_tools = [str(t).strip() for t in raw_tools]
    else:
        allowed_tools = []

    context = str(front_matter.get("context", ""))

    # Parse declared sub-skills from front-matter `skills:` list
    declared_skills: dict[str, str] = {}
    raw_skills = front_matter.get("skills", [])
    if isinstance(raw_skills, list):
        for entry in raw_skills:
            if isinstance(entry, dict):
                sub_name = str(entry.get("name", ""))
                sub_path = str(entry.get("path", ""))
                if sub_name:
                    declared_skills[sub_name] = sub_path

    return SkillNode(
        path=path,
        name=name,
        description=description,
        allowed_tools=allowed_tools,
        context=context,
        body=body,
        raw_front_matter=front_matter,
        declared_skills=declared_skills,
        format=fmt,
    )


def _parse_gpt_actions(path: Path) -> SkillNode | None:
    """Parse a gpt_actions.json OpenAI Actions manifest into a SkillNode."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(data, dict):
        return None

    name = str(data.get("name", path.parent.name))
    description = str(data.get("description", ""))

    # Extract tool names from functions array
    allowed_tools: list[str] = []
    functions = data.get("functions", data.get("actions", []))
    if isinstance(functions, list):
        for fn in functions:
            if isinstance(fn, dict):
                fn_name = fn.get("name", "")
                if fn_name:
                    allowed_tools.append(str(fn_name))

    # Also check top-level tools array (some formats)
    top_tools = data.get("tools", [])
    if isinstance(top_tools, list):
        for t in top_tools:
            if isinstance(t, dict):
                t_name = t.get("name", t.get("type", ""))
                if t_name:
                    allowed_tools.append(str(t_name))
            elif isinstance(t, str):
                allowed_tools.append(t)

    body = json.dumps(data, indent=2)

    return SkillNode(
        path=path,
        name=name,
        description=description,
        allowed_tools=list(dict.fromkeys(allowed_tools)),  # deduplicate, preserve order
        body=body,
        format="gpt_actions",
    )


def _parse_skill_file(path: Path) -> SkillNode | None:
    """Dispatch to the correct parser based on filename."""
    name = path.name.lower()
    if name == "gpt_actions.json":
        return _parse_gpt_actions(path)
    elif name == "claude.md":
        return _parse_skill_md(path, fmt="claude_md")
    else:
        return _parse_skill_md(path, fmt="skill_md")


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

# Filenames that are treated as skill definitions
_SKILL_FILENAMES = frozenset({"skill.md", "claude.md", "gpt_actions.json"})


def build_skill_graph(root: Path) -> SkillGraph:
    """Walk *root* and build a SkillGraph from all skill files found.

    Discovers:
    - ``SKILL.md``        Standard SkillScan / ClawHub format
    - ``CLAUDE.md``       Claude Projects format
    - ``gpt_actions.json`` OpenAI Actions manifest

    Also resolves path-based sub-skill references in front-matter ``skills:`` lists,
    loading referenced files even if they live outside the scanned tree.
    """
    graph = SkillGraph()

    for skill_path in sorted(root.rglob("*")):
        if skill_path.name.lower() not in _SKILL_FILENAMES:
            continue
        node = _parse_skill_file(skill_path)
        if node is None:
            continue
        key = str(skill_path)
        graph.nodes[key] = node

    # Second pass: resolve path-based declared_skills references.
    # A skill may declare sub-skills via a relative path that points outside the
    # scanned tree (e.g. ./skills/code-executor/SKILL.md).  Load those files so
    # the escalation check can compare tool grants.
    extra_nodes: dict[str, SkillNode] = {}
    for node in list(graph.nodes.values()):
        for sub_name, sub_rel_path in node.declared_skills.items():
            if not sub_rel_path:
                continue
            # Resolve relative to the parent directory of the declaring skill
            resolved = (node.path.parent / sub_rel_path).resolve()
            key = str(resolved)
            if key in graph.nodes or key in extra_nodes:
                continue
            # Try to load the referenced file
            if resolved.exists():
                sub_node = _parse_skill_file(resolved)
                if sub_node is not None:
                    extra_nodes[key] = sub_node
            else:
                # File doesn't exist on disk — create a synthetic stub so the
                # escalation check can still fire based on front-matter metadata
                # embedded in the declaring skill (e.g. inline tool declarations).
                # We can't infer tools from a missing file, so skip.
                pass

    graph.nodes.update(extra_nodes)

    # Build edges from declared_skills and body text references
    node_names = {n.name.lower() for n in graph.nodes.values()}
    for key, node in graph.nodes.items():
        # 1. Declared sub-skills in front-matter (by name)
        for sub_name in node.declared_skills:
            if sub_name.lower() in node_names and sub_name.lower() != node.name.lower():
                edge = (node.name, sub_name, "declares")
                if edge not in graph.edges:
                    graph.edges.append(edge)

        # 2. Body-text references
        for m in _SKILL_REF_RE.finditer(node.body):
            ref_name = (m.group(1) or m.group(2) or "").lower()
            if ref_name and ref_name in node_names and ref_name != node.name.lower():
                edge = (node.name, ref_name, "invokes")
                if edge not in graph.edges:
                    graph.edges.append(edge)

    return graph


# ---------------------------------------------------------------------------
# Rule detectors
# ---------------------------------------------------------------------------


def _check_remote_md_load(node: SkillNode) -> list[Finding]:
    """PINJ-GRAPH-001: skill body references a remote .md URL."""
    findings: list[Finding] = []
    full_text = node.description + "\n" + node.body

    # Case 1: explicit remote .md URL
    for m in _REMOTE_MD_RE.finditer(full_text):
        url = m.group(0)
        line_no = full_text[: m.start()].count("\n") + 1
        findings.append(
            Finding(
                id="PINJ-GRAPH-001",
                category="prompt_injection",
                severity=Severity.HIGH,
                confidence=0.88,
                title="Skill loads remote Markdown at runtime",
                evidence_path=str(node.path),
                line=line_no,
                snippet=url[:240],
                mitigation=(
                    "Remote .md files loaded at runtime can contain adversarial instructions. "
                    "Pin skill content locally or verify remote sources with a content hash."
                ),
            )
        )
        break  # one finding per skill is enough

    # Case 2: fetch-tool call present but no explicit .md URL — lower confidence
    if not findings and _FETCH_TOOL_RE.search(full_text):
        # Only flag if the body also mentions a URL-like pattern (http/https)
        if re.search(r"https?://", full_text, re.IGNORECASE):
            findings.append(
                Finding(
                    id="PINJ-GRAPH-001",
                    category="prompt_injection",
                    severity=Severity.MEDIUM,
                    confidence=0.60,
                    title="Skill may load remote content via fetch tool",
                    evidence_path=str(node.path),
                    snippet="fetch/curl/wget with remote URL detected",
                    mitigation=(
                        "Skill uses a network fetch tool alongside a remote URL. "
                        "Verify the fetched content cannot contain adversarial instructions."
                    ),
                )
            )

    return findings


def _check_tool_grant_without_purpose(node: SkillNode) -> list[Finding]:
    """PINJ-GRAPH-002: skill grants a high-risk tool but the body lacks a clear purpose."""
    findings: list[Finding] = []
    granted = [t.lower() for t in node.allowed_tools if t.lower() in _HIGH_RISK_TOOLS]
    if not granted:
        return findings

    # A "declared purpose" is at least one of: a ## Usage / ## Purpose / ## When to use section,
    # or a sentence of >= 20 words in the body that explains what the tool does.
    _purpose_re = re.compile(
        r"^#{1,3}\s*(usage|purpose|when to use|overview|description)",
        re.IGNORECASE | re.MULTILINE,
    )
    has_purpose_section = bool(_purpose_re.search(node.body))
    # Count meaningful body words (strip YAML artifacts)
    word_count = len(node.body.split())
    has_sufficient_body = word_count >= 30

    if not has_purpose_section and not has_sufficient_body:
        findings.append(
            Finding(
                id="PINJ-GRAPH-002",
                category="prompt_injection",
                severity=Severity.MEDIUM,
                confidence=0.72,
                title=f"High-risk tool granted without declared purpose: {', '.join(granted)}",
                evidence_path=str(node.path),
                snippet=f"allowed-tools: {', '.join(node.allowed_tools)}",
                mitigation=(
                    "Skills that grant Bash/Computer/Shell access should include a clear "
                    "## Usage or ## Purpose section explaining the intended use. "
                    "Undocumented tool grants are a common indicator of malicious skills."
                ),
            )
        )

    return findings


def _check_memory_write(node: SkillNode) -> list[Finding]:
    """PINJ-GRAPH-003: skill instructs agent to write a memory/config file."""
    findings: list[Finding] = []
    full_text = node.description + "\n" + node.body

    # Pattern 1: explicit write instruction mentioning a known memory file
    m = _WRITE_INSTRUCTION_RE.search(full_text)
    if m:
        line_no = full_text[: m.start()].count("\n") + 1
        findings.append(
            Finding(
                id="PINJ-GRAPH-003",
                category="prompt_injection",
                severity=Severity.CRITICAL,
                confidence=0.90,
                title="Skill instructs agent to write a memory/config file",
                evidence_path=str(node.path),
                line=line_no,
                snippet=m.group(0)[:240],
                mitigation=(
                    "Writing to SOUL.md, MEMORY.md, AGENTS.md, or settings files persists "
                    "instructions across all future agent sessions. "
                    "This is a high-confidence memory-poisoning indicator. "
                    "Remove the skill and audit any affected memory files."
                ),
            )
        )
        return findings  # one finding per skill

    # Pattern 2: memory file name appears in body without explicit write verb — lower confidence
    for mem_file in _MEMORY_FILES:
        if mem_file in full_text.lower():
            # Only flag if there's also an action verb nearby
            pattern = re.compile(
                r"\b(?:update|modify|append|overwrite|save|edit|create|patch|write)\b"
                r"[^.]{0,120}"
                + re.escape(mem_file),
                re.IGNORECASE,
            )
            m2 = pattern.search(full_text.lower())
            if m2:
                line_no = full_text.lower()[: m2.start()].count("\n") + 1
                findings.append(
                    Finding(
                        id="PINJ-GRAPH-003",
                        category="prompt_injection",
                        severity=Severity.HIGH,
                        confidence=0.75,
                        title=f"Skill references memory file with write intent: {mem_file}",
                        evidence_path=str(node.path),
                        line=line_no,
                        snippet=m2.group(0)[:240],
                        mitigation=(
                            "Skill references a memory/config file alongside a write-intent verb. "
                            "Verify this is intentional and the skill is from a trusted source."
                        ),
                    )
                )
                break

    return findings


def _check_tool_escalation(graph: SkillGraph) -> list[Finding]:
    """PINJ-GRAPH-004: a skill references another skill that grants higher-risk tools.

    Detection logic:
    1. For each edge (source → target) in the graph, compare the maximum tool risk
       tier of source vs target.
    2. If target_risk > source_risk, the source gains effective access to tools it
       does not declare — a cross-skill escalation path.
    3. Also check declared_skills in front-matter, which may reference skills not
       yet loaded into the graph (path-based references).
    """
    findings: list[Finding] = []

    # Build a name → node lookup (case-insensitive)
    name_to_node: dict[str, SkillNode] = {}
    for node in graph.nodes.values():
        name_to_node[node.name.lower()] = node

    seen: set[tuple[str, str]] = set()

    for source_name, target_name, _edge_type in graph.edges:
        pair = (source_name.lower(), target_name.lower())
        if pair in seen:
            continue
        seen.add(pair)

        source_node = name_to_node.get(source_name.lower())
        target_node = name_to_node.get(target_name.lower())
        if source_node is None or target_node is None:
            continue

        source_risk = _max_tool_risk(source_node.allowed_tools)
        target_risk = _max_tool_risk(target_node.allowed_tools)

        if target_risk > source_risk:
            # Determine which tools are the escalation vector
            escalation_tools = [
                t for t in target_node.allowed_tools
                if _TOOL_RISK.get(t.lower(), 0) > source_risk
            ]
            severity = Severity.CRITICAL if target_risk >= 3 else Severity.HIGH
            confidence = 0.88 if target_risk >= 3 else 0.75

            findings.append(
                Finding(
                    id="PINJ-GRAPH-004",
                    category="prompt_injection",
                    severity=severity,
                    confidence=confidence,
                    title=(
                        f"Cross-skill tool escalation: '{source_name}' → '{target_name}' "
                        f"grants {', '.join(escalation_tools)}"
                    ),
                    evidence_path=str(source_node.path),
                    snippet=(
                        f"'{source_name}' declares {source_node.allowed_tools or ['(none)']}; "
                        f"invoked skill '{target_name}' grants {target_node.allowed_tools}"
                    ),
                    mitigation=(
                        f"Skill '{source_name}' invokes '{target_name}', which grants "
                        f"{', '.join(escalation_tools)} — higher-risk tools than the invoking "
                        f"skill declares. An agent running '{source_name}' effectively has access "
                        f"to these tools. Either declare the escalated tools explicitly in "
                        f"'{source_name}' (so operators can make an informed trust decision) or "
                        f"remove the invocation of '{target_name}'."
                    ),
                )
            )

    return findings


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def skill_graph_findings(root: Path) -> list[Finding]:
    """Build the skill graph for *root* and return all graph-level findings."""
    graph = build_skill_graph(root)
    findings: list[Finding] = []

    for node in graph.nodes.values():
        findings.extend(_check_remote_md_load(node))
        findings.extend(_check_tool_grant_without_purpose(node))
        findings.extend(_check_memory_write(node))

    # Graph-level checks (require the full graph)
    findings.extend(_check_tool_escalation(graph))

    return findings
