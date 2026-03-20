---
name: hile-monorepo
description: "引导 AI 在本仓库或使用 Hile 的项目中，正确选用并遵守各 Hile 模块的约束与用法。编辑/生成涉及 @hile/* 或 create-hile 的代码时必读。"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: cevio/hile
# corpus-url: https://github.com/cevio/hile/blob/de770121768d0aab3babf3544205b806176f9009/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Hile monorepo — AI 编程约束

本文档面向 AI 编码模型：在**本仓库**或**使用 Hile 的应用项目**中生成或修改代码时，必须按本 SKILL 选用模块并遵守各包约束，确保与 Hile 架构一致。

---

## 1. 何时必须遵守本 SKILL

- 编辑或新增的代码**引用**了任意 `@hile/*` 或 `create-hile`
- 编辑或新增 **`*.boot.ts` / `*.boot.js`**、**`*.controller.ts`**、或 **Hile 服务**（`defineService` / `loadService`）
- 修改 **`packages/*`** 下任意子包源码时，除本 SKILL 外**必须同时阅读并遵守**该包目录下的 **`SKILL.md`**

---

## 2. 包与职责速查（选对模块）

| 场景 | 使用包 | 说明 |
|------|--------|------|
| 定义/加载异步服务、生命周期、依赖图、优雅关闭 | `@hile/core` | 基础容器，所有依赖容器的包都基于它 |
| 启动应用、扫描 boot、容器事件日志、退出钩子 | `@hile/cli` | 与 core 配合，入口为 `hile start` |
| HTTP API：Koa、路由、中间件、文件系统路由 | `@hile/http` | 与 core 集成时在 defineService 内 new Http、load、listen、shutdown(close) |
| API + Next.js SSR 同端口 | `@hile/http-next` | 基于 http，控制器前缀固定 `/-`，控制器在 `src/app/*.controller.ts` |
| TypeORM DataSource、事务与补偿回调 | `@hile/typeorm` | 默认导出为 Hile 服务，配合 `auto_load_packages` 或 boot 中 loadService |
| Redis 客户端、环境变量配置、优雅断连 | `@hile/ioredis` | 同上，环境变量 `REDIS_*` |
| 传输无关的请求/响应消息抽象（超时、中止、错误透传） | `@hile/message-modem` | 独立于 core，实现类需实现 `post` / `exec` |
| Node 父子进程 IPC 请求/响应 | `@hile/message-ipc` | 基于 message-modem |
| 主线程与 Worker 线程请求/响应 | `@hile/message-worker-thread` | 基于 message-modem |
| WebSocket 请求/响应 | `@hile/message-ws` | 基于 message-modem + ws |
| 按目录映射消息路由（`*.msg.ts`）、与 message-* 搭配 | `@hile/message-loader` | 独立于 core，`MessageLoader` + `defineMessage` |
| 一键创建 Hile + Next.js 项目 | `create-hile` | `npx create-hile create <name>` |

**依赖关系**：core ← cli / typeorm / ioredis；http ← http-next。message-modem ← message-ipc / message-worker-thread / message-ws。message-loader 可单独与任意 message 传输层搭配。

---

## 3. 跨包强约束（必须遵守）

以下约束适用于所有使用 `@hile/core`、`@hile/cli`、`@hile/http` 的代码。

### 3.1 服务定义与加载（@hile/core）

- 服务**必须**用 `defineService(async (shutdown) => { ... })` 定义，参数名建议为 `shutdown`。
- **禁止**在模块顶层写 `const x = await loadService(...)`；只在**函数/服务内部**或 boot 内按需 `loadService`。
- 创建外部资源（连接、服务器、定时器等）后**必须**立即 `shutdown(() => ...)` 注册清理；清理顺序为 LIFO。
- 获取实例**只能**通过 `loadService(service)` 或 `container.resolve(service)`，禁止手造 `{ id, fn }` 等假服务对象。

### 3.2 Boot 与启动（@hile/cli）

- Boot 文件**必须**命名为 `*.boot.ts` 或 `*.boot.js`，且 **`export default`** 为 `defineService(...)` 或 `container.register(...)` 的返回值。
- `package.json` 中的 **`hile.auto_load_packages`** 仅允许**模块名**（如 `@hile/typeorm`），禁止文件路径。
- 加载顺序固定：先 `auto_load_packages`，再扫描运行目录下的 `*.boot.{ts,js}`。运行目录：`HILE_RUNTIME_DIR` > `--dev` 时 `src/` > 否则 `dist/`。

### 3.3 HTTP 与控制器（@hile/http / @hile/http-next）

- 与 core 集成时：在 **defineService** 内创建 **Http** / **HttpNext**，在 **listen() 之前**完成 `use`、`load`，**listen()** 返回的关闭函数必须传给 **shutdown(close)**。
- 控制器**必须**用 **defineController(method, fn)** 或 **defineController(method, [middlewares], fn)**，文件 **export default** 单个控制器或数组；控制器函数签名为 **(ctx)**，不要 **(ctx, next)**。
- 使用 **@hile/http-next** 时：API 路由前缀**必须**为 **`/-`**；控制器文件放在 **`src/app/`** 下，命名为 **`*.controller.ts`**。

### 3.4 数据库与缓存（@hile/typeorm / @hile/ioredis）

- 通过 **loadService(typeormService)** / **loadService(ioredisService)** 获取实例；需在应用启动时即加载时，在 **`hile.auto_load_packages`** 中加入 **`@hile/typeorm`** / **`@hile/ioredis`**。
- TypeORM 事务与补偿使用 **transaction(ds, async (runner, rollback) => { ... })**，禁止在事务外混用 runner 或忽略 rollback 注册。

---

## 4. 按场景的代码导向

- **新建一个“可运行的服务入口”**  
  → 在运行目录（如 `src/`）下新增 **`*.boot.ts`**，**export default defineService(async (shutdown) => { ... })**，其中创建 Http/HttpNext 或其它资源并 **shutdown(close)**。用 **`hile start --dev`** 加载。

- **新增 HTTP API 路由**  
  → 使用 **defineController** 的 **`*.controller.ts`**，放在 **http.load()** 所加载的目录下（如 `src/controllers/` 或 http-next 的 `src/app/`）；**不要**在控制器里写 **ctx.body = ... 再 return**，只 **return** 结果，由响应插件链写 **ctx.body**。

- **API + 页面同端口（Next.js）**  
  → 使用 **@hile/http-next**，在 boot 中 **new HttpNext({ port, cwd, publicPath })**，**shutdown(await httpNext.start())**；API 仅 **`/-`** 前缀，页面用 Next 约定文件（如 **page.tsx**）。

- **使用数据库/Redis**  
  → 在 **package.json** 的 **hile.auto_load_packages** 中加入 **@hile/typeorm** / **@hile/ioredis**，在控制器或其它服务**内部** **await loadService(typeormService)** 或 **loadService(ioredisService)**；环境变量按各包 README/SKILL 配置。

- **消息通信（IPC/Worker/WS）+ 文件系统路由**  
  → 用 **@hile/message-loader** 的 **MessageLoader** 与 **defineMessage** 做路由表，在 **@hile/message-ipc** / **message-worker-thread** / **message-ws** 子类的 **exec** 中调用 **loader.dispatch(url, data)**。

---

## 5. 各包 SKILL 的引用规则

在**修改或生成**下列目录/包内代码时，**必须**打开并遵守对应 SKILL，再写代码：

| 包路径 | SKILL 路径 | 侧重 |
|--------|------------|------|
| `packages/core` | `packages/core/SKILL.md` | 服务形态、shutdown、依赖图、事件、反模式 |
| `packages/http` | `packages/http/SKILL.md` | Http、defineController、Loader、响应插件、与 core 集成 |
| `packages/http-next` | `packages/http-next/SKILL.md` | HttpNext、`/-` 前缀、控制器位置、start 流程 |
| `packages/cli` | `packages/cli/SKILL.md` | boot 规范、auto_load_packages、事件日志、退出钩子 |
| `packages/typeorm` | `packages/typeorm/SKILL.md` | DataSource 服务、transaction、rollback、环境变量 |
| `packages/ioredis` | `packages/ioredis/SKILL.md` | 客户端服务、环境变量、断连 |
| `packages/message-modem` | `packages/message-modem/SKILL.md` | MessageModem、post/exec、超时与错误 |
| `packages/message-ipc` | `packages/message-ipc/SKILL.md` | IPC 实现与用法 |
| `packages/message-worker-thread` | `packages/message-worker-thread/SKILL.md` | Worker 实现与用法 |
| `packages/message-ws` | `packages/message-ws/SKILL.md` | WebSocket 实现与用法 |
| `packages/message-loader` | `packages/message-loader/SKILL.md` | MessageLoader、defineMessage、路径映射 |

---

## 6. 常见反模式（禁止）

- 在**模块顶层** **await loadService(...)** 并导出或缓存该实例。
- **Boot 文件** **export default** 普通函数、配置对象或空实现。
- **控制器**中同时写 **ctx.body = ...** 和 **return ...**（应只 **return**，由响应插件写 body）。
- **控制器**签名为 **(ctx, next)** 并调用 **next()**（控制器无 next，需 next 的逻辑放中间件）。
- 在 **@hile/http-next** 中为 API 使用非 **`/-`** 前缀或把控制器放到非 **src/app/** 的约定外且未在 HttpNext 选项中说明。
- **auto_load_packages** 中写相对路径或 `.ts` 文件路径而非模块名。
- 创建 **Http** / **HttpNext** 后未将 **listen()** 返回的关闭函数传给 **shutdown(...)**。
- 使用 **@hile/typeorm** 事务时在 **transaction** 外使用同一 **runner** 或忘记在失败路径注册 **rollback**。

---

## 7. 文档与版本

- 各包**使用方式**以该包 **README.md** 与 **docs/** 为准；**代码生成与约束**以各包 **SKILL.md** 为准。
- 根目录 **README.md** 中的「包一览」与「依赖关系」描述当前仓库包划分与依赖；版本号以各包 **package.json** 为准。

遵守本 SKILL 并结合具体包的 SKILL，可保证生成的 Hile 相关代码与仓库架构一致、可被 CLI 正确加载并优雅关闭。