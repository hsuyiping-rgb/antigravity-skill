# 🌌 Antigravity 專用教學與自動化技能集 (Antigravity Skills)

本專案是專為 **Antigravity** (Gemini AI 助理) 所量身打造的整合技能集。
包含教學簡報製作、GitHub Pages 自動部署發佈等多元自動化技能。

相較於原始的 Claude Code 版本，此版本針對 Antigravity 進行了以下優化：
1. **免 API Key 原生生圖**：不再需要設定額外付費的 OpenAI `draw` 腳本，改為呼叫 Antigravity 內建的 `generate_image` 繪圖引擎。
2. **自動化目錄同步**：產生的圖片會從 Antigravity 的臨時 Artifacts 目錄中自動被複製到專案對應的圖片目錄。
3. **無縫載入**：直接放置在工作區的自訂路徑中（`.agents/skills/`），AI 助理在對話開始時即可自動載入使用。

---

## 🛠️ 五大核心技能介紹

本專案將 AI 簡報生成系統與全平台連接懶人包完美整合，提供以下五大核心自動化技能：

### 1. 📊 SOIL 教學簡報生成系統 (`soil-deck-skills`)
* **特色**：整合了三種簡報輸出格式，以滿足不同的備課與教學場景需求：
  - **🖼️ 純圖片簡報 (`soil-image-deck`)**：使用 `generate_image` 逐頁產生「包含標題字與排版」的高品質全版圖像並自動打包成 `.pptx`。適合社群分享與研習暖場。觸發關鍵字：`做純圖片簡報`、`全圖簡報`。
  - **📝 可編輯簡報 (`soil-teaching-deck`)**：將教學脈絡結構化拆解，文字與圖形分離以利後續修改，並由 AI 自動配圖產生 `.pptx`。適合常規公開課。觸發關鍵字：`幫我做教學簡報`、`用 SOIL 做簡報`。
  - **🌐 互動網頁簡報 (`soil-html-deck`)**：產生單一可攜式 `.html`，支援 Chart.js 互動圖表、動態轉場與響應式佈局，生圖自動進行 base64 壓縮內嵌。觸發關鍵字：`做 HTML 簡報`、`網頁版簡報`。

### 2. 📓 Google NotebookLM 連接技能
* **特色**：
  - 整合 `notebooklm-mcp-cli` 工具，使 AI 助理可直接檢索、讀取與整理您的 NotebookLM 筆記與外部來源。
  - 自動處理 Windows 系統下的 CP950 編碼問題，確保資訊擷取與對話的繁體中文穩定性。

### 3. 🔥 Firebase 雲端資料庫連接技能
* **特色**：
  - 整合 `firebase-tools` 管理工具，賦予 AI 助理對 Firebase 進行初始化、資料表讀寫、權限調整與雲端部署的能力。
  - 自動繞過 Windows PowerShell 執行原則限制，提供穩定無礙的資料庫整合開發環境。

### 4. 🧠 Obsidian 第二大腦雙向連接
* **特色**：
  - 透過 `@bitbonsai/mcpvault` 與本地 Markdown 筆記雙向同步，讓 AI 助理將專案進度、日誌直接記錄於您的 Obsidian 每日筆記中。
  - 便於實現「Obsidian 規劃任務 $\rightarrow$ AI 助理讀取執行 $\rightarrow$ 自動回報進度」的工作流閉環。

### 5. 🐙 GitHub 連接與 Pages 自動部署 (`github-pages-deployer`)
* **特色**：
  - **GH 帳戶安全授權**：配置 Git 全域使用者資訊與安全 Token 認證。
  - **一鍵自動架站服務**：自動偵測網頁檔案、建立 GitHub 公開倉庫並推播。同時調用 Pages API 啟用服務，自動生成公開網址（`https://{owner}.github.io/{repo}/`），完成靜態網頁快速部署。

---

## ⚙️ 技能安裝路徑與依賴

### 1. 目錄結構
專案的主要目錄與檔案結構如下（已成功部署至 GitHub）：
```
├── .agents/
│   └── skills/
│       ├── github-pages-deployer/
│       │   └── SKILL.md
│       ├── soil-html-deck/
│       │   └── SKILL.md
│       ├── soil-image-deck/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── pack_pptx.py
│       └── soil-teaching-deck/
│           └── SKILL.md
├── test-page/
│   ├── index.html
│   └── ai_brain_hub.png
├── 09-AntiGravity專屬懶人包.md
├── ANTIGRAVITY.md
└── README.md
```

### 2. 依賴套件安裝
在執行簡報打包、轉譯分析與網頁生成時，您的本地電腦需要準備以下套件：
```powershell
# 安裝 Python 依賴（簡報打包、影片轉譯、網頁爬蟲與生圖）
pip install Pillow python-pptx cairosvg pyyaml faster-whisper yt-dlp beautifulsoup4 requests --break-system-packages

# 安裝 Node.js 依賴（用於 PptxGenJS 與 Mock DOM 測試）
npm install -g pptxgenjs jsdom
```

---

## 🛠️ 全平台服務連接與整合指南 (整合懶人包)

本專案提供了一套終極整合方案，協助您的 AI 助理連接本機與雲端的所有主流服務：

### 1. 🎯 連接 Google NotebookLM (MCP)
1. **安裝 CLI 工具**：
   ```powershell
   pip install notebooklm-mcp-cli
   ```
2. **登入 Google 帳號**：
   ```powershell
   nlm login
   ```
3. **繞過 Windows CP950 編碼錯誤**（關鍵防踩坑）：
   在 Windows 終端機執行 `nlm` 指令前，務必加上 `PYTHONIOENCODING=utf-8` 環境變數：
   ```powershell
   $env:PYTHONIOENCODING="utf-8"
   nlm list
   ```

---

### 2. 🎯 連接 Firebase 資料庫
1. **安裝 Firebase CLI**：
   ```powershell
   npm install -g firebase-tools
   ```
2. **繞過 Windows PowerShell 執行原則限制 (`PSSecurityException`)**：
   Windows 預設會拒絕載入 `firebase.ps1`。請使用 **CMD 包裝器** 執行：
   ```powershell
   cmd /c firebase login
   cmd /c firebase projects:list
   ```

---

### 3. 🎯 連接 GitHub 帳戶與 Pages 自動部署
1. **驗證與登入**：
   使用 GitHub CLI 進行網頁端安全授權：
   ```powershell
   $env:GITHUB_TOKEN=""  # 確保清除 AI 代理人的權限干擾
   gh auth login --web --git-protocol https
   gh auth status
   ```
2. **設定 Git 全域使用者資訊**：
   ```powershell
   git config --global user.name "您的名字"
   git config --global user.email "您的email@example.com"
   ```
3. **GitHub Pages 自動化部署 (`github-pages-deployer`)**：
   啟用本機自訂技能後，當對 AI 助理下達「發佈網頁到 GitHub」時，助理會自動：
   - 偵測專案中的 HTML/CSS/JS 網頁檔案。
   - 自動配置 Git 本地倉庫並防範 Google Drive 同步衝突。
   - 使用 `gh` CLI 建立遠端公開倉庫並推播。
   - 調用 GitHub Pages API 自動啟用靜態網站託管，並直接輸出網站 URL。

---

### 4. 🎯 連接 Obsidian 第二大腦
1. **安裝全域 MCP 伺服器**：
   ```powershell
   npm install -g @bitbonsai/mcpvault
   ```
2. **設定 `opencode.json`**：
   在您專案根目錄建立 `opencode.json`，將實體路徑指向您的 Obsidian Vault 目錄（例如 `G:\\我的雲端硬碟\\secondbrain`）：
   ```json
   {
     "mcp": {
       "obsidian": {
         "type": "local",
         "command": ["npx", "@bitbonsai/mcpvault", "G:\\我的雲端硬碟\\secondbrain"],
         "enabled": true
       }
     }
   }
   ```

---

## 🟢 專案自動化 SOP 工作流 (ANTIGRAVITY.md)

當您在對話中對 AI 助理說出關鍵字時，將會自動觸發定義於 `ANTIGRAVITY.md` 專案駕駛艙中的自動化 SOP 工作流：

### 1. 🟢 說「開工」或「我來了」時
AI 助理會自動：
* **確認 Git 倉庫狀態**：執行 `git status` 與 `git branch -a`。
* **同步遠端變更**：執行 `git log -n 5`，並拉取遠端最新代碼。
* **讀取 Obsidian 每日筆記**：從設定的每日筆記目錄中讀取「上次做到哪」與「下一步計畫」。
* **提供行動建議**：彙整代碼狀態，給出今日的第一步具體行動建議。

### 2. 🔴 說「收工」或「下班了」時
AI 助理會自動：
* **資安防護掃描**：掃描敏感檔案（如 `.env` 等），確保金鑰無外洩風險。
* **自動 Git 提交與推播**：自動追蹤變更、生成符合 Commit 規範的 message，執行 `git commit` 與 `git push`。
* **更新 Obsidian 每日筆記**：在每日筆記中寫入今日的「已完成工作」與「留待明日待辦事項」。

### 3. 🔵 說「初始化專案」時
AI 助理會自動：
* **基礎建設部署**：自動產生 `ANTIGRAVITY.md`、`.gitignore` 與 `README.md`。
* **Git 本地初始化**：執行 `git init` 並完成 Initial Commit。
* **建立雲端倉庫**：呼叫 `gh repo create` 自動在 GitHub 上建立遠端倉庫並推送代碼。
* **Obsidian 工作區對接**：在您的 Obsidian 第二大腦中，同步建立專案工作資料夾。
