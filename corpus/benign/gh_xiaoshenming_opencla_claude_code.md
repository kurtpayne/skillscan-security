---
name: claude-code
description: "Launch and manage Claude Code CLI sessions for coding tasks. Use when: (1) building features or apps, (2) refactoring codebases, (3) debugging complex issues, (4) reviewing PRs, (5) writing tests, (6) any task requiring multi-file code exploration and editing. Triggers on: 'use claude code', 'coding task', 'build feature', 'fix bug', 'refactor', 'write tests', 'review PR', 'create project'. User prefers --dangerously-skip-permissions mode and team mode (multi-agent). NOT for: simple one-liner fixes (just edit directly), reading code (use read tool), or work inside ~/clawd workspace."
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: xiaoshenming/openclaw-claude-code-skills
# corpus-url: https://github.com/xiaoshenming/openclaw-claude-code-skills/blob/34f91b96c92963e9e1237b140b4669ea5419d87a/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Claude Code Skill

Launch Claude Code CLI (`claude`) from OpenClaw to handle coding tasks. User has team mode enabled and prefers `--dangerously-skip-permissions`.

## Quick Reference

```bash
# One-shot task (non-interactive, exits when done)
claude -p "your prompt" --dangerously-skip-permissions

# One-shot with specific project dir
cd /home/ming/data/Project/your-project && claude -p "your prompt" --dangerously-skip-permissions

# Interactive session (needs PTY)
claude --dangerously-skip-permissions

# Continue last conversation
claude -c --dangerously-skip-permissions

# Resume named session
claude -r "session-name" --dangerously-skip-permissions
```

## ⚠️ PTY Required for Interactive Mode

Claude Code is a terminal app. Always use `pty:true` for interactive sessions:

```bash
# ✅ Correct
exec pty:true workdir:/home/ming/data/Project/myproject command:"claude --dangerously-skip-permissions"

# ✅ One-shot (no PTY needed)
exec workdir:/home/ming/data/Project/myproject command:"claude -p 'your prompt' --dangerously-skip-permissions"
```

## Execution Patterns

### Pattern 1: One-Shot Task (Recommended for most tasks)

Best for well-defined tasks. Runs and exits cleanly.

```bash
exec workdir:/home/ming/data/Project/myproject command:"claude -p 'Add error handling to all API endpoints. Run tests after.' --dangerously-skip-permissions"
```

### Pattern 2: Background Long-Running Task

For complex tasks that take time:

```bash
# Start in background
exec pty:true background:true workdir:/home/ming/data/Project/myproject command:"claude -p 'Refactor the entire auth module to use OAuth2. Write tests. Commit when done.' --dangerously-skip-permissions"

# Monitor progress
process action:log sessionId:XXX

# Check if done
process action:poll sessionId:XXX

# Send input if needed
process action:submit sessionId:XXX data:"yes"
```

### Pattern 3: Multi-Agent / Team Mode

User has team mode enabled. For complex tasks, use subagents or agent teams:

```bash
# Use built-in subagents (automatic delegation)
claude -p "Explore the auth module, plan improvements, then implement them" --dangerously-skip-permissions

# Explicit subagent usage with custom agents
claude -p "Use the code-reviewer agent to check src/auth/" --dangerously-skip-permissions --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a senior code reviewer.","tools":["Read","Grep","Glob","Bash"]}}'

# Agent teams (experimental, for parallel work)
# Requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions
# Then: "Create a team: one on frontend, one on backend, one on tests"
```

### Pattern 4: PR Review

```bash
# Review current branch changes
exec workdir:/home/ming/data/Project/myproject command:"claude -p 'Review the changes in this branch vs main. Focus on security, performance, and code quality. git diff main...HEAD' --dangerously-skip-permissions"

# Review specific PR (clone to temp)
REVIEW_DIR=$(mktemp -d) && git clone <repo-url> $REVIEW_DIR && cd $REVIEW_DIR && gh pr checkout <PR#>
exec workdir:$REVIEW_DIR command:"claude -p 'Review this PR thoroughly' --dangerously-skip-permissions"
```

### Pattern 5: Piped Input

```bash
# Analyze logs
cat error.log | claude -p "Explain these errors and suggest fixes" --dangerously-skip-permissions

# Review changed files
git diff main --name-only | claude -p "Review these changed files for security issues" --dangerously-skip-permissions

# Process data
cat data.json | claude -p "Transform this into a CSV format" --dangerously-skip-permissions
```

## Key CLI Flags

| Flag | Description |
|------|-------------|
| `-p "prompt"` | One-shot mode (non-interactive, exits when done) |
| `-c` | Continue most recent conversation |
| `-r "session"` | Resume session by ID or name |
| `--dangerously-skip-permissions` | Skip all permission prompts |
| `--model sonnet/opus/haiku` | Choose model |
| `--add-dir ../other-dir` | Add extra working directories |
| `--max-turns N` | Limit agentic turns (print mode) |
| `--max-budget-usd N` | Limit spending (print mode) |
| `--agents '{...}'` | Define custom subagents via JSON |
| `--verbose` | Show extended thinking |
| `--permission-mode plan` | Read-only plan mode |

## Best Practices

1. **Provide verification criteria** — tell Claude how to check its work: "run tests", "build should pass", "take a screenshot"
2. **Be specific** — reference files, mention constraints, point to patterns
3. **Use plan mode first for complex tasks** — `--permission-mode plan` to explore before coding
4. **Use @file references** — `@src/auth.js` includes file content directly
5. **Manage context** — use `/compact` to reduce context when it fills up
6. **Use CLAUDE.md** — project-level instructions Claude reads every session

## Prompt Templates

### Build Feature
```
Build [feature description]. Follow existing patterns in [reference file/dir].
Write tests. Run them. Fix any failures. Commit with a descriptive message.
```

### Fix Bug
```
[paste error or describe symptom]. Check [likely location].
Write a failing test that reproduces the issue, then fix it.
Run the full test suite to verify nothing else broke.
```

### Refactor
```
Refactor [target] to use [new pattern/approach].
Maintain backward compatibility. Run tests after each change.
Commit incrementally with descriptive messages.
```

### Write Tests
```
Write tests for [module/file]. Cover edge cases:
[list specific scenarios]. Run tests and fix failures.
Follow existing test patterns in [test dir].
```

## Troubleshooting

See `references/troubleshooting.md` for common issues and solutions.

## Auto-Notify on Completion

For background tasks, use completion notification:

```bash
# At the end of your prompt, add:
exec pty:true background:true workdir:/home/ming/data/Project/AIcode/your-project command:"claude -p 'Your task here.

When done, output a summary with the project name and what was changed.' --dangerously-skip-permissions"
```

**重要：** 通知会显示 `workdir` 路径，所以务必设置正确的项目路径，不要在 skills 目录运行开发任务。

## Rules

1. **Always use `--dangerously-skip-permissions`** — user preference
2. **Use `-p` for one-shot tasks** — cleaner, exits when done
3. **Use `pty:true` for interactive sessions** — Claude Code needs a terminal
4. **Set `workdir` to the project directory** — don't run from workspace root
5. **Default dev path: `/home/ming/data/Project/AIcode/`** — AI 开发项目默认放这里
6. **Project root: `/home/ming/data/Project/`** — 项目总路径
7. **Monitor background tasks** — use `process action:log` to check progress
8. **Never run in `~/.openclaw/`** — keep workspace clean
9. **Use proxy if network issues** — `http://127.0.0.1:7897`
10. **长提示用文件传入** — `cat prompt.md | claude -p "..." ` 比直接 `-p` 传长字符串更稳定
11. **生成项目后检查 .gitignore** — 确保 node_modules/dist 等不被提交
12. **后台进程用 nohup** — `nohup cmd > /dev/null 2>&1 &` 而非单纯 `&`