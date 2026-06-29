---
name: soil-html-deck
description: >
  HTML 簡報技能 (自由度天花板)。用單一 HTML 檔案模擬簡報的呈現邏輯，
  圖像由 Antigravity 的 generate_image 生成並 base64 內嵌，排版/文字/互動全部由 HTML + CSS + JS 處理，
  支援互動圖表 (Chart.js)、可點擊表格、影片嵌入、RWD 跨裝置、一鍵分享 URL。
  當使用者說「做 HTML 簡報」、「網頁版簡報」、「互動式簡報」、「線上簡報」、
  「可分享連結的簡報」、「要有互動圖表的簡報」、「不受 PowerPoint 限制的簡報」、
  「最自由的簡報格式」時，請使用此技能。
  本技能與 soil-image-deck (全圖 .pptx)、soil-teaching-deck (可編輯 .pptx) 的差別：
  本技能輸出是單一 .html，自由度最高、可嵌互動、可立即線上分享，
  但需要瀏覽器環境播放，不適合給只用 PowerPoint 的對象。
---

# SOIL HTML 簡報工作流 (soil-html-deck)

以 SOIL 教學設計邏輯為骨架，用 **HTML + Antigravity generate_image 圖像 + JS 互動** 產出單一 `.html` 簡報檔。
所有設計決策都遵循 **林長揚 30 原則** 與 **SOIL 六引擎**。

---

## 適用情境

| 情境 | 為什麼用本技能 |
|------|----------------|
| 線上研習 / 直播教學 | 觀眾用手機/電腦打開 URL 即可同步看 |
| 互動展演 | 嵌入 Chart.js 互動圖表、可點擊表格 |
| 數據視覺化導向 | HTML 原生支援 SVG / Canvas / D3 |
| 想脫離 PowerPoint 框架 | 任何網頁能做的，簡報就能做 |
| 跨裝置呈現 | RWD，手機平板桌機都能看 |

**不適用**：對方只能用 PowerPoint 接收檔案、需要離線投影但無瀏覽器、講者不熟悉 HTML 排版。

---

## 輸入

使用者需提供：
- **內容素材** (必要)：Markdown 大綱或主題描述。
- **頁數預期** (選填，預設 8-12 頁)
- **風格關鍵字** (選填，例：「黑板粉筆」「科技藍」)

---

## 執行流程

### 第 1 步：讀懂素材、規劃章節
讀取素材後，先輸出 **章節骨架** 給使用者確認，等使用者點頭再進下一步。

### 第 2 步：統一視覺風格 (產出 CSS 變數區塊)
```css
:root {
  --bg: #0a0e27; --bg-2: #11163a;
  --ink: #eef3ff; --ink-2: #b8c5e0;
  --accent: #00d4ff;   /* 主強調色 */
  --accent-2: #ff006e; /* 輔強調色 */
}
```

### 第 3 步：批次生成圖像 (使用原生 `generate_image`)
呼叫 Antigravity 原生的 `generate_image` 生圖工具。
- **Prompt**：應包含風格描述，強制加入「以繁體中文顯示文字（或無文字）」的要求，並留下留白區供文字疊放。
- **ImageName**：按 `html_page_01` 等規律命名。

### 第 4 步：Base64 內嵌圖像
為了讓單一 HTML 檔案完全可攜，不要使用相對路徑。一律用 Pillow 壓縮並轉成 base64 內嵌：
生圖完成後，從 Antigravity Artifacts 目錄中將生成的圖片複製到本機專案目錄，再執行以下 Python 程式碼進行壓縮與 base64 編碼，最後替換入 HTML 中：

```python
# b64_encoder.py
from PIL import Image
import base64, io

def encode_image(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    target_w = 1280
    if w > target_w:
        img = img.resize((target_w, int(h*target_w/w)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=78, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}"
```

### 第 5 步：產出單一 HTML (架構與排版)
整合所有 HTML, CSS, JS 及內嵌的 base64 圖像，產出最終的網頁簡報檔。
