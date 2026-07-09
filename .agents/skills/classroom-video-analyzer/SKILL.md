---
name: classroom-video-analyzer
description: >-
  當使用者提供影片網址時，下載音檔（MP3 格式）、用 Whisper 轉譯生成 SRT 與完整逐字稿、擷取重點分析、引導生成至少 12 頁的 PPTX/HTML 課例研究簡報，並自動繪製用於 FB/IG 的核心概念社群圖檔。
---

# Classroom Video Analyzer

## Overview
本技能旨在提供全自動化的「課堂公開課影片分析與課例研究（Lesson Study）」工作流程。以影片網址（主要是 YouTube）為起點，自動提取高音質音訊、利用本地 Whisper 語音識別模型產出雙語/繁體中文 SRT 字幕及文字稿。接著，依據「傾聽（Listening）、串聯（Connecting）、回歸（Returning）」的觀課對話架構，以及「描述 $\rightarrow$ 詮釋 $\rightarrow$ 反思」三階層分析模型，自動生成至少 12 頁的課例分析簡報與 FB/IG 核心概念社群圖檔。

## Dependencies
*   `uv` 技能：用於執行與依賴的管理。
*   `yt-dlp` 與 `ffmpeg`：用於影片下載與轉碼。
*   `faster-whisper`：用於高精度、具備斷句的本地語音辨識。
*   `python-pptx`：用於自動化簡報（PowerPoint）的版面配置與寫入。
*   `pillow`：用於自動化核心概念圖片的排版與繪製。

## Quick Start
以下是引導 Agent 執行全流程分析的極簡指令示例：

1.  **擷取音訊**：
    ```bash
    uv run scripts/classroom_analyzer_helper.py fetch-audio "https://youtu.be/2qaBMMWbYDk" --output output/audio.mp3
    ```
2.  **語音轉譯**：
    ```bash
    uv run --with faster-whisper scripts/classroom_analyzer_helper.py transcribe output/audio.mp3 --output-srt output/subtitles.srt --output-txt output/transcript.txt --model medium
    ```
3.  **生成分析簡報**（需先將分析內容寫入 `output/analysis.txt`）：
    ```bash
    uv run --with python-pptx scripts/classroom_analyzer_helper.py generate-slides --analysis output/analysis.txt --output output/slides.pptx --style pastel
    ```
4.  **生成概念圖片**（需先將重點核心句寫入 `output/concept.txt`）：
    ```bash
    uv run --with pillow scripts/classroom_analyzer_helper.py generate-image --text output/concept.txt --output output/concept_post.png --style blue
    ```

## Utility Scripts
所有的核心功能均封裝在 CLI 輔助工具中。請使用 `uv run` 呼叫並搭配需要的套件依賴。

### 1. `fetch-audio` (下載影片音訊)
*   **指令格式**：`uv run scripts/classroom_analyzer_helper.py fetch-audio {URL} --output {PATH}`
*   **作用**：自動呼叫本地 `yt-dlp` 下載音訊並由 `ffmpeg` 轉成 MP3 格式。
*   **範例**：
    ```bash
    uv run scripts/classroom_analyzer_helper.py fetch-audio "https://youtu.be/SCW-T9SxsrM" --output output/audio3.mp3
    ```

### 2. `transcribe` (語音辨識轉譯)
*   **指令格式**：`uv run --with faster-whisper scripts/classroom_analyzer_helper.py transcribe {AUDIO_PATH} --output-srt {SRT_PATH} --output-txt {TXT_PATH} [--model {MODEL}] [--device {DEVICE}]`
*   **作用**：使用 Whisper 辨識中文發音，自動生成帶有時間戳記的 SRT 與不帶時間的 TXT 逐字稿。
*   **注意事項**：預設為 `cpu` 上執行 `medium` 模型，如果系統負載過重，模型會自動降級至 `small` 或 `base`。
*   **範例**：
    ```bash
    uv run --with faster-whisper scripts/classroom_analyzer_helper.py transcribe output/audio3.mp3 --output-srt output/subtitles3.srt --output-txt output/transcript3.txt --model medium
    ```

### 3. `generate-slides` (生成課例簡報)
*   **指令格式**：`uv run --with python-pptx scripts/classroom_analyzer_helper.py generate-slides --analysis {TXT_PATH} --output {PPTX_PATH} [--style {style}]`
*   **作用**：讀取包含 Markdown 標題及條列句的文本，自動拆分為至少 12 頁的 PPTX 投影片，並套用指定風格。
*   **簡報風格選單**：
    *   `modern`：現代極簡黑白風（預設）。
    *   `pastel`：粉彩柔和教育風。
    *   `blue`：科技商務藍風。
*   **範例**：
    ```bash
    uv run --with python-pptx scripts/classroom_analyzer_helper.py generate-slides --analysis output/analysis.txt --output output/slides.pptx --style pastel
    ```

### 4. `generate-image` (生成概念分享圖)
*   **指令格式**：`uv run --with pillow scripts/classroom_analyzer_helper.py generate-image --text {TXT_PATH} --output {PNG_PATH} [--style {style}]`
*   **作用**：讀取概念文字，自動繪製出適合 IG / FB 發布的 1080x1080 像素方圖。
*   **圖檔風格選單**：
    *   `modern`、`pastel`、`blue`、`dark` (暗黑學院風)。
*   **範例**：
    ```bash
    uv run --with pillow scripts/classroom_analyzer_helper.py generate-image --text output/concept.txt --output output/concept_post.png --style dark
    ```

## Rate Limiting
- 本地 Whisper 語音轉錄及圖片生成為純本地端計算，**無任何 Rate Limit 限制**。
- `fetch-audio` (調用 `yt-dlp` 下載) 會受限於 YouTube 的訪問速率限制。如果發生 HTTP 429 或 403 錯誤，腳本會自動進行退避重試。

## Common Mistakes
1.  **直接動筆計算而非先理解題意**：在引導使用者或自行撰寫分析報告時，切忌直接列出數學解題式，必須遵循公開課校長的要求，**「不要用算式，全用中文」**將算式先轉譯為物理概念。
2.  **漏掉簡報頁數要求**：生成的 PPTX 必須**至少包含 12 頁**。如果分析內容過少，必須對現有標題下的內容進行細化或自動添加專題討論投影片，確保大綱完整。
3.  **括號字元導致連結損壞**：在 Markdown 報告中如果引用了含有圓括號 `()` 的本地文件，必須將連結路徑中的 `(` 轉譯為 `%28`，`)` 轉譯為 `%29`，以防止渲染引擎解析失敗。
