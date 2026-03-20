---
name: cve-fixer
description: "CVE vulnerability fixing workflow for Debian packages. Searches CVE databases, generates patches with one-CVE-per-patch enforcement, validates with quilt (or git apply fallback), and submits to Gerrit/GitHub. Works without quilt/devscripts using fallback methods. Use when fixing CVEs in Debian packages, applying security patches, or managing Debian security updates."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: deepin-community/.deepin-cve-fixer
# corpus-url: https://github.com/deepin-community/.deepin-cve-fixer/blob/e6aaedd2de2bb914aa3523f1762f3d3c758402d4/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# CVE Fixer

Complete workflow for identifying, fixing, and submitting CVE security patches.

## ⚡ No-Dependency Mode

CVE Fixer works in environments **without quilt or devscripts installed**:

| Tool | Required? | Fallback |
|------|-----------|----------|
| quilt | Optional | `git apply` for patch validation |
| dch (devscripts) | Optional | Direct changelog file update |
| git | Required | - |
| Python 3.8+ | Required | - |

**Check your environment:**
```bash
python3 scripts/changelog_helper.py check-deps
python3 scripts/patch_helper.py check-deps
```

**No-quilt validation:**
```bash
# Validate patches without quilt
python3 scripts/patch_helper.py validate --repo /path/to/worktree

# Generate report
python3 scripts/patch_helper.py report --repo /path/to/worktree
```

**No-dch changelog update:**
```bash
# Update changelog directly (works without devscripts)
python3 scripts/changelog_helper.py update \
  --repo /path/to/worktree \
  --cve-id CVE-2024-10041 \
  --description "Fix buffer overflow"
```

## Directory Structure

```
~/.openclaw/workspace/.cve-fixer/  # Default work directory (configurable)
├── git-repos/              # Repository cache (auto-named by type: gerrit/github/other)
└── git-worktree/           # Per-CVE worktrees
    └── pkg-CVE-ID/         # Single CVE, or pkg-CVE1-CVE2-CVE3 for multi-CVE
        ├── .cve-fixer/     # CVE data (gitignored)
        │   └── workflow_state.json  # Per-CVE state tracking
        └── debian/         # Your fix
            └── patches/
```

## Core Concepts

**Phase-Based Workflow** (0→1→2→3→4→5): Setup → Research → Development → Packaging → Validation → Submission. Start with [references/cve-workflow.md](references/cve-workflow.md).

**Multi-CVE Worktrees**: Shared worktrees for sequential CVE fixes. Single: `repo-name-CVE-ID`. Multi: `repo-name-CVE1-CVE2-CVE3` (sorted). State: `.cve-fixer/CVE-ID/workflow_state.json`.

**One-CVE-Per-Patch** (STRICT): Each CVE needs its own `debian/patches/CVE-YYYY-XXXXX.patch`. Multiple CVEs can be committed together with shared changelog. See [references/phase-3-debian-packaging.md](references/phase-3-debian-packaging.md).

## Quick Start

**STRICT**: Complete phases sequentially 0→1→2→3→4→5. See [Workflow Enforcement](#workflow-enforcement-summary).

**Language Configuration** (默认中文/Chinese by default):
```bash
# Set language (zh/en)
python3 scripts/config.py --set language=zh  # 简体中文 (默认/default)
python3 scripts/config.py --set language=en  # English
```

**首次运行 (First Run)**: 运行任何脚本时，如果未配置工作目录，系统会通过交互式提示引导您设置工作目录路径。语言默认设为中文，所有输出信息将使用中文显示。

```bash
# Phase 0: Worktree Setup (MANDATORY)
python3 scripts/config.py --setup
python3 scripts/git_worktree_manager.py add-repo <url>              # auto-named
python3 scripts/git_worktree_manager.py create <cache-name> CVE-2024-10041
# Multi-CVE: python3 scripts/git_worktree_manager.py create <cache-name> CVE-2024-10041,CVE-2024-10042

# Phase 1: CVE Research
python3 scripts/search_cve.py CVE-2024-10041 --format json --repo-name pkg

# Phase 2: Patch Development
# Step 0 (MANDATORY): Verify CVE is not already fixed
python3 scripts/discover_cve_patch.py CVE-2024-10041 --dir /path/to/package --status-only

# Phase 3: Debian Packaging (changelog MANDATORY for every fix)
# AUTOMATED: generate_patch.py will automatically update changelog
# Uses dch if available, falls back to direct update if not
python3 scripts/generate_patch.py \
  --cve-id CVE-2024-10041 \
  --patch-content patch_file.txt \
  --repo /path/to/worktree

# See references/phase-3-debian-packaging.md for patch format & quilt workflow

# Phase 4: Validation
# With quilt:
python3 scripts/validate_patch.py --repo /path/to/worktree
# Without quilt (fallback):
python3 scripts/patch_helper.py validate --repo /path/to/worktree

# Phase 5: Submission
python3 scripts/submit_patch.py --cve-id CVE-2024-10041 --description "Fix ..." --repo /path/to/worktree
```

## Workflow Enforcement Summary

**STRICT:** Phases must be completed in sequence. Each phase validates prerequisite completion.

**Key requirements:**
- Phase 2, Step 0 CVE status check is MANDATORY before patch development
- Attempting to skip phases results in `Error: Phase X must be completed before Phase Y`
- Use `--force` ONLY for recovery (not for skipping mandatory checks)
- Enable `DEEPIN_CVE_AUDIT_MODE=1` to audit force flag usage

**State file:** `.cve-fixer/workflow_state.json` (single-CVE) or `.cve-fixer/CVE-ID/workflow_state.json` (multi-CVE)

**For detailed enforcement rules, state file format, force flag usage, and error recovery, see [references/workflow-enforcement.md](references/workflow-enforcement.md)**

## Scripts

**Core:**
- `git_worktree_manager.py` - Worktree lifecycle (validates Phase 0)
- `config.py` - Configuration management (includes language settings: zh/en)
- `workflow_state.py` - Workflow state tracking (--get-state, --set-phase, --validate, --reset)
- `i18n.py` - Internationalization module for multi-language support

**Workflow scripts (auto-validate phases):**
- `search_cve.py` - CVE database search (validates Phase 0, updates Phase 1)
- `discover_cve_patch.py` - Patch discovery & CVE status check (validates Phase 1, updates Phase 2, Step 0 mandatory)
- `generate_patch.py` - Patch generation (validates Phase 2 Step 0)
- `validate_patch.py` - Patch validation (validates Phase 2, can update Phase 4)
- `validate_cve_patch.py` - CVE compliance (validates Phase 2)
- `submit_patch.py` - Patch submission (validates Phase 4, updates Phase 5)

**No-dependency helpers:**
- `changelog_helper.py` - Update changelog without dch (devscripts)
- `patch_helper.py` - Validate patches without quilt (uses git apply)

## Troubleshooting

**Missing dependencies:**
```bash
# Check what's available
python3 scripts/changelog_helper.py check-deps
python3 scripts/patch_helper.py check-deps

# Install if needed (requires sudo)
sudo apt install quilt devscripts
```

**Common issues:**
- **Workflow state errors** → See [references/workflow-enforcement.md](references/workflow-enforcement.md)
- **Patch application/build/submission failures** → See [references/troubleshooting.md](references/troubleshooting.md)
- **Emergency procedures** → See [references/emergency.md](references/emergency.md)

**Language support:**
- **Default language**: Chinese/简体中文 (`zh`) - 所有用户输出信息默认使用中文
- **Switch language**: `python3 scripts/config.py --set language=zh` 或 `--set language=en`
- **All user messages**: 已本地化为中文和英文

## References

**Start here:**
- `references/cve-workflow.md` (195 lines) - Workflow navigation and quick lookup

**Phase guides** (load when needed):
- `references/phase-0-worktree-setup.md` (191 lines) - Worktree lifecycle & repo caching
- `references/phases-1-2-4-research-dev-validation.md` (321 lines) - Research + Development + Validation
- `references/phase-3-debian-packaging.md` (222 lines) - Packaging, quilt, changelog, commit
- `references/phase-5-submission.md` (146 lines) - Gerrit + GitHub workflows

**Support:**
- `references/workflow-enforcement.md` (232 lines) - Phase validation, state management
- `references/troubleshooting.md` (48 lines) - Common issues
- `references/emergency.md` (37 lines) - Emergency procedures

**Templates** (format reference):
- `assets/commit-msg-template` - Git commit message format
- `assets/patch-template.patch` - Patch file header format