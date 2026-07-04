import os
import sys
import re
import json
import urllib.request
import urllib.parse
import html
import time
import subprocess
import argparse
from html.parser import HTMLParser

# ----------------------------------------------------------------------
# HTML Parser for Text Extraction
# ----------------------------------------------------------------------
class WebTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.in_script_or_style = False
        self.links = []
        self.tables = []
        self.current_table = None
        self.current_row = None
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.in_script_or_style = True
        elif tag == 'a':
            for attr, val in attrs:
                if attr == 'href' and val:
                    self.links.append(val)
        elif tag == 'table':
            self.current_table = []
        elif tag == 'tr' and self.current_table is not None:
            self.current_row = []
        elif tag in ['td', 'th'] and self.current_row is not None:
            self.current_cell = []

    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script_or_style = False
        elif tag == 'table' and self.current_table is not None:
            self.tables.append(self.current_table)
            self.current_table = None
        elif tag == 'tr' and self.current_row is not None:
            self.current_table.append(self.current_row)
            self.current_row = None
        elif tag in ['td', 'th'] and self.current_cell is not None:
            cell_text = "".join(self.current_cell).strip()
            self.current_row.append(cell_text)
            self.current_cell = None

    def handle_data(self, data):
        if self.in_script_or_style:
            return
        if self.current_cell is not None:
            self.current_cell.append(data)
        self.text_content.append(data)

    def get_clean_text(self):
        full_text = " ".join(self.text_content)
        # Unescape HTML entities
        full_text = html.unescape(full_text)
        # Normalize whitespace
        full_text = re.sub(r'\s+', '\n', full_text)
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]
        
        # Filter out boilerplate
        clean_lines = []
        for line in lines:
            if any(term in line for term in ["WIZ_global_data", "timing", "ppConfig", "WIZ", "goog", "Atari", "atari", "Google", "google"]):
                continue
            if len(line) < 2:
                continue
            clean_lines.append(line)
        return "\n".join(clean_lines)

# ----------------------------------------------------------------------
# Crawler Implementation
# ----------------------------------------------------------------------
def fetch_url(url, headers):
    try:
        parsed = urllib.parse.urlparse(url)
        encoded_path = urllib.parse.quote(parsed.path)
        encoded_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, encoded_path, parsed.params, parsed.query, parsed.fragment))
        
        req = urllib.request.Request(encoded_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None

def crawl_site(base_url, max_depth=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    visited = set()
    to_visit = [(base_url, 1)]
    crawled_data = {}
    
    keywords = ["行政", "組織", "成員", "電話", "分機", "簡介", "交通", "願景", "招生", "幼兒園", "家長"]
    
    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)
        
        print(f"Crawling: {url} (Depth: {depth})...")
        html_content = fetch_url(url, headers)
        if not html_content:
            continue
            
        parser = WebTextExtractor()
        try:
            parser.feed(html_content)
        except Exception as e:
            print(f"  Warning: Parser error on {url}: {e}", file=sys.stderr)
            continue
            
        clean_text = parser.get_clean_text()
        crawled_data[url] = {
            "text": clean_text,
            "tables": parser.tables
        }
        
        # Extract and filter child links
        if depth < max_depth:
            for link in parser.links:
                full_link = urllib.parse.urljoin(url, link)
                # Normalize link
                full_link = full_link.split('#')[0]
                if full_link in visited:
                    continue
                
                # Verify link belongs to the same domain or Google Sites reference
                parsed_base = urllib.parse.urlparse(base_url)
                parsed_link = urllib.parse.urlparse(full_link)
                
                is_same_domain = parsed_link.netloc == parsed_base.netloc
                is_subsite_link = any(kw in urllib.parse.unquote(full_link) for kw in keywords) or "sites.google.com" in parsed_link.netloc
                
                if (is_same_domain or is_subsite_link) and parsed_link.scheme in ['http', 'https']:
                    to_visit.append((full_link, depth + 1))
        
        time.sleep(1) # Politeness delay
        
    return crawled_data

# ----------------------------------------------------------------------
# Knowledge Base Classifier
# ----------------------------------------------------------------------
def structure_qa_data(crawled_data):
    # Standard keys in chatKnowledgeBase
    qa_db = {
        "交通": "",
        "電話": "",
        "行政組織": "",
        "幼兒園": "",
        "家長會": "",
        "最新": "",
        "認識": "",
        "處室": "",
        "平台": "",
        "最新消息": ""
    }
    
    # Simple heuristics to categorize scraped pages
    for url, data in crawled_data.items():
        text = data["text"]
        tables = data["tables"]
        
        decoded_url = urllib.parse.unquote(url).lower()
        
        # Categorize
        if "交通" in decoded_url or "位置" in decoded_url or "地圖" in decoded_url:
            qa_db["交通"] += f"\n--- 來源: {url} ---\n" + text
        elif "電話" in decoded_url or "分機" in decoded_url:
            qa_db["電話"] += f"\n--- 來源: {url} ---\n" + text
        elif "行政" in decoded_url or "成員" in decoded_url or "組織" in decoded_url:
            qa_db["行政組織"] += f"\n--- 來源: {url} ---\n" + text
            # Format tables if any
            for table in tables:
                for row in table:
                    qa_db["行政組織"] += f"\n🔹 " + " | ".join(row)
        elif "幼" in decoded_url or "kid" in decoded_url or "child" in decoded_url:
            qa_db["幼兒園"] += f"\n--- 來源: {url} ---\n" + text
        elif "家長" in decoded_url or "parent" in decoded_url:
            qa_db["家長會"] += f"\n--- 來源: {url} ---\n" + text
        elif "最新" in decoded_url or "新聞" in decoded_url or "榮譽" in decoded_url:
            qa_db["最新消息"] += f"\n--- 來源: {url} ---\n" + text
        elif "簡介" in decoded_url or "願景" in decoded_url or "認識" in decoded_url or "校史" in decoded_url:
            qa_db["認識"] += f"\n--- 來源: {url} ---\n" + text
        else:
            # Fallback based on keywords inside text
            if "交通" in text or "捷運" in text or "公車" in text:
                qa_db["交通"] += f"\n--- 來源: {url} ---\n" + text[:2000] # Limit size
            elif "分機" in text or "電話" in text:
                qa_db["電話"] += f"\n--- 來源: {url} ---\n" + text[:2000]
            elif "處室" in text or "主任" in text or "組長" in text:
                qa_db["行政組織"] += f"\n--- 來源: {url} ---\n" + text[:2000]
            else:
                # Add to general recognition
                qa_db["認識"] += f"\n--- 來源: {url} ---\n" + text[:1000]

    # Clean and summarize each category
    for key in qa_db:
        raw_text = qa_db[key].strip()
        if not raw_text:
            qa_db[key] = f"關於本校的{key}資訊，目前仍在整理建置中，歡迎您稍後再進行查詢！"
        else:
            # Clean text block to match markdown styles
            # Remove multiple redundant empty lines
            cleaned = re.sub(r'\n{3,}', '\n\n', raw_text)
            qa_db[key] = cleaned
            
    return qa_db

# ----------------------------------------------------------------------
# File Generation
# ----------------------------------------------------------------------
def generate_files(school_name, sec_name, qa_data, features, templates_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)
    
    # Load templates
    with open(os.path.join(templates_dir, "index.html.template"), "r", encoding="utf-8") as f:
        html_tpl = f.read()
    with open(os.path.join(templates_dir, "styles.css.template"), "r", encoding="utf-8") as f:
        css_tpl = f.read()
    with open(os.path.join(templates_dir, "app.js.template"), "r", encoding="utf-8") as f:
        js_tpl = f.read()
        
    # Replacements
    # HTML
    html_out = html_tpl.replace("{{SCHOOL_NAME}}", school_name)
    html_out = html_out.replace("{{SECRETARY_NAME}}", sec_name)
    
    # JS
    js_out = js_tpl.replace("{{SCHOOL_NAME}}", school_name)
    js_out = js_out.replace("{{SECRETARY_NAME}}", sec_name)
    
    # JSON Data inject
    # Ensure escaped JS template strings
    escaped_qa = {}
    for k, v in qa_data.items():
        # Escape backticks and backslashes for JS Template Literals
        escaped_val = v.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        escaped_qa[k] = escaped_val
        
    qa_json_str = json.dumps(escaped_qa, ensure_ascii=False, indent=2)
    # We strip the outer curly brackets from JSON and format as JS Object Literal
    js_out = js_out.replace("{{KNOWLEDGE_BASE_JSON}}", qa_json_str)
    
    # Write output
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    with open(os.path.join(out_dir, "styles.css"), "w", encoding="utf-8") as f:
        f.write(css_tpl)
    with open(os.path.join(out_dir, "app.js"), "w", encoding="utf-8") as f:
        f.write(js_out)
        
    print(f"Generated index.html, styles.css, app.js in: {out_dir}")

# ----------------------------------------------------------------------
# Automated Mock DOM Testing
# ----------------------------------------------------------------------
def run_dom_test(project_dir):
    test_runner_code = """
const fs = require('fs');
const path = require('path');

// Mock DOM
const mockElements = {};
const listeners = {};

class MockElement {
  constructor(id, tagName = 'div') {
    this.id = id;
    this.tagName = tagName.toUpperCase();
    this.classList = {
      classes: new Set(),
      add(...c) { c.forEach(x => this.classes.add(x)); },
      remove(x) { this.classes.delete(x); },
      contains(x) { return this.classes.has(x); }
    };
    this.style = {};
    this.value = '';
    this.textContent = '';
    this.innerHTML = '';
    this.eventListeners = {};
    this.parentElement = this;
  }
  addEventListener(event, cb) {
    if (!this.eventListeners[event]) this.eventListeners[event] = [];
    this.eventListeners[event].push(cb);
  }
  dispatchEvent(event, ...args) {
    if (this.eventListeners[event]) this.eventListeners[event].forEach(cb => cb(...args));
  }
  setAttribute(k, v) { this[k] = v; }
  getAttribute(k) { return ''; }
  querySelector(sel) { return null; }
  querySelectorAll(sel) { return []; }
  appendChild(c) {}
  remove() {}
}

global.document = {
  addEventListener(event, cb) { listeners[event] = cb; },
  getElementById(id) {
    if (!mockElements[id]) mockElements[id] = new MockElement(id);
    return mockElements[id];
  },
  querySelector(sel) {
    if (sel === '.chat-chips') return this.getElementById('chat-chips');
    if (sel === '.sidebar') return this.getElementById('sidebar');
    return null;
  },
  querySelectorAll() { return []; },
  createElement(tag) { return new MockElement(null, tag); }
};

global.window = {
  addEventListener(event, cb) { listeners[event] = cb; },
  localStorage: {
    store: {},
    getItem(k) { return this.store[k] || null; },
    setItem(k, v) { this.store[k] = String(v); },
    removeItem(k) { delete this.store[k]; }
  }
};
global.localStorage = global.window.localStorage;

try {
  const appJsCode = fs.readFileSync(path.join(__dirname, 'app.js'), 'utf8');
  eval(appJsCode);
  if (listeners['DOMContentLoaded']) {
    listeners['DOMContentLoaded']();
  }
  console.log("SUCCESS: app.js loaded and DOMContentLoaded fired successfully!");
  process.exit(0);
} catch (e) {
  console.error("ERROR: Mock DOM execution failed!");
  console.error(e.stack);
  process.exit(1);
}
"""
    test_runner_path = os.path.join(project_dir, "test_runner.js")
    with open(test_runner_path, "w", encoding="utf-8") as f:
        f.write(test_runner_code)
        
    try:
        res = subprocess.run(["node", test_runner_path], capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            print("Mock DOM Test Verification: PASSED")
            print(res.stdout)
            # Clean up
            os.remove(test_runner_path)
            return True
        else:
            print("Mock DOM Test Verification: FAILED", file=sys.stderr)
            print(res.stderr, file=sys.stderr)
            return False
    except Exception as e:
        print(f"Mock DOM Test Execution failed: {e}", file=sys.stderr)
        return False

# ----------------------------------------------------------------------
# Main Entry CLI
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="School AI Secretary Builder CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl school website Q&A data")
    crawl_parser.add_argument("--url", required=True, help="Base URL of school site")
    crawl_parser.add_argument("--depth", type=int, default=2, help="Crawling recursion depth")
    crawl_parser.add_argument("--output", required=True, help="Output path for cleaned JSON")
    
    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate code files from templates")
    gen_parser.add_argument("--school-name", required=True, help="Name of school")
    gen_parser.add_argument("--sec-name", default="小光", help="Name of chatbot secretary")
    gen_parser.add_argument("--data", required=True, help="Cleaned crawling JSON data file")
    gen_parser.add_argument("--features", default="gemini,RAG", help="Comma-separated optional features")
    gen_parser.add_argument("--out-dir", required=True, help="Destination directory")
    
    # test command
    test_parser = subparsers.add_parser("test", help="Verify generated code using Node.js Mock DOM")
    test_parser.add_argument("--dir", required=True, help="Project directory containing app.js")
    
    # build command
    build_parser = subparsers.add_parser("build", help="Run crawl, generate, and test in sequence")
    build_parser.add_argument("--url", required=True, help="School website base URL")
    build_parser.add_argument("--name", required=True, help="School official name")
    build_parser.add_argument("--sec-name", default="小光", help="Secretary chatbot name")
    build_parser.add_argument("--out-dir", required=True, help="Project output folder")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")
    
    if args.command == "crawl":
        print(f"Starting crawl for: {args.url}")
        crawled = crawl_site(args.url, args.depth)
        qa_data = structure_qa_data(crawled)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(qa_data, f, ensure_ascii=False, indent=2)
        print(f"Crawl complete! Saved to: {args.output}")
        
    elif args.command == "generate":
        print(f"Generating project code files...")
        with open(args.data, "r", encoding="utf-8") as f:
            qa_data = json.load(f)
        generate_files(args.school_name, args.sec_name, qa_data, args.features.split(','), templates_dir, args.out_dir)
        
    elif args.command == "test":
        print(f"Running DOM tests...")
        success = run_dom_test(args.dir)
        if not success:
            sys.exit(1)
            
    elif args.command == "build":
        print(f"=== [Phase 1/3] Crawling {args.url} ===")
        crawled = crawl_site(args.url, max_depth=2)
        qa_data = structure_qa_data(crawled)
        
        temp_data_path = os.path.join(args.out_dir, "temp_crawled_data.json")
        os.makedirs(args.out_dir, exist_ok=True)
        with open(temp_data_path, "w", encoding="utf-8") as f:
            json.dump(qa_data, f, ensure_ascii=False, indent=2)
            
        print(f"=== [Phase 2/3] Generating Project Files ===")
        generate_files(args.name, args.sec_name, qa_data, ["gemini", "RAG"], templates_dir, args.out_dir)
        
        print(f"=== [Phase 3/3] Running DOM Verification Tests ===")
        success = run_dom_test(args.out_dir)
        
        # Clean temp data
        if os.path.exists(temp_data_path):
            os.remove(temp_data_path)
            
        if not success:
            print("Build FAILED during DOM tests verification.", file=sys.stderr)
            sys.exit(1)
        else:
            print("Build COMPLETED successfully!")

if __name__ == "__main__":
    main()
