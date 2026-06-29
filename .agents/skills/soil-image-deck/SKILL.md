---
name: soil-image-deck
description: >
  SOIL 純圖片教學簡報技能。遵循 SOIL Teaching Deck Workflow 六顆引擎的教學設計邏輯，
  但每一頁都是由 Antigravity 的 generate_image 完整生成的 PNG 圖片（包含標題、內文、視覺），
  最後打包成 .pptx（每張 slide 是一張全版圖）。
  當使用者要求「做純圖片簡報」、「全圖簡報」、「每頁都是 AI 生的圖」、
  「用 gpt-image-2 做整份簡報」、「做一份像海報一樣的教學簡報」、
  「快速做一份視覺震撼的簡報」或任何要求「整頁都是 AI 圖像」的教學簡報需求時，
  請使用此技能。
  本技能與 soil-teaching-deck 不同：soil-teaching-deck 產出「文字可編輯 + AI 插圖」的
  混合簡報；本技能產出「每頁都是單張 AI 圖」的純圖片簡報，適合
  快速產出、社群貼文、視覺強烈的開場、或不需後續文字編輯的場合。
---

# SOIL 純圖片教學簡報（soil-image-deck）

以 SOIL 六顆引擎的教學判斷為骨架，使用 Antigravity 原生的 `generate_image` 逐頁生成**整頁圖像**，最後使用腳本打包成 `.pptx`。

> **與 soil-teaching-deck 的差別**
> - `soil-teaching-deck`：產出「文字 + 插圖」的可編輯 PowerPoint 檔案。
> - `soil-image-deck`（本技能）：逐頁生出「整頁圖」，打包成 pptx（每張投影片就是一張全版滿版圖）。

---

## 適用情境

| 情境 | 為什麼用本技能 |
|------|----------------|
| 直播開場、研習暖場 | 要視覺衝擊，不需要台下帶回去編輯 |
| 社群分享、FB / IG 貼文 | 每張圖就是一則獨立素材 |
| 快速原型、腦力激盪 | 快速出圖，不糾結排版 |
| YouTube 影片章節過場 | 風格統一、節奏清楚 |
| 節慶／宣傳海報簡報 | 圖像為主、文字為輔 |

**不適合**：需要台下老師後續修改文字、有大量精細資料、需要動畫互動——這些請用 `soil-teaching-deck` 或 `soil-html-deck`。

---

## 第一步：判斷工作模式

**問使用者（只問這一題）：**

> 請問你目前的狀況是？
> 1. 我有素材（文字、教材、腳本），想做成純圖片簡報
> 2. 我只有一個主題或一句話，想從頭開始
> 3. 我有現成的 YAML 規格，直接跑生圖與打包

| 回答 | 跑哪幾顆引擎 |
|-----|--------------|
| 1 | 引擎 1→2→3→4→5→6 |
| 2 | 先協助擴充內容 → 引擎 1→2→3→4→5→6 |
| 3 | 跳過引擎 1-5，直接進入引擎 6（I-1 批次生圖 → I-2 視覺確認 → I-3 打包）|

---

## 第二步：進入引擎前問答

### 進引擎一前問答：
1. **教學對象是誰？**（國中生、高中生、老師研習、一般觀眾、社群受眾）
2. **簡報總頁數？**（預設 10 頁；社群貼文通常 6-9 頁）

### 進引擎五前問答：
1. **有偏好的視覺風格嗎？**（例如：扁平插畫、手繪粉筆風、新聞風、科技感、水彩）
2. **主要色系？**（例如：深藍 + 金黃、米色 + 墨綠、粉色系）

---

## 引擎一：概念定位師
同 `soil-teaching-deck` 引擎一。產出：總概念、三個子概念、三個常見誤解、帶走一句話、最小事實包。
*特別注意：因為每頁都是圖，**文字量要極度壓縮**。*

## 引擎二：脈絡定位師
同 `soil-teaching-deck` 引擎二。三段節奏（引起動機／維持注意／喚起行動），比例 2:6:2 左右。

## 引擎三：頁面架構師
每頁指定角色後，產出「**image brief**」，作為生圖的基礎。

### 輸出格式
```yaml
pages:
  - page: 1
    role: 封面
    core_point: "用生圖工具做教學簡報"
    on_image_text:
      title: "AI 生圖 × 教學簡報"
      subtitle: "SOIL 教學工作流實踐"
    image_brief: "Q版機器人老師站在發光黑板前手持畫筆，黑板上有數學公式與電路圖案"
    layout_hint: "左文右圖；標題置左上，圖像置右"
```

### 文字最小化原則
> [!IMPORTANT]
> 由於生圖文字渲染字數限制，**每張圖建議中文字 ≤ 20 字**。超過要拆成多頁或改用 `soil-teaching-deck`。

---

## 引擎四：認知編修師
逐頁用六個認知詞（降雜訊、區塊化、增資訊、結構化、順脈絡、步驟化）檢視 `image_brief` 與 `on_image_text`。

---

## 引擎五：風格建構師（產出 image_policy）
必填輸出：
```yaml
image_policy:
  style_tokens: "扁平向量插畫、16:9橫版、深夜藍#0D1B2A背景、亮青藍#00C6FF主色、金黃#FFD700點綴、現代教育科技風"
  negative: "不要逼真照片、不要雜亂背景、不要亂碼、不要英文字"
```

---

## 引擎六：簡報總導演（純圖片版）

### 1. 呼叫 `generate_image` 生圖
對於每一頁，合併 `image_policy.style_tokens` + `on_image_text` + `image_brief` + `layout_hint` 組成 `Prompt`。

**調用說明**：
- 使用 Antigravity 的 `generate_image` 工具。
- `Prompt`：包含畫面排版、內容描述、風格、負面提示，且明確要求「以繁體中文顯示文字：...」。
- `ImageName`：以 `page_01`、`page_02` 等順序命名。

### 2. 複製圖片至專案目錄
生圖完成後，圖片將保存在 Artifacts 目錄中。
請在 Terminal 中執行 `Copy-Item`（Windows PowerShell）或寫一個簡單的腳本，將圖片從 Artifacts 目錄（可在你的系統提示中找到實體路徑）複製到專案資料夾下的 `slides/images/` 中：
```powershell
# 範例
mkdir -p slides/images
Copy-Item "C:\Users\vm\.gemini\antigravity\brain\<conversation-id>\page_*.png" -Destination "slides/images/" -Force
```

### 3. 使用 `pack_pptx.py` 打包成 PPTX
在專案中執行打包腳本：
```powershell
python .agents/skills/soil-image-deck/scripts/pack_pptx.py --mode baked --images-dir slides/images --output slides/output.pptx
```

提供使用者下載連結並簡要說明結構。
