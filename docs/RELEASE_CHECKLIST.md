# Release Checklist

Use this checklist before creating a `vX.Y.Z` tag.

## External prerequisites (one-time)

- [ ] PyPI trusted publisher is configured for `kurtpayne/skillscan`
  - Workflow: `.github/workflows/release-pypi.yml`
  - Environment: `pypi`
- [ ] Docker Hub repository exists: `kurtpayne/skillscan`
- [ ] GitHub secrets are set:
  - [ ] `DOCKERHUB_USERNAME`
  - [ ] `DOCKERHUB_TOKEN`
- [ ] (Optional) `CODECOV_TOKEN` set for coverage uploads

## Release readiness (every release)

- [ ] `pyproject.toml` version bumped to intended release version
- [ ] Local verification passes:
  - [ ] `pytest -q`
  - [ ] `ruff check src tests`
  - [ ] `mypy src`
- [ ] `README.md` and `docs/DISTRIBUTION.md` reflect current release reality
- [ ] Rollback note prepared (last known-good version/tag)

## Tag and publish

- [ ] Merge to `main`
- [ ] Create and push tag matching pyproject version:
  - [ ] `git tag vX.Y.Z`
  - [ ] `git push origin vX.Y.Z`
- [ ] Verify workflows succeed:
  - [ ] `Release PyPI`
  - [ ] `Release Docker`

## Post-release verification

- [ ] Verify PyPI install:
  - [ ] `pip install skillscan-security==X.Y.Z`
  - [ ] `skillscan version`
- [ ] Verify Docker image:
  - [ ] `docker pull kurtpayne/skillscan:vX.Y.Z`
  - [ ] `docker run --rm kurtpayne/skillscan:vX.Y.Z version`
- [ ] Confirm release artifacts include:
  - [ ] wheel + sdist + SHA256SUMS
  - [ ] Python SBOM (`sbom-python.cdx.json`)
  - [ ] Docker SBOM (`sbom-docker.spdx.json`)
- [ ] SBOM validation step passed in workflows (`scripts/validate_sbom.py`)
