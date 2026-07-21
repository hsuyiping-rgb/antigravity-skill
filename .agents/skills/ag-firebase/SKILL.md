---
name: ag-firebase
description: Antigravity 連接 Firebase MCP。說「連接 Firebase」時載入。
---

# 連接 Firebase（Antigravity 版）

1. `npm install -g firebase-tools` → `firebase login`
2. 在專案目錄 `firebase init`
3. 手動編輯專案根目錄的 `opencode.json`，在 `mcpServers` 中新增 firebase 配置（指令為 `npx -y firebase-tools@latest mcp`）
4. 重啟後驗證：列出專案

⚠️ Admin SDK 憑證不可公開，學生資料只存代號。
