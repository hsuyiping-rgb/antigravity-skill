# Anti-Gravity 2 專屬懶人包 #10：跨電腦專案管理與 YAML 簡報生圖大整合

> 版本：v1.0 (Anti-Gravity 2 專屬版)
> 更新日期：2026-07-21
> 語系偏好：預設繁體中文（Taiwan）

---

## 🚀 這個懶人包包含什麼？

本懶人包專門收錄了今日為 **Anti-Gravity 2 (Gemini AI 助理)** 所部署與改造的 **15 個核心自訂技能**。這些技能已經過相容性改造，完美適配本機 `generate_image` 繪圖引擎與 `opencode.json` 設定，為您提供無縫的專案管理與圖像簡報工作流：

1. **跨電腦專案管理三部曲**（L1-L3 自動適配）：
   - `ag-project-init` (初始化專案)：建立 `agents.md` 與 `handoff.md` 本地與雲端基礎建設。
   - `ag-startup` (開工)：自動分析前次進度、比對電腦名稱防止 GDrive 衝突。
   - `ag-shutdown` (收工)：一鍵完成敏感資料掃描、自動 commit/push、並寫入 Obsidian 每日筆記。
2. **YAML 簡報生圖大師** (`yaml-image-deck`)：
   - 透過 YAML 設計合約批次生圖，支援 `baked` (字圖合一) 與 `plate` (無字底圖+可編輯 PPTX 文字) 雙模式，具備手勢滑動與自適應 HTML 簡報輸出。
3. **全平台連線懶人包全集**：
   - 提供開發環境、NotebookLM、GitHub、Obsidian、Supabase、Firebase、Ollama、Gemini API 的連線指令與設定檔說明。

---

## 📋 今日安裝的 15 個技能清單

| 序號 | 技能名稱 | 觸發關鍵字 | 核心功能 |
|:---:|---|---|---|
| **01** | **`ag-project-init`** | `初始化專案`、`專案初始化` | 建立專案藍圖 (`agents.md`) ＋ 交接檔 (`handoff.md`)，整合 GitHub 與 Obsidian。 |
| **02** | **`ag-startup`** | `開工`、`我來了`、`上次做到哪` | 讀取交接與藍圖進度，確認前次收工電腦名（防止 GDrive 同步衝突），提出今日下一步計畫。 |
| **03** | **`ag-shutdown`** | `收工`、`下班了` | 盤點對話成果，更新 `agents.md`/`handoff.md`，自動 commit+push，寫入 Obsidian 每日筆記。 |
| **04** | **`yaml-image-deck`** | `製作 YAML 簡報`、`YAML 生圖簡報` | 讀取 YAML 設計規格並使用 `generate_image` 繪圖引擎編譯生圖，產出 16:9 簡報與 Touch Swipe 網頁簡報。 |
| **05** | **`ag-draw`** | `生圖`、`畫圖`、`畫一張` | **Antigravity 免 API 版**：直接呼叫內建免費的 `generate_image` 生圖工具，將產出複製至專案中。 |
| **06** | **`ag-env-setup`** | `建置環境`、`安裝開發環境` | 檢查本機 Node.js 與 uv 版本，補裝缺失的開發工具鏈。 |
| **07** | **`ag-notebooklm`** | `連接 NotebookLM` | 安裝 `notebooklm-mcp-cli` 與登入，引導在 `opencode.json` 配置 NotebookLM MCP 伺服器。 |
| **08** | **`ag-github`** | `連接 GitHub` | 登入 GitHub CLI、全域 Git 設定，並自動推播測試倉庫。 |
| **09** | **`ag-obsidian`** | `連接 Obsidian` | 安裝全域 `@bitbonsai/mcpvault`，並於專案 `opencode.json` 配置 Obsidian 第二大腦。 |
| **10** | **`ag-second-brain`**| `建立第二大腦` | 在 Obsidian 建立「每日筆記、創作庫、知識庫」三層結構，並配置駕駛艙。 |
| **11** | **`ag-supabase`** | `連接 Supabase` | 安裝並於 `opencode.json` 中設定全域 `@supabase/mcp-server-supabase`。 |
| **12** | **`ag-firebase`** | `連接 Firebase` | 透過 `firebase-tools` 完成專案初始化，並於 `opencode.json` 設定 Firebase MCP。 |
| **13** | **`ag-ollama`** | `安裝 Ollama`、`本地 AI` | 下載 Ollama、拉取本地模型（如 Llama3.2/Gemma3），配置本地模型呼叫。 |
| **14** | **`ag-gemini`** | `設定 Gemini`、`Gemini API` | 建立免費 API 密鑰，存入 `~/.gemini.env` 檔供腳本調用。 |
| **15** | **`ag-install-all`** | `全部安裝`、`裝完所有懶人包` | 一鍵依序引導並載入上述 11 個平台與生圖連線技能。 |

---

## 🛠️ 第一部分：跨電腦專案管理技能使用指南

我們已經將您的 GitHub 帳號 (`hsuyiping-rgb`) 與電子郵件 (`hsuyiping@gmail.com`) 自動配置於 `ag-project-init` 技能中。

### 1. 🟢 開新專案：「初始化專案」
當您對我說**「初始化專案」**時，我會自動：
1. 本地建立 `agents.md`（專案藍圖）與 `handoff.md`（交接檔）。
2. 初始化 Git 倉庫，寫入專用 `.gitignore`，並設定 `windows.appendAtomically false`（避免 GDrive 衝突）。
3. 透過 `gh` CLI 自動在您帳號下建立同名私有 repo 並推上去。
4. 與您的 Obsidian Vault (`G:\我的雲端硬碟\secondbrain`) 對接，建立對應的工作區日誌。

### 2. 🟢 家裡/學校換電腦繼續：「開工」
當您對我說**「開工」**或**「上次做到哪」**時，我會自動：
1. 讀取 `handoff.md` 的最後更新時間與電腦名稱。如果最後收工的電腦與目前電腦不同，我會主動提醒您確認 Google 雲端硬碟同步狀態。
2. 進行 `git status` 與 `git fetch` 檢查遠端是否有新的更新。
3. 提出今日的第一步具體行動建議。

### 3. 🔴 結束工作：「收工」
當您對我說**「收工」**時，我會自動：
1. 進行敏感金鑰與憑證掃描，防範 API Key 外洩。
2. 更新藍圖與交接檔手記，寫明今日進度與留待明日的工作。
3. 自動進行 Git commit 並 push 雲端備份。
4. 同步更新 Obsidian 中的工作日誌。

---

## 🎨 第二部分：YAML 簡報生圖與原生生圖使用指南

### 1. 批次簡報生圖 (`yaml-image-deck`)
當您說**「製作 YAML 簡報」**時，您可以：
1. 建立 `spec.yaml` 規格（可參考 `assets/spec-template.yaml`）。
2. 在 YAML 中定義每頁的 `layout.id` 與風格配色。
3. 透過內建 `generate_image` 繪製高質感的簡報插圖（採用日系粉圓/源柔等 Traditional Chinese 圓體字美學）。
4. 自動產生 `slides.pptx` 與平板/手機自適應並支援 **Touch Swipe 手勢滑動** 換頁的 HTML 簡報檔。

### 2. 單張免費生圖 (`ag-draw`)
當您說**「生圖」**或**「畫一張 [畫面描述]」**時：
1. 我會呼叫免費的原生生圖工具，依照您的要求（以繁體中文與溫潤水彩繪本風格為主）進行生圖。
2. 生圖完成後會直接儲存在對話 Artifacts 中，並可引導複製到您專案的 `generated/` 目錄下。
