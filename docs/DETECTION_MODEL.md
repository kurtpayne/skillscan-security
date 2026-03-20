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

The ML layer applies a fine-tuned DeBERTa-v3-base classifier to each text file in the skill bundle. The detection pipeline uses two sub-layers:

**4a — Local Semantic Classifier (`skillscan.semantic_local`)**

Before invoking the neural model, a lightweight deterministic classifier based on stemmed feature scoring runs on each file. It uses Porter stemmer roots grouped into six feature axes:

| Feature Axis | Example stems | Weight |
|---|---|---|
| Override | `ignor`, `disregard`, `overrid`, `bypass`, `jailbreak` | 0.18/match |
| Authority | `system`, `develop`, `instruct`, `guardrail`, `safeti` | 0.10/match |
| Secrecy | `silent`, `stealth`, `covert`, `hidden`, `conceal` | 0.12/match |
| Data access | `secret`, `token`, `credenti`, `password`, `apikey`, `env` | 0.11/match |
| Exfiltration | `send`, `upload`, `post`, `transmit`, `exfil`, `webhook` | 0.11/match |
| Coercion | `must`, `requir`, `mandatori`, `immedi`, `urgent`, `cannot` | 0.07/match |

A composite score above 0.65 emits a `PINJ-SEMANTIC-001` finding. A separate `SocialEngineeringClassifier` in the same module scores for social engineering patterns (imperative language, credential solicitation, urgency framing) and emits `PINJ-SE-001` above 0.65. Both classifiers run entirely offline with no model download required.

**4b — Neural ML Classifier (`skillscan.ml_detector`)**

The neural layer uses `protectai/deberta-v3-base-prompt-injection-v2` as the base model, fine-tuned with a LoRA adapter trained on the SkillScan corpus. The fine-tuned adapter (`kurtpayne/skillscan-deberta-adapter`) is downloaded explicitly via `skillscan model sync` and is never auto-downloaded.

Two inference backends are supported:

| Backend | Package extras | Model size | Latency |
|---------|---------------|------------|--------|
| ONNX Runtime (preferred) | `skillscan-security[ml-onnx]` | ~200 MB | ~50 ms/file |
| PyTorch / Transformers | `skillscan-security[ml]` | ~500 MB | ~200 ms/file |

The model outputs a binary label (`SAFE` / `INJECTION`) and a confidence score. Findings are emitted only when the injection probability exceeds 0.7. The ML layer is intentionally conservative — it is designed to catch semantic injection patterns that regex rules miss (e.g., natural-language jailbreaks, indirect instruction injection, Agent Hijacker P1/P4 patterns), not to replace the static layer.

**Fine-tune pipeline:** The LoRA adapter is trained on `corpus/` using `scripts/finetune_modal.py`, which runs on Modal (GPU: T4, 3 epochs, `r=32 alpha=32`). Training is triggered automatically by the `corpus-sync.yml` GitHub Actions workflow when the corpus delta threshold (50 examples or 10% growth) is crossed. The adapter is pushed to HuggingFace Hub only if the held-out eval macro F1 exceeds the gate threshold (currently **0.77** — lowered from 0.80 on 2026-03-20; see `corpus/EVAL_RESULTS.md` for rationale). The eval set (`corpus/held_out_eval/`) is a stratified 20% split covering all injection archetypes.

**Current corpus state (as of 2026-03-21):**

| Corpus split | Benign | Injection | Total |
|---|---|---|---|
| Training | 657 | 446 | 1,103 |
| Held-out eval | 138 | 62 | 200 |
| **Combined** | **795** | **508** | **1,303** |

**Injection corpus breakdown:**

| Subdirectory | Count | Archetype |
|---|---|---|
| `benchmark_injection/` | 150 | Data Thief (SC2+E2) — from zast-ai/skill-security-reviewer |
| `augmented/` | 117 | Data Thief — benign skills with appended attack phrases |
| `social_engineering/` | 85 | Social Engineering (SE) |
| `agent_hijacker/` | 40 | Agent Hijacker (P1/P4) — hand-crafted |
| `prompt_injection/` | 61 | Mixed — hand-crafted |
| `malicious/` | 23 | Mixed — real-world samples |
| `graph_injection/` | 12 | Graph/cross-skill injection |

**Latest eval results:** Macro F1 = 0.7544 (injection F1 = 0.667, benign F1 = 0.842). Gate lowered to 0.77 on 2026-03-20 after 9 consecutive runs plateaued at 0.73–0.78 (root cause: eval/train sets share the same hand-crafted sources; the model is not seeing enough out-of-distribution injection patterns). Improvement path: hand-craft more diverse injection examples across underrepresented archetypes (Agent Hijacker P1/P4, graph injection, temporal payloads), or generate ground-truth labels from `skillscan-trace` behavioral sandbox execution. Gate will be raised to 0.85 once injection F1 exceeds 0.80. Adapter push pending next fine-tune run. See `corpus/EVAL_RESULTS.md` for full history.

**Known limitation:** The base model's published accuracy (95.25%) is measured on a 20k general prompt-injection held-out set, not on SKILL.md-format files. The SkillScan fine-tune is specifically optimized for the skill file format and covers archetypes (Agent Hijacker, graph injection) not present in the base model's training data.

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

**`action_patterns` classification table:**

The following action categories are defined in `src/skillscan/data/rules/default.yaml`. Each is a compiled regex applied to the full normalized file text.

| Category | Backing | Description |
|---|---|---|
| `download` | static-backed | curl, wget, pip install, npm install, certutil, git clone, or any `https?://` URL |
| `execute` | static-backed | bash, sh, powershell, os.system, subprocess, python -c, node -e, perl -e |
| `secret_access` | static-backed | `.env`, `id_rsa`, `aws_access_key_id`, `ssh key`, `credentials` |
| `network` | static-backed | `https?://`, webhook, POST, upload, socket, `requests.` |
| `gh_actions_secrets` | chain-only | `${{ secrets.* }}` or `${{ toJSON(secrets) }}` in GitHub Actions context |
| `gh_pr_target` | chain-only | `pull_request_target` trigger in GitHub Actions |
| `gh_pr_head_checkout` | chain-only | `github.event.pull_request.head.sha/ref/repo.full_name` |
| `gh_pr_untrusted_meta` | chain-only | PR title/body/label/user.login in workflow expressions |
| `gh_pr_ref_meta` | chain-only | `github.head_ref`, `github.ref_name`, or PR head ref in expressions |
| `gh_cache_untrusted_key` | chain-only | Cache key derived from untrusted PR metadata |
| `gh_unpinned_action_ref` | chain-only | `uses: owner/repo@non-sha-ref` (unpinned action) |
| `privilege` | static-backed | `sudo`, `run as administrator`, `elevat` |
| `security_disable` | static-backed | Disable security/defender/AV instructions |
| `claude_hooks_marker` | chain-only | `"hooks"` key with `PreToolUse`/`PostToolUse`/etc. in `.claude/settings.json` |
| `hook_shell_command_field` | chain-only | `"command"` field with shell interpreter in hooks config |
| `mcp_tool_poison` | static-backed | `<IMPORTANT>` block or hidden telemetry/read/exfil instructions |
| `stealth_conceal` | static-backed | "do not mention", "hide this step", "background telemetry" |
| `container_escape` | static-backed | `docker.sock`, `--privileged`, `--cap-add ALL`, `nsenter`, `chroot /host` |
| `host_path_mount` | static-backed | `-v /etc:/`, `-v /root:/`, `--mount type=bind,source=/proc` |

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

## Layer 8 — Scoring and Policy Model

**Module:** `skillscan.analysis` (scoring logic), `skillscan.policies`
**Rule IDs:** N/A (produces verdict, not findings)

The scoring layer aggregates all findings from layers 1–7 and produces a final integer risk score and verdict. The score is a weighted sum of per-finding severity contributions, where the weight per finding is `severity_base_score × category_weight` from the active policy.

**Three built-in policies** are available via `--policy <name>`:

| Policy | Warn threshold | Block threshold | Use case |
|---|---|---|---|
| `permissive` | 80 | 200 | Local development, high-noise environments |
| `balanced` (default) | 50 | 120 | Developer and team use |
| `strict` | 30 | 70 | Security-focused CI, pre-publish gates |

**Category weights** (multiplied by finding severity score):

| Category | `balanced` | `strict` |
|---|---|---|
| `malware_pattern` | 2 | 3 |
| `instruction_abuse` | 2 | 2 |
| `prompt_injection_semantic` | 1 | 2 |
| `exfiltration` | 2 | 3 |
| `dependency_vulnerability` | 1 | 2 |
| `threat_intel` | 2 | 3 |
| `binary_artifact` | 1 | 1 |

**Hard-block rules** produce an immediate `block` verdict regardless of numeric score:

| Policy | Hard-block rules |
|---|---|
| `balanced` | `MAL-001` |
| `strict` | `MAL-001`, `IOC-001` |

> **Known gap (Issue H3):** Several critical-severity rules (`DEF-001`, `MAL-025`, `MAL-029`, `CHN-011`, `CHN-013`) are not in `strict.yaml`'s `hard_block_rules`. A skill with Defender disabling but a low overall score could reach `warn` instead of `block` in strict mode. Fix planned for Milestone 11.

The verdict bands for the default `balanced` policy are:

| Score | Verdict |
|---|---|
| 0 | `pass` |
| 1–49 | `pass` |
| 50–119 | `warn` |
| 120+ | `block` |

Any finding matching a `hard_block_rules` entry produces an immediate `block` verdict. The numeric score is still computed and reported for analyst context.

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
