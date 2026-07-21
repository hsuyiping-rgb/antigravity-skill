# 🌌 Antigravity 專用教學與自動化技能集 (Antigravity Skills)

本專案是專為 **Antigravity** (Gemini AI 助理) 所量身打造的整合技能集與全自動環境設置包。
包含教學簡報製作、公開課課例分析、全平台服務連接以及跨電腦專案自動化 SOP 技能。

相較於原始的 Claude Code 版本，此版本針對 Antigravity 進行了以下優化：
1. **免 API Key 原生生圖**：不再需要設定額外付費的 OpenAI `draw` 腳本，改為呼叫 Antigravity 內建的 `generate_image` 繪圖引擎。
2. **自動化目錄同步**：產生的圖片會從 Antigravity 的臨時 Artifacts 目錄中自動被複製到專案對應的圖片目錄。
3. **無縫載入**：直接放置在工作區的自訂路徑中（`.agents/skills/`），AI 助理在對話開始時即可自動載入使用。

---

## 🛠️ 技能目錄與核心功能介紹

本專案將 AI 簡報生成系統、公開課課例探究與全平台連接懶人包完美整合，提供以下三大類別、共 **20 個核心自動化技能**：

### 一、 簡報生成與公開課分析系統
* **🖼️ 純圖片簡報 (`soil-image-deck`)**：使用 `generate_image` 逐頁產生「包含標題字與排版」的高品質全版圖像並自動打包成 `.pptx`。適合社群分享與研習暖場。觸發關鍵字：`做純圖片簡報`、`全圖簡報`。
* **📝 可編輯簡報 (`soil-teaching-deck`)**：將教學脈絡結構化拆解，文字與圖形分離以利後續修改，並由 AI 自動配圖產生 `.pptx`。適合常規公開課。觸發關鍵字：`幫我做教學簡報`、`用 SOIL 做簡報`。
* **🌐 互動網頁簡報 (`soil-html-deck`)**：產生單一可攜式 `.html`，支援 Chart.js 互動圖表、動態轉場與響應式佈局，生圖自動進行 base64 壓縮內嵌。觸發關鍵字：`做 HTML 簡報`、`網頁版簡報`。
* **📹 學習共同體課例探究 (`slc-skill`)**：針對公開課影片的端到端自動化課例研究工作流。包含段落語意下載與 Whisper 轉譯、微觀行為（語言、眼神、姿態、手勢、沉默與互動）與多維關係分析。擷取關鍵畫格重繪為一致的「日系水彩／抹茶綠繪本風格」，產出 PPTX 簡報與專為平板/手機設計的 Touch Swipe 響應式 HTML 互動網頁簡報。

### 二、 跨電腦專案管理三部曲 (SOP)
* **🟢 `ag-project-init` (初始化專案)**：當您在對話中說 `初始化專案` 時觸發。建立專案藍圖 (`agents.md`) ＋ 交接檔 (`handoff.md`)，整合 GitHub 私有庫與 Obsidian，並寫入 Google 雲端硬碟防衝突設定。
* **🟢 `ag-startup` (開工)**：當您說 `開工`、`我來了`、`上次做到哪` 時觸發。自動分析前次進度，比對收工電腦名稱以防止兩台電腦的 GDrive 同步衝突，提出今日下一步計畫。
* **🔴 `ag-shutdown` (收工)**：當您說 `收工`、`下班了` 時觸發。盤點對話成果，更新藍圖與交接手記，自動 commit+push 備份，並同步寫入 Obsidian 每日筆記。

### 三、 YAML 簡報生圖大師
* **🎨 `yaml-image-deck`**：當您說 `製作 YAML 簡報`、`YAML 生圖簡報` 時載入。讀取 YAML 設計合約規格（如佈局、字型安全區域）並使用內建 `generate_image` 繪圖引擎編譯生圖，產出 16:9 簡報與 Touch Swipe 觸控網頁簡報。

### 四、 環境配置與平台服務連接懶人包
* **`ag-env-setup`** (環境建置)：檢查並確保本機 Node.js 與 uv 等基礎開發工具鏈就緒。
* **`ag-notebooklm`** (連接 NotebookLM)：安裝並設定 NotebookLM MCP，檢索、讀寫您的 NotebookLM 筆記本。
* **`ag-github`** (連接 GitHub)：驗證登入 GitHub CLI、全域 Git 設定並進行連線測試。
* **`ag-obsidian`** (連接 Obsidian)：安裝全域 `@bitbonsai/mcpvault` 並在 `opencode.json` 中配置 Obsidian 第二大腦。
* **`ag-second-brain`** (建立第二大腦)：在 Obsidian 建立「每日筆記、創作庫、知識庫」三層結構，並配置駕駛艙 `ANTIGRAVITY.md`。
* **`ag-supabase`** (連接 Supabase)：安裝並設定全域 `@supabase/mcp-server-supabase` 以讀寫 Supabase 資料庫。
* **`ag-firebase`** (連接 Firebase)：完成 Firebase 登入、初始化，並設定 Firebase MCP 連接。
* **`ag-ollama`** (安裝 Ollama)：下載 Ollama、拉取本地模型（如 Llama3.2/Gemma3）以配置本地模型呼叫。
* **`ag-gemini`** (設定 Gemini)：建立 Gemini 免費 API 密鑰，存入 `~/.gemini.env` 檔供腳本與工具調用。
* **`ag-workspace`** (專案工作模式)：自動建立 `ANTIGRAVITY.md` 與開收工 SOP。
* **`ag-draw`** (免 API 免費生圖)：直接呼叫內建免費的 `generate_image` 生圖工具，將產出複製至專案中。
* **`ag-install-all`** (一鍵全部安裝)：一鍵依序引導並載入上述 11 個平台與生圖連線技能。

---

## ⚙️ 技能安裝目錄結構

專案的所有技能均已成功部署在工作區的自訂技能目錄中：
```
├── .agents/
│   └── skills/
│       ├── ag-draw/               # 免金鑰原生生圖
│       ├── ag-env-setup/          # 環境建置 (Node/uv)
│       ├── ag-firebase/           # Firebase MCP 連接
│       ├── ag-gemini/             # Gemini API 密鑰設定
│       ├── ag-github/             # GitHub CLI 連接
│       ├── ag-install-all/        # 一鍵安裝所有懶人包
│       ├── ag-notebooklm/         # NotebookLM MCP 連接
│       ├── ag-obsidian/           # Obsidian MCPVault 連接
│       ├── ag-ollama/             # 本地 AI Ollama 連接
│       ├── ag-project-init/       # 專案初始化 SOP
│       ├── ag-second-brain/       # Obsidian 第二大腦結構
│       ├── ag-shutdown/           # 收工 SOP
│       ├── ag-startup/            # 開工 SOP
│       ├── ag-supabase/           # Supabase MCP 連接
│       ├── ag-workspace/          # 老師建專案模式
│       ├── github-pages-deployer/ # GitHub Pages 自動部署
│       ├── slc-skill/             # 學習共同體課例探究
│       ├── soil-html-deck/        # HTML 簡報生成
│       ├── soil-image-deck/       # 純圖片簡報生成
│       ├── soil-teaching-deck/    # 可編輯簡報生成
│       └── yaml-image-deck/       # YAML 設計規格生圖簡報
├── test-page/
├── 09-AntiGravity專屬懶人包.md
├── 10-AntiGravity專屬懶人包-跨電腦專案與YAML簡報生圖.md
├── ANTIGRAVITY.md
└── README.md
```

---

## 💻 依賴套件安裝

在執行簡報打包、轉譯分析與網頁生成時，您的本地電腦需要準備以下套件：
```powershell
# 安裝 Python 依賴
pip install Pillow python-pptx cairosvg pyyaml faster-whisper yt-dlp beautifulsoup4 requests --break-system-packages

# 安裝 Node.js 依賴
npm install -g pptxgenjs jsdom
```
