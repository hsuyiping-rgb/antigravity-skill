# Classroom Video Analyzer 🎬📝📊

一個專為「學習共同體課堂公開課（Lesson Study）」打造的自動化影片分析與課例研究工具包。

本工具以影片網址（如 YouTube）為核心輸入，自動提取高音質音訊、利用本地 Whisper 語音識別模型產出繁體中文 SRT 字幕及逐字稿，並能依據課例對話架構自動生成簡報大綱（PPTX 投影片）與適合 FB/IG 分享的核心概念社群圖檔。

---

## 🛠️ 核心功能 (Core Features)

1.  **音訊擷取 (`fetch-audio`)**：自動下載影片音軌並轉碼為高音質 MP3。
2.  **語音轉譯 (`transcribe`)**：調用本地高精度 `faster-whisper` 模型進行中文語音辨識，產出帶時間戳記的 SRT 字幕與不帶時間戳記的 TXT 逐字稿。
3.  **簡報生成 (`generate-slides`)**：讀取 Markdown 格式的對比分析報告，自動編排並生成至少 12 頁的 PPTX 投影片，支援多種設計風格。
4.  **概念圖繪製 (`generate-image`)**：自動將課堂核心概念字句排版並繪製成 1080x1080 像素的 FB/IG 社群分享圖。

---

## 📂 目錄結構 (Directory Structure)

```text
classroom-video-analyzer/
├── SKILL.md                              # Gemini Agent 技能引導文件
├── README.md                             # 專案說明文件 (本檔案)
├── .gitignore                            # Git 忽略清單
└── scripts/
    └── classroom_analyzer_helper.py      # 核心 CLI 自動化腳本 (Python)
```

---

## 📥 安裝與設定 (Installation & Setup)

要將此技能（Skill）安裝至您本機的 Gemini Agent 全域自訂路徑，以利於在任何工作區中直接呼叫，請遵循以下步驟：

### 1. 複製專案至全域自訂技能路徑
開啟終端機（如 PowerShell 或 CMD），執行以下指令將本專案 Clone 到您的全域設定目錄中：
```powershell
git clone https://github.com/hsuyiping-rgb/classroom-video-analyzer.git C:\Users\vm\.gemini\config\skills\classroom-video-analyzer
```
*(備註：若目錄中無 `skills` 資料夾，Git 會自動為您建立。)*

### 2. 安裝環境依賴 (Prerequisites)
確保您的系統上已安裝以下核心依賴：
1. **Python 3.8+** 與 **[uv](https://github.com/astral-sh/uv)**：Python 依賴管理工具。
2. **ffmpeg**：用於音訊轉碼。
   * **Windows 安裝命令**：
     ```powershell
     winget install Gyan.FFmpeg
     ```
     *(安裝完後需重新開啟終端機以載入環境變數)*
3. **yt-dlp**：用於下載影片音訊。

### 3. 驗證全域安裝
在您的終端機中執行以下命令，以確認 CLI 腳本可以成功載入與執行：
```powershell
uv run C:\Users\vm\.gemini\config\skills\classroom-video-analyzer\scripts\classroom_analyzer_helper.py --help
```
若成功輸出 CLI 的說明手冊（如下所示），代表安裝已順利完成！
```text
usage: classroom_analyzer_helper.py [-h] {fetch-audio,transcribe,generate-slides,generate-image} ...
```
之後，Gemini 系統在每次對話啟動時，皆會自動載入並辨識此目錄下的 `SKILL.md` 技能指引，您可以直接在對話中指示 AI Agent 執行該技能！

---

## 🚀 快速開始與使用說明 (CLI Usage)

所有核心功能均封裝在 `scripts/classroom_analyzer_helper.py` 中。請使用 `uv run` 自動安裝與載入依賴套件。

### 1. 擷取影片音軌
下載 YouTube 影片並轉為 MP3 音檔：
```bash
uv run scripts/classroom_analyzer_helper.py fetch-audio "https://youtu.be/2qaBMMWbYDk" --output output/audio.mp3
```

### 2. 本地語音辨識轉譯
使用 Whisper 模型（預設為 `medium`，會自動嘗試 `small`/`base` 作為硬體限制時的備用方案）產生 SRT 字幕與 TXT 逐字稿：
```bash
uv run --with faster-whisper scripts/classroom_analyzer_helper.py transcribe output/audio.mp3 --output-srt output/subtitles.srt --output-txt output/transcript.txt --model medium
```
*參數說明：*
*   `--model`：可選模型大小（`tiny`, `base`, `small`, `medium`, `large`）。
*   `--device`：預設為 `cpu`，若有 NVIDIA 顯卡環境可設為 `cuda` 加速。

### 3. 生成課例研究簡報 (PPTX)
讀取 Markdown 分析文字，自動切割並排版為至少 12 頁的 PPTX 投影片：
```bash
uv run --with python-pptx scripts/classroom_analyzer_helper.py generate-slides --analysis output/analysis.txt --output output/slides.pptx --style pastel
```
*風格風格選擇 (`--style`)：*
*   `modern`：現代極簡黑白風（預設）。
*   `pastel`：粉彩柔和教育風。
*   `blue`：科技商務藍風。

### 4. 生成社群概念分享圖 (PNG)
讀取核心摘要字句（每行一句，最多 8 行），產生符合 IG/FB 版面（1080x1080）的繁體中文分享圖：
```bash
uv run --with pillow scripts/classroom_analyzer_helper.py generate-image --text output/concept.txt --output output/concept_post.png --style dark
```
*圖檔風格選擇 (`--style`)：*
*   `modern`、`pastel`、`blue`、`dark` (暗黑學院風)。

---

## 📝 授權條款 (License)

本專案基於 MIT 授權條款發布。歡迎自由修改與分享！
