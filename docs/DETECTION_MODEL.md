# SkillScan Detection Model

This document describes the seven detection layers that SkillScan applies when scanning an AI skill bundle. Understanding the model helps contributors write effective rules, interpret findings, and reason about false positives and false negatives.

---

## Overview

SkillScan operates a layered, deterministic-first pipeline. Each layer runs independently and emits zero or more `Finding` objects. Findings are deduplicated, scored, and assembled into a `Report` at the end of the scan. The layers are ordered from cheapest/most deterministic to most expensive/most semantic:

| # | Layer | Trigger | Default On |
|---|-------|---------|------------|
| 1 | Binary artifact detection | Always | Yes |
| 2 | ClamAV malware scan | `--clamav` flag | No |
| 3 | Static regex rules | Always | Yes |
| 4 | ML prompt-injection classifier | `--ml` flag | No |
| 5 | AST data-flow analysis | Always | Yes |
| 6 | Chain rules (co-occurrence) | Always | Yes |
| 7 | Skill graph analysis | `--graph` flag | No |
| 8 | AI semantic assist | `--ai` flag | No |

Additionally, the IOC/vuln intel layer runs alongside layers 3–6 to cross-reference extracted indicators against the bundled threat intelligence databases.

---

## Layer 1 — Binary Artifact Detection

**Module:** `analysis._binary_artifact_findings`
**Rule IDs:** `BIN-001`, `BIN-002`, `BIN-003`, `BIN-004`

Before any text analysis begins, SkillScan inspects every file in the skill bundle for binary content. The `_classify_non_text` function reads the first 4 KB of each file and classifies it using magic bytes. Detected artifact types and their associated rule IDs are:

| Artifact Type | Rule ID | Severity |
|---------------|---------|----------|
| Compiled Python bytecode (`.pyc`) | `BIN-001` | HIGH |
| ELF executable | `BIN-002` | CRITICAL |
| PE (Windows) executable | `BIN-003` | CRITICAL |
| Mach-O (macOS) executable | `BIN-003` | CRITICAL |
| Archive (ZIP, tar, gzip) | `BIN-004` | MEDIUM |

Binary artifacts in a skill bundle are almost always malicious or accidental. Legitimate skills are text-only (Markdown, YAML, Python source). Any compiled or executable artifact should be treated as a high-priority finding.

---

## Layer 2 — ClamAV Malware Scan

**Module:** `skillscan.clamav`
**Rule IDs:** `CLAM-001`, `CLAM-UNAVAIL`
**Enabled by:** `--clamav` flag

When `--clamav` is passed, SkillScan invokes the system `clamscan` binary against the extracted skill bundle root. Each ClamAV detection emits a `CLAM-001` finding at CRITICAL severity with the matched signature name as the snippet. If `clamscan` is not installed, a `CLAM-UNAVAIL` finding is emitted at LOW severity as an informational notice.

ClamAV provides broad-spectrum malware coverage and is particularly effective at detecting known malware droppers embedded in binary artifacts. It is disabled by default because it requires a separate installation and adds 2–10 seconds to scan time.

---

## Layer 3 — Static Regex Rules

**Module:** `analysis.scan` (inner loop over `ruleset.static_rules`)
**Rule IDs:** `MAL-*`, `EXF-*`, `PINJ-*`, `INJ-*`, and custom packs
**Config:** `src/skillscan/data/rules/default.yaml`, `exfil_channels.yaml`, and user packs

Static rules are the primary detection mechanism. Each rule consists of a compiled regex `pattern` applied to the full normalized text of each file in the skill bundle. The text is preprocessed by `_prepare_analysis_text`, which:

1. Normalizes Unicode (NFKC).
2. Decodes up to 6 base64 fragments found in the text (to catch obfuscated payloads).
3. Strips excessive whitespace.

A rule fires if its pattern matches anywhere in the preprocessed text. The match location and a 200-character snippet are captured as evidence.

**Rule schema:**

```yaml
static_rules:
  - id: MAL-001
    category: malware
    severity: high
    confidence: 0.95
    title: "Shell execution via curl pipe"
    pattern: "(?:curl|wget).*\\|.*(?:bash|sh)"
    mitigation: "Remove shell execution from skill instructions."
    metadata:
      techniques: [{id: T1059.004}]
      tags: [execution, remote_code]
```

Rules are organized into channels (`stable`, `beta`, `experimental`) controlled by the `--channel` flag. The `stable` channel is the default and contains only rules with a false-positive rate below 5% on the benchmark corpus.

---

## Layer 4 — ML Prompt-Injection Classifier

**Module:** `skillscan.ml_detector`
**Rule IDs:** `ML-PINJ-001`, `ML-UNAVAIL`
**Enabled by:** `--ml` flag

The ML layer applies a fine-tuned DeBERTa-v3-base classifier to each text file. The base model (`protectai/deberta-v3-base-prompt-injection-v2`) was pre-trained on a large prompt-injection corpus. SkillScan additionally fine-tunes this model on the project's own labeled corpus (currently 115 examples) when the corpus delta threshold is met.

Two inference backends are supported:

| Backend | Package extras | Model size | Latency |
|---------|---------------|------------|---------|
| ONNX Runtime (preferred) | `skillscan-security[ml-onnx]` | ~200 MB | ~50 ms/file |
| PyTorch / Transformers | `skillscan-security[ml]` | ~500 MB | ~200 ms/file |

The model outputs a binary label (`SAFE` / `INJECTION`) and a confidence score. Findings are emitted only when the injection probability exceeds 0.7. The ML layer is intentionally conservative — it is designed to catch semantic injection patterns that regex rules miss (e.g., natural-language jailbreaks, indirect instruction injection), not to replace the static layer.

**Known limitation:** The model's published accuracy (95.25%) is measured on the base model's 20k held-out set, not on the SkillScan-specific corpus. A proper held-out evaluation against the project corpus is planned for Milestone 7.

---

## Layer 5 — AST Data-Flow Analysis

**Module:** `skillscan.detectors.ast_flows` (via `detect_python_ast_flows`)
**Rule IDs:** `AST-FLOW-001`, `AST-FLOW-002`, `AST-FLOW-003`
**Config:** `src/skillscan/data/rules/ast_flows.yaml`

The AST layer detects dangerous data-flow patterns in Python source files embedded in skill bundles. Rather than matching raw text, it performs a lightweight taint analysis using the `ast` module:

- **Source → Sink flows (`AST-FLOW-001`):** Tracks values from secret sources (`os.getenv`, `dotenv_values`, credential file reads) to network sinks (`requests.post`, `urllib.request.urlopen`, socket operations). A finding is emitted when a tainted value reaches a network sink.
- **Decode → Exec flows (`AST-FLOW-002`):** Tracks values from decode calls (`base64.b64decode`, `bytes.fromhex`, `zlib.decompress`) to execution sinks (`eval`, `exec`, `subprocess.run`). This catches the classic "download and execute encoded payload" pattern.
- **Exec sink calls (`AST-FLOW-003`):** Flags any call to a high-risk execution sink regardless of data flow, when the call appears in a context that suggests runtime construction of the command string.

The AST layer only runs on files that parse as valid Python. Files that fail to parse are silently skipped (the static regex layer still covers them).

---

## Layer 6 — Chain Rules (Co-occurrence Detection)

**Module:** `analysis.scan` (inner loop over `ruleset.chain_rules`)
**Rule IDs:** `CHN-*`
**Config:** `src/skillscan/data/rules/default.yaml` (`chain_rules` section)

Chain rules fire when two or more `action_patterns` co-occur within a single skill file. Action patterns are broader, lower-precision regexes that classify text into semantic action categories (e.g., `network`, `credential_access`, `shell_execution`). A chain rule specifies an `all_of` list of action categories; it fires if all listed categories match anywhere in the file.

**Example:**

```yaml
chain_rules:
  - id: CHN-002
    category: exfiltration
    severity: high
    confidence: 0.92
    title: "Credential access combined with network exfiltration"
    all_of: [credential_access, network]
    mitigation: "Separate credential handling from network operations."
```

**Important design notes:**

- **No proximity constraint:** Chain rules currently fire if all constituent patterns match anywhere in the file, regardless of how far apart they appear. A skill with a `https://` URL in one section and a credential reference in another will trigger `CHN-002` even if they are unrelated. Proximity windowing (`window_lines` field) is planned for Milestone 6 (Issue G3).
- **Confidence uplift:** Chain rules carry higher confidence than their constituent static rules because co-occurrence of multiple suspicious patterns is a stronger signal of malicious intent than any single pattern alone.
- **Dual-use of action_patterns:** The `action_patterns` vocabulary serves double duty — it is both the chain detection substrate and a softer, broader detection layer. A skill can trigger a chain rule without triggering any static rule (e.g., a bare `https://` URL + a credential file reference hits `CHN-002` but may not match any `MAL-*` or `EXF-*` rule). This is intentional but means chain rules have a higher false-positive rate than static rules on benign skills that legitimately combine network and credential operations.

---

## Layer 7 — Skill Graph Analysis

**Module:** `skillscan.detectors.skill_graph`
**Rule IDs:** `PINJ-GRAPH-001`, `PINJ-GRAPH-002`, `PINJ-GRAPH-003`
**Enabled by:** `--graph` flag

The skill graph layer detects cross-skill and agent-level abuse patterns that single-file analysis cannot see. It operates on the full skill bundle directory rather than individual files.

| Rule ID | Pattern | Description |
|---------|---------|-------------|
| `PINJ-GRAPH-001` | Remote `.md` fetch | Skill loads a remote Markdown file at runtime (e.g., `fetch https://evil.example/payload.md`). The fetched file could contain injected instructions that override the skill's declared behavior. |
| `PINJ-GRAPH-002` | Undeclared high-risk tool | Skill grants a high-risk tool (`bash`, `computer`, `shell`, `exec`) without a declared purpose in the skill metadata. |
| `PINJ-GRAPH-003` | Memory/config file write | Skill instructs the agent to write to a memory or configuration file (`soul.md`, `memory.md`, `.claude/settings.json`, etc.) that persists across agent sessions, enabling persistent instruction injection. |

**Planned — `PINJ-GRAPH-004`:** Cross-skill tool escalation detection. A skill that invokes another skill and requests elevated tool permissions not present in the invoked skill's declared scope. This rule is referenced in the CHANGELOG but not yet implemented.

---

## Layer 8 — Scoring and Risk Bands

**Module:** `skillscan.analysis` (scoring logic)
**Rule IDs:** N/A (produces verdict, not findings)

The scoring layer aggregates all findings from layers 1–7 and produces a final risk score and verdict band. Findings are weighted by severity and source layer. Hard-block rules (`block` verdict) override the numeric score and immediately produce a `block` verdict regardless of total score.

| Band | Score Range | Verdict |
|------|-------------|--------|
| Clean | 0 | `pass` |
| Low | 1–29 | `pass` |
| Medium | 30–59 | `warn` |
| High | 60–89 | `warn` |
| Critical | 90+ | `block` |

Any finding with `block: true` in its rule definition produces an immediate `block` verdict. The numeric score is still computed and reported for analyst context.

### Optional Offline ML Detection

**Module:** `skillscan.detectors.ml`
**Rule IDs:** `ML-PINJ-*`
**Enabled by:** `--ml-detect` flag
**Requires:** `pip install skillscan-security[ml-onnx]` and `skillscan model sync`

The optional ML layer runs `protectai/deberta-v3-base-prompt-injection-v2` locally via ONNX Runtime (CPU) or torch (GPU). It scores each instruction block for prompt injection intent and emits `ML-PINJ-*` findings above threshold. The model runs entirely offline once synced — no API key, no network call during scan.

---

## Intel Layer — IOC and Vulnerability Cross-Reference

**Module:** `analysis._load_builtin_ioc_db`, `analysis._load_builtin_vuln_db`, `analysis._merge_user_intel`
**Rule IDs:** `IOC-001`, `IOC-POLICY-001`, `DEP-001`, `DEP-UNPINNED`

The intel layer runs alongside layers 3–6 and cross-references extracted indicators against two databases:

### IOC Database (`ioc_db.json`)

Extracted IOCs (domains, IPs, URLs) are matched against the bundled IOC database. The bundled DB contains:
- Hand-curated campaign IOCs (GlassWorm/PylangGhost and similar)
- Active malware-hosting domains from URLhaus
- Active C2 IPs from Feodo Tracker
- Hijacked IP blocks from Spamhaus DROP

Large feeds (Hagezi TIF, Phishing Army, KADhosts) are not bundled; they are downloaded at runtime via `skillscan intel sync` and merged at scan time. This keeps the installed package small (~50 KB for the bundled DB) while allowing users who run `intel sync` to benefit from broader coverage.

### Vulnerability Database (`vuln_db.json`)

Dependency declarations (`requirements.txt`, `package.json`) are parsed and each pinned package version is checked against the bundled vulnerability database. The bundled DB covers the top MCP-adjacent Python and npm packages, seeded from OSV.dev. Only the highest-severity CVE per package version is stored to keep the DB compact.

### User Intel

Users can supply additional IOC and vuln data via `~/.skillscan/intel/` (JSON files in the same schema). User intel is merged with the bundled DB at scan time and takes precedence on conflicts.

---

## Scoring and Risk Assessment

After all layers run, the `Report` object computes a `risk_score` (0.0–1.0) using a weighted sum of finding severities:

| Severity | Weight |
|----------|--------|
| CRITICAL | 10 |
| HIGH | 5 |
| MEDIUM | 2 |
| LOW | 0.5 |
| INFO | 0 |

The score is normalized by the total number of files scanned and capped at 1.0. A score above 0.7 is considered high risk; above 0.4 is medium risk. The risk band is included in all output formats.

---

## False Positive Management

SkillScan supports per-finding suppressions via `skillscan suppress` and a `.skillscan-suppressions.yaml` file in the skill bundle. Suppressions are scoped to a specific rule ID and optionally a file path and expiry date. Suppressions with no expiry date are flagged by CI as a warning (Issue H2).

The `--channel` flag controls which rules are active. The `experimental` channel includes rules with higher false-positive rates that are not yet validated against the benchmark corpus. Contributors should not promote rules from `experimental` to `stable` without benchmark evidence.

---

## Adding a New Detection Rule

1. **Choose the right layer.** Static regex for pattern-based detection; chain rules for co-occurrence; AST flows for Python data-flow; skill graph for cross-skill abuse.
2. **Write the rule** in the appropriate YAML file under `src/skillscan/data/rules/`.
3. **Add a corpus example.** Every new rule must have at least one labeled injection example in `corpus/` that the rule fires on, and at least one benign example it does not fire on.
4. **Run the benchmark.** `skillscan benchmark --format json` must show no regression in precision/recall on the existing corpus.
5. **Start in `experimental` channel.** Promote to `beta` after 30 days of production use with no confirmed false positives. Promote to `stable` after benchmark validation.
6. **Open a PR.** Branch protection requires CI to pass before merge.
