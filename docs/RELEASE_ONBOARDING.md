# Release Onboarding (Docker Hub + PyPI)

Use this once to complete external account setup before first tagged release.

## Canonical publish targets

- PyPI package: `skillscan-security`
- Docker image: `kurtpayne/skillscan-security`

## 1) Docker Hub

1. Sign in to Docker Hub account `kurtpayne`.
2. Create repository: `skillscan-security` (public).
3. Create an access token with read/write scope.
4. Add GitHub repo secrets:
   - `DOCKERHUB_USERNAME` = `kurtpayne`
   - `DOCKERHUB_TOKEN` = `<dockerhub-access-token>`

## 2) PyPI Trusted Publishing

1. Sign in to PyPI account `kurtpayne`.
2. Create the project if needed (first publish can create it).
3. Configure Trusted Publisher for repo `kurtpayne/skillscan`:
   - Workflow: `.github/workflows/release-pypi.yml`
   - Environment: `pypi`
4. (Recommended) Repeat on TestPyPI first for dry run.

## 3) First release procedure

1. Bump package version in `pyproject.toml`.
2. Commit + push to `main`.
3. Create and push tag:
   - `git tag vX.Y.Z`
   - `git push origin vX.Y.Z`
4. Verify workflows:
   - `Release PyPI`
   - `Release Docker`
5. Validate installs:
   - `pip install skillscan-security==X.Y.Z`
   - `docker pull kurtpayne/skillscan-security:vX.Y.Z`
6. Verify SBOM artifacts were generated and uploaded:
   - Python: `sbom-python.cdx.json`
   - Docker: `sbom-docker.spdx.json`

## 4) Rollback

- Publish a new patch version that reverts bad behavior.
- For Docker consumers, pin to prior known-good tag.
- For pip consumers, pin prior known-good `skillscan-security==...`.
