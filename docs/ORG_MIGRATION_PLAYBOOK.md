# Org Migration Playbook — skillscan-dev

*Prepared March 2026. Execute this playbook in order. Do not skip steps.*

This document covers the full migration from personal accounts (`kurtpayne` on GitHub, PyPI, Docker Hub) to the `skillscan-dev` org. The migration should be done in a single session at a laptop to avoid leaving things in a half-migrated state.

**Namespaces reserved:**

| Platform | Handle | Email |
|---|---|---|
| GitHub | `skillscan-dev` (org) | `dev@skillscan.sh` |
| PyPI | `skillscan-dev` (org account) | `dev@skillscan.sh` |
| Docker Hub | `skillscandev` (org, no hyphens) | `dev@skillscan.sh` |
| VS Code Marketplace | `skillscan-dev` (publisher) | `dev@skillscan.sh` |

---

## Phase 1 — GitHub Org Setup (15 min)

**1.1 Invite yourself as owner of `skillscan-dev` org** (if not already done during registration).

**1.2 Transfer repos** — for each repo, go to **Settings → Danger Zone → Transfer ownership** and transfer to `skillscan-dev`:
- `skillscan-security`
- `skillscan-lint`
- `skillscan-website`

After transfer, GitHub automatically creates redirects from the old URLs. Existing `git remote` URLs in clones will continue to work, but update them anyway:

```bash
git remote set-url origin https://github.com/skillscan-dev/skillscan-security.git
```

**1.3 Re-add branch protection rules** — branch protection rules do not transfer. For each repo, go to **Settings → Branches** and recreate the `main` protection rule:
- Require pull request reviews before merging
- Require status checks to pass (select the same checks as before)
- Do not allow bypassing the above settings

**1.4 Add `CODEOWNERS` file** to each repo root:

```
# CODEOWNERS
* @skillscan-dev/maintainers
```

Commit directly to `main` (or via PR if branch protection is already in place).

---

## Phase 2 — Secrets & Tokens (30 min)

This is the most tedious phase. Do it in one pass to avoid confusion about which tokens are active.

**2.1 Generate a new GitHub PAT for the org** — go to **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens**. Create a new token scoped to the `skillscan-dev` org with:
- `Contents: Read and write` (for `INDEX_PAT` — pushes `index.txt`)
- `Workflows: Read and write` (for `INDEX_PAT` — needed to push workflow-triggered commits)

Save this as `INDEX_PAT` in each repo's **Settings → Secrets and variables → Actions**.

**2.2 Generate a PyPI API token** — log in to PyPI as `skillscan-dev`, go to **Account settings → API tokens**, create a token scoped to the `skillscan-security` and `skillscan-lint` projects. Save as `PYPI_API_TOKEN` in repo secrets.

**2.3 Generate a Docker Hub access token** — log in to Docker Hub as `skillscandev`, go to **Account Settings → Security → New Access Token**. Save as `DOCKER_HUB_TOKEN` in repo secrets. Also save `DOCKER_HUB_USERNAME` as `skillscandev`.

**2.4 Register VS Code Marketplace publisher** — go to [marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage), sign in with the Microsoft account linked to `dev@skillscan.sh`, and create a publisher with ID `skillscan-dev`. Then generate a PAT at [dev.azure.com](https://dev.azure.com) with **Marketplace → Manage** scope. Save as `VSCE_PAT` in repo secrets.

**2.5 Add `CORPUS_DEPLOY_KEY`** (when the private corpus repo exists) — generate an SSH deploy key, add the public key to `skillscan-corpus` repo deploy keys (read-only), and add the private key as `CORPUS_DEPLOY_KEY` in `skillscan-security` repo secrets.

**2.6 Revoke old personal tokens** — after confirming all workflows pass (Phase 5), revoke the old `kurtpayne`-scoped tokens from your personal GitHub account.

---

## Phase 3 — PyPI Migration (20 min)

**3.1 Add `skillscan-dev` as maintainer** on existing packages *before* revoking the personal token:
- Go to [pypi.org/manage/project/skillscan-security/collaboration](https://pypi.org/manage/project/skillscan-security/collaboration/)
- Add `skillscan-dev` as maintainer
- Repeat for `skillscan-lint`

**3.2 Verify publish works** — trigger a test publish from the new token by bumping the dev version and running the publish workflow manually. Confirm the package appears on PyPI under the new publisher.

**3.3 Update install instructions** in README.md and DISTRIBUTION.md — the package names (`skillscan-security`, `skillscan-lint`) stay the same; only the publisher changes. No user-facing change required.

---

## Phase 4 — Docker Hub Migration (20 min)

**4.1 Create the `skillscandev` org** on Docker Hub (already reserved).

**4.2 Re-tag and push existing images** under the new namespace:

```bash
docker pull kurtpayne/skillscan-security:latest
docker tag kurtpayne/skillscan-security:latest skillscandev/skillscan-security:latest
docker push skillscandev/skillscan-security:latest

# Repeat for each versioned tag (v0.3.1, v0.3.2, etc.)
docker tag kurtpayne/skillscan-security:v0.3.2 skillscandev/skillscan-security:v0.3.2
docker push skillscandev/skillscan-security:v0.3.2
```

**4.3 Add deprecation notice** to the old `kurtpayne/skillscan-security` Docker Hub repo description:

> ⚠️ This image has moved to `skillscandev/skillscan-security`. Please update your `docker pull` commands. This repository will not receive further updates.

**4.4 Update DISTRIBUTION.md** with the new `docker pull skillscandev/skillscan-security` instructions.

---

## Phase 5 — Update All References (30 min)

Search for and update all references to the old namespaces. The following files are known to contain them:

| File | What to update |
|---|---|
| `README.md` | `docker pull kurtpayne/...` → `skillscandev/...` |
| `docs/DISTRIBUTION.md` | Docker pull commands, PyPI publisher |
| `docs/GITHUB_ACTIONS.md` | Any `kurtpayne/` image references |
| `.github/workflows/*.yml` | `DOCKER_HUB_USERNAME`, image tags |
| `editors/vscode/package.json` | Publisher field → `skillscan-dev` |
| `integrations/github-actions/skillscan-scan.yml` | Image reference |
| Website `data/scan_feed.json` CDN URL | `kurtpayne` → `skillscan-dev` in raw GitHub URL |

After updating, commit to a branch and open a PR. The CI workflows will validate everything before merge.

---

## Phase 6 — Verify CI Green (15 min)

After merging the reference-update PR:

1. Trigger the `update-index` workflow manually — confirm `index.txt` is updated and committed.
2. Trigger the publish workflow for each package — confirm PyPI and Docker Hub receive the new artifacts.
3. Check that the website feed URL resolves correctly after the GitHub org transfer.
4. Confirm the VS Code extension build workflow passes with the new publisher ID.

---

## Phase 7 — Private Corpus Repo (10 min, when ready)

This step is separate from the main migration and can be done any time after the org is set up.

1. Create `skillscan-dev/skillscan-corpus` as a **private** repo.
2. Move adversarial fixtures and held-out eval set from `skillscan-security/corpus/` to the private repo.
3. Generate a deploy key, add public key to `skillscan-corpus` deploy keys (read-only).
4. Add private key as `CORPUS_DEPLOY_KEY` secret in `skillscan-security`.
5. Update `corpus-sync` workflow to clone from the private repo using the deploy key.

---

## Checklist Summary

- [ ] GitHub repos transferred to `skillscan-dev` org
- [ ] Branch protection rules recreated on all repos
- [ ] `CODEOWNERS` added to all repos
- [ ] `INDEX_PAT` regenerated and saved in new org repo secrets
- [ ] `PYPI_API_TOKEN` regenerated and saved
- [ ] `DOCKER_HUB_TOKEN` and `DOCKER_HUB_USERNAME` saved
- [ ] `VSCE_PAT` generated and saved; VS Code publisher `skillscan-dev` registered
- [ ] `skillscan-dev` added as PyPI maintainer on both packages
- [ ] Docker images re-tagged and pushed to `skillscandev/` namespace
- [ ] Deprecation notice added to old Docker Hub repos
- [ ] All README/docs/workflow references updated to new namespaces
- [ ] CI workflows green after migration
- [ ] Old personal tokens revoked
- [ ] (Later) Private corpus repo created and `CORPUS_DEPLOY_KEY` configured
