---
name: github-pages-deployer
description: >
  GitHub Pages 網頁發佈助手。當使用者要求「發佈網頁到 GitHub」、「部署網頁到 GitHub Pages」、
  「幫我把這個網頁發佈出去」、「啟動 GitHub Pages 網頁發佈」、「網頁上線」、「架設靜態網頁」等任何需要將靜態網頁（HTML/CSS/JS）
  發佈至 GitHub Pages 的情境時，請一定要使用此技能。此技能會自動初始化 Git、建立/連接 GitHub 公開儲存庫、
  推播網頁檔案，並利用 GitHub API 自動啟用 GitHub Pages，最後回報公開的網頁網址。
---

# GitHub Pages 網頁發佈助手 (github-pages-deployer)

本技能協助您將本地的靜態網頁（包含 `index.html` 等 HTML/CSS/JS 資源）快速且自動地發佈到 GitHub Pages 上。

---

## 觸發情境
當使用者提出以下或類似請求時：
- 「幫我把這個網頁發佈到 GitHub Pages」
- 「把這個網站上線到 GitHub」
- 「我想部署這個網頁」
- 「靜態網站架設與發佈」

---

## 執行 SOP

### 步驟 1：偵測與確認網頁檔案
- 檢查當前工作目錄是否存在 `index.html`。
- 如果當前目錄沒有，但在子目錄中（例如 `dist/` 或 `tools/coordinate-hunter/`），詢問使用者要發佈哪一個資料夾。
- 確定發佈的根目錄路徑。

### 步驟 2：初始化 Git 本地倉庫（若尚未初始化）
- 檢查該目錄下是否存在 `.git/`。
- 若無，執行：
  ```powershell
  git init
  git config windows.appendAtomically false
  ```
  *(註：`windows.appendAtomically false` 是為了解決 Google Drive 同步衝突，若在雲端硬碟下務必執行)*
- 建立一個標準的 `.gitignore`，確保排除 `.claude/`、`.gemini/` 以及敏感憑證（如 `.env`）。

### 步驟 3：提交本地變更
- 執行 `git status` 檢查是否有未提交的檔案。
- 將所有相關網頁檔案加入暫存區：
  ```powershell
  git add .
  ```
- 提交變更：
  ```powershell
  git commit -m "deploy: publish webpage via GitHub Pages"
  ```

### 步驟 4：確認 GitHub 遠端儲存庫與推播
- 執行以下指令檢查是否已設定 `origin` 遠端倉庫：
  ```powershell
  $env:GITHUB_TOKEN=""; git remote -v
  ```
- **若尚未設定遠端**：
  - 詢問使用者 GitHub 倉庫名稱（預設為當前資料夾名稱）。
  - 執行以下指令建立一個公開儲存庫並推播上去（GitHub Pages 免費版需為公開倉庫）：
    ```powershell
    $env:GITHUB_TOKEN=""; gh repo create "<repo-name>" --public --source=. --push
    ```
- **若已設定遠端**：
  - 取得當前分支名稱：
    ```powershell
    git branch --show-current
    ```
  - 推播最新代碼：
    ```powershell
    $env:GITHUB_TOKEN=""; git push -u origin <branch_name>
    ```

### 步驟 5：啟用 GitHub Pages (透過 REST API)
- 從 Git 遠端 URL 中擷取使用者名稱（Owner）與倉庫名稱（Repo）。
  - 例如：`https://github.com/owner/repo.git` 中的 `<owner>` 為 `owner`，`<repo>` 為 `repo`。
- 執行以下 API 呼叫，為該倉庫啟用 GitHub Pages 服務（預設指定當前分支為來源，目錄為 `/` 根目錄）：
  ```powershell
  $env:GITHUB_TOKEN=""; gh api -X POST /repos/<owner>/<repo>/pages -f source[branch]=<branch_name> -f source[path]=/
  ```
  *(註：如果 API 回傳 `409 Conflict` 代表該儲存庫的 Pages 已經啟動，此為正常現象，可直接跳到下一步)*

### 步驟 6：回報網頁網址
- 計算出該網頁的公開存取網址：
  `https://<owner>.github.io/<repo>/` (如果發佈的是子目錄，請加上子路徑)
- 將網址以顯眼的卡片形式呈獻給使用者，恭喜網頁成功上線！
