---
name: cherry-pick-backport
description: Backport upstream commits into downstream release branches via cherry-pick. Use when the user mentions backport, cherry-pick, or porting upstream commits to an older branch.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: aslakknutsen/ossm-cherry-pick-backport-skill
# corpus-url: https://github.com/aslakknutsen/ossm-cherry-pick-backport-skill/blob/2dd44b3ec822605a806ad50b60113f3cc277bbe0/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Cherry-Pick Backport

Backport one or more upstream commits into one or more downstream release branches.

The user provides:
- **Source SHA(s)** — commits to backport, probably from upstream (comma or space separated)
- **Target branch(es)** — downstream release branches to cherry-pick into (comma or space separated)
- **Push remote** (optional) — remote name to push cherry-pick branches to
- **Extra context** (optional) — known issues, files to skip, etc.

## Phase 0: Parse, Detect Remotes, Plan

1. Parse SHAs and branches from the user's message. Accept comma-separated, space-separated, or one-per-line.
2. Generate the cross-product of (SHA, branch) pairs.
3. Detect git remotes by running `git remote -v`:
   - **Upstream remote**: the remote whose URL contains `istio/istio` (the upstream org/repo). Store the remote name.
   - **Downstream remote**: the remote whose URL contains `openshift-service-mesh/istio`. Store the remote name.
   - If either cannot be determined, ask the user.
4. For each source SHA, check if it exists locally (`git cat-file -t <sha>`). If not, fetch it from the upstream remote: `git fetch <upstream-remote> <sha>`.
5. Push remote is **never assumed**. Only push if the user explicitly provides a remote name.

## Phase 1: Create Worktrees

For each (SHA, branch) pair:

```bash
SHORT="${SHA:0:8}"
WORKTREE="/tmp/cherry-pick-${SHORT}-into-${BRANCH}"
git worktree add "$WORKTREE" "<downstream-remote>/${BRANCH}"
```

If the worktree path already exists, remove it first: `git worktree remove "$WORKTREE" --force`.

## Phase 2: Dispatch Sub-Agents

Launch one `Task` sub-agent per (SHA, branch) pair. Max 4 concurrent — batch the rest.

Use `subagent_type: "generalPurpose"` for each sub-agent.

The prompt for each sub-agent must be **fully self-contained** (it has no access to this conversation). Build it from this template, substituting the concrete values:

---

BEGIN SUB-AGENT PROMPT TEMPLATE:

You are a release engineer backporting upstream commit `{SHA}` into the `{BRANCH}` branch.

Your working directory is `{WORKTREE}`. Use `working_directory: "{WORKTREE}"` for ALL shell commands.

### Setup

1. Create the cherry-pick branch:
   ```
   git checkout -b cherry-pick-{SHORT}-into-{BRANCH}
   ```
2. Run the backport hints script:
   ```
   bash {SKILL_DIR}/scripts/generate-backport-hints.sh {SHA} {BRANCH}
   ```
3. Read the hints file at `/tmp/backport-hints-{SHORT}-{BRANCH}`. These describe known divergences between this branch and the upstream source. Use them throughout — do not waste time rediscovering them.
4. Attempt the cherry-pick:
   ```
   git cherry-pick {SHA} || true
   ```

### Conflict Resolution

If the cherry-pick produced conflicts:
1. Find all files with conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
2. Resolve each conflict, preserving the upstream commit's intent within the older branch's architecture.
3. Remove all conflict markers.
4. `git add` the resolved files and run `git cherry-pick --continue`.

### Downstream-Only Files

If `istio.deps` was modified by the cherry-pick, revert it immediately:
```
git checkout HEAD -- istio.deps
```
This file is maintained separately downstream and must never be overwritten by upstream commits.

### Code Adaptation

Even if the cherry-pick was clean, audit the changed files for branch-specific mismatches. Use the hints file. Adapt as needed:
- **Import paths / APIs**: internal APIs or file structures may differ on this branch. Update imports and function calls to match.
- **Language features**: do not use Go features or stdlib additions unsupported by this branch's Go version (check the hints for the Go version).
- **Dependencies**: if the upstream commit uses newer third-party packages, adapt the code to work with the versions in this branch's go.mod. Do not bump dependency versions unless the fix cannot work otherwise.
- **Test fixtures / golden files**: update hardcoded version strings or expected outputs that reference the upstream branch.

### Verification

1. Identify which test suites cover the modified code.
2. Run them: `go test ./path/to/package/...`
3. If tests fail, analyze the failure, fix the code, and re-run.
4. If the backport requires a massive architectural rewrite that makes it fundamentally incompatible, stop and explain why.

### Finalization

If you made ANY changes beyond a clean cherry-pick (conflict resolution, API adaptation, syntax downgrades, test fixes):
1. Amend the commit: `git commit --amend` (do NOT use `--no-edit`).
2. Keep the original commit message, author intent, and the `(cherry picked from commit ...)` line.
3. Append git trailers at the very end of the message:
   ```
   Backport-Change: <one-line summary of what you modified or dropped>
   Backport-Reason: <one-line explanation of why the adaptation was needed>
   ```

### Return

When done, output a single summary line in this format:
```
RESULT: {SHA} into {BRANCH} — <status: clean|adapted|failed> — <one-line detail>
```

END SUB-AGENT PROMPT TEMPLATE

---

To resolve `{SKILL_DIR}`, use the absolute path to this skill's directory. You can determine it from the path of this SKILL.md file — it is the parent directory. For example, if this file is at `/home/user/repo/.cursor/skills/cherry-pick-backport/SKILL.md`, then `{SKILL_DIR}` is `/home/user/repo/.cursor/skills/cherry-pick-backport`.

## Phase 2.5: Review Sub-Agents

After ALL backport sub-agents from Phase 2 have completed, launch a second round of review sub-agents — one per (SHA, branch) pair whose backport status was `clean` or `adapted` (skip `failed` pairs).

- Use `subagent_type: "generalPurpose"`, `readonly: true`.
- Max 4 concurrent, batch the rest.
- Each review agent is a **fresh agent** with no shared context from the backport agent.

The review agent does **not** fail or block the backport. It surfaces concerns for the user to evaluate.

Build the review prompt from this template, substituting concrete values:

---

BEGIN REVIEW SUB-AGENT PROMPT TEMPLATE:

You are a code reviewer verifying a cherry-pick backport. Your job is to compare the backported result against the original upstream commit and flag any unjustified divergences.

Your working directory is `{WORKTREE}`. Use `working_directory: "{WORKTREE}"` for ALL shell commands. Do NOT modify any files.

### Inputs

- Original upstream commit: `{SHA}`
- Target branch: `{BRANCH}`
- Cherry-pick branch (currently checked out): `cherry-pick-{SHORT}-into-{BRANCH}`
- Hints file: `/tmp/backport-hints-{SHORT}-{BRANCH}`

### Steps

1. Read the original commit message to understand intent:
   ```
   git log -1 --format=%B {SHA}
   ```

2. Read the hints file at `/tmp/backport-hints-{SHORT}-{BRANCH}`. These describe known, expected divergences (Go version differences, dependency deltas, gateway-api migration, downstream-only files). Divergences explained by these hints are acceptable.

3. Show the original upstream diff (what the commit changed in its original context):
   ```
   git diff {SHA}~1..{SHA}
   ```

4. Show the backported diff (what the cherry-pick branch changed relative to its base):
   ```
   git log -1 -p HEAD
   ```

5. Compare the two diffs. For every difference between them, determine whether it is:
   - **Expected**: explained by the hints file or obvious branch context (different import paths, older APIs, file renames).
   - **Suspicious**: not explained by hints or context. This includes:
     - Dropped hunks (code from the original that is missing in the backport without explanation)
     - Unrelated new code not present in the original commit
     - Logic inversions or semantic changes to conditionals, return values, error handling
     - Removed or weakened test coverage
     - Changes to files not touched by the original commit

### Output

Return a single structured result:
```
REVIEW: {SHA} into {BRANCH} — <pass|concerns> — <detail>
```

- Use `pass` if all divergences are justified.
- Use `concerns` if any suspicious divergences exist. List each concern as a bullet point in the detail.

END REVIEW SUB-AGENT PROMPT TEMPLATE

---

## Phase 3: Collect Results

After all backport and review sub-agents complete:

1. Report a summary table with columns: **pair**, **backport status**, **review verdict**, **details**.
2. If the user specified a push remote, for each pair where review is `pass` (or the user explicitly overrides):
   ```bash
   git push -u <push-remote> cherry-pick-<SHORT>-into-<BRANCH>
   ```
   Then optionally create PRs:
   ```bash
   gh pr create \
     --base "<BRANCH>" \
     --head "cherry-pick-<SHORT>-into-<BRANCH>" \
     --title "[cherry-pick] <SHORT> into <BRANCH>" \
     --body "Cherry-pick of <SHA> into <BRANCH>."
   ```
   Do **not** push pairs where review raised concerns unless the user says to proceed.
3. Clean up all worktrees:
   ```bash
   git worktree remove /tmp/cherry-pick-<SHORT>-into-<BRANCH>
   ```