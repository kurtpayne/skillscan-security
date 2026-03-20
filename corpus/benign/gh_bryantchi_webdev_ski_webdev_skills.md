---
name: 網站開發技能系統 (Webdev Skills)
description: 完整的網站開發指南 (Full-stack Web Development Skills)，涵蓋 UI/UX、前後端框架、Coding Style，支援互動式選擇精靈。
aliases:
  - webdev
  - web-development
  - frontend
  - backend
  - 網站開發
  - 網頁設計
keywords:
  - React
  - Vue
  - Next.js
  - Tailwind
  - Laravel
  - Node.js
  - UI/UX
  - Design System
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: BryantChi/webdev-skills
# corpus-url: https://github.com/BryantChi/webdev-skills/blob/3f4b2920fe76e6b5db465297b2276acc6eb39020/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# 🌐 網站開發技能系統

> 適用於任何 AI 工具的完整網站開發指南

---

## 🚀 核心指令

**啟動指令：**

```text
幫我建立一個網站
```

**AI 行為：**
收到此指令後，將自動啟動下方的 **[標準作業程序 (SOP)](#-標準作業程序-sop)**。

➡️ [詳細工作流程參考](workflows/build-website.md)

---

## ⚠️ 核心設計原則

**所有設計必須遵守 [去 AI 感設計指南](ui/no-ai-feel.md)**：

- ❌ 不要過於完美對稱的佈局
- ❌ 不要庫存照片（握手、微笑商務人士）
- ❌ 不要空洞的商業文案
- ❌ 不要千篇一律的模板感
- ✅ 要有個性、有溫度、有故事感
- ✅ 要適度的不對稱和變化
- ✅ 要真實的內容和照片

---

## 🔄 標準作業程序 (SOP)

**互動協議 (Protocol)：**
當用戶指令包含 `「建立網站」`、`「Build Website」` 或類似意圖時，**必須** 嚴格遵守以下執行順序，不得跳過。

### Phase 1: 智慧推理 (Reasoning)
> 🛑 **Constraint**: 在寫任何 Code 之前，必須先完成此步驟。

1. **分析意圖**：判斷專案類型 (SaaS/E-commerce/Portfolio/etc.)。
2. **執行推理**：讀取並應用 `logic/reasoning.md` 的規則。
3. **輸出決策**：展示 **Design Reasoning Block** (ASCII 表格)，確認風格、配色與反模式。

### Phase 2: 設計系統生成 (Design System)
> 🛑 **Constraint**: 必須建立單一真理來源 (Source of Truth)。

1. **讀取邏輯**：參照 `logic/design-system-gen.md`。
2. **生成檔案**：建立 `styles/design-system/MASTER.md`。
3. **定義變數**：確保色彩、字體、間距 tokens 已明確定義。

### Phase 3: 專案初始化 (Initialization)

1. **技術決策**：根據 Phase 1 推理結果，選擇最佳技術棧 (若用戶無指定)。
    - *SEO 優先* → Next.js
    - *快速開發* → Vue/Vite
    - *全端應用* → Laravel/Node
2. **建立專案**：執行初始化指令 (e.g., `npx create-next-app`).
3. **配置環境**：設定 Tailwind (`tailwind.config.js`) 連結至 `MASTER.md` 的變數。

### Phase 4: 開發執行 (Execution)

1. **元件開發**：優先製作基礎元件 (Button, Card, Input)。
2. **頁面組裝**：運用 `tpl/page/SKILL.md` 的結構進行開發。
3. **去 AI 感檢查**：隨時與 `ui/no-ai-feel.md` 對照，確保設計「有人味」。

---

## 🔧 手動/進階選項 (Manual Mode)

如果你希望能逐一步驟微調，或需要更細粒度的控制，可以使用互動精靈：

### 互動選擇精靈 ✨

| 精靈 | 說明 | 指令 |
|-----|------|-----|
| 🔧 [技術棧精靈](wizard/tech.md) | 選擇前後端框架 | `幫我選擇技術棧` |
| 🎨 [風格精靈](wizard/style.md) | 選擇設計風格 | `幫我選擇設計風格` |
| 📝 [Coding Style 精靈](wizard/code.md) | 選擇程式碼規範 | `幫我選擇 coding style` |

### 直接指定

告訴我你的需求，例如：
- `用 React + Tailwind 建立一個電商網站`
- `用 Laravel 建立 REST API`


---

## 📚 技能索引

### 核心邏輯 (New!)
| 類別 | 內容 |
|-----|------|
| [推理引擎](logic/reasoning.md) | 設計決策、反模式過濾 |
| [設計系統生成](logic/design-system-gen.md) | Master/Page 覆寫機制 |

### 設計相關
| 類別 | 內容 |
|-----|------|
| [UI 設計](ui/SKILL.md) | 色彩、排版、間距、55+ 設計風格 |
| [響應式設計](rwd/SKILL.md) | 斷點、行動優先、多裝置適配 |

### 前端開發
| 類別 | 內容 |
|-----|------|
| [前端框架](fe/SKILL.md) | React、Vue、Next.js、Nuxt.js、Vanilla |
| [CSS 架構](css/SKILL.md) | Tailwind、Bootstrap、SCSS、Vanilla |

### 後端開發
| 類別 | 內容 |
|-----|------|
| [後端框架](be/SKILL.md) | Laravel、Node.js、Django、FastAPI |
| [API 設計](api/SKILL.md) | REST、GraphQL、版本控制 |
| [資料庫](db/SKILL.md) | Schema 設計、ORM、遷移 |
| [安全性](sec/SKILL.md) | 驗證、授權、安全檢查清單 |

### 工作流程
| 類別 | 內容 |
|-----|------|
| [開發流程](flow/SKILL.md) | Git、測試、部署、效能優化 |
| [檢查清單](check/launch.md) | 上線前、SEO、安全審計 |
| [Coding Style](code/SKILL.md) | JS、TS、PHP、Python、CSS 規範 |

### 模板
| 類別 | 內容 |
|-----|------|
| [元件模板](tpl/comp/SKILL.md) | 按鈕、表單、卡片、導航、Modal |
| [頁面模板](tpl/page/SKILL.md) | Landing、Dashboard、認證頁 |

---

## 📋 需求規格書

開始新專案前，建議先建立需求規格書：

➡️ [需求規格書模板](spec.md)

---

## 🤖 AI 工具使用指南

不同的 AI 編程助手載入方式不同：

| AI 工具 | 載入方式 |
|--------|----------|
| **Cursor** | `@.agent/skills/webdev/SKILL.md` |
| **Windsurf** | `@.agent/skills/webdev/SKILL.md` |
| **Copilot** | `#file:.agent/skills/webdev/SKILL.md` |
| **Claude** | Projects 上傳或貼上內容 |
| **ChatGPT** | 建立 GPT 或貼上內容 |

➡️ [完整 AI 工具使用指南](ai-tools-guide.md)

---

## 版本資訊

- 版本：1.2.0
- 更新日期：2026-01-29
- 語言：繁體中文
- 總檔案數：102
- 設計風格：55 種