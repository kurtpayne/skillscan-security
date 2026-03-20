---
name: mathpix
description: "Mathpix API 文档转换 -- PDF/图片/PPT/Word 转 Markdown、LaTeX、DOCX。当用户说 'PDF转MD'、'转换PDF'、'公式识别'、'图片转LaTeX'、'mathpix'、'读PDF'、'读PPT'、'读Word' 时触发。"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: YonganZhang/everything-to-md-for-agent
# corpus-url: https://github.com/YonganZhang/everything-to-md-for-agent/blob/b0780d92486d5ed2d0db3e46bb22e6a020f9c1f3/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Mathpix API 文档转换

通过 Mathpix API 将 PDF/图片/PPT/Word 转换为 Markdown（含 LaTeX 公式）等格式。

## 自动选择策略

收到"读 PDF/PPT/Word"请求时，按以下规则自动选择方式：

| 文档特征 | 方式 | 原因 |
|---------|------|------|
| 含公式、复杂表格 | **Mathpix 转 MD 后再处理** | 公式/表格识别准确 |
| 纯文字为主、无公式 | **Read 工具直接读** | 免费、更快 |
| 需要理解图表含义（曲线图、流程图） | **Read 工具直接读** | Mathpix 不理解图片语义，Read 可多模态视觉理解 |
| 公式多 + 也有图表需理解 | **Mathpix 转文字部分 + Read 看图** | 组合使用，各取所长 |

判断不确定时，问用户"文档里有公式/复杂表格吗？"再决定。

## 环境变量配置

脚本通过环境变量读取 API 凭证，**不在代码中硬编码**：

```bash
export MATHPIX_APP_ID=your_app_id
export MATHPIX_APP_KEY=your_app_key
# 国内用户需代理
export HTTPS_PROXY=http://127.0.0.1:7890
```

## 功能

| 模式 | 输入 | 输出 | 说明 |
|------|------|------|------|
| PDF 转换 | PDF/DOCX/PPTX | `.mmd` `.md` `.docx` `.tex.zip` `.html` | 异步：上传→等待→下载 |
| 图片识别 | PNG/JPG | LaTeX、纯文本 | 同步返回，公式/手写/表格均可 |

## 使用方式

运行 `scripts/mathpix_convert.py`：

```bash
# PDF → Mathpix Markdown（含 LaTeX 公式，推荐学术文档）
python scripts/mathpix_convert.py input.pdf -f mmd

# PDF → 纯 Markdown
python scripts/mathpix_convert.py input.pdf -f md

# 指定页码范围和输出路径
python scripts/mathpix_convert.py input.pdf -o output.md -f mmd -p "1-5"

# 图片公式识别
python scripts/mathpix_convert.py formula.png -m image

# PDF → Word
python scripts/mathpix_convert.py input.pdf -f docx

# 自定义图片子目录名（默认图片与 .md 同目录）
python scripts/mathpix_convert.py input.pdf -f md --img-dir images
```

## 图片处理

- `--img-dir` 不指定时：图片下载到与 .md 同目录，引用路径为 `fig_01.jpg`
- `--img-dir images` 时：图片下载到 `images/` 子目录，引用路径为 `images/fig_01.jpg`
- 批量转换建议：每篇论文一个文件夹，.md 和图片放一起

## 注意事项

- 默认输出 `.mmd`（Mathpix Markdown），保留 LaTeX 公式源码，适合学术文档
- `.md` 为纯 Markdown，公式渲染为 Unicode，适合非学术场景
- 费用约 $0.005/页（~3.5分/页），新账户有 $29 免费额度（~5800页）
- 文件大小上限 1 GB