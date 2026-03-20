---
name: tencent-cloud-advisor-report-parser
description: 解析腾讯云智能顾问巡检报告邮件。用于处理腾讯云发送的Advisor巡检报告（包括邮件解析、Excel附件下载、风险数据分析），生成结构化风险汇总。
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: fisherhhyu/tencent-cloud-smart-advisor-risk-assessment-report
# corpus-url: https://github.com/fisherhhyu/tencent-cloud-smart-advisor-risk-assessment-report/blob/82fc20393d0861d6529d6d42d90e5e1980930441/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# 腾讯云智能顾问巡检报告解析

## 前置准备

### 1. 订阅巡检报告

在使用此 Skill 之前，需要先在腾讯云智能顾问中订阅巡检报告。具体操作请参考：
[智能顾问巡检报告订阅文档](https://cloud.tencent.com/document/product/1264/73853)

订阅成功后，巡检报告会发送到您配置的邮箱地址。

### 2. 邮箱配置

在 OpenClaw 配置中设置邮箱参数（建议使用环境变量或配置文件）：

```python
# 邮箱配置（请根据实际使用的邮箱填写）
EMAIL_ADDR = os.environ.get('ADVISOR_EMAIL_ADDR')      # 你的邮箱地址
EMAIL_PASSWORD = os.environ.get('ADVISOR_EMAIL_PASSWORD')  # 邮箱授权码/密码
POP3_SERVER = os.environ.get('ADVISOR_POP3_SERVER')    # 邮箱 POP3 服务器地址
```

支持的常见邮箱服务：
- 126 邮箱：pop.126.com
- 163 邮箱：pop.163.com
- QQ 邮箱：pop.qq.com
- Gmail：pop.gmail.com（需启用应用专用密码）

## 使用场景

当用户要求分析腾讯云智能顾问（Tencent Cloud Advisor）巡检报告时使用此 Skill。

## 工作流程

### 1. 邮件接收

使用 POP3 协议连接邮箱，获取巡检报告邮件：

```python
import poplib
import os

p = poplib.POP3(os.environ.get('POP3_SERVER', 'pop.yourmail.com'))
p.user(os.environ.get('EMAIL_ADDR'))
p.pass_(os.environ.get('EMAIL_PASSWORD'))
```

邮件主题包含 "Tencent Cloud Advisor" 或 "智能顾问"。

### 2. 下载 Excel 附件

巡检报告为 Excel 文件 (.xlsx)，包含多个 Sheet：
- Overview - 概览
- COS - 对象存储
- CVM - 云服务器
- CLB - 负载均衡
- CBS - 云硬盘
- CAM - 访问管理
- EdgeOne

### 3. 解析 Excel

Excel 为 xlsx 格式，可用 zipfile 解压后解析 XML：

```python
import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取共享字符串
    with z.open('xl/sharedStrings.xml') as f:
        strings = ET.parse(f).getroot()
    
    # 读取各sheet
    for sheet in ['sheet2.xml', 'sheet3.xml', ...]:
        with z.open(f'xl/worksheets/{sheet}') as f:
            rows = ET.parse(f).getroot()
```

### 4. 风险数据提取

主要字段：
- Type: 风险类型 (Security/Reliability/Cost/Performance)
- Risk Level: 高风险/中风险/无风险
- Assessment Item: 风险项名称
- Resource List: 涉及的资源实例

### 5. 输出报告

生成结构化风险汇总，包含：
- 各服务风险数量统计
- 高风险项详情
- 受影响资源列表

## 脚本位置

解析脚本位于：
```
skills/tencent-cloud-advisor-report-parser/scripts/parse_report.py
```

## 示例输出

```
【COS】
  - 高风险: Referer 防盗链配置
  - 中风险: 日志管理未开启
  - 中风险: 版本控制未开启

总计: 高风险 1 项, 中风险 6 项
```

---

## 统计能力

当用户要求"统计"报告中的风险时，启用此能力。

### 工作流程

1. **统计分析与反馈**
   - 基于已解析的报告内容，按用户要求进行统计（如：按风险等级、按服务类型、按地域等）
   - 将统计结果以清晰的形式反馈给用户

2. **生成网页文件**
   - 使用 HTML 模板生成统计结果的可视化网页
   - 网页文件命名格式：`risk_stats_{timestamp}.html`
   - 网页底部必须添加固定文字：
     > 请访问智能顾问进行云上架构风险治理：https://console.cloud.tencent.com/advisor

3. **截图发送给用户**
   - 使用浏览器工具对生成的网页进行完整截图
   - 将截图发送给用户
   - 询问用户是否需要更多分析统计

### HTML 模板参考

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>风险统计报告</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; background: #f5f5f5; }
        .card { background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
        .stat-item { background: #f8f9fa; padding: 16px; border-radius: 8px; text-align: center; }
        .stat-value { font-size: 32px; font-weight: bold; color: #1a73e8; }
        .stat-label { color: #666; margin-top: 8px; }
        .high-risk { color: #d93025; }
        .medium-risk { color: #f9ab00; }
        .low-risk { color: #1e8e3e; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📊 风险统计报告</h1>
        <div class="stat-grid">
            <!-- 统计项将动态插入 -->
        </div>
    </div>
    <div class="footer">
        请访问智能顾问进行云上架构风险治理：https://console.cloud.tencent.com/advisor
    </div>
</body>
</html>
```

### 关键实现要点

- 统计维度可包括：风险等级（高/中/低）、服务类型（COS/CVM/CLB等）、地域、账号等
- 生成的 HTML 文件保存在 workspace 目录
- 截图时使用浏览器工具的 `screenshot` action，capture entire page
- 截图完成后询问用户："是否需要其他维度的统计分析？"