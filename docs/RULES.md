# Detection Rules and Verdict Logic

## Core detection rules

Rule content is defined in:

- `src/skillscan/data/rules/default.yaml`
- `src/skillscan/data/rules/exfil_channels.yaml`
- `src/skillscan/data/rules/ast_flows.yaml`

The scanner compiles this YAML at runtime via `src/skillscan/rules.py`.

Current built-in IDs:

1. `MAL-001` (critical): download-and-exec patterns such as `curl|bash`.
2. `MAL-002` (high): base64 decode plus execution patterns.
3. `ABU-001` (high): coercive instruction text (for example disabling security controls).
4. `EXF-001` (high): sensitive credential file access markers.
5. `IOC-001` (high): IOC matched against local intel blocklists (domain, URL, IP, or CIDR netblock).
6. `POL-IOC-BLOCK` (high): domain matched explicit `block_domains` policy list.
7. `DEP-001` (severity from feed): vulnerable dependency version matched local vuln data.
8. `DEP-UNPIN` (medium): unpinned dependency version specification.
9. `CHN-001` (critical): dangerous action chain includes both download and execution intents.
10. `CHN-002` (critical): potential secret exfiltration chain combines secret access and outbound network.
11. `ABU-002` (high): privilege elevation combined with security-disable instruction sequence.
12. `SRC-READ-ERR` (low): URL mode could not fetch one or more linked sources.
13. `URL-SKIP-POLICY` (low): URL mode skipped one or more links due to same-origin safety policy.
14. `PINJ-001` (high): prompt override/jailbreak instruction pattern.
15. `MAL-003` (high): subshell downloader execution / encoded PowerShell execution patterns.
16. `OBF-001` (medium): bidirectional Unicode control characters (Trojan Source style obfuscation).
17. `SUP-001` (high): risky npm lifecycle install script (preinstall/install/postinstall/prepare).
18. `MAL-006` (high): PowerShell web request piped to `Invoke-Expression` (`iwr|irm ... | iex` / `Invoke-Expression (irm ...)`).
19. `SUP-004` (high): npm `preinstall`/`postinstall` shell bootstrap pattern (`curl`/`wget`/PowerShell/`bash -c` style loaders).
20. `AST-001` (critical): constructed/secret-tainted input reaches Python execution sink.
21. `AST-002` (critical): secret-tainted input reaches Python network sink.
22. `BIN-001` (high): executable binary artifact detected in scanned target.
23. `BIN-002` (medium): compiled library artifact detected in scanned target.
24. `BIN-003` (medium): binary blob artifact detected in scanned target.
25. `BIN-004` (low): Python bytecode/cache artifact detected in scanned target.
26. `SE-001` (high): social engineering instruction to harvest credentials or tokens from users.
27. `PINJ-SEM-001` (medium): offline semantic prompt injection score above threshold.
28. `SE-SEM-001` (medium): offline semantic social engineering score above threshold.
29. `ML-PINJ-*` (severity from model output): optional offline ML-based prompt injection findings (only with `--ml-detect`).

## Instruction hardening pipeline

SkillScan now processes instruction text through a deterministic hardening pipeline before matching:

1. Unicode normalization (`NFKC`) and zero-width character stripping.
2. Defanged IOC recovery (`hxxp`/`hxxps`, `[.]`, `(.)`, `{.}` normalization).
3. Bounded base64 fragment decoding for hidden text payloads (including split quoted fragments).
4. Action extraction (`download`, `execute`, `secret_access`, `network`, `privilege`, `security_disable`).
5. Chain checks that emit high-confidence findings for risky action combinations.

## Mitigation guidance by rule

1. `MAL-001`: Remove download-and-execute chains. Pin and verify artifacts before execution.
2. `MAL-002`: Remove decode-and-exec flows. Commit reviewed scripts and execute trusted local files only.
3. `ABU-001`: Remove coercive setup instructions and never require disabling host security controls.
4. `EXF-001`: Avoid direct secret-file access; use scoped secret providers and least-privilege credentials.
5. `IOC-001`: Treat as high risk, block deployment, and remove indicator references pending investigation.
6. `POL-IOC-BLOCK`: Replace blocked domains with approved endpoints or remove outbound dependency.
7. `DEP-001`: Upgrade affected package versions and regenerate lockfiles.
8. `DEP-UNPIN`: Pin exact package versions to reduce supply-chain drift and improve reproducibility.
9. `CHN-001`: Break download+execute flows; require reviewed local artifacts and explicit integrity checks.
10. `CHN-002`: Remove any secret-to-network path; use scoped token exchange or local-only processing.
11. `ABU-002`: Remove elevation plus security-disable guidance from setup instructions.
12. `SRC-READ-ERR`: Verify referenced source links are reachable and public; review unresolved links manually.
13. `URL-SKIP-POLICY`: Review skipped cross-origin links manually or opt in with `--no-url-same-origin-only`.
14. `PINJ-001`: Remove or quarantine prompt-override language and keep instruction provenance auditable.
15. `MAL-003`: Remove subshell/encoded execution patterns and require explicit, reviewed commands.
16. `OBF-001`: Strip bidi controls and verify text rendering equals actual execution content.
17. `SUP-001`: Remove network/bootstrap actions from npm lifecycle hooks and use explicit setup steps.
18. `MAL-006`: Remove web-request-to-`Invoke-Expression` chains; download reviewed scripts, verify integrity, and execute from explicit local paths.
19. `SUP-004`: Remove shell/bootstrap execution from npm `preinstall`/`postinstall` hooks and move setup to explicit reviewed steps.
20. `AST-001`: Remove dynamic execution flows where constructed or secret-linked values reach execution sinks.
21. `AST-002`: Remove secret-to-network dataflow and enforce explicit allowlisted egress paths.
22. `BIN-001`: Treat executable artifacts as high-risk supply-chain content pending provenance validation.
23. `BIN-002`: Validate compiled library hashes/signatures against trusted release metadata.
24. `BIN-003`: Manually inspect binary blobs and replace with transparent source artifacts when possible.
25. `BIN-004`: Confirm bytecode corresponds to reviewed source and cannot hide unreviewed logic.
26. `SE-001`: Remove credential-solicitation instructions; never ask users to provide tokens, passwords, or session cookies in skill instructions.
27. `PINJ-SEM-001` / `SE-SEM-001`: Review instruction text for covert credential-harvest or override language; remove or rewrite the flagged section.

## Capability inference rules

SkillScan also infers non-verdict capabilities from pattern matches:

1. `shell_execution`
2. `network_access`
3. `filesystem_write`

## Scoring model

Each finding has a severity base score:

- low: 5
- medium: 15
- high: 35
- critical: 60

Final score is the sum of `severity_score * policy_category_weight`.

## Built-in policy profiles

### strict (default)

- warn: `>=30`
- block: `>=70`
- hard blocks: `MAL-001`, `IOC-001`

### balanced

- warn: `>=50`
- block: `>=120`
- hard blocks: `MAL-001`

### permissive

- warn: `>=90`
- block: `>=190`
- hard blocks: none

## Verdict order

1. If any hard-block rule is present => `block`
2. Else if score >= block threshold => `block`
3. Else if score >= warn threshold => `warn`
4. Else => `allow`

## Rule metadata and query

Rules can now include optional additive metadata (for example techniques/tags/status/version) without changing rule IDs.

Explore current rules via CLI:

```bash
# List rules in text format
skillscan rule list

# List rules as JSON
skillscan rule list --format json

# Filter by technique or tag (when metadata is present)
skillscan rule list --technique EVASION-001
skillscan rule list --tag exfiltration
```

This metadata is additive and backward-compatible: existing rules continue to function unchanged even if they do not yet define metadata.

### Technique ID naming convention

Technique IDs should use a stable uppercase prefix and a 3-digit suffix:

- `EXFIL-001`, `EXFIL-016`
- `EVASION-001`, `EXEC-004`
- `SUPPLY-002`, `ABUSE-005`

Format guidance: `^[A-Z][A-Z0-9_-]*-\d{3}$`

Keep rule IDs and technique IDs separate:
- Rule ID = detector implementation identity (for example `OBF-003`)
- Technique ID = taxonomy identity (for example `EVASION-003`)
