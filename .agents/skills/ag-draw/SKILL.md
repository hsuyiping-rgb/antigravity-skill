---
name: ag-draw
description: Antigravity 畫圖與生圖技能。說「安裝生圖」「畫圖」「生圖」時載入。
---

# 生圖技能（Antigravity 版）

## 說明
在 Antigravity 中，您不需要設定 OpenAI API 金鑰或執行任何外部 python 腳本。Antigravity 原生支援 `generate_image` 生圖工具。

當使用者說「畫一張 XX」、「畫圖」、「生圖」時，請直接呼叫 Antigravity 內建的 `generate_image` 工具來進行生圖。

## 使用步驟
1. 直接呼叫 `generate_image` 工具：
   - `Prompt`：填入使用者的描述，如果需要，可自動翻譯或優化 Prompt（例如加上風格、配色等詞彙，並要求以繁體中文顯示文字）。
   - `ImageName`：設定適當的檔名（小寫加底線）。
2. 生圖完成後，提示使用者圖片已保存在 Artifacts 中，並詢問是否需要將圖片複製到專案的 `generated/` 目錄中。
