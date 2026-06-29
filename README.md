# 🌌 Antigravity 專用 SOIL 教學簡報技能集 (SOIL Deck Skills)

本專案是專為 **Antigravity** (Gemini AI 助理) 所量身打造的教學簡報製作技能集。
以李俊儀教授的 **SOIL Teaching Deck Workflow（六大引擎）** 教學設計邏輯為骨架，協助老師或講師將教材與概念轉化為具備教學力的簡報。

相較於原始的 Claude Code 版本，此版本針對 Antigravity 進行了以下優化：
1. **免 API Key 原生生圖**：不再需要設定額外付費的 OpenAI `draw` 腳本，改為呼叫 Antigravity 內建的 `generate_image` 繪圖引擎。
2. **自動化目錄同步**：產生的圖片會從 Antigravity 的臨時 Artifacts 目錄中自動被複製到專案對應的圖片目錄。
3. **無縫載入**：直接放置在工作區的自訂路徑中（`.agents/skills/`），AI 助理在對話開始時即可自動載入使用。

---

## 🛠️ 三大教學簡報技能介紹

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

---

## ⚙️ 技能安裝路徑與依賴

### 1. 目錄結構
本技能放置於工作區的自訂技能目錄 `.agents/` 底下：
```
.agents/
└── skills/
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
在執行簡報打包與 base64 編碼時，您的本地電腦需要準備以下套件：
```powershell
# 安裝 Python 依賴（用於處理圖片與打包 PPTX）
pip install Pillow python-pptx cairosvg pyyaml --break-system-packages

# 安裝 Node.js 依賴（用於 PptxGenJS 打包可編輯投影片）
npm install -g pptxgenjs
```
