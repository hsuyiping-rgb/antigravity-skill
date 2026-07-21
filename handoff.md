# 交接檔 (handoff.md)

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（若有 L3）。

## ⏯️ 目前做到哪
* 本機成功將專案中 20 個自訂技能全域安裝為 Antigravity 的 Plugin，任何人與任何目錄皆可呼叫。
* 成功完成 `ag-install-all` 一鍵全部安裝：建置好本機 Node.js (v26.4.0)、全域 npm 依賴 (`pptxgenjs`, `jsdom`, `@supabase/mcp-server-supabase`)、Python 依賴、以及與 NotebookLM、GitHub、Obsidian 的全套連線。
* 於專案根目錄建立了 `opencode.json`，將 Obsidian 連接指向實體路徑 `G:\我的雲端硬碟\secondbrain`。

## 🚦 目前狀態
* 運行環境與全域技能已完全配置並驗證成功，目前專案 Git 狀態有新檔案（`opencode.json` 等）待同步。

## ➡️ 下一步
1. 下次開工時，直接對助理說「開工」或「我來了」即可讀取此交接檔案。
2. 可利用「製作 YAML 簡報」或「做純圖片簡報」測試簡報生圖引擎是否正常。
3. (選用) 在 AI Studio 申請免費 API key 並建立 `~/.gemini.env` 檔供 API 技能使用。

## ⚠️ 注意事項
* 本次安裝使用了 `winget` 來配置本機 Node.js & npm。如果未來執行時出現指令找不到，請重開終端機或重載助理以重新讀取最新 PATH 環境變數。

## 🕐 最後更新
- 時間：2026-07-21 20:30
- 更新者：Antigravity @ KFES
- Git push：待推
