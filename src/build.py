#!/usr/bin/env python3
"""Static site generator for Sarasota Sewer Specialists (43 pages)."""
import json, os, re, glob, html as ihtml
from string import Template

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
DIST = os.path.join(ROOT, "dist")

# ---- single-source constants (swap PHONE here before deploy) ----
BIZ = "Sarasota Sewer Specialists"
PHONE = "(941) 344-0088"
PHONE_TEL = "tel:+19413440088"
DOMAIN = "https://sewerlinerepairsarasotafl.com"
CITY = "Sarasota, FL"
STREET = "2354 Margaret St"
P_ZIP = "34237"

ZIPS_ALL = ["34228", "34229", "34231", "34232", "34233", "34234", "34236",
            "34238", "34239", "34240", "34242", "34243", "34275", "34285",
            "34286", "34287", "34288", "34292", "34293", "34205", "34208", "34209"]

# ---------------- CSS (Gulf Teal design system, extended) ----------------
CSS = """\
:root{
  --deep:#0A3D42; --brand:#0E6B6E; --cta:#E8713A; --cta-dark:#C85A28;
  --cta-ink:#FFFFFF; --bg:#F2F7F6; --card:#FFFFFF;
  --ink:#1E2A2B; --muted:#5A6B6C; --accent:#2AA5A0;
  --hero-a:#0E6B6E; --hero-b:#083B41;
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.65}
a{text-decoration:none;color:inherit}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px}
main{display:block}
/* topbar */
.topbar{background:var(--deep);color:#fff;font-size:13px}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;padding-top:8px;padding-bottom:8px;gap:12px;flex-wrap:wrap}
.topbar .phone{background:var(--cta);color:var(--cta-ink);font-weight:700;padding:4px 14px;border-radius:999px}
/* nav */
.nav{background:var(--card);border-bottom:1px solid rgba(0,0,0,.08);position:sticky;top:0;z-index:50}
.nav .wrap{display:flex;align-items:center;gap:26px;padding-top:12px;padding-bottom:12px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:19px}
.logo .mark{width:38px;height:38px;flex:none;display:block}
.logo .mark svg{display:block;width:38px;height:38px}
.logo small{display:block;font-weight:600;font-size:11px;letter-spacing:3px;color:var(--muted)}
.nav-links{display:flex;gap:20px;margin-left:auto;font-size:15px;font-weight:600;align-items:center;list-style:none}
.nav-links>li>a{color:var(--ink);padding:6px 2px;display:inline-block}
.nav-links a:hover{color:var(--brand)}
.dropdown{position:relative}
.dropdown>ul{position:absolute;top:100%;left:0;background:var(--card);border:1px solid rgba(0,0,0,.1);border-radius:10px;box-shadow:0 14px 34px rgba(0,0,0,.14);list-style:none;min-width:270px;padding:10px;display:none;z-index:60}
.dropdown.wide>ul{min-width:480px;column-count:2;column-gap:8px}
.dropdown:hover>ul,.dropdown:focus-within>ul{display:block}
.dropdown>ul a{display:block;padding:8px 12px;font-size:14px;font-weight:500;border-radius:6px}
.dropdown>ul a:hover{background:var(--bg);color:var(--brand)}
.nav-cta{background:var(--cta);color:var(--cta-ink)!important;font-weight:700;padding:9px 20px!important;border-radius:8px;white-space:nowrap}
.nav-cta:hover{background:var(--cta-dark);color:var(--cta-ink)!important}
.nav-toggle{display:none;background:none;border:0;font-size:26px;cursor:pointer;color:var(--ink);margin-left:auto}
/* hero - flashy: relevant photo behind content */
.hero{position:relative;overflow:hidden;color:#fff;padding:90px 0}
.hero-bg{position:absolute;inset:0}
.hero-bg img{width:100%;height:100%;object-fit:cover;display:block}
.hero-shade{position:absolute;inset:0;background:linear-gradient(100deg,rgba(8,45,50,.95) 15%,rgba(8,45,50,.62) 55%,rgba(8,45,50,.28))}
.hero-content{position:relative;z-index:1}
.eyebrow{display:inline-block;font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#fff;margin-bottom:14px;border:1px solid rgba(255,255,255,.45);background:rgba(232,113,58,.25);padding:7px 16px;border-radius:999px}
.hero h1{font-size:42px;line-height:1.15;max-width:680px;margin-bottom:16px;text-shadow:0 2px 14px rgba(0,0,0,.45)}
.hero .lede{max-width:620px;font-size:18px;opacity:.94;margin-bottom:28px;text-shadow:0 1px 8px rgba(0,0,0,.4)}
.hero .ctas{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:26px}
.trustrow{display:flex;gap:12px;flex-wrap:wrap;font-size:14px;font-weight:600}
.trustrow span{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);padding:8px 16px;border-radius:999px}
.trustrow span::before{content:"\\2713  ";color:var(--cta);font-weight:800}
.crumbs{font-size:13px;color:var(--muted);padding:16px 0 0}
.crumbs a{color:var(--brand)}
.crumbs a:hover{text-decoration:underline}
/* buttons */
.btn{display:inline-block;background:var(--cta);color:var(--cta-ink);font-weight:700;padding:12px 26px;border-radius:8px;font-size:16px;box-shadow:0 8px 22px rgba(232,113,58,.35);transition:transform .2s ease,box-shadow .2s ease,background .2s ease}
.btn:hover{background:var(--cta-dark);transform:translateY(-2px);box-shadow:0 12px 28px rgba(232,113,58,.45)}
.btn.ghost{background:rgba(255,255,255,.08);color:#fff;border:2px solid #fff;box-shadow:none}
.btn.ghost:hover{background:rgba(255,255,255,.18);transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,.3)}
/* sections */
section.block{padding:60px 0}
.prose{max-width:780px}
.prose h2{font-size:30px;margin:0 0 16px}
.prose h3{font-size:21px;margin:26px 0 10px;color:var(--brand)}
.prose p{margin-bottom:14px;color:#33414a;font-size:16.5px}
.prose p strong{color:var(--ink)}
.prose ul,.prose ol{margin:0 0 16px 22px;color:#33414a}
.prose li{margin-bottom:8px}
.prose a{color:var(--brand);font-weight:600}
.prose a:hover{text-decoration:underline}
.split{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:start}
.sticky-visual{position:sticky;top:96px;border-radius:14px;min-height:420px;background:linear-gradient(160deg,var(--hero-a),var(--hero-b));display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,.8);font-size:13px;letter-spacing:2px;text-align:center;padding:20px}
.sticky-visual.has-photo{padding:0;overflow:hidden;background:none}
.sticky-visual.has-photo img{width:100%;height:100%;object-fit:cover;display:block;min-height:420px}
/* cards / grids */
.sec-head{max-width:720px;margin-bottom:32px}
.sec-head h2{font-size:30px;margin-bottom:10px}
.sec-head p{color:var(--muted);font-size:17px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:var(--card);border:1px solid rgba(0,0,0,.07);border-radius:12px;padding:26px;display:flex;flex-direction:column}
.card h3{font-size:18px;margin-bottom:8px}
.card h3 a:hover{color:var(--brand)}
.card p{font-size:15px;color:var(--muted);flex:1}
.card .more{margin-top:14px;color:var(--brand);font-weight:700;font-size:15px}
/* flashy image cards */
.card.pic{padding:0;overflow:hidden;box-shadow:0 6px 20px rgba(10,61,66,.10);transition:transform .25s ease,box-shadow .25s ease}
.card.pic:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(10,61,66,.18)}
.card-pic{display:block;aspect-ratio:16/10;overflow:hidden;position:relative}
.card-pic::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(8,45,50,.35))}
.card-pic img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s ease}
.card.pic:hover .card-pic img{transform:scale(1.06)}
.card-body{padding:22px;display:flex;flex-direction:column;flex:1}
.card-body h3{font-size:18px;margin-bottom:8px}
.card-body h3 a:hover{color:var(--brand)}
.card-body p{font-size:15px;color:var(--muted);flex:1}
.card-body .more{margin-top:14px;color:var(--brand);font-weight:700;font-size:15px}
/* pills */
.pills{display:flex;flex-wrap:wrap;gap:10px}
.pill{background:var(--card);border:1px solid rgba(0,0,0,.1);padding:9px 18px;border-radius:999px;font-size:14px;font-weight:600}
.pill:hover{border-color:var(--brand);color:var(--brand)}
.pill b{color:var(--brand)}
/* faq */
.faq{max-width:820px}
.faq details{background:var(--card);border:1px solid rgba(0,0,0,.08);border-radius:10px;margin-bottom:12px;padding:18px 22px}
.faq summary{cursor:pointer;font-weight:700;font-size:16.5px}
.faq summary:hover{color:var(--brand)}
.faq details p{margin-top:10px;color:#33414a;font-size:15.5px}
/* cta band */
.ctaband{background:var(--deep);color:#fff;text-align:center;padding:56px 0}
.ctaband h2{font-size:30px;margin-bottom:10px}
.ctaband p{opacity:.85;margin-bottom:24px}
/* map */
.mapwrap{border-radius:14px;overflow:hidden;border:1px solid rgba(0,0,0,.1);margin-top:8px}
.mapwrap iframe{width:100%;height:400px;border:0;display:block}
/* footer */
footer{background:var(--deep);color:#fff;padding:48px 0 24px;font-size:14px}
.fgrid{display:grid;grid-template-columns:1.3fr 1fr 1fr 1fr;gap:32px;margin-bottom:32px}
.fgrid h4{font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--cta);margin-bottom:14px}
.fgrid ul{list-style:none}
.fgrid li{margin-bottom:8px;opacity:.88}
.fgrid a:hover{color:var(--cta)}
.fgrid details summary{cursor:pointer;color:var(--cta);font-weight:700;margin:6px 0 8px}
.fbottom{border-top:1px solid rgba(255,255,255,.15);padding-top:18px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;opacity:.7;font-size:13px}
@media(max-width:900px){
  .grid{grid-template-columns:1fr 1fr}
  .split{grid-template-columns:1fr}
  .sticky-visual{position:static;min-height:220px}
  .sticky-visual.has-photo img{min-height:220px}
  .hero{padding:64px 0}
  .hero h1{font-size:32px}
  .nav-toggle{display:block}
  .nav-links{display:none;flex-direction:column;align-items:stretch;position:absolute;top:100%;left:0;right:0;background:var(--card);padding:12px 20px 20px;border-bottom:1px solid rgba(0,0,0,.1);gap:4px}
  .nav-links.open{display:flex}
  .dropdown>ul{position:static;display:block;box-shadow:none;border:0;padding:0 0 0 14px;column-count:1!important;min-width:0}
  .fgrid{grid-template-columns:1fr 1fr}
}
@media(max-width:560px){.grid{grid-template-columns:1fr}.fgrid{grid-template-columns:1fr}}
"""

NAV_JS = """<script defer>
document.addEventListener('DOMContentLoaded',function(){
var t=document.querySelector('.nav-toggle'),m=document.querySelector('.nav-links');
if(t&&m){t.addEventListener('click',function(){m.classList.toggle('open');});}
});
</script>"""

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="15" fill="#0A3D42"/><path d="M20 45V30a11 11 0 0 1 11-11h13" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round"/><path d="M13 52.5q6.5-5.5 13 0t13 0 13 0" fill="none" stroke="#E8713A" stroke-width="5" stroke-linecap="round"/></svg>"""

# ---------------- content registry ----------------
ALLOWED_TAGS = {"p", "h3", "ul", "ol", "li", "strong", "a", "em"}

def sanitize_html(html):
    """Strip any tag not in the allowlist, keeping inner text."""
    def repl(m):
        tag = m.group(1).lower()
        return m.group(0) if tag in ALLOWED_TAGS else ""
    return re.sub(r"</?([a-zA-Z][a-zA-Z0-9]*)[^>]*>", repl, html)

def load_registry():
    reg = {}
    for f in glob.glob(os.path.join(CONTENT, "*", "*.json")):
        with open(f) as fh:
            d = json.load(fh)
        reg[d["url_path"]] = d
    return reg

SERVICE_ORDER = ["trenchless-sewer-repair","sewer-line-replacement","pipe-bursting",
"cipp-pipe-lining","sewer-camera-inspection","emergency-sewer-repair","tree-root-removal",
"hydro-jetting","commercial-sewer-services","septic-to-sewer-conversion","sewer-odor-detection"]

def services(reg):
    return sorted([d for d in reg.values() if d["kind"] == "service"],
                  key=lambda d: SERVICE_ORDER.index(d["slug"]))

def locations(reg):
    return sorted([d for d in reg.values() if d["kind"] == "location"],
                  key=lambda d: d["url_path"])

def blogs(reg):
    return sorted([d for d in reg.values() if d["kind"] == "blog"],
                  key=lambda d: d.get("date", ""), reverse=True)

SHORTS = {
    "trenchless-sewer-repair": "Trenchless Sewer Repair",
    "pipe-bursting": "Pipe Bursting",
    "cipp-pipe-lining": "CIPP Pipe Lining",
    "sewer-camera-inspection": "Sewer Camera Inspection",
    "sewer-line-replacement": "Sewer Line Replacement",
    "tree-root-removal": "Tree Root Removal",
    "hydro-jetting": "Hydro Jetting",
    "sewer-odor-detection": "Sewer Odor Detection",
    "emergency-sewer-repair": "Emergency Sewer Repair",
    "commercial-sewer-services": "Commercial Sewer Services",
    "septic-to-sewer-conversion": "Septic-to-Sewer Conversion",
}

# service slug -> 2 blog slugs
SERVICE_BLOGS = {
    "trenchless-sewer-repair": ["trenchless-vs-traditional-sewer-repair", "pipe-bursting-vs-pipe-lining"],
    "pipe-bursting": ["pipe-bursting-vs-pipe-lining", "cast-iron-sewer-pipe-sarasota-slab-homes"],
    "cipp-pipe-lining": ["pipe-bursting-vs-pipe-lining", "cast-iron-sewer-pipe-sarasota-slab-homes"],
    "sewer-camera-inspection": ["sewer-camera-inspection-what-to-expect", "signs-sewer-line-failure"],
    "sewer-line-replacement": ["signs-sewer-line-failure", "cast-iron-sewer-pipe-sarasota-slab-homes"],
    "tree-root-removal": ["tree-roots-sewer-lines-sarasota", "hydro-jetting-vs-snaking"],
    "hydro-jetting": ["hydro-jetting-vs-snaking", "tree-roots-sewer-lines-sarasota"],
    "sewer-odor-detection": ["signs-sewer-line-failure", "sewer-camera-inspection-what-to-expect"],
    "emergency-sewer-repair": ["rainy-season-sewer-backups-sarasota", "signs-sewer-line-failure"],
    "commercial-sewer-services": ["hydro-jetting-vs-snaking", "trenchless-vs-traditional-sewer-repair"],
    "septic-to-sewer-conversion": ["septic-to-sewer-conversion-sarasota-county", "siesta-key-barrier-island-sewer-challenges"],
}
# location slug -> 2 blog slugs
LOCATION_BLOGS = {
    "downtown-sarasota-34236": ["trenchless-vs-traditional-sewer-repair", "cast-iron-sewer-pipe-sarasota-slab-homes"],
    "st-armands-lido-key": ["siesta-key-barrier-island-sewer-challenges", "sewer-camera-inspection-what-to-expect"],
    "siesta-key-34242": ["siesta-key-barrier-island-sewer-challenges", "rainy-season-sewer-backups-sarasota"],
    "longboat-key-34228": ["siesta-key-barrier-island-sewer-challenges", "septic-to-sewer-conversion-sarasota-county"],
    "gulf-gate-34231": ["cast-iron-sewer-pipe-sarasota-slab-homes", "signs-sewer-line-failure"],
    "bee-ridge-34233": ["rainy-season-sewer-backups-sarasota", "pipe-bursting-vs-pipe-lining"],
    "southgate-pinecraft-34239": ["tree-roots-sewer-lines-sarasota", "cast-iron-sewer-pipe-sarasota-slab-homes"],
    "north-sarasota-34234": ["tree-roots-sewer-lines-sarasota", "signs-sewer-line-failure"],
    "palmer-ranch-34238": ["sewer-camera-inspection-what-to-expect", "trenchless-vs-traditional-sewer-repair"],
    "fruitville-34232": ["pipe-bursting-vs-pipe-lining", "cast-iron-sewer-pipe-sarasota-slab-homes"],
    "bradenton": ["hydro-jetting-vs-snaking", "signs-sewer-line-failure"],
    "venice": ["septic-to-sewer-conversion-sarasota-county", "rainy-season-sewer-backups-sarasota"],
    "north-port": ["septic-to-sewer-conversion-sarasota-county", "rainy-season-sewer-backups-sarasota"],
    "osprey-nokomis": ["hydro-jetting-vs-snaking", "tree-roots-sewer-lines-sarasota"],
}
# blog slug -> related service slugs + location slugs
BLOG_REL = {
    "cast-iron-sewer-pipe-sarasota-slab-homes": (["sewer-camera-inspection", "cipp-pipe-lining", "sewer-line-replacement"], ["gulf-gate-34231", "bee-ridge-34233"]),
    "rainy-season-sewer-backups-sarasota": (["emergency-sewer-repair", "sewer-camera-inspection"], ["bee-ridge-34233", "siesta-key-34242"]),
    "trenchless-vs-traditional-sewer-repair": (["trenchless-sewer-repair", "pipe-bursting", "cipp-pipe-lining"], ["downtown-sarasota-34236", "gulf-gate-34231"]),
    "tree-roots-sewer-lines-sarasota": (["tree-root-removal", "sewer-camera-inspection", "hydro-jetting"], ["southgate-pinecraft-34239", "north-sarasota-34234"]),
    "sewer-camera-inspection-what-to-expect": (["sewer-camera-inspection", "sewer-odor-detection"], ["st-armands-lido-key", "palmer-ranch-34238"]),
    "signs-sewer-line-failure": (["sewer-line-replacement", "emergency-sewer-repair"], ["gulf-gate-34231", "north-sarasota-34234"]),
    "septic-to-sewer-conversion-sarasota-county": (["septic-to-sewer-conversion", "sewer-line-replacement"], ["north-port", "venice"]),
    "pipe-bursting-vs-pipe-lining": (["pipe-bursting", "cipp-pipe-lining", "trenchless-sewer-repair"], ["bee-ridge-34233", "fruitville-34232"]),
    "siesta-key-barrier-island-sewer-challenges": (["sewer-line-replacement", "emergency-sewer-repair"], ["siesta-key-34242", "longboat-key-34228"]),
    "hydro-jetting-vs-snaking": (["hydro-jetting", "tree-root-removal"], ["bradenton", "osprey-nokomis"]),
}

# ---------------- JSON-LD ----------------
def ld_breadcrumbs(items):
    els = []
    for i, (name, path) in enumerate(items, 1):
        els.append({"@type": "ListItem", "position": i, "name": name,
                    "item": DOMAIN + path})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": els}

def ld_faq(faqs):
    def txt(h):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": txt(f["a"])}}
                           for f in faqs]}

def ld_localbusiness():
    return {"@context": "https://schema.org", "@type": "Plumber",
            "name": BIZ, "telephone": PHONE, "url": DOMAIN + "/",
            "address": {"@type": "PostalAddress", "streetAddress": STREET,
                        "addressLocality": "Sarasota", "addressRegion": "FL",
                        "postalCode": P_ZIP, "addressCountry": "US"},
            "areaServed": ["Sarasota, FL"] + ZIPS_ALL}

def ld_service(d):
    short = SHORTS.get(d["slug"], d["h1"])
    return {"@context": "https://schema.org", "@type": "Service",
            "name": short + " in Sarasota, FL",
            "description": d["meta"],
            "url": DOMAIN + d["url_path"],
            "provider": {"@type": "Plumber", "name": BIZ, "telephone": PHONE,
                         "url": DOMAIN + "/",
                         "address": {"@type": "PostalAddress", "streetAddress": STREET,
                                     "addressLocality": "Sarasota", "addressRegion": "FL",
                                     "postalCode": P_ZIP, "addressCountry": "US"}},
            "areaServed": ["Sarasota, FL"] + ZIPS_ALL}

def ld_scripts(blocks):
    out = []
    for b in blocks:
        out.append('<script type="application/ld+json">\n' +
                   json.dumps(b, indent=2) + '\n</script>')
    return "\n".join(out)

# ---------------- shared chrome ----------------
def esc(s):
    return ihtml.escape(s, quote=True)

def nav_html(reg):
    svc = "".join(
        f'<li><a href="{d["url_path"]}">{esc(SHORTS[d["slug"]])}</a></li>'
        for d in services(reg))
    loc = "".join(
        f'<li><a href="{d["url_path"]}">{esc(d["area_label"])}</a></li>'
        for d in locations(reg))
    return f"""<nav class="nav" aria-label="Main"><div class="wrap">
<a class="logo" href="/" aria-label="{esc(BIZ)} home"><span class="mark"><svg viewBox="0 0 44 44" aria-hidden="true"><rect width="44" height="44" rx="11" fill="#0A3D42"/><path d="M14 31V21a8 8 0 0 1 8-8h9" fill="none" stroke="#FFFFFF" stroke-width="6.5" stroke-linecap="round"/><path d="M9 36.5q5-4.5 10 0t10 0 10 0" fill="none" stroke="#E8713A" stroke-width="3.6" stroke-linecap="round"/></svg></span><span>{esc(BIZ)}<small>SARASOTA, FL</small></span></a>
<button class="nav-toggle" aria-label="Open menu">&#9776;</button>
<ul class="nav-links">
<li><a href="/">Home</a></li>
<li class="dropdown"><a href="/services/" aria-haspopup="true">Services</a><ul>{svc}</ul></li>
<li class="dropdown wide"><a href="/locations/" aria-haspopup="true">Service Areas</a><ul>{loc}</ul></li>
<li><a href="/blog/">Blog</a></li>
<li><a href="/about/">About</a></li>
<li><a href="/contact/">Contact</a></li>
<li><a class="nav-cta" href="{PHONE_TEL}">{esc(PHONE)}</a></li>
</ul></div></nav>"""

def footer_html(reg):
    svc_links = "".join(
        f'<li><a href="{d["url_path"]}">{esc(SHORTS[d["slug"]])}</a></li>'
        for d in services(reg)[:6])
    area_top = "".join(
        f'<li><a href="{d["url_path"]}">{esc(d["area_label"])}</a></li>'
        for d in locations(reg)[:4])
    area_all = "".join(
        f'<li><a href="{d["url_path"]}">{esc(d["area_label"])}</a></li>'
        for d in locations(reg))
    return f"""<footer><div class="wrap"><div class="fgrid">
<div><h4>{esc(BIZ)}</h4><p style="opacity:.8">Sewer line repair and trenchless specialists serving Sarasota, FL and surrounding Gulf Coast communities.</p></div>
<div><h4>Services</h4><ul>{svc_links}<li><a href="/services/">All services</a></li></ul></div>
<div><h4>Service Areas</h4><ul>{area_top}</ul><details><summary>View all service areas</summary><ul>{area_all}</ul></details></div>
<div><h4>Contact</h4><ul><li><a href="{PHONE_TEL}">{esc(PHONE)}</a></li><li>{esc(STREET)}, {esc(CITY)} {esc(P_ZIP)}</li><li><a href="/contact/">Contact page</a></li></ul></div>
</div><div class="fbottom"><span>&copy; 2026 {esc(BIZ)}. All rights reserved.</span><span><a href="/privacy-policy/">Privacy Policy</a> &middot; <a href="/terms-of-service/">Terms of Service</a></span></div></div></footer>"""

def cta_band():
    return f"""<div class="ctaband"><div class="wrap">
<h2>Sewer Problems in Sarasota? Talk to a Specialist.</h2>
<p>One call. A camera in the line. A straight answer about repair vs. replacement.</p>
<a class="btn" href="{PHONE_TEL}">Call {esc(PHONE)}</a></div></div>"""

def head_html(d, ld_blocks, extra=""):
    og_type = "article" if d["kind"] == "blog" else "website"
    hero = HERO_IMG[d["url_path"]]
    hero_abs = f"{DOMAIN}/images/{hero}.webp"
    return f"""<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(d["title"])}</title>
<meta name="description" content="{esc(d["meta"])}">
<link rel="canonical" href="{DOMAIN}{d["url_path"]}">
<link rel="preload" as="image" href="/images/{hero}.webp" fetchpriority="high">
<meta property="og:title" content="{esc(d["title"])}">
<meta property="og:description" content="{esc(d["meta"])}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{DOMAIN}{d["url_path"]}">
<meta property="og:site_name" content="{esc(BIZ)}">
<meta property="og:image" content="{hero_abs}">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="853">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(d["title"])}">
<meta name="twitter:description" content="{esc(d["meta"])}">
<meta name="twitter:image" content="{hero_abs}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon-64.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>{CSS}</style>
{ld_scripts(ld_blocks)}
{NAV_JS}
{extra}</head>"""

# ---------------- image maps (verified webp, truthful filenames) ----------------
HERO_IMG = {
 "/": "trenchless-drilling-rig",
 "/services/": "trenchless-drilling-rig",
 "/services/trenchless-sewer-repair/": "trenchless-drilling-rig",
 "/services/pipe-bursting/": "pipe-bursting-head",
 "/services/cipp-pipe-lining/": "cipp-pipe-lining",
 "/services/sewer-camera-inspection/": "sewer-camera-inspection",
 "/services/sewer-line-replacement/": "excavation-pipe-replacement",
 "/services/tree-root-removal/": "tree-root-removal",
 "/services/hydro-jetting/": "hydro-jetting",
 "/services/sewer-odor-detection/": "sewer-camera-inspection",
 "/services/emergency-sewer-repair/": "work-van-technician",
 "/services/commercial-sewer-services/": "excavation-pipe-replacement",
 "/services/septic-to-sewer-conversion/": "septic-tank-install",
 "/locations/": "siesta-key-beach",
 "/locations/downtown-sarasota-34236/": "downtown-sarasota",
 "/locations/st-armands-lido-key/": "st-armands-circle",
 "/locations/siesta-key-34242/": "siesta-key-beach",
 "/locations/longboat-key-34228/": "barrier-island-aerial",
 "/locations/gulf-gate-34231/": "suburban-street-live-oaks",
 "/locations/bee-ridge-34233/": "suburban-street-live-oaks",
 "/locations/southgate-pinecraft-34239/": "suburban-street-live-oaks",
 "/locations/north-sarasota-34234/": "suburban-street-live-oaks",
 "/locations/palmer-ranch-34238/": "suburban-street-live-oaks",
 "/locations/fruitville-34232/": "suburban-street-live-oaks",
 "/locations/bradenton/": "downtown-sarasota",
 "/locations/venice/": "siesta-key-beach",
 "/locations/north-port/": "suburban-street-live-oaks",
 "/locations/osprey-nokomis/": "barrier-island-aerial",
 "/blog/": "trenchless-drilling-rig",
 "/blog/cast-iron-sewer-pipe-sarasota-slab-homes/": "pipe-bursting-head",
 "/blog/rainy-season-sewer-backups-sarasota/": "suburban-street-live-oaks",
 "/blog/trenchless-vs-traditional-sewer-repair/": "trenchless-drilling-rig",
 "/blog/tree-roots-sewer-lines-sarasota/": "tree-root-removal",
 "/blog/sewer-camera-inspection-what-to-expect/": "sewer-camera-inspection",
 "/blog/signs-sewer-line-failure/": "sewer-camera-inspection",
 "/blog/septic-to-sewer-conversion-sarasota-county/": "septic-tank-install",
 "/blog/pipe-bursting-vs-pipe-lining/": "cipp-pipe-lining",
 "/blog/siesta-key-barrier-island-sewer-challenges/": "barrier-island-aerial",
 "/blog/hydro-jetting-vs-snaking/": "hydro-jetting",
 "/about/": "work-van-technician",
 "/contact/": "downtown-sarasota",
 "/privacy-policy/": "suburban-street-live-oaks",
 "/terms-of-service/": "downtown-sarasota",
}
STICKY_IMG = {
 "/": "suburban-street-live-oaks",
 "/services/": "pipe-bursting-head",
 "/services/trenchless-sewer-repair/": "pipe-bursting-head",
 "/services/pipe-bursting/": "excavation-pipe-replacement",
 "/services/cipp-pipe-lining/": "trenchless-drilling-rig",
 "/services/sewer-camera-inspection/": "hydro-jetting",
 "/services/sewer-line-replacement/": "pipe-bursting-head",
 "/services/tree-root-removal/": "sewer-camera-inspection",
 "/services/hydro-jetting/": "sewer-camera-inspection",
 "/services/sewer-odor-detection/": "work-van-technician",
 "/services/emergency-sewer-repair/": "hydro-jetting",
 "/services/commercial-sewer-services/": "work-van-technician",
 "/services/septic-to-sewer-conversion/": "excavation-pipe-replacement",
 "/locations/": "downtown-sarasota",
 "/locations/downtown-sarasota-34236/": "siesta-key-beach",
 "/locations/st-armands-lido-key/": "barrier-island-aerial",
 "/locations/siesta-key-34242/": "st-armands-circle",
 "/locations/longboat-key-34228/": "siesta-key-beach",
 "/locations/gulf-gate-34231/": "downtown-sarasota",
 "/locations/bee-ridge-34233/": "siesta-key-beach",
 "/locations/southgate-pinecraft-34239/": "st-armands-circle",
 "/locations/north-sarasota-34234/": "downtown-sarasota",
 "/locations/palmer-ranch-34238/": "barrier-island-aerial",
 "/locations/fruitville-34232/": "siesta-key-beach",
 "/locations/bradenton/": "suburban-street-live-oaks",
 "/locations/venice/": "barrier-island-aerial",
 "/locations/north-port/": "downtown-sarasota",
 "/locations/osprey-nokomis/": "siesta-key-beach",
 "/blog/": "cipp-pipe-lining",
 "/blog/cast-iron-sewer-pipe-sarasota-slab-homes/": "tree-root-removal",
 "/blog/rainy-season-sewer-backups-sarasota/": "downtown-sarasota",
 "/blog/trenchless-vs-traditional-sewer-repair/": "cipp-pipe-lining",
 "/blog/tree-roots-sewer-lines-sarasota/": "pipe-bursting-head",
 "/blog/sewer-camera-inspection-what-to-expect/": "work-van-technician",
 "/blog/signs-sewer-line-failure/": "hydro-jetting",
 "/blog/septic-to-sewer-conversion-sarasota-county/": "excavation-pipe-replacement",
 "/blog/pipe-bursting-vs-pipe-lining/": "pipe-bursting-head",
 "/blog/siesta-key-barrier-island-sewer-challenges/": "siesta-key-beach",
 "/blog/hydro-jetting-vs-snaking/": "sewer-camera-inspection",
 "/about/": "downtown-sarasota",
 "/contact/": "work-van-technician",
 "/privacy-policy/": "downtown-sarasota",
 "/terms-of-service/": "suburban-street-live-oaks",
}
STICKY_ALT = {
 "trenchless-drilling-rig": "Trenchless drilling rig set up over an entry pit at a Sarasota home",
 "pipe-bursting-head": "Pipe bursting head pulling new HDPE pipe through sandy soil",
 "cipp-pipe-lining": "Cured-in-place pipe liner being installed at a Sarasota jobsite",
 "sewer-camera-inspection": "Technician running a sewer camera inspection at a Florida home",
 "excavation-pipe-replacement": "Open-trench sewer line replacement with new PVC pipe in Sarasota",
 "tree-root-removal": "Tree roots clogging a broken clay sewer pipe",
 "hydro-jetting": "Hydro jetting hose cleaning a residential sewer cleanout",
 "siesta-key-beach": "Siesta Key Beach, Sarasota, Florida",
 "downtown-sarasota": "Downtown Sarasota bayfront",
 "st-armands-circle": "St. Armands Circle, Sarasota",
 "suburban-street-live-oaks": "Sarasota suburban street with mature live oaks",
 "barrier-island-aerial": "Aerial view of a Florida Gulf Coast barrier island",
 "work-van-technician": "Plumbing service van at a Sarasota home",
 "septic-tank-install": "Septic tank installation in Sarasota",
}

def hero_html(d, trust_items, bg_img):
    trust = "".join(f"<span>{ihtml.escape(t)}</span>" for t in trust_items)
    return f"""<header class="hero"><div class="hero-bg" aria-hidden="true"><img src="/images/{bg_img}.webp" alt="" fetchpriority="high" width="1280" height="853"></div><div class="hero-shade"></div><div class="wrap hero-content">
<span class="eyebrow">{esc(d.get("eyebrow") or "Sarasota, FL \u00b7 Sewer Line Specialists")}</span>
<h1>{esc(d["h1"])}</h1>
<p class="lede">{esc(d["hero_sub"])}</p>
<div class="ctas"><a class="btn" href="{PHONE_TEL}">Call {esc(PHONE)}</a><a class="btn ghost" href="/services/">Explore Services</a></div>
<div class="trustrow">{trust}</div></div></header>"""

TRUST_DEFAULT = ["Trenchless & No-Dig Methods", "HD Sewer Camera Inspections",
                 "Cast-Iron, Clay & PVC Experts"]

def sections_html(d, split_from=1):
    secs = d["sections"]
    out = []
    # first section: full-width prose
    if secs:
        s = secs[0]
        out.append(f'<section class="block"><div class="wrap"><div class="prose">'
                   f'<h2>{esc(s["h2"])}</h2>{sanitize_html(s["html"])}</div></div></section>')
    # remaining sections: split layout with sticky visual
    if len(secs) > 1:
        body = "".join(f'<h2>{esc(s["h2"])}</h2>{sanitize_html(s["html"])}' for s in secs[1:])
        out.append(f'<section class="block" style="background:var(--card)"><div class="wrap">'
                   f'<div class="split"><div class="prose">{body}</div>'
                   f'<aside class="sticky-visual has-photo"><img src="/images/{STICKY_IMG[d["url_path"]]}.webp" alt="{STICKY_ALT[STICKY_IMG[d["url_path"]]]}" width="1280" height="853" loading="lazy"></aside>'
                   f'</div></div></section>')
    return "\n".join(out)

def faq_html(d):
    faqs = d.get("faqs") or []
    if not faqs:
        return ""
    items = "".join(
        f'<details><summary>{esc(f["q"])}</summary>{sanitize_html(f["a"])}</details>'
        for f in faqs)
    return (f'<section class="block"><div class="wrap"><div class="faq">'
            f'<div class="sec-head"><h2>Frequently Asked Questions</h2></div>'
            f'{items}</div></div></section>')

def crumbs_for(d):
    kind = d["kind"]
    path = d["url_path"]
    if path == "/":
        return [("Home", "/")]
    if kind == "service":
        return [("Home", "/"), ("Services", "/services/"), (SHORTS[d["slug"]], path)]
    if kind == "location":
        return [("Home", "/"), ("Service Areas", "/locations/"), (d["area_label"], path)]
    if kind == "blog":
        return [("Home", "/"), ("Blog", "/blog/"), ("Guide", path)]
    names = {"services": "Services", "locations": "Service Areas", "blog": "Blog",
             "about": "About", "contact": "Contact",
             "privacy-policy": "Privacy Policy", "terms-of-service": "Terms of Service"}
    label = names.get(d["slug"], d["h1"])
    if path in ("/services/", "/locations/", "/blog/"):
        return [("Home", "/"), (label, path)]
    return [("Home", "/"), (label, path)]

# ---------------- page-type bodies ----------------
def by_slug(reg, kind, slug):
    for d in reg.values():
        if d["kind"] == kind and d["slug"] == slug:
            return d
    raise KeyError(f"missing {kind}/{slug}")

def card_grid(items, more_text="Learn more"):
    cards = "".join(
        f'<div class="card pic"><a class="card-pic" href="{d["url_path"]}" aria-label="{esc(label)}">'
        f'<img src="/images/{HERO_IMG[d["url_path"]]}.webp" alt="{esc(label)}" loading="lazy" width="1280" height="853"></a>'
        f'<div class="card-body"><h3><a href="{d["url_path"]}">{esc(label)}</a></h3>'
        f'<p>{esc(blurb)}</p><a class="more" href="{d["url_path"]}">{more_text} &rarr;</a></div></div>'
        for d, label, blurb in items)
    return f'<div class="grid">{cards}</div>'

def related_service_body(d, reg):
    locs = locations(reg)
    i = services(reg).index(d)
    picks = [locs[(i * 2 + k) % len(locs)] for k in range(5)]
    pills = "".join(
        f'<a class="pill" href="{l["url_path"]}">{esc(l["area_label"])}'
        + (f' <b>{" / ".join(l.get("zips") or [])}</b>' if l.get("zips") else "")
        + '</a>' for l in picks)
    blog_cards = [(by_slug(reg, "blog", s), by_slug(reg, "blog", s)["h1"],
                   by_slug(reg, "blog", s)["meta"][:110] + "…")
                  for s in SERVICE_BLOGS[d["slug"]]]
    return (f'<section class="block"><div class="wrap">'
            f'<div class="sec-head"><h2>{esc(SHORTS[d["slug"]])} Across Sarasota</h2>'
            f'<p>We bring {esc(SHORTS[d["slug"]].lower())} to homes throughout Sarasota and nearby Gulf Coast cities.</p></div>'
            f'<div class="pills">{pills}</div></div></section>'
            f'<section class="block" style="background:var(--card)"><div class="wrap">'
            f'<div class="sec-head"><h2>Related Reading</h2></div>'
            f'{card_grid(blog_cards)}</div></section>')

def related_location_body(d, reg):
    svcs = services(reg)
    j = locations(reg).index(d)
    picks = [svcs[(j * 3 + k) % len(svcs)] for k in range(5)]
    cards = [(s, SHORTS[s["slug"]], s["meta"][:110] + "…") for s in picks]
    blog_cards = [(by_slug(reg, "blog", s), by_slug(reg, "blog", s)["h1"],
                   by_slug(reg, "blog", s)["meta"][:110] + "…")
                  for s in LOCATION_BLOGS[d["slug"]]]
    zips = d.get("zips") or []
    zip_pills = ("".join(f'<span class="pill">ZIP <b>{z}</b></span>' for z in zips)
                 if zips else "")
    return (f'<section class="block"><div class="wrap">'
            f'<div class="sec-head"><h2>Sewer Services in {esc(d["area_label"])}</h2>'
            f'<p>Full-service sewer line care for {esc(d["area_label"])} homes.</p></div>'
            f'{card_grid(cards)}</div></section>'
            + (f'<section class="block" style="background:var(--card)"><div class="wrap">'
                f'<div class="sec-head"><h2>ZIP Codes Served</h2></div>'
                f'<div class="pills">{zip_pills}</div></div></section>' if zip_pills else "")
            + f'<section class="block"><div class="wrap">'
            f'<div class="sec-head"><h2>Local Sewer Guides</h2></div>'
            f'{card_grid(blog_cards)}</div></section>')

def related_blog_body(d, reg):
    svc_slugs, loc_slugs = BLOG_REL[d["slug"]]
    svc_cards = [(by_slug(reg, "service", s), SHORTS[s],
                  by_slug(reg, "service", s)["meta"][:110] + "…") for s in svc_slugs]
    loc_pills = "".join(
        f'<a class="pill" href="{by_slug(reg, "location", s)["url_path"]}">'
        f'{esc(by_slug(reg, "location", s)["area_label"])}</a>' for s in loc_slugs)
    date = d.get("date", "")
    dateline = f'<p style="color:var(--muted);font-size:14px;margin-bottom:18px">Published {esc(date)} · {esc(BIZ)}</p>' if date else ""
    return (dateline
            + f'<section class="block"><div class="wrap">'
            f'<div class="sec-head"><h2>Related Sewer Services</h2></div>'
            f'{card_grid(svc_cards)}</div></section>'
            f'<section class="block" style="background:var(--card)"><div class="wrap">'
            f'<div class="sec-head"><h2>Nearby Service Areas</h2></div>'
            f'<div class="pills">{loc_pills}</div></div></section>')

def hub_body(d, reg):
    slug = d["slug"]
    if slug == "services":
        items = [(s, SHORTS[s["slug"]], s["hero_sub"][:120] + "…") for s in services(reg)]
        return (f'<section class="block"><div class="wrap">'
                f'<div class="sec-head"><h2>All Sewer Services</h2>'
                f'<p>Eleven specialized services, one focus: Sarasota sewer lines.</p></div>'
                f'{card_grid(items)}</div></section>')
    if slug == "locations":
        pills = "".join(
            f'<a class="pill" href="{l["url_path"]}">{esc(l["area_label"])}'
            + (f' <b>{" / ".join(l.get("zips") or [])}</b>' if l.get("zips") else "")
            + '</a>' for l in locations(reg))
        return (f'<section class="block"><div class="wrap">'
                f'<div class="sec-head"><h2>All Service Areas</h2>'
                f'<p>ZIP-code-level sewer line service across Sarasota and nearby cities.</p></div>'
                f'<div class="pills">{pills}</div></div></section>')
    if slug == "blog":
        items = [(b, b["h1"], b["meta"][:120] + "…") for b in blogs(reg)]
        return (f'<section class="block"><div class="wrap">'
                f'<div class="sec-head"><h2>All Guides</h2>'
                f'<p>Sarasota-specific sewer knowledge, written for homeowners.</p></div>'
                f'{card_grid(items, more_text="Read guide")}</div></section>')
    return ""

def home_body(d, reg):
    svc_items = [(s, SHORTS[s["slug"]], s["hero_sub"][:110] + "…")
                 for s in services(reg)[:6]]
    pills = "".join(
        f'<a class="pill" href="{l["url_path"]}">{esc(l["area_label"])}'
        + (f' <b>{" / ".join(l.get("zips") or [])}</b>' if l.get("zips") else "")
        + '</a>' for l in locations(reg))
    return (f'<section class="block"><div class="wrap">'
            f'<div class="sec-head"><h2>Our Sewer Services</h2>'
            f'<p>Specialized services for every kind of Sarasota sewer line problem.</p></div>'
            f'{card_grid(svc_items)}'
            f'<p style="margin-top:22px"><a class="btn" href="/services/">View All Services</a></p>'
            f'</div></section>'
            f'<section class="block" style="background:var(--card)"><div class="wrap">'
            f'<div class="sec-head"><h2>Where We Work</h2>'
            f'<p>ZIP-code coverage across Sarasota, the barrier islands, and nearby Gulf Coast cities.</p></div>'
            f'<div class="pills">{pills}</div></div></section>')

def contact_extra(d):
    return (f'<section class="block"><div class="wrap"><div class="prose">'
            f'<h2>Find Us in Sarasota</h2>'
            f'<p>We serve homes and businesses throughout Sarasota, FL and surrounding communities.</p>'
            f'<div class="mapwrap"><iframe title="Map - 2354 Margaret St, Sarasota, FL 34237" loading="lazy" '
            f'src="https://www.google.com/maps?q=2354+Margaret+St,Sarasota,FL+34237&output=embed"></iframe></div>'
            f'</div></div></section>')

# ---------------- page assembler ----------------
def render_page(d, reg):
    crumbs = crumbs_for(d)
    # no visible breadcrumb on the homepage (it would just say "Home")
    crumb_html = ""
    if d["url_path"] != "/":
        crumb_html = ('<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">'
                      + " &rsaquo; ".join(
                          f'<a href="{p}">{esc(n)}</a>' if p != d["url_path"]
                          else f'<span>{esc(n)}</span>' for n, p in crumbs)
                      + "</nav></div>")
    ld = [ld_breadcrumbs(crumbs)]
    if d.get("faqs"):
        ld.append(ld_faq(d["faqs"]))
    if d["kind"] == "service":
        ld.append(ld_service(d))
    if d["url_path"] in ("/", "/contact/"):
        ld.append(ld_localbusiness())

    kind = d["kind"]
    body_extra = ""
    if kind == "service":
        body_extra = related_service_body(d, reg)
    elif kind == "location":
        body_extra = related_location_body(d, reg)
    elif kind == "blog":
        body_extra = related_blog_body(d, reg)
    elif d["slug"] == "home":
        body_extra = home_body(d, reg)
    elif d["slug"] in ("services", "locations", "blog"):
        body_extra = hub_body(d, reg)
    if d["url_path"] == "/contact/":
        body_extra += contact_extra(d)

    html = f"""<!DOCTYPE html>
<html lang="en">
{head_html(d, ld)}
<body>
<div class="topbar"><div class="wrap">
<span>Trenchless Sewer Line Repair in {esc(CITY)}</span>
<span>Serving All Sarasota ZIP Codes &nbsp; <a class="phone" href="{PHONE_TEL}">{esc(PHONE)}</a></span>
</div></div>
{nav_html(reg)}
{crumb_html}
<main>
{hero_html(d, TRUST_DEFAULT, HERO_IMG[d["url_path"]])}
{sections_html(d)}
{body_extra}
{faq_html(d)}
</main>
{cta_band()}
{footer_html(reg)}
</body></html>"""
    return html

# ---------------- output ----------------
def write_page(d, html):
    path = d["url_path"].strip("/")
    outdir = os.path.join(DIST, path) if path else DIST
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(html)

def write_sitemap(reg):
    urls = sorted(reg.keys())
    items = "\n".join(
        f'  <url><loc>{DOMAIN}{u}</loc><lastmod>2026-10-09</lastmod></url>'
        for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + items + '\n</urlset>\n')
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write(xml)
    return len(urls)

def write_robots():
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

def write_favicon():
    with open(os.path.join(DIST, "favicon.svg"), "w") as f:
        f.write(FAVICON_SVG)

def write_favicon_pngs():
    from PIL import Image, ImageDraw
    import math
    def draw_mark(size):
        s = float(size) / 44.0
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        dr.rounded_rectangle([0, 0, size, size], radius=int(11 * s), fill="#0A3D42")
        w = max(1, int(6.5 * s))
        dr.line([(14 * s, 31 * s), (14 * s, 21 * s)], fill="white", width=w)
        dr.arc([14 * s, 13 * s, 30 * s, 29 * s], start=180, end=270, fill="white", width=w)
        dr.line([(22 * s, 13 * s), (31 * s, 13 * s)], fill="white", width=w)
        ww = max(1, int(3.6 * s))
        pts = [(x * s, (36.5 - 2.25 * math.sin(2 * math.pi * (x - 9) / 10)) * s)
               for x in range(9, 40)]
        dr.line(pts, fill="#E8713A", width=ww, joint="curve")
        return im
    draw_mark(64).save(os.path.join(DIST, "favicon-64.png"))
    draw_mark(180).save(os.path.join(DIST, "apple-touch-icon.png"))
def main():
    reg = load_registry()
    print(f"loaded {len(reg)} pages")
    for path, d in sorted(reg.items()):
        write_page(d, render_page(d, reg))
    n = write_sitemap(reg)
    write_robots()
    write_favicon()
    write_favicon_pngs()
    print(f"wrote {n} pages + sitemap.xml + robots.txt + favicon.svg to dist/")

if __name__ == "__main__":
    main()
