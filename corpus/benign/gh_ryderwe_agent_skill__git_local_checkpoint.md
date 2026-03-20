---
name: git-local-checkpoint
description: 在本地 Git 仓库创建代码快照（Commit），仅限本地保存，严禁推送到远程仓库。
metadata:
  version: 1.1.0
tools:
  - run_shell_command
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Ryderwe/agent-skill-git-checkpoint
# corpus-url: https://github.com/Ryderwe/agent-skill-git-checkpoint/blob/2c5db689423820ae9b35c839780591efc0745962/%EF%BC%88%E6%89%8B%E5%8A%A8%E8%A7%A6%E5%8F%91%E7%89%88%E6%9C%AC%EF%BC%89SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Git Local Checkpoint (Local Save Only)

用于在代码修改后创建本地存档（Commit），便于回滚/对比。**仅限本地**，严禁任何远程操作。

## 核心安全规则

1. 禁止执行 `git push`（以及任何变体/脚本包装）。
2. 不要运行会接触远程的命令（例如 `git pull`/`git fetch`）。

## 工作流（按顺序执行）

### 1) 检查工作区状态

运行：`git status`

### 2) 参考最近提交信息风格（只读）

运行：`git log -n 5 --pretty=format:'%s'`

### 3) 总结本次改动（可选但推荐）

运行：`git diff --stat`

如需更细：`git diff`

### 4) 生成提交信息

要求：一句话、与仓库历史风格一致（中文/英文/Conventional Commits/是否带 Emoji）。

提示：如果是 AI 自动中间存档，可在末尾加 `(AI Auto-save)`，也可不加。

### 5) 暂存改动（选择其一）

- **只暂存已跟踪文件的改动（更安全）**：`git add -u`
- **暂存所有改动（含新文件）**：`git add -A`

在选择 `git add -A` 前，先确认没有误提交的文件（例如：大文件、密钥、临时产物）。

### 6) 创建本地 Commit

运行：`git commit -m 'YOUR_MESSAGE'`

如果提示 “nothing to commit”，说明当前无可提交改动：回到第 1 步确认状态即可。

### 7) 完成反馈（本地保存确认）

运行：`git rev-parse --short HEAD`

对用户说明：已在本地创建存档（给出 commit hash），未推送到远程。