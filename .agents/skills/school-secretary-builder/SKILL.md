---
name: school-secretary-builder
description: >-
  Automates crawling school websites, extracting structured Q&A, and building
  a customizable, responsive AI Secretary chatbot application with Gemini API
  and local fallback, complete with automated DOM testing.
---

# School AI Secretary Builder

A global utility for building and maintaining responsive "AI Secretary" chatbot web applications for schools. It automates the scraping of official school websites, structural text extraction, code generation from clean HTML/CSS/JS templates, and automated validation using a Node.js Mock DOM environment.

## Dependencies
- Node.js (for headless mock DOM testing)
- Python 3.10+ (standard libraries only)

## Quick Start

To crawl a school website and build a new AI Secretary app from scratch:

```bash
uv run python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py build \
  --url "https://www.kfes.ntpc.edu.tw" \
  --name "中和區光復國小" \
  --sec-name "小光" \
  --out-dir "./my-new-secretary"
```

## Utility Scripts

The builder CLI script is located at `C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py`.

### Command Reference

#### 1. `crawl`
Crawls the main page and subpages (including Google Sites links) of a school website. It sanitizes HTML, strips boilerplate, and outputs structured text to a JSON file.

```bash
uv run python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py crawl \
  --url "https://www.kfes.ntpc.edu.tw" \
  --output "scraped_data.json"
```

#### 2. `generate`
Generates `index.html`, `styles.css`, and `app.js` using customizable templates, inserting crawled data into `chatKnowledgeBase`.

```bash
uv run python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py generate \
  --school-name "光復國小" \
  --sec-name "小光" \
  --data "scraped_data.json" \
  --out-dir "./dist"
```

#### 3. `test`
Generates a mock DOM test environment using Node.js and verifies Q&A matching logic.

```bash
uv run python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py test \
  --dir "./dist"
```

#### 4. `build`
Runs `crawl`, `generate`, and `test` in sequence.

```bash
uv run python C:\Users\vm\.gemini\config\skills\school-secretary-builder\scripts\builder_cli.py build \
  --url "https://www.kfes.ntpc.edu.tw" \
  --name "光復國小" \
  --sec-name "小光" \
  --out-dir "./dist"
```

## Common Mistakes
- **Node.js Missing**: The `test` command requires Node.js to be installed on the system to execute Mock DOM verification.
- **Path Spaces**: When calling on Windows, ensure paths containing spaces or Chinese characters are double-quoted.
