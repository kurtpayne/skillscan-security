# Release Onboarding (Docker Hub + PyPI)

Use this once to complete external account setup before first tagged release.

## 1) Docker Hub

1. Create/login Docker Hub account/org.
2. Create repository: `skillscan`.
3. Create access token with push scope.
4. Add GitHub repo secrets:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`

## 2) PyPI Trusted Publishing

1. Create/login PyPI account.
2. Configure Trusted Publisher for repo `kurtpayne/skillscan`:
   - Workflow: `.github/workflows/release-pypi.yml`
   - Environment: `pypi`
3. (Recommended) Repeat on TestPyPI first for dry run.

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
   - `pip install skillscan==X.Y.Z`
   - `docker pull <docker-user>/skillscan:vX.Y.Z`

## 4) Rollback

- Publish a new patch version that reverts bad behavior.
- For Docker consumers, pin to prior known-good tag.
- For pip consumers, pin prior known-good `skillscan==...`.
