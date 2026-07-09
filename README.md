# 🌌 Antigravity 專用教學與自動化技能集 (Antigravity Skills)

本專案是專為 **Antigravity** (Gemini AI 助理) 所量身打造的整合技能集。
包含教學簡報製作、課堂公開課影片分析與學校 AI 秘書建立等多元自動化技能。

相較於原始的 Claude Code 版本，此版本針對 Antigravity 進行了以下優化：
1. **免 API Key 原生生圖**：不再需要設定額外付費的 OpenAI `draw` 腳本，改為呼叫 Antigravity 內建的 `generate_image` 繪圖引擎。
2. **自動化目錄同步**：產生的圖片會從 Antigravity 的臨時 Artifacts 目錄中自動被複製到專案對應的圖片目錄。
3. **無縫載入**：直接放置在工作區的自訂路徑中（`.agents/skills/`），AI 助理在對話開始時即可自動載入使用。

---

## 🛠️ 五大核心技能介紹

本技能集包含三種輸出格式的技能，以滿足不同的教學場景需求：

### 1. 🖼️ SOIL 純圖片教學簡報 (`soil-image-deck`)
* **觸發關鍵字**：`做純圖片簡報`、`全圖簡報`、`每頁都是 AI 生的圖`
* **輸出格式**：`.pptx`（每張投影片即是一張全版滿版圖）
* **特色**：
  - 專門應對需要高視覺衝擊的場合（例如：研習暖場、FB/IG 社群分享、YouTube章節過場）。
  - 使用 `generate_image` 逐頁產生「整頁圖像」（包含排版與繁體中文標題字），並透過 [pack_pptx.py](.agents/skills/soil-image-deck/scripts/pack_pptx.py) 自動打包。
  - **不適合**後續需要修改文字的場合。

### 2. 📝 SOIL 可編輯教學簡報 (`soil-teaching-deck`)
* **觸發關鍵字**：`幫我做教學簡報`、`做一份上課用的投影片`、`用 SOIL 做簡報`
* **輸出格式**：`.pptx`（文字可直接在 PowerPoint 中編輯，並內嵌 AI 插圖）
* **特色**：
  - 最符合老師日常備課需求的格式。
  - 將教學脈絡拆分為：**引起動機 (20%)**、**維持注意 (60%)**、**喚起行動 (20%)**。
  - 每張投影片均有明確的角色（如：問題引入頁、迷思澄清頁、雙欄比較頁），文字與幾何圖形/插畫分離，便於日後編輯。

### 3. 🌐 SOIL 互動式網頁簡報 (`soil-html-deck`)
* **觸發關鍵字**：`做 HTML 簡報`、`網頁版簡報`、`互動式簡報`、`線上簡報`
* **輸出格式**：單一可攜式 `.html` 檔案
* **特色**：
  - 自由度最高的簡報格式，適合線上研習、直播教學或跨裝置（手機/平板）呈現。
  - 支援嵌入 **Chart.js** 互動圖表、可點擊表格、CSS 動態效果與 JS 互動。
  - 生圖會透過 Python 自動進行 base64 壓縮並內嵌於網頁中，方便一鍵分享。

### 4. 📹 課堂公開課影片分析與課例研究 (`classroom-video-analyzer`)
* **觸發關鍵字**：當使用者提供影片網址時（例如 YouTube 連結）
* **特色**：
  - 一鍵下載影片音檔（MP3 格式）、使用 Whisper 模型進行本地轉譯，產出具備精確斷句與時間軸的繁體中文/雙語 SRT 字幕及逐字稿。
  - 基於佐藤學「傾聽、串聯、回歸」觀課對話架構，以及「描述 $\rightarrow$ 詮釋 $\rightarrow$ 反思」三階層分析模型，自動生成至少 12 頁的課例分析簡報與 FB/IG 社群概念圖檔。

### 5. 🤖 學校 AI 秘書建立器 (`school-secretary-builder`)
* **觸發關鍵字**：自動建立學校秘書、建立學校 AI 秘書等關鍵字
* **特色**：
  - 自動爬取指定的學校官方網站，清洗 HTML、去除冗餘欄位，並將核心網頁結構化提取為問答 JSON 資料庫。
  - 基於乾淨網頁範本（HTML/CSS/JS），自動生成一個支援 Gemini API（與本地 Fallback 機制）的精美響應式 AI 秘書對話機器人，並透過 Headless Mock DOM 進行自動化功能驗證。

---

## ⚙️ 技能安裝路徑與依賴

### 1. 目錄結構
本技能放置於工作區的自訂技能目錄 `.agents/` 底下：
```
.agents/
└── skills/
    ├── classroom-video-analyzer/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── classroom_analyzer_helper.py
    ├── school-secretary-builder/
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   └── builder_cli.py
    │   └── templates/
    │       ├── app.js.template
    │       ├── index.html.template
    │       └── styles.css.template
    ├── soil-html-deck/
    │   └── SKILL.md
    ├── soil-image-deck/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── pack_pptx.py
    └── soil-teaching-deck/
        └── SKILL.md
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

### 3. 🎯 連接 GitHub 帳戶
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
