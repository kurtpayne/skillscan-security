---
name: power-of-ten
description: Use when reviewing code quality, auditing scripts or programs for robustness, or when asked to check code against safety-critical standards. Triggers on "code review", "code quality", "audit this code", "power of ten", "nasa check"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: remigius-labs/power-of-ten
# corpus-url: https://github.com/remigius-labs/power-of-ten/blob/07627a6e162586d8701fa44be65edba89dad3085/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Power of Ten

## Overview

Systematic code quality audit based on NASA/JPL's **"Power of Ten"** rules (Gerard Holzmann). Ten rules originally written for safety-critical C, adapted here for any language. The goal: code that is analyzable, testable, and defensible.

**Core principle:** If you can't prove it's correct, it's not correct.

> Based on "The Power of Ten: Rules for Developing Safety-Critical Code" by Gerard J. Holzmann, NASA/JPL. Published in IEEE Computer, June 2006.

## When to Use

- Code quality review or audit requested
- Preparing code for production or shared use
- After major refactoring
- Before claiming code is "clean" or "done"

**When NOT to use:** Quick prototypes, throwaway scripts, exploratory code the user explicitly marks as draft.

## The 10 Rules (Language-Adapted)

Run these **in order**. Each rule has a concrete check. Report findings per rule with location and severity.

### Rule 1: Simple Control Flow

**Original:** No goto, setjmp/longjmp, recursion.
**Adapted:** No recursion unless bounded. No unreachable code. No convoluted branching (deeply nested if/else chains, fall-through switches without comments).

**Check:**
- Grep for recursive calls (function calls itself)
- Flag functions with nesting depth > 4
- Flag unreachable code after return/exit/break

| Language | What to grep |
|----------|-------------|
| Bash | Function name appearing inside its own body |
| Python | `def foo` ... `foo(` inside same function |
| JS/TS | Function/method calling itself without base case |
| Solidity | Internal calls to self (watch for indirect recursion via internal functions) |

### Rule 2: Bounded Loops

**Original:** All loops must have a fixed upper bound.
**Adapted:** Every loop must terminate. Identify unbounded loops and verify they have an exit condition.

**Check:**
- `while true` / `while :` / `for (;;)` — must have `break` or bounded exit
- `while read` loops — OK (bounded by input)
- Verify no infinite retry loops without backoff or max attempts

### Rule 3: No Unsafe Dynamic Allocation

**Original:** No heap allocation after initialization.
**Adapted:** Resources acquired in setup, not mid-operation. Watch for unbounded growth.

**Check:**
- Arrays/lists that grow without bound inside loops
- Temp files created but never cleaned up
- File handles opened but never closed
- Background processes spawned without `wait`

| Language | What to check |
|----------|--------------|
| Bash | `mktemp` without trap cleanup, background `&` without `wait` |
| Python | Files opened without `with`, unbounded list appends in loops |
| JS/TS | Event listeners never removed, intervals never cleared |
| Solidity | Unbounded array pushes, storage growth in loops |

### Rule 4: Function Length — Max 60 Lines

**Original:** No function longer than a single printed page (~60 lines).
**Adapted:** Same. 60 lines of logic (excluding blank lines and comments).

**Check:**
```bash
# Bash: count lines per function
awk '/^[a-zA-Z_][a-zA-Z_0-9]*\(\)/{name=$1; count=0; next} /^\}/{if(count>60) print name": "count" lines"; count=0} {count++}' "$file"
```
- Flag every function > 60 lines
- Suggest how to decompose (extract helpers, split phases)

### Rule 5: Defensive Checks — 2+ Assertions Per Function

**Original:** Minimum 2 assertions per function on average.
**Adapted:** Functions must validate assumptions. Not literal `assert` — any guard check counts.

**What counts as an assertion:**
- Parameter validation (`[ -z "$arg" ] && return 1`)
- Precondition checks (`if ! command -v rsync; then ...`)
- State validation (`[[ -d "$dir" ]] || { echo "missing"; exit 1; }`)
- Return value checks on critical operations

**Check:**
- Count guard/validation checks per function
- Flag functions with 0 defensive checks (especially functions that take parameters or interact with filesystem/network)
- Pure display/UI functions may be exempt

### Rule 6: Smallest Scope

**Original:** Declare variables at smallest possible scope.
**Adapted:** No unnecessary globals. Variables declared close to use.

**Check:**
- List all global/module-level variables — justify each one
- Flag globals that are only used in one function
- Flag variables set by side-effect in one function, read in another (hidden coupling)
- Verify `local`/`let`/`const` used appropriately

### Rule 7: Check Every Return Value

**Original:** Check return value of every non-void function. Check all function parameters.
**Adapted:** No silently ignored errors. Every external call's result is checked or explicitly discarded.

**Check:**
- Commands whose exit code is never tested
- Functions that return values nobody reads
- `> /dev/null 2>&1` without checking `$?` or using `|| handle_error`
- Piped commands where intermediate failures are masked (no `set -o pipefail` in bash)

**Common violations:**
```bash
# BAD: silent failure
cd "$dir"
rm -rf "$path"

# GOOD: checked
cd "$dir" || { echo "Failed to cd"; exit 1; }
```

### Rule 8: Minimal Metaprogramming

**Original:** Limit preprocessor to includes and simple conditionals.
**Adapted:** Limit eval, exec, metaprogramming, code generation. Keep code readable without tracing through indirection.

**Check:**
- `eval`, `exec`, `source` of dynamic paths
- Python `exec()`, `eval()`, excessive decorators that obscure flow
- JS `eval()`, dynamic `import()`, complex proxy chains
- Solidity `delegatecall`, inline assembly

### Rule 9: Limit Indirection

**Original:** Restrict pointers to single dereference.
**Adapted:** Limit levels of indirection. Code should be traceable — you can follow a value from source to use.

**Check:**
- Bash: `${!var}` (indirect expansion), deeply nested variable references
- Python: `getattr` chains, deeply nested dict access
- JS: Optional chaining more than 3 levels deep
- General: Data flowing through 3+ transformations before use

### Rule 10: Zero Warnings from Static Analysis

**Original:** Compile with all warnings on, use static analyzers, zero warnings.
**Adapted:** Run the language's standard linter with strict settings. Zero warnings.

**Check — run the right tool:**

| Language | Tool | Strict flags |
|----------|------|-------------|
| Bash | `shellcheck` | Default (all warnings) |
| Python | `ruff` or `pylint` | `--select=ALL` or default |
| JS/TS | `eslint` | Recommended config |
| Solidity | `slither` | Default detectors |
| Go | `go vet` + `staticcheck` | Default |
| Rust | `clippy` | `-- -D warnings` |

- Run the tool
- Report warning count
- Fix all warnings or justify each suppression

## Audit Report Format

Structure your report as:

```
# NASA Code Check: [filename]

## Summary
- Total functions: N
- Functions > 60 lines: N (list them)
- Static analysis warnings: N
- Rules passed: N/10
- Rules failed: N/10

## Findings by Rule

### Rule 1: Simple Control Flow — PASS/FAIL
[findings — if FAIL, list each violation with location]

### Rule 2: Bounded Loops — PASS/FAIL
...

Verdict is PASS or FAIL only — no "conditional" or "partial". Any violation = FAIL.

## Recommendations
[prioritized list — HIGH items first]
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping static analysis ("I'll read the code instead") | Tool catches what eyes miss. Always run it. |
| Counting blank lines in function length | Count logic lines only |
| Ignoring Rule 5 for "simple" functions | Simple functions still take parameters — validate them |
| Treating `set -e` as sufficient error handling | `set -e` has many gotchas; explicit checks are better |
| Marking Rule 3/8/9 as N/A without checking | Adapted versions apply to every language. Check before exempting. |

## Quick Reference

```
 1. Simple control flow    → no recursion, no deep nesting
 2. Bounded loops          → every loop terminates provably
 3. No unsafe allocation   → resources acquired in setup, cleaned up
 4. Functions ≤ 60 lines   → measure it, break up violations
 5. 2+ checks per function → validate params, state, returns
 6. Smallest scope         → no unnecessary globals
 7. Check all returns      → no silent failures
 8. Minimal metaprogramming→ no eval/exec/dynamic code
 9. Limit indirection      → traceable data flow
10. Zero static warnings   → run the linter, fix everything
```