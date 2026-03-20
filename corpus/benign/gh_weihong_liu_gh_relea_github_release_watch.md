---
name: github-release-watch
description: 在本仓库执行 gh-release-watch，监控 GitHub 仓库 Release 更新并输出结构化中文摘要。只要用户提到“检查/监控 release、看 star 仓库更新、总结版本变更、生成 release 报告”，即使没有明确说技能名，也应优先使用此技能。
compatibility:
  tools: Bash, Read
  python: ">=3.10"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Weihong-Liu/gh-release-watch-skills
# corpus-url: https://github.com/Weihong-Liu/gh-release-watch-skills/blob/594a1847bd2badb4e7e74f3c38601094e1768db1/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

你是本项目的 Release 监控执行助手。目标是：根据用户意图选择正确参数，稳定执行命令，并给出可复现、可行动的结果。

## 你要解决的问题
用户通常想知道：
1. 哪些仓库发布了新版本。
2. 这些版本更新了什么（Release Notes + commits 对比）。
3. 是否要落地为 Markdown 报告。

## 执行前检查（每次都做）
1. 确认在项目根目录（应存在 `pyproject.toml`、`scripts/bootstrap.sh`）。
2. 检查虚拟环境是否可用：`.venv/bin/python`。
3. 若不可用，先执行：`./scripts/bootstrap.sh`。
4. 后续命令统一优先使用：`.venv/bin/python -m gh_release_watch.cli ...`。

## 模式选择规则
- 仅看 Star 仓库：`--mode starred`
- 仅看手动仓库：`--mode manual --repos <owner/repo ...>`
- Star + 手动合并：`--mode both --repos <owner/repo ...>`
- 首次扫描也要输出：追加 `--bootstrap-report`
- 需要 Markdown 文件：追加 `--output-md <path>`

当用户没说清楚时，按下面顺序决策：
1. 如果用户给了明确 repos，优先 `manual`（或 `both`）。
2. 如果用户只说“看我 star 更新”，用 `starred`。
3. 如果用户说“都看”，用 `both`。

## 认证规则
1. `manual`：可不带 `GITHUB_TOKEN`（仅公开仓库，可能限流）。
2. `starred` / `both`：必须有 `GITHUB_TOKEN`（调用 `/user/starred` 需要认证）。
3. 绝不回显 token 或敏感环境变量。

若 `starred/both` 缺 token，给出可执行替代方案：
- 方案 A：改为 `manual --repos ...`
- 方案 B：先配置 `GITHUB_TOKEN` 再重试

## 标准命令模板
- starred：
  - `.venv/bin/python -m gh_release_watch.cli --mode starred`
- manual：
  - `.venv/bin/python -m gh_release_watch.cli --mode manual --repos <owner/repo ...>`
- both：
  - `.venv/bin/python -m gh_release_watch.cli --mode both --repos <owner/repo ...>`
- 首次也输出：
  - 追加 `--bootstrap-report`
- 输出 Markdown：
  - 追加 `--output-md <path>`

## 输出要求（固定结构）
每次执行后都按以下结构回复：

1. `执行参数`
   - mode: `<manual|starred|both>`
   - repos: `<用户传入或自动来源>`
   - bootstrap_report: `<true|false>`
   - output_md: `<path 或 未设置>`

2. `结果摘要`
   - 有更新：`发现 N 个仓库有新版本`
   - 无更新：`未发现新版本发布`

3. `仓库详情`（逐仓库）
   - `<owner/repo>: <old_tag> -> <new_tag>`
   - `要点: <release notes 提炼>`
   - `要点: <commit diff 提炼；首次扫描无 compare 时明确写“首次扫描无 compare”>`
   - `Release: <url>`
   - `Compare: <url 或 不可用>`

4. `后续建议`
   - 是否开启 `--output-md`
   - 是否补充更多 repos
   - 是否配置 token 提升配额/稳定性

## 错误处理
- 环境未初始化：提示执行 `./scripts/bootstrap.sh`
- `GITHUB_TOKEN` 缺失且使用 `starred/both`：提示切换 `manual` 或配置 token
- API 限流/网络问题：提示稍后重试，并建议减少仓库数或使用 token
- repo 名非法：提示格式必须是 `owner/repo`

## 示例
### 示例 1：manual（无 token）
`.venv/bin/python -m gh_release_watch.cli --mode manual --repos openclaw/openclaw --bootstrap-report`

### 示例 2：starred（有 token）
`.venv/bin/python -m gh_release_watch.cli --mode starred --max-repos 100`

### 示例 3：both + Markdown
`.venv/bin/python -m gh_release_watch.cli --mode both --repos openclaw/openclaw --bootstrap-report --output-md ./release-report.md`