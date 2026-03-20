---
name: reddit-skill
description: >
  当用户想搜索 Reddit 帖子、解析 reddit.com 或 redd.it 链接、查看帖子详情或评论，
  或排查代理配置问题时，使用这个技能。对"Reddit"、"reddit.com"、粘贴的 Reddit 链接，
  以及相关代理或访问故障自动触发。
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: hwj123hwj/reddit-skill
# corpus-url: https://github.com/hwj123hwj/reddit-skill/blob/9ce903b8802d3e16323e1ae8b165dc8201865d3b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Reddit Skill

通过 ISP 代理或 Exa 搜索，完成 Reddit 内容的搜索、读取和排障。

## 工作区规则

- 不要在 skill 工作区里创建临时辅助文件。

## 工作流程

1. **先确认访问方式。**
   先检查是否配置了 `reddit_proxy`。只有在需要精确命令、代理写入或排障细节时再读取 [references/operations.md](references/operations.md)。
   - 有代理：优先用 Reddit JSON API 读取完整帖子和评论。
   - 无代理：降级为 Exa 搜索，只返回搜索到的 Reddit 结果摘要，并明确说明限制。

2. **选择最小可行操作。**
   - 搜索关键词：优先走 Exa。
   - 解析 Reddit 链接：先识别是 `reddit.com` 还是 `redd.it`，再决定是直接补 `.json` 还是先跟随跳转。
   - 读取帖子详情：优先返回标题、作者、正文、分数、评论数，再补代表性评论摘要。

3. **直接给出可用结果。**
   默认用中文总结，除非用户明确要求保留英文原文。引用帖子内容时，优先摘取核心信息，不要整段转抄评论楼。

## 约束

- 不要假设用户有代理，先检查配置状态。
- 如果被代理问题阻塞，直接说明卡在哪一步，并引导用户配置或跳过。
- 不承诺发帖/评论等写操作，当前只支持读取。

## 参考文件

- [references/operations.md](references/operations.md)：代理配置、连通性测试、命令格式和排障说明。