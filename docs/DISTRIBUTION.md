# Distribution Guide

This document describes supported ways to install and operate SkillScan in local development and CI.

## Install Matrix

| Path | Best for | Command |
|---|---|---|
| PyPI | End users / CI | `pip install skillscan-security` |
| Docker | Reproducible CI, isolated runtime | `docker run --rm -v "$PWD:/work" kurtpayne/skillscan-security:<tag> scan /work` |
| Pre-commit | Local dev gate on every commit | `.pre-commit-hooks.yaml` (see below) |
| GitHub Actions (reusable) | Third-party CI with zero config | `uses: kurtpayne/skillscan-security/.github/workflows/skillscan-reusable.yml@main` |
| VS Code extension | IDE inline diagnostics | `editors/vscode/` or VS Code Marketplace |
| Source/dev | Contributors | `pip install -e '.[dev]'` |

> Release automation is wired through GitHub Actions tag workflows (`release-pypi.yml`, `release-docker.yml`).

---

## Current Stable Path (Source/Dev)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
skillscan-security version
```

Run a quick validation scan:

```bash
skillscan scan examples/showcase/01_download_execute --fail-on never
```

---

## Convenience Installer

```bash
curl -fsSL https://raw.githubusercontent.com/kurtpayne/skillscan/main/scripts/install.sh | bash
```

If using a fork/private location, set `SKILLSCAN_REPO_URL` first.

---

## PyPI Install

```bash
pip install skillscan-security
skillscan-security version
```

Published by: `kurtpayne` (PyPI trusted publishing from `kurtpayne/skillscan`).

Pin a specific version in CI:

```bash
pip install "skillscan-security==X.Y.Z"
```

---

## Docker Usage

```bash
docker run --rm -v "$PWD:/work" kurtpayne/skillscan-security:<tag> scan /work --fail-on never
```

Expected tags:
- `<tag>` = `vX.Y.Z`
- `latest` = latest stable release

---

## Upgrade

### Source/dev

```bash
git pull
source .venv/bin/activate
pip install -e '.[dev]'
skillscan-security version
```

### Future PyPI

```bash
pip install --upgrade skillscan-security
skillscan-security version
```

### Future Docker

```bash
docker pull <image>:latest
```

---

## Rollback

### Source/dev

```bash
git checkout <known-good-tag-or-commit>
source .venv/bin/activate
pip install -e '.[dev]'
```

### Future PyPI

```bash
pip install "skillscan-security==<previous-version>"
```

### Future Docker

```bash
docker pull <image>:<previous-tag>
```

---

See also: `docs/RELEASE_ONBOARDING.md` for first-time account and publisher setup.

## Release Automation Notes

- PyPI publish runs on `v*` tags via `.github/workflows/release-pypi.yml`.
- Docker multi-arch publish runs on `v*` tags via `.github/workflows/release-docker.yml`.
- Both release workflows validate that tag `vX.Y.Z` matches `project.version` in `pyproject.toml`.
- Required GitHub secrets for Docker publish:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
- PyPI publish is configured for trusted publishing (`id-token: write`) with environment `pypi`.
- Release artifacts include SBOMs:
  - Python dependencies: `sbom-python.cdx.json` (CycloneDX)
  - Docker image: `sbom-docker.spdx.json` (SPDX JSON)
- Release workflows generate Sigstore/cosign keyless signatures:
  - Python support artifacts: `sbom-python.cdx.json.sig/.pem`, `SHA256SUMS.sig/.pem`
  - Docker SBOM artifact: `sbom-docker.spdx.json.sig/.pem`
  - Container image signatures + SBOM attestation are published to the registry (OCI referrers).

## Pre-commit Hook

Add to `.pre-commit-config.yaml` in any repo to gate commits:

```yaml
repos:
  - repo: https://github.com/kurtpayne/skillscan-security
    rev: v0.3.1
    hooks:
      - id: skillscan-security
        args: [--fail-on, warn]
```

Run `pre-commit install` once, then every `git commit` automatically scans staged skill files.

## GitHub Actions (Reusable Workflow)

Call from any repo without installing anything — results appear in the GitHub Security tab as SARIF findings:

```yaml
jobs:
  security:
    uses: kurtpayne/skillscan-security/.github/workflows/skillscan-reusable.yml@main
    with:
      fail-on: warn          # block | warn | info
      paths: "skills/"       # path(s) to scan
      extra-args: "--ml-detect --graph"
```

Outputs: `verdict` (`allow`/`warn`/`block`) and `finding-count` for downstream job conditions.

## CI Recommendations

1. Pin versions (`pip` or image tag) for deterministic builds.
2. Cache dependencies between runs.
3. Use `--format json` output for automation.
4. Gate with `--fail-on block` (or stricter policy as needed).

Example:

```bash
skillscan scan . --format json --out skillscan-report.json --fail-on block
```

---

## Troubleshooting

### `python: command not found`
Use `python3` explicitly.

### Missing virtualenv/pip tooling
Install Python dev tooling for your OS, then recreate `.venv`.

### `skillscan: command not found`
Activate your virtualenv or ensure install path is on `PATH`.

### Slow scans in CI
Tune policy limits (`max_files`, `max_bytes`, timeout) and avoid scanning giant artifact trees unnecessarily.

### Verify release signatures/attestations
Use `cosign` to verify release artifacts and container provenance:

```bash
# Verify signed Python SBOM blob
cosign verify-blob \
  --certificate dist/sbom-python.cdx.json.pem \
  --signature dist/sbom-python.cdx.json.sig \
  --certificate-identity-regexp "https://github.com/.+" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  dist/sbom-python.cdx.json

# Verify signed checksum file blob
cosign verify-blob \
  --certificate dist/SHA256SUMS.pem \
  --signature dist/SHA256SUMS.sig \
  --certificate-identity-regexp "https://github.com/.+" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  dist/SHA256SUMS

# Verify signed container image
cosign verify \
  --certificate-identity-regexp "https://github.com/.+" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  kurtpayne/skillscan-security:vX.Y.Z

# Verify SBOM attestation on container image
cosign verify-attestation \
  --type spdxjson \
  --certificate-identity-regexp "https://github.com/.+" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  kurtpayne/skillscan-security:vX.Y.Z
```
