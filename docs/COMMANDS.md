# Command Reference

## `skillscan scan <path>`

Run a scan on a folder, file, archive, or URL.

Options:
- `--policy-profile, --profile`: `strict|balanced|permissive` (default `strict`)
- `--policy`: custom policy YAML file
- `--format`: `text|json` (default `text`)
- `--out`: write JSON report to file
- `--fail-on`: `warn|block|never` (default `block`)
- `--auto-intel/--no-auto-intel`: enable/disable managed intel auto-refresh (default enabled)
- `--intel-max-age-minutes`: staleness threshold before refresh (default 60)
- `--url-max-links`: max followed links for URL targets (default 25)
- `--url-same-origin-only/--no-url-same-origin-only`: link-following origin policy (default same-origin only)
- `--ml-detect/--no-ml-detect`: enable offline ML-based prompt injection detection (default disabled; requires `skillscan model sync` first; no API key or network call needed)
- `--graph/--no-graph`: enable skill graph analysis — detects remote instruction loads, unsafe tool grants, and memory poisoning chains across all SKILL.md files in the scan root (default disabled)

Examples:

```bash
skillscan scan ./examples/suspicious_skill
skillscan scan ./artifact.zip --format json --out report.json
skillscan scan ./artifact --profile balanced --fail-on never
skillscan scan "https://github.com/blader/humanizer/blob/main/SKILL.md?plain=1"
skillscan scan ./examples/showcase/20_social_engineering_credential_harvest --fail-on never
skillscan scan ./skills/ --ml-detect --graph --format json --out report.json
```

## `skillscan explain <report.json>`

Render a previously generated JSON report in pretty terminal format.

```bash
skillscan explain ./report.json
```

## `skillscan policy show-default`

Print a built-in policy profile.

```bash
skillscan policy show-default --profile strict
```

## `skillscan policy validate <policy.yaml>`

Validate a custom policy file.

```bash
skillscan policy validate ./examples/policies/strict_custom.yaml
```

## `skillscan intel ...`

Manage local intel sources.

Commands:
- `status`
- `list`
- `add <path> --type ioc|vuln|rules --name <name>`
- `remove <name>`
- `enable <name>`
- `disable <name>`
- `rebuild`
- `sync [--force] [--max-age-minutes N]`

## `skillscan model`

Manage the local ML model used by `--ml-detect`.

Subcommands:
- `sync [--force]`: download or update the ONNX INT8 model from HuggingFace. Safe to run repeatedly — skips if already current.
- `status`: show installed model version, download date, and staleness. The scanner emits `PINJ-ML-STALE` when the model is older than 30 days.

```bash
skillscan model sync
skillscan model status
```

## `skillscan rule`

Manage the local rulepack.

Subcommands:
- `sync [--force]`: pull the latest rulepack from the managed channel.
- `status`: show current rulepack version, rule count, and age.

```bash
skillscan rule sync
skillscan rule status
```

## `skillscan uninstall`

Uninstall local runtime artifacts.

Options:
- `--keep-data`: preserve `~/.skillscan` data files.

## `skillscan version`

Print installed version.
