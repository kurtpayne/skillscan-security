---
name: xiaohongshu-publish
description: 使用 OpenClaw 浏览器发布小红书笔记（图文/视频）。当用户需要发布小红书笔记时使用此 skill，包括：发布图文笔记、发布视频笔记、批量发布多篇笔记。
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: zangqilong198812/openclaw-xiaohongshu-publish-skill
# corpus-url: https://github.com/zangqilong198812/openclaw-xiaohongshu-publish-skill/blob/ba6182567624a6f7ecbb875bf3bfb514ce946e54/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# 小红书发布 Skill

## 使用前提

1. **账号文件夹**：`~/xiaohongshu-<账号名>/`
   - `account.md` - 账号信息
   - `resource.md` - 素材列表
   - `resources/` - 素材文件目录
2. **用户已登录小红书**

## 首次登录

```bash
openclaw browser --browser-profile openclaw open https://www.xiaohongshu.com/
```

## 账号文件夹结构

创建 `~/xiaohongshu-<账号名>/`，例如 `~/xiaohongshu-meizhuang/`：

```
~/xiaohongshu-meizhuang/
├── account.md
├── resource.md
└── resources/
    ├── img1.jpg
    ├── img2.jpg
    └── video1.mp4
```

### account.md 模板

```markdown
# 账号信息

## 账号定位
美妆博主

## 目标受众
年轻女性

## 内容风格
温柔亲切

## 产品/服务
[描述]

## 其他要求
- 禁止：xxx
- 必须：xxx
```

### resource.md 模板

```markdown
# 素材列表

## 素材1
- 类型：图文
- 文件：img1.jpg
- 描述：xxx

## 素材2
- 类型：视频
- 文件：video1.mp4
- 描述：xxx
```

## 发布流程

### Step 1: 询问账号

问用户要发布到哪个账号（哪个文件夹）

### Step 2: 读取账号信息

读取 `~/xiaohongshu-<账号名>/account.md`

### Step 3: 读取素材信息

读取 `~/xiaohongshu-<账号名>/resource.md`，让用户选择要发布的素材

### Step 4: AI 生成文案

生成标题（≤20字）、正文、话题，提交用户确认

### Step 5: 打开发布页

```bash
openclaw browser --browser-profile openclaw open https://creator.xiaohongshu.com/publish/publish
```

### Step 6: 上传内容

1. `openclaw browser --browser-profile openclaw snapshot`
2. `openclaw browser --browser-profile openclaw click <ref>`
3. `openclaw browser --browser-profile openclaw upload ~/xiaohongshu-<账号名>/resources/<filename>`

### Step 7: 填写文案

`openclaw browser --browser-profile openclaw type <ref> "文案"`

### Step 8: 发布

### Step 9: 记录历史

更新 `~/xiaohongshu-<账号名>/history.md`

## 注意

- 标题 ≤20 字
- 视频上传慢
- 验证码用户手动处理