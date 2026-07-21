# antigravity-skill (專案藍圖)

> 本檔為跨 Agent 通用的專案藍圖（AGENTS.md 開放標準）。任何 Agent 的每個 session 都應先讀本檔＋`handoff.md`。

## 專案簡介
本專案為 Antigravity (Gemini AI 助理) 教學與自動化自訂技能集倉庫，提供簡報製作、公開課研究、服務連接與跨電腦管理能力。

## 關鍵時程
- 專案打包與全平台技能安裝完成：2026-07-21

## 目標與路線圖
- [x] 階段一：實作學習共同體分析技能 (`slc-skill`)，包含 Whisper、去評價、日系抹茶綠水彩生圖與 Touch Swipe 網頁簡報。
- [x] 階段二：轉換並安裝 `claude-code-lazy-packs` 中的 12 個雲端與本地連線技能，並改造 `ag-draw` 為免費原生生圖版。
- [x] 階段三：轉換並安裝 `cross-device-agent-skills` 中的專案管理三部曲 (`ag-project-init`, `ag-startup`, `ag-shutdown`)，自動填寫帳號及 email。
- [x] 階段四：轉換並安裝 `yaml-image-deck` 簡報生圖技能，並進行相容性與語意對齊調整。
- [x] 階段五：將 16 個技能打包拷貝至專案的 `.agents/skills/` 中，更新 `README.md` 並推播 GitHub。

## 資料夾結構
* `.agents/skills/` - 本地存放的 20 個自訂技能
* `test-page/` - 網頁測試檔案
* `09-AntiGravity專屬懶人包.md` - 全平台服務連線指南
* `10-AntiGravity專屬懶人包-跨電腦專案與YAML簡報生圖.md` - 專案管理與 YAML 簡報指南
* `ANTIGRAVITY.md` - 專案駕駛艙與關鍵字觸發配置
* `README.md` - 專案總覽與全技能樹狀圖

## 同步層級（本專案初始化至第 L3 層級）

| 層級 | 平台 | 位置 | 讀取時機 |
|------|------|------|---------|
| L1 | 本地（GDrive） | `agents.md`＋`handoff.md` | 每個 session |
| L2 | GitHub | [hsuyiping-rgb/antigravity-skill](https://github.com/hsuyiping-rgb/antigravity-skill) | 指定時 |
| L3 | Obsidian | `secondbrain` 知識庫與工作流程 (G:\我的雲端硬碟\secondbrain) | 有需要時 |

## 工作約定
- 任何 Agent、任何電腦：**開工先讀 `handoff.md`，收工必更新 `handoff.md`**
- 修改共用檔案前先讀最新內容，避免覆蓋其他 Agent 的變更
- 所有回應與文件使用繁體中文
- 修改前先確認計畫，優先保留原有資料結構
