---
name: douyin-pusher
description: >
  AI 视频生成与社交媒体自动化发布技能。支持通过 OpenAI Sora 2、火山引擎 Seedance 2.0、即梦AI视频生成3.0 生成高质量视频，并利用 PinchTab 自动发布到抖音创作者中心。
  使用触发词："生成视频"、"生成短剧"、"发布视频"、"登录抖音"。
  支持：(1) 文生视频，(2) 图生视频，(3) 短剧生成（多 Agent 协作），(4) 视频自动发布到抖音，(5) 评论自动回复。
metadata:
  openclaw:
    homepage: https://github.com/Boos4721/douyin-pusher
    init: "pip3 install requests volcengine openai python-dotenv --break-system-packages && curl -fsSL https://pinchtab.com/install.sh | bash"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Boos4721/douyin-pusher
# corpus-url: https://github.com/Boos4721/douyin-pusher/blob/09e62b431119246507fa755582db6fe8f36ea7f8/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Douyin Pusher Skill

AI 视频生成与社交媒体自动化发布技能。集成火山引擎 Seedance / 即梦AI / Atlas Sora 与 PinchTab 浏览器控制引擎。

## 🚀 功能
- **视频生成**：调用 **火山引擎 Ark (Seedance 2.0)**、**即梦AI 3.0** 或 **Atlas Cloud Sora** 生成视频（支持文生视频与图生视频）。
- **短剧生成**：6 Agent 协作（ShowRunner → Writer → Shot Designer → Prompt Engineer → Generator → Editor → Finalizer）
- **自动发布**：驱动 `pinchtab` 命令将生成的视频发布到抖音（Douyin）创作者中心。
- **评论管理**：自动获取评论并支持自动回复。
- **定时任务**：支持定时发布视频。
- **任务流水线**：从生成、状态轮询到文件下载与上传的全流程自动化。

## 📁 目录结构
```
scripts/
├── agent.py          # OpenClaw 智能代理入口
├── cli.py            # 命令行工具入口
├── storage.py        # 数据持久化（Cookie、任务、评论）
├── video/
│   ├── generator.py  # 统一视频生成器入口
│   ├── jimeng.py     # 即梦AI 3.0 生成器
│   ├── volc.py       # 火山引擎 Seedance 生成器
│   ├── atlas.py      # Atlas Cloud Sora 生成器
│   ├── optimizer.py  # 提示词优化器
│   ├── scheduler.py  # 定时任务调度
│   └── moviegen/     # 短剧生成模块
│       ├── main.py       # 主入口
│       ├── showrunner.py # 剧情规划
│       ├── writer.py     # 编剧
│       ├── shot.py       # 镜头设计
│       ├── prompt.py     # 提示词优化
│       ├── generator.py  # 视频生成
│       ├── editor.py     # 视频剪辑
│       └── finalizer.py  # 最终处理
├── douyin/
│   ├── login.py      # 抖音扫码登录
│   ├── publish.py    # 视频发布
│   ├── comment.py    # 评论管理 + 自动回复
│   └── selector.py   # 页面元素选择器
```

## 🛠️ 配置要求
- **火山引擎 Ark (Seedance)**: `VOLC_API_KEY` (API 密钥) 及 `VOLC_MODEL_ENDPOINT` (推理终端 ID)。
- **即梦AI**: `VOLC_ACCESSKEY` (AK) 及 `VOLC_SECRETKEY` (SK)。
- **Atlas Cloud Sora**: `ATLAS_API_KEY` (API 密钥)
- **OpenAI (短剧生成)**: `OPENAI_API_KEY`
- 登录状态：如果系统尚未登录抖音，Agent 需要访问创作者中心，获取登录二维码的截图并回传给用户，等待用户扫码完成后再执行后续发布。PinchTab 会持久化保存 profile。

## 🎯 使用方法

### CLI 命令
```bash
# 生成视频
python scripts/cli.py gen "视频提示词" -m jimeng-pro -d 5 -o output.mp4

# 生成短剧
python scripts/cli.py movie "短剧内容" -s 电影 -n 6

# 发布视频
python scripts/cli.py publish video.mp4 -t "视频标题"

# 登录抖音
python scripts/cli.py login --check

# 定时发布
python scripts/cli.py schedule video.mp4 "2024-01-01 12:00"
python scripts/cli.py schedule --list

# 查看任务
python scripts/cli.py tasks

# 查看评论
python scripts/cli.py comments

# 开启自动回复
python scripts/cli.py auto-reply --enable
```

### 自然语言命令 (agent.py)
```bash
# 交互模式
python scripts/agent.py -i

# 单次执行
python scripts/agent.py "生成视频: 赛博朋克城市"
python scripts/agent.py "生成短剧: 风格 科幻 内容 未来世界"
python scripts/agent.py "发布视频: output.mp4"
python scripts/agent.py "登录抖音"
python scripts/agent.py "定时发布: video.mp4 时间: 2024-01-01 12:00"
python scripts/agent.py "查看定时任务"
python scripts/agent.py "开启自动回复"
python scripts/agent.py "查看评论"
```

### Python API
```python
from video.generator import VideoGenerator

# 初始化生成器
gen = VideoGenerator(model="auto")  # 自动选择最佳模型
# 或指定模型: jimeng-pro, jimeng-720p, jimeng-1080p, seedance, sora

# 生成视频
task_id = gen.generate(prompt="提示词", image="可选图片路径", duration=5)
video_url = gen.poll(task_id)
local_path = gen.download(video_url, "output.mp4")

# 一键生成+下载
path = gen.generate_and_download(
    prompt="提示词",
    image="图片路径或URL",  # 可选
    duration=5,
    output="output.mp4"
)
```

### 短剧生成
```python
from video.moviegen import MovieGenerator

gen = MovieGenerator()
result = gen.generate(
    content="短剧内容描述",
    style="电影",  # 风格
    num_shots=6,   # 镜头数
    output_dir="output/movie"
)
```

## 📝 核心规则 (Rules)
1. **模型选择**：
   - 用户可用自然语言指定模型（如"用即梦3.0"、"用豆包Seedance"、"用Sora"等）。如果用户没有指定，默认使用"即梦AI 3.0 Pro"。
   - 在执行生成任务前，检查对话历史中是否已经提供了对应的 API 凭证。如果对话中已经有 API Key 或 AK/SK，请直接提取并在代码中传入，**不要**再向用户询问。只有在对话历史和环境变量中都找不到所需凭证时，才向用户索要。
2. **多模态适配**：
   - 如果用户随消息上传了图片附件，Agent 需要读取该图片的本地路径，并将此路径传入生成脚本，从而触发图生视频逻辑。
3. **视频发布**：
   - 生成成功并下载后，自动调用 `pinchtab` 命令行执行上传与发布指令。
4. **超时与重试**：
   - 默认超时 900 秒，自动处理异步状态轮询。

## 📖 使用示例
- "生成视频: 赛博朋克风格的城市夜景"
- "生成短剧: 风格 科幻 内容 未来世界的冒险故事"
- "用这张图片作为首帧生成无人机飞行视频"
- "发布视频: output.mp4 标题: AI 浪潮"
- "登录抖音"
- "定时发布: video.mp4 时间: 明天上午10点"
- "开启自动回复"

## 🤝 鸣谢
- 流程参考 [social-push](https://github.com/jihe520/social-push)
- 理念参考 [page-agent](https://github.com/alibaba/page-agent)