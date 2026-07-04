# 🏫 School AI Secretary Builder (school-secretary-builder)

這是一個全域的 Antigravity 代理人技能（Agent Skill），專為快速建置、維護及驗證各級學校的「AI 秘書 / 聊天機器人」網頁應用程式而設計。

---

## 🌟 核心功能特性 (Features)

本工具為學校 AI 秘書的開發提供了一整套自動化解決方案，具備以下核心功能：

1. **一鍵流水線建置 (`build` Command)**  
   整合爬蟲抓取、範本程式碼填充、Mock DOM 自動測試三合一流程，輸入網址後直接輸出立即可用的網頁專案。

2. **智慧網頁爬取與清洗 (`crawl` Command)**  
   - **Google Sites 支援**：自動分析 Google 協作平台特有的 DOM 結構與腳本狀態變數（如 `WIZ_global_data`），抽取內置的乾淨文本。
   - **網頁表單與表格解析**：自動識別網頁中的表格（Table / `tr` / `td`）並轉換為易讀的 Markdown 條列格式。
   - **防封鎖與限流（Politeness Delay）**：每頁抓取設有 1 秒延遲，避免伺服器頻繁存取限制，並配合自訂 User-Agent。

3. **生成的 AI 秘書網頁特色 (Generated Web App Features)**  
   - **在地知識庫模式 (Local Database Mode)**：免 API 金鑰、免成本、零延遲。完全在瀏覽器端比對問答資料庫回答。
   - **AI 智慧模式 (AI Intelligent Mode)**：在介面中輸入 Google Gemini API 金鑰後即可啟用。採用 RAG（檢索增強生成）架構，將爬取到的在地知識做為 Context 提供給 `gemini-1.5-flash`，以獲得更口語化、具推理能力的回答，並在網路異常或金鑰無效時**自動降級（Fallback）回在地知識庫模式**。
   - **滿版極致美學 layout (Responsive RWD)**：介面設計完美適配 `100vw`/`100vh` 滿版視口，採用精美現代的毛玻璃漸層質感、流暢的氣泡微動畫，並內建行動裝置漢堡選單抽屜。
   - **家長請假信產生器**：內建家長專用的請假信產生器，可自訂語氣（誠懇、客氣、簡短）並一鍵複製。

4. **安全防護與自動驗證 (`test` Command)**  
   程式碼寫入前會自動建立 Node.js 虛擬 DOM 環境，執行 Mock DOM 測試，確認 DOMContentLoaded 事件正常觸發且無語法錯誤後才可完成，確保產出的程式碼 100% 可執行。

---

## 📖 第一部分：建置原理與技術課程 (How it's Built)

### 1. 爬蟲設計與資料分類 (Crawler & Classifier)
- **爬取策略**：使用 Python `urllib` 進行遞迴爬取。
- **特定架構解析**：自動過濾 Google 相關的狀態變數，只保留核心網頁文字。
- **自動分類器**：基於網址關鍵字（例如 `交通`、`電話`、`行政`、`幼`）與內文啟發式演算法，將爬取到的文本自動歸檔到系統預設的 Q&A 類別中（如：`交通`、`電話`、`行政組織`、`幼兒園`、`家長會`、`最新消息`、`認識`、`處室`、`平台`）。

### 2. 模板引擎設計 (Template System)
採用引數化預留位置填充：
- `index.html.template`：保留精美現代的響應式聊天介面，設有 `{{SCHOOL_NAME}}` 與 `{{SECRETARY_NAME}}` 預留位置。
- `styles.css.template`：預存滿版（100vw/100vh）的現代毛玻璃風格與微動畫樣式。
- `app.js.template`：設有 `const chatKnowledgeBase = {{KNOWLEDGE_BASE_JSON}};`，在生成階段會直接將清洗後的問答 JSON 資料注入，並自動轉義反引號（\`）與變數插值（`${}`）防止 JS 語法崩潰。

### 3. 無頭 Mock DOM 驗證 (Automated Verification)
- 模擬了 `global.window`、`global.document`、`global.localStorage`。
- 模擬了 `MockElement` 類別，支援 `classList`（add, remove, contains）、`style`、`addEventListener`、`dispatchEvent`、`parentElement` 遞迴尋找、`querySelector` 與 `querySelectorAll` 方法。
- 測試腳本載入產出的 `app.js` 並觸發 `DOMContentLoaded` 事件，若有任何未定義 we DOM 操作或 JavaScript 語法錯誤，測試會立即以非零狀態碼（`exit 1`）中止，使 AI 能夠捕獲錯誤日誌並進行自我修正（Self-Correction）。

---

## 💻 第二部分：全域使用說明書 (Usage Manual)

### 📋 系統要求
1. **Python 3.10+** (僅需標準函式庫)
2. **Node.js 16+** (用於執行 DOM 自動驗證)
3. 安裝完成的 `school-secretary-builder` 全域 Skill。

### 🚀 快速開始：一鍵爬取與建置 (Build)
使用 `build` 指令可一次性完成「網頁爬取 ➡️ 代碼生成 ➡️ DOM 測試驗證」的完整工作流：

```bash
python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py build \
  --url "https://www.kfes.ntpc.edu.tw" \
  --name "中和區光復國小" \
  --sec-name "小光" \
  --out-dir "./kfes-secretary"
```

### ⚙️ CLI 命令行參數詳細說明

#### 1. `build` (一鍵建置)
- `--url` (必填): 目標學校網站的入口網址（如首頁或 Google Sites 門戶網址）。
- `--name` (必填): 學校的官方全銜（如 "中和區光復國小"），將用於網頁標題與介面顯示。
- `--sec-name` (選填): AI 秘書的稱呼，預設為 `"小光"`。
- `--out-dir` (必填): 建置完成後的專案代碼輸出路徑。

#### 2. `crawl` (單獨爬取與清洗數據)
```bash
python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py crawl \
  --url "https://www.kfes.ntpc.edu.tw" \
  --depth 2 \
  --output "./scraped_data.json"
```
- `--depth` (選填): 爬蟲最大遞迴深度，預設為 `2`。

#### 3. `generate` (單獨生成代碼檔案)
```bash
python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py generate \
  --school-name "光復國小" \
  --sec-name "小光" \
  --data "./scraped_data.json" \
  --out-dir "./dist"
```

#### 4. `test` (單獨執行 Mock DOM 測試)
```bash
python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py test \
  --dir "./dist"
```

---

## 🛠️ 開發與維護 (Developer Notes)
本 Skill 原始碼已託管於 GitHub：[school-secretary-builder](https://github.com/hsuyiping-rgb/school-secretary-builder)。

如果您修改了 Skill 的範本或腳本，請記得將變更推播至 GitHub 儲存庫：
```bash
cd C:\Users\vm\.gemini\config\skills\school-secretary-builder
git add .
git commit -m "Update: [描述您的變更]"
git push origin main
```
