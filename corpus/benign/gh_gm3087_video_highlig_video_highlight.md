---
name: video-highlight
description: 从视频中自动提取高光片段，支持 AI 语义分析(Whisper+CLIP)和音频节奏分析两种模式。自动检测平台/GPU/Miniconda。
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["bash"],"os":["darwin","linux"]}}}
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: gm3087/video-highlight-extractor
# corpus-url: https://github.com/gm3087/video-highlight-extractor/blob/e327b59524756f83ea16048148683142db04dbdf/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# 视频高光提取

从视频中找出最精彩的片段，裁剪拼接为高光合集。

## 何时使用

用户需要从视频中提取精彩片段、制作预告片、生成视频封面素材时触发。

## 首次安装

运行前必须先检查 `{baseDir}/.venv/bin/python` 是否存在，不存在则执行安装：

```bash
bash {baseDir}/setup.sh all
```

安装脚本自动处理:
- 平台检测 (macOS Apple Silicon/Intel, Ubuntu x86_64/aarch64)
- Miniconda 安装 (ARM 原生，自动检测并替换 x86 版 Anaconda/Miniconda)
- GPU 检测 (NVIDIA CUDA → CUDA 版 PyTorch; Apple MPS → 标准版; 无 GPU → CPU)
- FFmpeg 安装 (Homebrew / apt)
- conda 环境 `video-highlight` (Python 3.11)

首次安装约 5 分钟，包含模型下载。

## 核心命令

```bash
# v10 AI 模式（推荐，Whisper 语音识别 + CLIP 画面评分）
bash {baseDir}/run.sh v10 <视频路径> [参数]

# v9 节奏模式（轻量，纯信号处理，无需 AI 模型）
bash {baseDir}/run.sh v9 <视频路径> [参数]
```

## 参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `-o` | `{输入名}_highlight.mp4` | 输出路径 |
| `-d` | 5 | 片段时长（秒） |
| `-n` | 2 | 提取数量 |
| `--skip-head` | 120 | 跳过片头（秒） |
| `--skip-tail` | 30 | 跳过片尾（秒） |
| `--min-gap` | 30 | 片段最小间隔（秒） |
| `--whisper-model` | tiny | Whisper 模型: tiny/base/small（仅 v10） |
| `--json` | - | JSON 格式输出 |

## 方案选择

| 场景 | 推荐 |
|------|------|
| 有 GPU (CUDA/MPS) | v10 — AI 语义理解，效果最好 |
| 无 GPU / 资源有限 | v9 — 轻量快速，纯信号分析 |
| 节奏感强的内容 | v9 — 音频节拍+运动量检测 |
| 需要语义理解 | v10 — Whisper 内容分类 + CLIP 画面匹配 |

## 护栏

- 绝不修改或删除用户的源视频文件。
- 若 `{baseDir}/.venv/bin/python` 不存在，先执行 `bash {baseDir}/setup.sh all`。
- 命令失败时展示错误信息并停止，不要重试。
- 输出文件默认写在源视频同目录下，不要改变用户未指定的路径。