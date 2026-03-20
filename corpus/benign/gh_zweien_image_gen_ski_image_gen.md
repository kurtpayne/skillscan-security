---
name: image-gen
description: |
  Nano-banana 图像生成与编辑 Skill。支持文生图和图生图，根据文字描述或参考图使用 AI 生成/编辑图像，自动压缩大图，保存到 workspace/img 目录，并直接在飞书中展示。
  触发场景：用户要求生成图片、画图、AI 绘图、创建图像、修改图片、基于图片生成、图生图。
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: zweien/image-gen-skill
# corpus-url: https://github.com/zweien/image-gen-skill/blob/1c91e23861860e18d49d7cc7d7eaf7158b3eb7ab/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Nano-banana 图像生成与编辑 Skill

使用 Nano-banana-3.1-Flash API 进行图像生成与编辑，支持：
- **文生图 (text-to-image)**: 根据文字描述生成图像
- **图生图 (image-to-image)**: 基于参考图生成新图像

自动压缩超过 1MB 的图片，保存到 workspace，并直接在飞书中展示。

## 配置

在workspace目录下创建 `.env` 文件：

```bash
# .env
IMAGE_API_BASE_URL=https://api.imyaigc.top
IMAGE_API_KEY=your-api-key-here
IMAGE_MODEL=gemini-3.1-flash-image-preview
IMAGE_SIZE=2K
IMAGE_ASPECT_RATIO=1:1
```

## 图片保存位置

所有生成的图片保存在：
```
~/.openclaw/workspace/img/
```

文件名格式：`image_YYYYMMDD_HHMMSS.png`

**压缩规则：**
- 原始图片保存为：`image_YYYYMMDD_HHMMSS_original.png`
- 如果原图 > 1MB，自动压缩并保存为：`image_YYYYMMDD_HHMMSS.png`
- 发送到时使用压缩后的版本

## 使用方法

### 1. 文生图 (Text-to-Image)

直接告诉我要生成什么图片：

示例：
- "生成一张夕阳下的海滩图片"
- "画一只可爱的猫咪"
- "创建一个赛博朋克风格的大龙虾，16:9 比例"

### 2. 图生图 (Image-to-Image)

提供参考图和修改描述：

示例：
- "基于这张图，改成水彩风格"
- "把这张图改成夜景"
- "参考这张图，生成一个类似风格的建筑"
- "把这张照片变成油画风格"

**工作流程：**
1. 用户提供参考图（发送图片）
2. 下载图片并转为 base64
3. 调用 API 时传入 `image` 参数
4. 返回基于参考图生成的新图像

## 工作流程

### 文生图流程

1. **解析参数**
   - 提取提示词
   - 识别宽高比参数（如 "16:9"、"1:1"）

2. **调用 API**
   ```bash
   curl -X POST "${IMAGE_API_BASE_URL}/v1/images/generations" \
       -H "Authorization: Bearer ${IMAGE_API_KEY}" \
       -H "Content-Type: application/json" \
       -d '{
           "model": "'"${IMAGE_MODEL}"'",
           "prompt": "描述内容",
           "response_format": "url",
           "aspect_ratio": "16:9"
       }'
   ```

### 图生图流程

1. **获取参考图**
   - 用户发送图片
   - 下载图片并转为 base64

2. **调用 API**
   ```bash
   curl -X POST "${IMAGE_API_BASE_URL}/v1/images/generations" \
       -H "Authorization: Bearer ${IMAGE_API_KEY}" \
       -H "Content-Type: application/json" \
       -d '{
           "model": "'"${IMAGE_MODEL}"'",
           "prompt": "修改描述（如：改为水彩风格）",
           "response_format": "url",
           "aspect_ratio": "16:9",
           "image": ["data:image/png;base64,iVBORw0KGgo..."]
       }'
   ```

3. **获取图片 URL**
   - 从响应中提取 `data[0].url`

4. **下载并保存原始图片**
   ```bash
   OUTPUT_DIR=~/.openclaw/workspace/img
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   ORIGINAL_FILE="${OUTPUT_DIR}/image_${TIMESTAMP}_original.png"
   FINAL_FILE="${OUTPUT_DIR}/image_${TIMESTAMP}.png"

   curl -o "$ORIGINAL_FILE" "$IMAGE_URL"
   ```

5. **检查大小并压缩（如需要）**
   ```bash
   FILE_SIZE=$(stat -f%z "$ORIGINAL_FILE" 2>/dev/null || stat -c%s "$ORIGINAL_FILE")
   MAX_SIZE=$((1024 * 1024))  # 1MB

   if [ "$FILE_SIZE" -gt "$MAX_SIZE" ]; then
       echo "图片超过 1MB，正在压缩..."
       python3 compress_image.py "$ORIGINAL_FILE" "$FINAL_FILE" 1
   else
       cp "$ORIGINAL_FILE" "$FINAL_FILE"
   fi
   ```

6. **发送到飞书**
如果在飞书对话中，注意以下发送方式
   ```
   message(
     action="send",
     channel="feishu",
     accountId="second",
     target="用户或群组ID",
     media="~/.openclaw/workspace/img/image_xxx.png"
   )
   ```

## 压缩工具

使用 `compress_image.py` 进行图片压缩：

```bash
# 用法
python3 compress_image.py <input> <output> [max_size_mb]

# 示例
python3 compress_image.py original.png compressed.png 1
```

**压缩策略：**
1. 如果图片 ≤ 1MB，不压缩
2. 如果图片 > 1MB：
   - 逐步降低 JPEG 质量 (85 → 10)
   - 如果仍超过限制，缩小尺寸 (90% → 30%)
3. 保留原始文件，压缩结果另存

## 支持的参数

### 宽高比 (aspect_ratio)
- `1:1` - 正方形（默认）
- `4:3`, `3:4` - 标准比例
- `16:9`, `9:16` - 宽屏/竖屏
- `2:3`, `3:2` - 照片比例
- `4:5`, `5:4` - 接近正方形
- `21:9` - 超宽屏
- `1:4`, `4:1` - 长条形
- `8:1`, `1:8` - 超长条形

### 图像尺寸 (image_size)
- `1K` - 适合快速预览
- `2K` - 推荐默认（默认）
- `4K` - 高清大图
- `512px` - 小图

### 参考图 (image)
- 类型：字符串数组
- 格式：URL 或 base64 编码（推荐 `data:image/png;base64,...` 格式）
- 支持：单张或多张参考图

## API 信息

- **Endpoint:** `POST /v1/images/generations`
- **认证:** `Authorization: Bearer {{YOUR_API_KEY}}`
- **模型:** `${IMAGE_MODEL}` (默认: `gemini-3.1-flash-image-preview`)
- **Base URL:** `https://api.imyaigc.top`

### 完整请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | ✅ | 模型名称 |
| prompt | string | ✅ | 生成描述 |
| response_format | string | ❌ | `url` 或 `b64_json` |
| aspect_ratio | string | ❌ | 宽高比 |
| image | array | ❌ | 参考图数组（URL 或 base64） |
| image_size | string | ❌ | 图像尺寸（仅 nano-banana-2 支持） |

## 目录结构

```
~/.openclaw/workspace/
├── img/                          # 生成的图片保存目录
│   ├── image_20260302_221900_original.png  # 原始图片
│   ├── image_20260302_221900.png           # 压缩后（用于发送）
│   └── ...
└── skills/
    └── image-gen/
        ├── SKILL.md              # 本说明文件
        ├── image-gen.sh          # 生成脚本
        ├── compress_image.py     # 压缩工具
        ├── .env                  # API 配置
        └── .env.example          # 配置示例
```

## 注意事项

1. 图片**必须**保存在 `~/.openclaw/workspace/img/` 目录
2. 超过 1MB 的图片会自动压缩后再发送到飞书
3. 原始图片保留，方便后续使用
4. 文件名使用时间戳避免冲突
5. 提示词会自动翻译为英文以获得更好的生成效果
6. API 调用可能需要 30-60 秒，请告知用户等待
7. **图生图时**：参考图会转为 base64 传入 API 的 `image` 参数