---
name: ag-supabase
description: Antigravity 連接 Supabase MCP。說「連接 Supabase」時載入。
---

# 連接 Supabase（Antigravity 版）

1. 安裝：`npm install -g @supabase/mcp-server-supabase`
2. 登入 Supabase → 取得 project ref + API key
3. 手動編輯專案根目錄的 `opencode.json`，在 `mcpServers` 中新增 supabase 配置（指令為 `npx @supabase/mcp-server-supabase --project-ref <ref> --api-key <key>`）
4. 重啟後驗證：查詢資料庫表格

⚠️ 不把 API key 寫進 ANTIGRAVITY.md 或 repo。
