---
name: bilibili-follow
description: "B站关注 UP 主 AI 辅助分类与分组同步。触发词：B站关注、UP主分类、bilibili关注整理、关注列表分组"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sunrisever/bilibili-follow-classifier
# corpus-url: https://github.com/sunrisever/bilibili-follow-classifier/blob/ac3a2f934f212e5ffdfa95929d34e56fb247a057/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# B站关注分类

自动分类 B站关注的 UP 主，并将分类结果同步到 B站关注分组。

## 触发关键词

B站关注、UP主分类、bilibili关注整理、关注列表分组、整理关注、UP主分组

## 适用场景

- 需要整理已经关注的大量 UP 主
- 希望把学习、考研、技术、娱乐等关注对象分进不同分组
- 想先本地预览分类结果，再决定是否真的同步到 B站

## 运行前提

- 在 `data/config.json` 中填写有效的 B站 Cookie：
  - `sessdata`
  - `bili_jct`
  - `buvid3`
  - `dedeuserid`
- 运行环境默认使用 Anaconda `base`
- 安装依赖：`bilibili-api-python>=16.0.0`、`httpx>=0.24.0`
- 如果需要生成或调整分类规则，可额外配好你的 LLM API

## 数据与隐私

- 私密配置只放在 `local/` 或 `data/config.json` 这一类本地文件中
- 不要把 Cookie、账号信息、导出的个人数据提交到 Git
- 发布前按 [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) 复核

## 标准工作流

### 1. 采集关注数据

```bash
python fetch.py all
```

可选：

```bash
python fetch.py zones
python fetch.py <mid>
```

输出：

- `data/up主详细数据.json`

### 2. 自动分类

```bash
python classify.py
```

分类依据：

- UP 主名称、签名
- 合集名、系列名
- 视频标题、标签
- 专栏文章标题
- 投稿分区

输出：

- `data/分类结果.json`
- `data/分类结果.md`

### 3. 预览同步

```bash
python sync_groups.py --dry-run
python sync_groups.py --dry-run --category "学习"
```

### 4. 执行同步

```bash
python sync_groups.py
python sync_groups.py --category "考研" --category "AI"
```

## 辅助脚本

### 增量添加 UP 主

```bash
python add_new.py 12345678 87654321
```

### 生成信息汇总

```bash
python generate_info.py
```

## 风险提醒

- `sync_groups.py` 会重建你在 B站上的自定义关注分组，务必先 `--dry-run`
- Cookie 过期后需要重新抓取
- 分组名中的非法字符会被自动替换
- 频繁调用 B站接口可能触发风控，脚本内部已做基础限速