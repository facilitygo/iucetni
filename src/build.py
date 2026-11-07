#!/usr/bin/env python3
"""Sestaví web do public/ ze zdrojů v src/.

src/pages/<jazyk>/<klíč>.html  – hlavička (title, description, kind, key) + '---' + obsah
src/ill/<název>.svg            – ilustrace; vkládají se značkou {{ill:název}}
[[česky|english]]              – text podle jazyka (hlavně v ilustracích)

Spuštění: python3 src/build.py
"""
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, PUB = ROOT / "src", ROOT / "public"
SITE = "https://iucetni.com"

ROUTES = {  # klíč: (cesta cs, cesta en)
    "index": ("/", "/en/"),
    "soukromi": ("/soukromi/", "/en/privacy/"),
    "podminky": ("/podminky/", "/en/terms/"),
    "podpora": ("/podpora/", "/en/support/"),
    "mcp": ("/mcp/", "/en/mcp/"),
}

L = {
    "cs": {
        "home_nav": [("#funkce", "Funkce"), ("#apple", "Pro Apple"), ("#pribehy", "Příběhy"), ("#ai", "AI asistent"), ("#cenik", "Ceník"), ("/mcp/", "MCP")],
        "doc_nav": [("/#funkce", "Funkce"), ("/#pribehy", "Příběhy"), ("/#cenik", "Ceník"), ("/mcp/", "MCP server"), ("/podpora/", "Podpora")],
        "cta": "Brzy v App Store", "cta_home": "#stahnout", "cta_doc": "/#stahnout",
        "switch": ("EN", "English version"), "home": "iÚčetní – úvod", "menu": "Menu",
        "suffix": " – iÚčetní", "locale": "cs_CZ",
        "footer": """<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="/"><img src="/img/logo.png" alt="" width="28" height="28">iÚčetní</a>
        <p>Vyvíjí a provozuje NEMOSERVIS Praha s.r.o.<br>Belgická 23, 120 00 Praha 2<br>IČO 26122375 · DIČ CZ26122375</p>
      </div>
      <div>
        <h4>Aplikace</h4>
        <ul><li><a href="/#funkce">Funkce</a></li><li><a href="/#pribehy">Příběhy</a></li><li><a href="/#cenik">Ceník</a></li><li><a href="/mcp/">MCP server</a></li></ul>
      </div>
      <div>
        <h4>Informace</h4>
        <ul><li><a href="/podpora/">Podpora</a></li><li><a href="/podminky/">Podmínky použití</a></li><li><a href="/soukromi/">Ochrana soukromí</a></li><li><a href="mailto:support@iucetni.com">support@iucetni.com</a></li></ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 NEMOSERVIS Praha s.r.o. Apple, iPhone, iPad, Mac, Siri a App Store jsou ochranné známky společnosti Apple Inc.</span>
      <span class="foot-tools"><a class="lang-link" href="{other}" hreflang="en" lang="en">English</a><button class="theme-btn" id="theme" type="button" aria-label="Přepnout motiv">Motiv: auto</button></span>
    </div>
  </div>
</footer>""",
    },
    "en": {
        "home_nav": [("#features", "Features"), ("#apple", "Made for Apple"), ("#use-cases", "Use cases"), ("#ai", "AI assistant"), ("#pricing", "Pricing"), ("/en/mcp/", "MCP")],
        "doc_nav": [("/en/#features", "Features"), ("/en/#use-cases", "Use cases"), ("/en/#pricing", "Pricing"), ("/en/mcp/", "MCP server"), ("/en/support/", "Support")],
        "cta": "Coming to the App Store", "cta_home": "#download", "cta_doc": "/en/#download",
        "switch": ("CZ", "Česká verze"), "home": "iÚčetní – home", "menu": "Menu",
        "suffix": " – iÚčetní", "locale": "en_US",
        "footer": """<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="/en/"><img src="/img/logo.png" alt="" width="28" height="28">iÚčetní</a>
        <p>Developed and operated by NEMOSERVIS Praha s.r.o.<br>Belgická 23, 120 00 Prague 2, Czech Republic<br>Company ID 26122375 · VAT ID CZ26122375</p>
      </div>
      <div>
        <h4>Product</h4>
        <ul><li><a href="/en/#features">Features</a></li><li><a href="/en/#use-cases">Use cases</a></li><li><a href="/en/#pricing">Pricing</a></li><li><a href="/en/mcp/">MCP server</a></li></ul>
      </div>
      <div>
        <h4>Information</h4>
        <ul><li><a href="/en/support/">Support</a></li><li><a href="/en/terms/">Terms of Use</a></li><li><a href="/en/privacy/">Privacy Policy</a></li><li><a href="mailto:support@iucetni.com">support@iucetni.com</a></li></ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 NEMOSERVIS Praha s.r.o. Apple, iPhone, iPad, Mac, Siri and App Store are trademarks of Apple Inc.</span>
      <span class="foot-tools"><a class="lang-link" href="{other}" hreflang="cs" lang="cs">Česky</a><button class="theme-btn" id="theme" type="button" aria-label="Switch theme">Theme: auto</button></span>
    </div>
  </div>
</footer>""",
    },
}

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#6e0a63" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#140d18" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{site}{path}">
<link rel="alternate" hreflang="cs" href="{site}{cs}">
<link rel="alternate" hreflang="en" href="{site}{en}">
<link rel="alternate" hreflang="x-default" href="{site}{cs}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:site_name" content="iÚčetní">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{path}">
<meta property="og:image" content="{site}/img/icon-512.png">
<script>try{{var t=localStorage.getItem('theme');if(t&&t!=='auto')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/site.css?v={ver}">
</head>
<body>
"""

HEADER = """<header>
  <div class="wrap nav">
    <a class="brand" href="{home_path}" aria-label="{home_label}"><img src="/img/logo.png" alt="" width="32" height="32">iÚčetní</a>
    <ul id="menu">
{items}
    </ul>
    <a class="lang-btn" href="{other}" hreflang="{other_lang}" lang="{other_lang}" aria-label="{switch_label}">{switch}</a>
    <a class="btn btn-primary btn-sm" href="{cta_href}">{cta}</a>
    <button class="menu-btn" type="button" aria-label="{menu}" aria-controls="menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>
"""


def parse(path):
    text = path.read_text()
    meta_raw, body = text.split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in meta_raw.splitlines() if ": " in line)
    return meta, body.strip()


def localize(text, lang):
    i = 0 if lang == "cs" else 1
    return re.sub(r"\[\[(.*?)\|(.*?)\]\]", lambda m: m.group(1 + i), text)


def main():
    import hashlib
    ver = hashlib.sha1((PUB / "assets/site.css").read_bytes() + (PUB / "assets/site.js").read_bytes()).hexdigest()[:8]
    ills = {p.stem: p.read_text().strip() for p in (SRC / "ill").glob("*.svg")}
    for lang in ("cs", "en"):
        conf = L[lang]
        other_lang = "en" if lang == "cs" else "cs"
        for src in sorted((SRC / "pages" / lang).glob("*.html")):
            meta, body = parse(src)
            key = meta["key"]
            cs_path, en_path = ROUTES[key]
            path = cs_path if lang == "cs" else en_path
            other = en_path if lang == "cs" else cs_path
            home = meta.get("kind") == "home"
            title = meta["title"] if meta.get("fulltitle") else meta["title"] + conf["suffix"]
            nav = conf["home_nav"] if home else conf["doc_nav"]
            items = "\n".join(f'      <li><a href="{h}">{html.escape(t)}</a></li>' for h, t in nav)
            body = re.sub(r"\{\{ill:([\w-]+)\}\}", lambda m: ills[m.group(1)], body)
            if not home:
                body = f'<main class="wrap"><article class="doc">\n{body}\n</article></main>'
            else:
                body = f"<main>\n{body}\n</main>"
            page = (
                HEAD.format(lang=lang, title=html.escape(title, quote=True), desc=html.escape(meta["description"], quote=True),
                            site=SITE, path=path, cs=cs_path, en=en_path, locale=conf["locale"], ver=ver)
                + HEADER.format(home_path=ROUTES["index"][0 if lang == "cs" else 1], home_label=conf["home"], items=items,
                                other=other, other_lang=other_lang, switch=conf["switch"][0], switch_label=conf["switch"][1],
                                cta_href=conf["cta_home"] if home else conf["cta_doc"], cta=conf["cta"], menu=conf["menu"])
                + "\n" + body + "\n\n" + conf["footer"].replace("{other}", other)
                + '\n<script src="/assets/site.js?v=' + ver + '" defer></script>\n</body>\n</html>\n'
            )
            page = localize(page, lang)
            out = PUB / path.lstrip("/") / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page)
            print("ok", out.relative_to(ROOT))
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc></url>" for pair in ROUTES.values() for p in pair)
    (PUB / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


if __name__ == "__main__":
    main()
