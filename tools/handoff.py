#!/usr/bin/env python3
"""交接包盤點與檢查（只用 Python 標準庫，不需安裝任何套件）。

    python3 tools/handoff.py inventory   # 從 HTML 重新產生 handoff/content.md、handoff/assets.md
    python3 tools/handoff.py check       # 改完 HTML 後跑：缺圖、清單過期、色票外的色值

HTML 是正本。content.md / assets.md 都是這支腳本產生的，不要手改。
"""
import os
import re
import struct
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "business-groups.html"]          # 正本頁面
ARCHIVE_DIR = "archive"                                  # 封存頁：只檢查引用，不列文案
ASSETS_DIR = "assets"
OUT_DIR = "handoff"

# DESIGN-SYSTEM.md §1 的 11 色，外加白色簡寫
PALETTE = {"#e21e28", "#a0151c", "#811117", "#f39ea3", "#262626", "#595959",
           "#959595", "#bfbfbf", "#d9d9d9", "#f6f6f6", "#ffffff", "#fff"}

# DESIGN-SYSTEM.md「刻意破格的色值」：(頁面, CSS 選擇器, 色值)
COLOR_EXCEPTIONS = {
    ("index.html", ".btn--ghost:active", "#000"),
    ("index.html", ".hero__stats::before", "#25282f"),
    ("index.html", ".hero__stats::before", "#030508"),
}

CONTAINERS = {"head", "section", "header", "footer", "nav"}
BLOCKS = {"title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "a", "button", "label",
          "figcaption", "blockquote", "dt", "dd", "td", "th", "caption", "summary",
          "div", "legend", "option"}
VOID = {"img", "br", "hr", "input", "meta", "link", "source", "wbr", "area", "col"}
TEXT_ATTRS = ("alt", "aria-label", "title", "placeholder")
META_COPY = {"description", "og:title", "og:description", "twitter:title", "twitter:description"}
ASSET_RE = re.compile(r"assets/([A-Za-z0-9_.\-]+\.(?:png|jpe?g|webp|svg|gif|avif|mp4))")
HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
CJK_RE = re.compile(r"[一-鿿]")


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


# ---------- HTML 解析 ----------

class Page(HTMLParser):
    """收集：區塊範圍、可見文案、屬性文案。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # [tag, label, is_block, buffer, line]
        self.containers = []     # [id, start, end]
        self.rows = []           # (line, section, kind, element, text)
        self.skip = 0

    def section(self):
        for c in reversed(self.stack):
            if c[0] in CONTAINERS:
                return c[1]
        return "body"

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag in ("script", "style", "template"):
            self.skip += 1
            return
        if self.skip:
            return
        cls = (a.get("class") or "").split()
        label = "#" + a["id"] if a.get("id") else tag + ("." + cls[0] if cls else "")
        if tag == "br":
            for c in reversed(self.stack):
                if c[2]:
                    c[3].append(" ↵ ")
                    break
            return
        if tag == "meta" and (a.get("name") or a.get("property") or "") in META_COPY:
            self.rows.append((line, "head", "meta " + (a.get("name") or a.get("property")), "meta", norm(a.get("content") or "")))
        if tag == "a" and a.get("href") and not a["href"].startswith("#"):
            self.rows.append((line, None, "link", label, a["href"]))
        for k in TEXT_ATTRS:
            v = norm(a.get(k) or "")
            if v and a.get("aria-hidden") != "true":
                self.rows.append((line, None, k, label, v))
        if tag in VOID:
            return
        if tag in CONTAINERS:
            self.containers.append([label, line, None])
        self.stack.append([tag, label, tag in BLOCKS or tag in CONTAINERS, [], line])

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag in VOID:
            return
        while self.stack:
            node = self.stack.pop()
            text = norm("".join(node[3])).strip("↵ ").strip()
            if node[2] and text:
                self.rows.append((node[4], self.section() if node[0] not in CONTAINERS else node[1],
                                  "text", node[1], text))
            elif not node[2] and node[3]:
                # inline 元素：文字併回外層
                for c in reversed(self.stack):
                    c[3].extend(node[3])
                    break
            if node[0] in CONTAINERS:
                for c in reversed(self.containers):
                    if c[0] == node[1] and c[2] is None:
                        c[2] = self.getpos()[0]
                        break
            if node[0] == tag:
                break

    def handle_data(self, data):
        if self.skip or not self.stack:
            return
        self.stack[-1][3].append(data)


def section_at(containers, line):
    best = None
    for cid, start, end in containers:
        if start <= line <= (end or 10**9):
            if best is None or start >= best[1]:
                best = (cid, start)
    return best[0] if best else "body"


def parse(path):
    src = read(path)
    p = Page()
    p.feed(src)
    rows = []
    for line, sec, kind, el, text in p.rows:
        rows.append((line, sec or section_at(p.containers, line), kind, el, text))
    rows.sort(key=lambda r: r[0])
    return src, p.containers, rows


def js_strings(src):
    """<script> 內含中文的字串常數（按鈕切換文字、狀態標籤等）。"""
    out = []
    for m in re.finditer(r"<script\b[^>]*>(.*?)</script>", src, re.S):
        body, base = m.group(1), m.start(1)
        body = re.sub(r"/\*.*?\*/", lambda x: " " * len(x.group(0)), body, flags=re.S)
        body = re.sub(r"(?m)^\s*//.*$", lambda x: " " * len(x.group(0)), body)
        for s in re.finditer(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'', body):
            val = s.group(1) if s.group(1) is not None else s.group(2)
            if CJK_RE.search(val):
                out.append((src.count("\n", 0, base + s.start()) + 1, val))
    return out


# ---------- 圖片 ----------

def image_size(path):
    try:
        with open(path, "rb") as f:
            head = f.read(64 * 1024)
    except OSError:
        return None
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", head[16:24])
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        chunk = head[12:16]
        if chunk == b"VP8X":
            return (int.from_bytes(head[24:27], "little") + 1, int.from_bytes(head[27:30], "little") + 1)
        if chunk == b"VP8 ":
            w, h = struct.unpack("<HH", head[26:30])
            return (w & 0x3FFF, h & 0x3FFF)
        if chunk == b"VP8L":
            b = int.from_bytes(head[21:25], "little")
            return ((b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1)
    if head[:2] == b"\xff\xd8":
        with open(path, "rb") as f:
            data = f.read()
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return (w, h)
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    if path.endswith(".svg"):
        txt = head.decode("utf-8", "ignore")
        m = re.search(r'viewBox="[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', txt)
        if m:
            return (round(float(m.group(1))), round(float(m.group(2))))
    return None


def asset_refs():
    """{檔名: [(頁面, 行, 區塊)]}，含封存頁。"""
    refs = {}
    files = list(PAGES)
    adir = os.path.join(ROOT, ARCHIVE_DIR)
    if os.path.isdir(adir):
        files += [os.path.join(ARCHIVE_DIR, f) for f in sorted(os.listdir(adir)) if f.endswith(".html")]
    for page in files:
        src, containers, _ = parse(page)
        for m in ASSET_RE.finditer(src):
            line = src.count("\n", 0, m.start()) + 1
            refs.setdefault(m.group(1), []).append((page, line, section_at(containers, line)))
    return refs


# ---------- 產生清單 ----------

HEADER = "<!-- 由 tools/handoff.py inventory 產生，不要手改。要改文案請改 HTML，再重跑腳本。 -->\n\n"


def md_cell(s):
    return s.replace("|", "\\|")


def build_content():
    out = [HEADER, "# 全站文案清單\n\n",
           "HTML 是正本，這份是從 HTML 抽出來的快照，用來審稿、比對版本。\n",
           "「行」是 HTML 原始碼行號；`↵` 代表 `<br>` 斷行；`alt` / `aria-label` 是讀屏與圖片替代文字，同樣要校稿；`link` 是連結網址。\n"]
    for page in PAGES:
        src, _, rows = parse(page)
        out.append("\n---\n\n# `%s`\n" % page)
        groups = {}
        for line, sec, kind, el, text in rows:
            groups.setdefault(sec, []).append("| %d | %s | `%s` | %s |\n" % (line, kind, el, md_cell(text)))
        for sec, lines in groups.items():
            out.append("\n## `%s`\n\n| 行 | 類型 | 元素 | 文案 |\n|---|---|---|---|\n" % sec)
            out.extend(lines)
        js = js_strings(src)
        if js:
            out.append("\n## JS 動態文案\n\n互動後才會出現的文字（按鈕切換、狀態標籤），寫在 `<script>` 裡。\n\n"
                       "| 行 | 字串 |\n|---|---|\n")
            for line, val in js:
                out.append("| %d | %s |\n" % (line, md_cell(val)))
    return "".join(out)


def build_assets():
    refs = asset_refs()
    names = sorted(f for f in os.listdir(os.path.join(ROOT, ASSETS_DIR)) if not f.startswith("."))
    out = [HEADER, "# 圖片清單\n\n",
           "`assets/` 每個檔案的尺寸與用在哪裡。尺寸是檔案原始像素，不是畫面顯示大小。\n\n",
           "| 檔案 | 尺寸 (px) | KB | 用在 |\n|---|---|---|---|\n"]
    for n in names:
        p = os.path.join(ROOT, ASSETS_DIR, n)
        size = image_size(p)
        dims = "%d × %d" % size if size else "?"
        kb = round(os.path.getsize(p) / 1024)
        used = [r for r in refs.get(n, []) if not r[0].startswith(ARCHIVE_DIR)]
        where = "<br>".join("%s:%d `%s`" % u for u in used)
        if not used:
            where = "**未使用**" + ("（僅封存頁）" if n in refs else "")
        out.append("| `%s` | %s | %d | %s |\n" % (n, dims, kb, where))
    missing = sorted(set(refs) - set(names))
    if missing:
        out.append("\n## 引用了但檔案不存在\n\n")
        for n in missing:
            out.append("- `assets/%s`：%s\n" % (n, ", ".join("%s:%d" % r[:2] for r in refs[n])))
    return "".join(out)


def outputs():
    return {os.path.join(OUT_DIR, "content.md"): build_content(),
            os.path.join(OUT_DIR, "assets.md"): build_assets()}


# ---------- 指令 ----------

def inventory():
    os.makedirs(os.path.join(ROOT, OUT_DIR), exist_ok=True)
    for path, text in outputs().items():
        with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
            f.write(text)
        print("寫入", path)


def check():
    problems, warnings = [], []

    refs = asset_refs()
    names = set(f for f in os.listdir(os.path.join(ROOT, ASSETS_DIR)) if not f.startswith("."))
    for n in sorted(set(refs) - names):
        where = ", ".join("%s:%d" % r[:2] for r in refs[n])
        problems.append("缺圖  assets/%s（%s）" % (n, where))
    live = {n for n, rs in refs.items() if any(not r[0].startswith(ARCHIVE_DIR) for r in rs)}
    for n in sorted(names - live):
        warnings.append("未使用  assets/%s" % n)

    for path, text in outputs().items():
        full = os.path.join(ROOT, path)
        if not os.path.exists(full) or read(path) != text:
            problems.append("過期  %s 和 HTML 不一致，跑 `python3 tools/handoff.py inventory` 後檢查 git diff" % path)

    for page in PAGES:
        # 註解裡提到的色值不算（保留長度，行號才對得上）
        src = re.sub(r"/\*.*?\*/|<!--.*?-->", lambda x: re.sub(r"[^\n]", " ", x.group(0)), read(page), flags=re.S)
        for m in HEX_RE.finditer(src):
            hex_ = m.group(0).lower()
            if hex_ in PALETTE:
                continue
            rule_start = max(src.rfind("}", 0, m.start()), src.rfind(";", 0, src.rfind("{", 0, m.start())))
            selector = norm(src[rule_start + 1:src.rfind("{", 0, m.start())])
            if (page, selector, hex_) in COLOR_EXCEPTIONS:
                continue
            line = src.count("\n", 0, m.start()) + 1
            warnings.append("色票外  %s:%d %s（%s）" % (page, line, m.group(0), selector))

    for w in warnings:
        print("⚠️ ", w)
    for p in problems:
        print("❌", p)
    print("\n%d 個錯誤、%d 個提醒" % (len(problems), len(warnings)))
    return 1 if problems else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "inventory":
        inventory()
    elif cmd == "check":
        sys.exit(check())
    else:
        print(__doc__)
        sys.exit(2)
