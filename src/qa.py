#!/usr/bin/env python3
"""QA checks for the Sarasota Sewer Specialists static build."""
import json, os, re, glob
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
CONTENT = os.path.join(ROOT, "content")
DOMAIN = "https://sewerlinerepairsarasotafl.com"
PHONE = "(941) 344-0088"

issues = []
def flag(msg):
    issues.append(msg)
    print("ISSUE:", msg)

# ---------- collect pages ----------
pages = {}  # url_path -> html
for f in glob.glob(os.path.join(DIST, "**", "index.html"), recursive=True):
    rel = os.path.relpath(f, DIST)
    url = "/" + os.path.dirname(rel).replace(os.sep, "/")
    url = url if url != "/." else "/"
    if not url.endswith("/"):
        url += "/"
    with open(f) as fh:
        pages[url] = fh.read()
print(f"1. page count: {len(pages)} (expect 43)")
if len(pages) != 43:
    flag(f"page count {len(pages)} != 43")

def text_of(html_snippet):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_snippet)).strip()

def words(s):
    return len(text_of(s).split())

# ---------- word counts from content JSON ----------
THRESH = {"service": 1250, "location": 950, "blog": 1350, "core": 650}
for f in glob.glob(os.path.join(CONTENT, "*", "*.json")):
    d = json.load(open(f))
    body = d.get("hero_sub", "") + " " + " ".join(
        s.get("h2", "") + " " + s.get("html", "") for s in d.get("sections", []))
    n = words(body)
    need = THRESH[d["kind"]] + (150 if d.get("slug") == "home" else 0)
    status = "OK " if n >= need else "SHORT"
    print(f"   [{status}] {d['url_path']}: {n} words (need {need})")
    if n < need:
        flag(f"thin content: {d['url_path']} has {n} body words, need {need}")
    # faq counts
    nf = len(d.get("faqs") or [])
    if d["kind"] == "service" and not (6 <= nf <= 8):
        flag(f"faq count {nf} on {d['url_path']} (want 6-8)")
    if d["kind"] == "location" and not (6 <= nf <= 8):
        flag(f"faq count {nf} on {d['url_path']} (want 6-8)")
    if d["kind"] == "blog" and not (4 <= nf <= 6):
        flag(f"faq count {nf} on {d['url_path']} (want 4-6)")

# ---------- internal links + orphans ----------
def page_exists(href):
    if not href.startswith("/"):
        return True  # external or anchor; checked separately
    if href.startswith("//"):
        return True
    p = href.split("#")[0].split("?")[0]
    if p in ("", "/"):
        return True
    cand = os.path.join(DIST, p.strip("/"), "index.html")
    if os.path.isfile(cand):
        return True
    cand2 = os.path.join(DIST, p.strip("/"))
    if os.path.isfile(cand2):
        return True
    return False

link_re = re.compile(r'href="([^"]+)"')
all_internal = set()
for url, html in pages.items():
    for href in link_re.findall(html):
        if href.startswith("/") and not href.startswith("//"):
            all_internal.add(href)
            if not page_exists(href):
                flag(f"broken internal link on {url}: {href}")
        elif href.startswith("http"):
            if "google.com/maps" not in href and "sewerlinerepairsarasotafl.com" not in href:
                flag(f"unexpected external link on {url}: {href}")

# BFS orphans from /
seen, stack = set(), ["/"]
while stack:
    u = stack.pop()
    if u in seen or u not in pages:
        continue
    seen.add(u)
    for href in link_re.findall(pages[u]):
        if href.startswith("/") and not href.startswith("//"):
            p = href.split("#")[0]
            if p in pages and p not in seen:
                stack.append(p)
orphans = set(pages) - seen
print(f"2. orphans: {len(orphans)}")
for o in sorted(orphans):
    flag(f"orphan page (unreachable from /): {o}")

# ---------- JSON-LD ----------
ld_re = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)
for url, html in pages.items():
    blocks = ld_re.findall(html)
    if not blocks:
        flag(f"no JSON-LD on {url}")
        continue
    types = []
    for b in blocks:
        try:
            j = json.loads(b)
        except Exception as e:
            flag(f"JSON-LD parse error on {url}: {e}")
            continue
        types.append(j.get("@type"))
    if "BreadcrumbList" not in types:
        flag(f"missing BreadcrumbList on {url}")
print("3. JSON-LD parsed on all pages")

# ---------- forbidden content ----------
forbidden = re.compile(r"aggregateRating|\"review\"|'review'|CFC\d+|license\s*(no|#|number)\s*[:#]?\s*\d|certified|★★|⭐|\b\d+(\.\d+)?\s*stars?\b", re.I)
phone_re = re.compile(r"\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}")
for url, html in pages.items():
    body = re.sub(r"<head>.*?</head>", "", html, flags=re.S)
    if forbidden.search(body):
        m = forbidden.search(body)
        flag(f"forbidden content on {url}: ...{body[max(0,m.start()-40):m.end()+40]}...")
    for ph in set(phone_re.findall(body)):
        if PHONE not in ph and ph.replace(" ", "") not in PHONE.replace(" ", ""):
            # allow only the placeholder
            digits = re.sub(r"\D", "", ph)
            if digits != "19413440088":
                flag(f"non-placeholder phone on {url}: {ph}")
print("4. fabrication/phone scan done")

# ---------- metas ----------
titles, metas = {}, {}
for url, html in pages.items():
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    m = re.search(r'<meta name="description" content="(.*?)">', html)
    if not t or not m:
        flag(f"missing title/meta on {url}")
        continue
    title, meta = t.group(1), m.group(1)
    if len(meta) > 155:
        flag(f"meta too long ({len(meta)}) on {url}")
    if title in titles:
        flag(f"duplicate title: {title}")
    titles[title] = url
    if meta in metas:
        flag(f"duplicate meta on {url} and {metas[meta]}")
    metas[meta] = url
    kind = ("blog" if url.startswith("/blog/") and url != "/blog/" else
            "hub" if url in ("/blog/",) else "money")
    if PHONE not in meta:
        flag(f"phone missing from meta: {url}")
    # canonical + h1 count + heading order
    if f'<link rel="canonical" href="{DOMAIN}{url}">' not in html:
        flag(f"bad/missing canonical on {url}")
    h1s = re.findall(r"<h1[ >]", html)
    if len(h1s) != 1:
        flag(f"{len(h1s)} h1 tags on {url}")
print("5. meta/title/canonical/h1 checks done")

# ---------- heading hierarchy in content html ----------
for f in glob.glob(os.path.join(CONTENT, "*", "*.json")):
    d = json.load(open(f))
    for s in d.get("sections", []):
        tags = re.findall(r"<(h[1-6])", s.get("html", ""))
        if "h1" in tags or "h2" in tags:
            flag(f"h1/h2 inside section html: {d['url_path']}")
        if "h4" in tags or "h5" in tags or "h6" in tags:
            flag(f"skipped heading level in {d['url_path']}")
print("6. heading hierarchy in content OK")

# ---------- similarity (8-word shingles) ----------
def shingles(text, n=8):
    w = text_of(text).lower().split()
    return set(tuple(w[i:i+n]) for i in range(len(w) - n + 1))

def body_text(d):
    return d.get("hero_sub", "") + " " + " ".join(
        s.get("h2", "") + " " + s.get("html", "") for s in d.get("sections", []))

groups = {}
for f in glob.glob(os.path.join(CONTENT, "*", "*.json")):
    d = json.load(open(f))
    groups.setdefault(d["kind"], []).append(d)

for kind in ("location", "service"):
    docs = groups.get(kind, [])
    sh = {d["url_path"]: shingles(body_text(d)) for d in docs}
    worst = 0
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            a, b = sh[docs[i]["url_path"]], sh[docs[j]["url_path"]]
            if not a or not b:
                continue
            ratio = len(a & b) / min(len(a), len(b))
            worst = max(worst, ratio)
            if ratio > 0.25:
                flag(f"similarity {ratio:.0%} between {docs[i]['url_path']} and {docs[j]['url_path']}")
    print(f"7. max {kind} pairwise similarity: {worst:.0%} (limit 25%)")

# ---------- placeholders & head hygiene ----------
for url, html in pages.items():
    no_style = re.sub(r"<style.*?</style>", "", html, flags=re.S)
    if "{{" in no_style or "}}" in no_style:
        flag(f"template placeholder braces on {url}")
    if "lorem" in html.lower():
        flag(f"lorem ipsum on {url}")
    if re.search(r"TBD|TODO", html):
        flag(f"TBD/TODO on {url}")
    head = re.search(r"<head>(.*?)</head>", html, re.S)
    if head:
        cleaned = re.sub(r"<script.*?</script>", "", head.group(1), flags=re.S)
        cleaned = re.sub(r"<style.*?</style>", "", cleaned, flags=re.S)
        cleaned = re.sub(r"<title.*?</title>", "", cleaned, flags=re.S)
        txt = re.sub(r"<[^>]+>", "", cleaned).strip()
        if txt:
            flag(f"text node in <head> on {url}: {txt[:60]}")
    # malformed attribute check: ="...=" inside a tag
    for tag in re.findall(r"<[^>]+>", html):
        if re.search(r'="[^"]*="', tag):
            flag(f"malformed attribute on {url}: {tag[:80]}")
            break
print("8. placeholder/head/attribute checks done")

# ---------- tag balance ----------
class Balancer(HTMLParser):
    VOID = {"meta", "link", "br", "hr", "img", "input", "source", "path",
            "circle", "rect", "iframe", "wbr", "col", "embed"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            # search for match (tolerate)
            names = [t for t, _ in self.stack]
            if tag in names:
                while self.stack and self.stack[-1][0] != tag:
                    bad = self.stack.pop()
                    self.errors.append(f"unclosed <{bad[0]}> at {bad[1]}")
                self.stack.pop()
            else:
                self.errors.append(f"stray </{tag}> at {self.getpos()}")

for url, html in pages.items():
    b = Balancer()
    try:
        b.feed(html)
    except Exception as e:
        flag(f"parse error on {url}: {e}")
    for t, pos in b.stack:
        b.errors.append(f"unclosed <{t}> opened at {pos}")
    for e in b.errors[:3]:
        flag(f"tag balance {url}: {e}")
print("9. tag balance done")

# ---------- sitemap / robots / favicon ----------
sm = open(os.path.join(DIST, "sitemap.xml")).read()
n_urls = sm.count("<url>")
print(f"10. sitemap urls: {n_urls} (expect 43)")
if n_urls != 43:
    flag("sitemap url count != 43")
rb = open(os.path.join(DIST, "robots.txt")).read()
if "Sitemap:" not in rb or "Allow: /" not in rb:
    flag("robots.txt missing Allow/Sitemap")
if not os.path.isfile(os.path.join(DIST, "favicon.svg")):
    flag("favicon.svg missing")
print("11. robots/favicon done")

print()
print("=" * 50)
if issues:
    print(f"QA FAILED: {len(issues)} issue(s)")
else:
    print("QA PASSED: all checks green")
