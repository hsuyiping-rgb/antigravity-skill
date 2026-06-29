# 🌌 Anti-Gravity 2 專案駕駛艙 (ANTIGRAVITY.md)

歡迎來到專案自動化控制中心。本檔案定義了專案的 **自動化 SOP 技能**。當您對 AI 助理說出對應關鍵字時，將會自動觸發以下高階工作流：

---

## 🟢 技能一：開工 / 我來了 (Start Work Flow)

> [!NOTE]
> **觸發關鍵字**：`開工`、`我來了`
> **自動化執行步驟**：
> 1. **確認 Git 倉庫狀態**：執行 `git status` 與 `git branch -a`，檢查當前是否位於正確的工作分支。
> 2. **同步遠端變更**：執行 `git log -n 5`，並拉取遠端最新代碼以避免衝突。
> 3. **讀取 Obsidian 每日筆記**：
>    - 讀取 `G:\我的雲端硬碟\secondbrain\每日筆記\`（或您的 Obsidian Vault 每日筆記目錄）中最新的筆記。
>    - 尋找「上次做到哪」與「下一步計畫」。
> 4. **產生開工簡報**：
>    - 彙整當前代碼狀態與筆記內容。
>    - 提供今天的第一步具體行動建議。

---

## 🔴 技能二：收工 / 下班了 (End Work Flow)

> [!WARNING]
> **觸發關鍵字**：`收工`、`下班了`
> **自動化執行步驟**：
> 1. **資安防護掃描**：
>    - 掃描專案內所有檔案，確保沒有 `.env`、API Key 或任何敏感金鑰被誤寫入代碼（尤其防範將金鑰上傳至 GitHub）。
> 2. **自動 Git 提交與推播**：
>    - 執行 `git status` 檢查有變動的檔案。
>    - 執行 `git add .`。
>    - 自動分析代碼變更，產生結構化且符合 Git Commit 規範的 commit message。
>    - 執行 `git commit -m "[訊息]"` 並 `git push` 到遠端倉庫。
> 3. **寫入 Obsidian 每日筆記**：
>    - 自動在您的 Obsidian 每日筆記中，追加今日的「已完成工作」與「留待明日待辦事項」，實現今日事今日畢。

---

## 🔵 技能三：初始化專案 (Initialize Project Flow)

> [!IMPORTANT]
> **觸發關鍵字**：`初始化專案`
> **自動化執行步驟**：
> 1. **基礎建設部署**：
>    - 在根目錄自動產生 `ANTIGRAVITY.md`、優質的 `.gitignore`、以及專案說明首頁 `README.md`。
> 2. **Git 本地初始化**：
>    - 執行 `git init`，並進行 initial commit 提交。
> 3. **建立雲端倉庫**：
>    - 呼叫 `gh repo create`，以互動式或自動式在 GitHub 上建立同名遠端倉庫，並自動將本地代碼 `git push -u origin main`。
> 4. **Obsidian 工作區對接**：
>    - 直接在您的 Obsidian 第二大腦中，同步建立一個對應此專案的工作資料夾與規劃檔案。

---

## 🛠️ 本地 MCP 與服務配置資訊
* **NotebookLM CLI**: 已安裝，支援 `nlm` 指令。
* **Firebase CLI**: 已安裝，支援 `cmd /c firebase` 指令。
* **Obsidian MCP**: 設定檔 `opencode.json` 已配置，路徑指向 `G:\我的雲端硬碟\secondbrain`。
