# Distribution Guide

This document describes supported ways to install and operate SkillScan in local development and CI.

## Install Matrix

| Path | Best for | Command |
|---|---|---|
| PyPI | End users / CI | `pip install skillscan` |
| Docker | Reproducible CI, isolated runtime | `docker run --rm -v "$PWD:/work" <image> scan /work` |
| Source/dev | Contributors | `pip install -e '.[dev]'` |
| Convenience script | Quick local bootstrap | `curl -fsSL .../scripts/install.sh \| bash` |

> Release automation is wired through GitHub Actions tag workflows (`release-pypi.yml`, `release-docker.yml`).

---

## Current Stable Path (Source/Dev)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
skillscan version
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
pip install skillscan
skillscan version
```

Pin a specific version in CI:

```bash
pip install "skillscan==X.Y.Z"
```

---

## Docker Usage

```bash
docker run --rm -v "$PWD:/work" <image>:<tag> skillscan scan /work --fail-on never
```

Expected tags:
- `<tag>` = semver release
- `latest` = latest stable release

---

## Upgrade

### Source/dev

```bash
git pull
source .venv/bin/activate
pip install -e '.[dev]'
skillscan version
```

### Future PyPI

```bash
pip install --upgrade skillscan
skillscan version
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
pip install "skillscan==<previous-version>"
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
- Required GitHub secrets for Docker publish:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
- PyPI publish is configured for trusted publishing (`id-token: write`) with environment `pypi`.

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

### Non-deterministic results from optional AI assist
Keep AI assist off in strict deterministic CI paths, or pin provider/model and document expected behavior.
