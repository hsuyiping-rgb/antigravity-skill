---
name: ag-obsidian
description: Antigravity 連接 Obsidian MCPVault。說「連接 Obsidian」時載入。
---

# 連接 Obsidian（Antigravity 版）

1. 找 vault 路徑：搜尋含 `.obsidian` 子資料夾的目錄
2. `npm install -g @bitbonsai/mcpvault`
3. 手動編輯專案根目錄的 `opencode.json`，在 `mcpServers` 中新增 obsidian 配置（指令為 `npx @bitbonsai/mcpvault <VAULT_PATH>`）
4. 重啟後驗證讀寫

### 進階
若需全文檢索：安裝 Obsidian Local REST API plugin + `pip install cli-anything-hub && cli-hub install obsidian`

回報：vault 路徑、mcpvault 版本、讀取/寫入測試結果。
