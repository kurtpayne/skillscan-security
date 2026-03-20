---
name: repo-issue-triage
description: >-
  Automate GitHub issue and PR triage by cross-referencing open issues against
  pending PRs, merged PRs, and the current main branch to produce an actionable
  report with close/keep recommendations. Includes PR health monitoring.
  USE FOR: triage issues, issue checkup, PR status, close stale issues,
  issue audit, what can we close, outstanding issues, issue report,
  cross-reference PRs and issues, repo health check, sprint planning.
  DO NOT USE FOR: creating issues (use GitHub directly), fixing bugs
  (use coding skills), or PR code review (use code-review agent).
license: MIT
metadata:
  version: "2.0"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: spboyer/repo-issue-triage
# corpus-url: https://github.com/spboyer/repo-issue-triage/blob/7790ca937d29fe7a93bca08ba996978549e71e3f/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Repo Issue Triage

Automates the process of auditing all open GitHub issues against pending PRs,
recently merged PRs, and the current main branch codebase, then produces a
structured report with close/keep recommendations and actionable work items.

## Quick Reference

| Property | Value |
|----------|-------|
| **MCP Tools** | `github-mcp-server` |
| **CLI Tools** | `grep`, `glob`, `git log` |
| **Tracking** | Session SQL database |
| **Output** | Structured markdown report |
| **Best For** | Periodic repo hygiene, sprint planning, release prep |

## When to Use This Skill

- Periodic issue hygiene (weekly/monthly triage)
- Sprint planning — identify what's already covered by PRs
- Pre-release audit — find issues that can be closed
- Post-merge cleanup — close issues covered by recent merges
- PR health monitoring — CI status, review threads, approvals

## Workflow

Execute these 7 phases in order. Use parallel tool calls wherever noted.

### Phase 1: PR HEALTH CHECK

Check the status of the user's open PRs first. This is always the
starting point — address any failing CI or unresolved review threads
before moving to issue triage.

**Parallel calls:**
```
For each PR owned by the user:
  - CI status: gh pr checks {number} → count failures/passes/running
  - Review threads: GraphQL reviewThreads → count unresolved
  - Approvals: reviews → list approved-by
```

**Output table:**
```
| PR | Title | CI | Approvals | Unresolved Threads | Status |
```

**Actions if issues found:**
- CI failures → fetch job logs, identify and fix
- Unresolved threads → read comments, address or resolve
- No approvals → note as "awaiting review"

### Phase 2: FETCH ALL DATA

Fetch all open issues, open PRs, and recently merged PRs in parallel.

**Parallel calls:**
```
gh issue list --state open --limit 500
gh pr list --state open --limit 100
gh pr list --state merged --limit 30  (recent merges)
```

Extract into structured format: `number | title | labels | assignees`

> **Important:** Use `--limit 500` for issues. Paginate if repo has more.
> Use CLI (`gh`) for bulk fetching — it's faster than individual API calls.

### Phase 3: BUILD COVERAGE MAP

Build a mapping of what PRs (open and merged) cover which issues.

**Method 1: Direct links**
- Scan PR titles/bodies for "Fixes #N", "Closes #N", "fix #N"
- Check issue bodies for PR references

**Method 2: Keyword matching**
- Match PR titles against issue titles using topic keywords
- Use regex patterns for common coverage relationships

**Method 3: Known mappings**
- If the user has been working in this session, use SQL tables
  from prior work to pre-populate known coverage

**Store in SQL:**
```sql
CREATE TABLE issue_triage (
  number INTEGER PRIMARY KEY,
  title TEXT,
  labels TEXT,
  assignees TEXT,
  status TEXT DEFAULT 'pending',
  covered_by TEXT,
  reason TEXT,
  tier TEXT
);
```

### Phase 4: DEEP ANALYSIS (Parallel Batches)

For issues not clearly mapped, do deep analysis using sub-agents.

**Split issues into batches of ~100-120 and send to parallel
explore agents.** Each agent gets:

1. The batch of issues (number | title | labels | assignees)
2. The list of open PRs with descriptions of what they change
3. The list of recently merged PRs
4. Instructions to check the codebase for implemented features

**Agent prompt pattern:**
```
Read {batch_file} containing ~{N} GitHub issues for {owner}/{repo}.

For each issue, determine if it could be CLOSED or PARTIALLY addressed
by any of these recent changes:

MERGED PRs:
- #{num}: {title} ({summary of changes})

OPEN PRs:
- #{num}: {title} ({summary of changes})

Also check the codebase in {repo_path} for any issues that might
already be implemented on main.

Output ONLY issues that are CLOSEABLE or PARTIALLY covered.
Format: #NUMBER | TITLE | STATUS (CLOSE/PARTIAL) | COVERED_BY | REASON
```

> **Key:** Use `explore` agent type with a capable model (e.g., Codex)
> for accurate codebase analysis. Run 4 batches in parallel.

### Phase 5: VERIFY ON MAIN

For issues flagged as potentially fixed, verify against the codebase:

```bash
# Search for the fix
grep -r "keyword" --include="*.go" cli/
glob "**/*relevant_file*"

# Check recent commits
git log --oneline --grep="issue-keyword" -20

# Verify file exists
ls path/to/expected/implementation
```

**Critical:** Don't trust keyword matches alone. Verify the actual
implementation exists and addresses the issue's requirements.

### Phase 6: CATEGORIZE AND TIER

Assign each issue to a category using the
[classification rules](references/classification-rules.md).

**Additionally, tier actionable issues:**

| Tier | Description | Criteria |
|------|-------------|----------|
| **Close Now** | Fully covered or already on main | Verified implementation exists |
| **Auto-Close** | Linked to open PR with "Fixes #N" | Will close when PR merges |
| **Partially Covered** | PR addresses part of issue | Note what's done and what remains |
| **Quick Win** | Small, well-defined, unassigned | Can fix in <1 hour |
| **Actionable Bug** | Clear scope, reproducible, unassigned | Can investigate and fix |
| **Needs Design** | Requires architecture decisions | Flag for team discussion |
| **Assigned** | Has owner, in progress | Skip — someone is working on it |
| **Epic/Tracking** | Tracking issue, not directly closeable | Skip |

### Phase 7: REPORT

Generate the final report using the
[report template](references/report-template.md).

**Report sections:**
1. PR Health Status table
2. Closeable issues (with reasons)
3. Auto-close on merge issues
4. Partially covered issues (what's done, what remains)
5. Quick wins and actionable items
6. Category breakdown of remaining issues
7. Summary statistics

**Output as a markdown file** and open in the user's editor.

## Closing Issues

When closing issues, always include a detailed comment explaining:

1. **What PR or commit** covers the issue
2. **Specifically how** the issue is addressed (mention code/features)
3. **Any remaining gaps** (for partial closures, note what's left)

**Pattern:**
```
Addressed by PR #{num} which {specific description of what the PR does}.
{Additional detail about how this resolves the issue's requirements}.
```

**Do NOT use generic close messages** like "Fixed" or "Resolved".

## Batch Processing Guidelines

To avoid flooding the GitHub API:

| Operation | Batch Size | Delay |
|-----------|-----------|-------|
| Issue fetching | 100-500 per call | None needed |
| PR status checks | All in parallel | None needed |
| Issue closing | 2-3 at a time | 1-2 seconds between |
| Comment posting | 2-3 at a time | 1-2 seconds between |
| Sub-agent analysis | 4 parallel batches | Wait for all to complete |

## MCP Tools Used

| Tool | Method | Purpose |
|------|--------|---------|
| `github-mcp-server` | `list_pull_requests` | Fetch all open/merged PRs |
| `github-mcp-server` | `list_issues` | Fetch all open issues |
| `github-mcp-server` | `issue_read` | Deep-read individual issues |
| `github-mcp-server` | `pull_request_read` | Check PR details/diff/status |
| `github-mcp-server` | `search_issues` | Find linked issues |
| `github-mcp-server` | `search_code` | Search codebase for implementations |
| `grep` | — | Search local codebase for fixes |
| `glob` | — | Find implementation files |

## Error Handling

| Error | Resolution |
|-------|------------|
| Pagination needed (>500 items) | Use `page` parameter, loop until empty |
| Rate limiting | Add delays between batches |
| Issue body too large | Extract first 500 chars for classification |
| Ambiguous classification | Default to `KEEP_OPEN` (conservative) |
| Sub-agent timeout | Retry with smaller batch |
| GraphQL thread query fails | Fall back to REST API reviews endpoint |

## Reference Documentation

- [Classification Rules](references/classification-rules.md) — Decision tree for categorizing issues
- [Report Template](references/report-template.md) — Output format specification