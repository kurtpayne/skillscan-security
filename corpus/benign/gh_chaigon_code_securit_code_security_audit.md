---
name: code-security-audit
description: >
  对代码项目进行全面安全审计，支持 Python、Node.js、Go、Java 四种语言。
  包含依赖漏洞扫描（结合原生工具 + Claude 分析）、代码安全模式检查（OWASP Top 10、注入、反序列化、
  敏感信息泄露、认证授权、加密问题等）、业务逻辑审计、攻击链构建、配置审计、以及结构化报告输出。
  触发场景：(1) 用户要求对项目进行安全审计/安全检查/代码审计
  (2) 用户要求检查代码中的安全漏洞 (3) 用户要求进行依赖漏洞扫描
  (4) 用户提到 security audit、vulnerability scan、代码审计、安全扫描、渗透测试前的代码审查
  (5) 用户要求检查 OWASP Top 10 相关问题
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: chaigon/code-security-audit-skill
# corpus-url: https://github.com/chaigon/code-security-audit-skill/blob/3e3953a62d0dd3e35585bebd2cc328f7462d9ae5/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# 代码安全审计

对项目执行安全审计，支持三种审计模式以平衡深度与 token 消耗。

## 审计模式选择

触发时先确定审计模式。用户明确指定则使用指定模式，否则默认 **中度**。

| 触发关键词 | 模式 |
|-----------|------|
| "快速扫描"、"quick scan"、"轻度审计"、"light" | 轻度 |
| "安全审计"、"代码审计"、"audit"（默认） | 中度 |
| "深度审计"、"full audit"、"deep"、"渗透测试级" | 深度 |

### 轻度审计（Quick Scan）

目标：快速发现高危问题，最小 token 消耗。

| 阶段 | 执行内容 |
|------|---------|
| Phase 1 | 仅识别语言/框架，不画模块地图和攻击面清单 |
| Phase 2 | 单 Agent，仅搜索 Critical/High 级别模式（每语言 Top 10 高危模式） |
| Phase 3 | 跳过 |
| Phase 4 | 跳过攻击链，仅基本验证（排除明显误报） |
| Phase 5 | 终端简要输出，不生成报告文件 |

不执行多轮审计。不加载 references 文件（使用内置知识）。依赖审计仅运行工具扫描，不做 Claude 分析。

**轻度模式 Top 10 高危模式**（跨语言通用）：
1. `eval(`/`exec(`/`Runtime.exec`/`os.system` — 代码/命令执行
2. `pickle.loads`/`ObjectInputStream`/`yaml.load` — 不安全反序列化
3. SQL 字符串拼接（`"SELECT.*" + `/`Statement`/`${}` in Mybatis）
4. 硬编码密码/密钥（`password\s*=\s*["']`/`secret`/`api_key`）
5. `shell=True`/`child_process.exec` — 命令注入
6. `dangerouslySetInnerHTML`/`innerHTML`/`v-html` — XSS
7. `verify=False`/`InsecureSkipVerify` — TLS 绕过
8. `DEBUG\s*=\s*True`/`NODE_ENV.*development` — 生产环境调试模式
9. `cors.*origin.*\*` — CORS 全开
10. `log4j`/`fastjson` 已知高危版本

### 中度审计（Standard Audit）

目标：覆盖主要安全风险，合理 token 消耗。

| 阶段 | 执行内容 |
|------|---------|
| Phase 1 | 完整信息收集 + 依赖审计（工具 + Claude 分析） |
| Phase 2 | 2-3 个 Agent 并行扫描，覆盖所有 Critical/High/Medium 模式 |
| Phase 3 | 仅审计 P0 文件（认证链 + 未认证端点 + 核心 Sink 聚合点） |
| Phase 4 | 基本验证（四步法），不构建攻击链 |
| Phase 5 | 完整报告（无攻击链章节） |

单轮审计。按需加载 vulnerability_rules.md 中对应语言章节。

### 深度审计（Full Audit）

目标：最大化发现率，适合安全评审和渗透测试前审查。

执行完整五阶段流程 + 多轮审计策略 + 攻击链构建。即下文描述的全部内容。

---

## 审计哲学

### 核心分析模型

所有安全漏洞的本质：**不可信的数据到达了危险的操作**。

```
Source（源）      用户可控的输入入口
     ↓
Propagation（传播） 数据流经的函数、过滤、转换
     ↓
Sink（汇）        SQL执行、命令执行、文件读写等危险操作
```

审计的三个核心动作：
1. 找到所有 Source（识别攻击面）
2. 追踪 Propagation（验证中间是否有有效过滤）
3. 确认是否有未过滤的路径到达 Sink（漏洞判定）

### 优先级排序

```
优先级 = (攻击面大小 × 潜在影响) / 利用复杂度
```

| 维度 | 高权重 | 低权重 |
|------|-------|-------|
| 攻击面 | 未认证可达 | 内部接口 |
| 潜在影响 | RCE、全库读取 | 信息收集 |
| 利用复杂度 | 单请求触发 | 需物理接触 |

**第一条决策原则：永远优先审计认证链。** 认证绕过能把所有需认证才能触发的漏洞升级为未认证漏洞。

## 五阶段审计流程

### Phase 1: 信息收集与攻击面识别（10% 精力）

此阶段**不搜漏洞**，只产出四样东西：

**1. 技术栈画像**
- 检测语言标识文件：Python (`requirements.txt`等), Node.js (`package.json`等), Go (`go.mod`), Java (`pom.xml`等)
- 识别框架（Django/Flask/FastAPI, Express/Koa/Next.js, Gin/Echo, Spring/Mybatis）
- 识别数据库、中间件、模板引擎

**2. 模块地图**
- 扫描目录结构，识别路由层、控制器层、服务层、数据访问层
- 标注各模块的职责和依赖关系

**3. 攻击面清单**
- 列出所有 API 端点（HTTP 方法、路径、认证状态）
- 标记未认证端点、GET 写操作、管理端点（admin/metrics/swagger/actuator）
- 识别所有外部入口（API、WebSocket、消息队列、定时任务）和出口（HTTP 出站、邮件、文件写入）

**4. 安全机制**
- 识别认证方案（JWT/Session/OAuth）、授权中间件、CSRF 保护
- 识别输入校验方式、输出编码、加密方案

**依赖审计**也在此阶段执行：
- 运行 `scripts/dep_audit.sh` 或 `scripts/dep_audit_java.sh`（工具不可用则跳过）
- 读取依赖清单，分析已知高危版本、废弃包、typosquatting、宽泛版本范围

> 后续所有 Agent 的方向、搜索模式、优先级排序，全部基于这张地图推导。没有地图就没有方向。

### Phase 2: 并行模式匹配扫描（30% 精力）

**Agent 决策链**：

```
Phase 1 攻击面清单 → 推导审计方向 → 按"可并行 + 不重叠"切分 Agent → 执行
```

**核心原则：Agent 的方向由攻击面决定，不是固定模板。** 项目没有文件上传就不设文件操作 Agent。

**切分约束**：
- 约束 1：搜索模式互不重叠，每个 Agent 有独占的 Grep 模式集
- 约束 2：可完全并行执行，Agent 之间零依赖

**典型 Agent 映射**（根据 Phase 1 发现动态调整）：

| 探测发现 | 审计方向 | Agent 任务 |
|---------|---------|-----------|
| Web 框架 + REST API | 认证/授权链 | Agent: 认证与授权 |
| 数据库连接 | SQL/NoSQL 注入 | Agent: 注入 |
| 文件上传 + HTTP 出站 | SSRF + 文件操作 | Agent: 文件/SSRF |
| 模板引擎/eval/exec | XSS/SSTI/RCE | Agent: 代码执行 |
| 业务交易逻辑 | IDOR/数值/竞态 | Agent: 业务逻辑 |

**Agent 数量**：小型项目 2-3 个，中型 3-5 个，大型 5-9 个。

按语言加载对应规则，参考 [references/vulnerability_rules.md](references/vulnerability_rules.md)。

核心检查项：
- **注入**: SQL注入、命令注入、LDAP注入、模板注入(SSTI)、XSS
- **NoSQL注入**: MongoDB `$where` 拼接、操作符注入(`$gt`/`$ne`/`$regex`)
- **反序列化**: pickle/yaml/ObjectInputStream/Fastjson 不安全反序列化
- **认证授权**: 硬编码凭证、JWT 配置、Session 管理、越权风险
- **加密**: 弱算法(MD5/SHA1/DES)、硬编码密钥、不安全随机数
- **敏感信息**: API Key/密码/Token 硬编码、日志泄露、错误信息泄露
- **文件操作**: 路径遍历、不受限的文件上传
- **SSRF/XXE**: 不受限的 URL 请求、XML 外部实体
- **前端安全**: `innerHTML`/`dangerouslySetInnerHTML`/`bypassSecurityTrust*`、前端路由泄露、前端硬编码凭据
- **业务逻辑**: IDOR、Mass Assignment、数值校验缺失、竞态条件、CSRF、反自动化
- **原型污染** (Node.js) / **Log4Shell** (Java)
- **供应链**: typosquatting、废弃包、可疑依赖来源

> Phase 2 的核心产出是"高风险区域地图"，不是最终漏洞清单。发现率 30-50% 是正常的。

### Phase 3: 关键路径深度审计（40% 精力）

对 Phase 2 标记的高风险文件做逐行审计。文件优先级排序：

| 优先级 | 文件类型 | 决策依据 |
|-------|---------|---------|
| P0 | 认证过滤器 / Token 处理 | 认证绕过影响全系统 |
| P0 | 未认证可达的接口 | 直接暴露的攻击面 |
| P0 | Sink 最密集的核心业务入口 | 漏洞密度最高 |
| P1 | 文件上传下载 / HTTP 出站工具类 | 路径遍历、SSRF |
| P2 | 配置类、加密工具类 | 配置缺陷、密钥管理 |

**逐行审计逻辑**：

```
对每个 P0/P1 文件:
  1. 读取完整结构（字段、方法列表）
  2. 从 public 方法开始，追踪每个参数的数据流
  3. 对每个分支判断:
     ├── 参数是否经过验证/过滤？→ 检查验证逻辑完整性
     ├── 参数是否到达 Sink？    → 记录完整路径
     └── 是否有绕过过滤的路径？ → 分析边界条件
  4. 记录: 文件 → 行号 → 漏洞类型 → 完整数据流路径
```

**关键决策：优先审计 Sink 聚合点。** 如果项目有统一的 HTTP 出站工具类，审计这一个文件就覆盖所有 SSRF 风险。

**配置审计**也在此阶段执行：
- DEBUG/开发模式、CORS 配置、安全 HTTP 头、数据库明文密码
- TLS/SSL 配置、Docker/K8s 安全（特权容器、root 运行）
- `.env` 文件是否被 `.gitignore` 排除
- Swagger/Actuator 等管理端点暴露

### Phase 4: 漏洞验证与攻击链构建（15% 精力）

**验证四步法** — 每个疑似漏洞必须过四关：

| 步骤 | 验证项 | 判定标准 |
|-----|-------|---------|
| 1 | 数据流完整性 | Source 到 Sink 中间无截断过滤 |
| 2 | 防护可绕过性 | 安全检查是否有遗漏的边界条件 |
| 3 | 前置条件可满足性 | 攻击者能否到达漏洞触发点 |
| 4 | 影响范围 | 利用后最大损害（RCE？数据泄露？提权？） |

四步全过 → 确认漏洞。任一步不过 → 降级或排除。

**攻击链构建**：

```
对每个 Critical/High 漏洞:
  1. 确认前置条件（需要认证？什么权限？什么网络位置？）
  2. 如果需要认证 → 检查是否有认证绕过可串联
  3. 确认利用结果（信息泄露？代码执行？权限提升？）
  4. 检查结果能否作为下一个漏洞的输入
  5. 组合为完整攻击链，评估整体影响
```

典型攻击链模式参考 [references/vulnerability_rules.md](references/vulnerability_rules.md) 中的攻击链模式章节。

**等级影响规则**：漏洞 A（认证绕过）消除漏洞 B 的认证前置条件 → B 按"未认证可达"重新评估。编号等级 = 独立等级，攻击链部分 = 组合等级。

### Phase 5: 报告输出（5% 精力）

参考 [references/report_template.md](references/report_template.md) 输出。

报告包含：
1. 审计摘要（各严重程度的发现数量）
2. 攻击面地图（端点清单、认证状态）
3. 漏洞详情（位置、代码片段、**完整数据流路径**、修复建议、CWE 编号）
4. 攻击链分析（漏洞组合路径、整体影响）
5. 依赖审计结果
6. 配置审计结果
7. 修复优先级建议

## 多轮审计策略

单轮审计漏报率可达 50-60%。多轮审计每轮执行不同类型的分析：

| 轮次 | 目标函数 | 方法 | 发现类型 |
|-----|---------|------|---------|
| 第一轮 | max(覆盖面) | 模式匹配（Grep + 并行 Agent） | 表面可见：硬编码、未验证、配置缺陷 |
| 第二轮 | max(深度) | 数据流追踪（逐行 Read） | 隐藏在数据流中：拼接链、协议注入、权限缺失 |
| 第三轮 | max(关联度) | 跨模块交叉验证 | 组合才危险：IDOR+白名单、加密体系缺陷 |

### 轮次终止规则

每轮结束后，强制回答三个问题：

1. **有没有计划搜索但没搜到的区域？** YES → 需要下一轮（补盲区）
2. **发现的入口点是否都追踪到了 Sink？** NO → 需要下一轮（追数据流）
3. **高风险发现之间是否可能存在跨模块关联？** YES → 需要下一轮（交叉验证）

三个问题的答案全部为 NO → 终止。任一为 YES → 继续。

### 轮次规模参考

| 项目规模 | 典型轮次 | Agent 总数 |
|---------|---------|-----------|
| 小型（<10K LOC） | 1 轮 | 2-3 个 |
| 中型（10K-50K） | 1-2 轮 | 3-5 个 |
| 大型（50K-200K） | 2-3 轮 | 5-9 个 |
| 超大型（>200K） | 2-4 轮 | 8-15 个 |

## 严重等级判定

三维决策模型：`严重等级 = f(可达性, 影响范围, 利用复杂度)`

```
                漏洞发现
                   │
           未认证可达？
             ╱        ╲
           YES         NO
           ╱             ╲
   RCE/全库读取？    RCE/全库读取？
     ╱     ╲         ╱     ╲
   YES     NO      YES     NO
    │       │       │       │
 Critical   │     High   Medium/Low
         广范围数据
         泄露/篡改？
          ╱    ╲
        YES    NO
         │      │
       High   Medium
```

编号体系：`C-001` (Critical 9.0-10.0), `H-001` (High 7.0-8.9), `M-001` (Medium 4.0-6.9), `L-001` (Low 0.1-3.9)

排序策略：影响最广排最前 → 攻击链根漏洞优先 → 同模块漏洞相邻。

攻击链对等级的影响：
- 编号等级 = 独立等级（假设攻击者无其他漏洞）
- 攻击链部分 = 组合等级
- 修复链中一环不影响剩余漏洞的独立评级

## 误报处理

确认漏洞前必须验证：
- 危险函数的输入是否来自用户可控数据
- 是否存在上游的输入校验/转义/参数化
- 是否在测试代码中（测试代码中的 `eval` 通常不是漏洞）
- 框架是否已内置防护（如 Django ORM 默认参数化）

标记为 "可能的误报" 而非直接忽略，让用户自行判断。

## 快速参考

依赖审计脚本：
- 通用: `scripts/dep_audit.sh <项目目录> [python|node|go|auto]`
- Java: `scripts/dep_audit_java.sh <项目目录>`

漏洞规则详情: `references/vulnerability_rules.md`
报告模板: `references/report_template.md`