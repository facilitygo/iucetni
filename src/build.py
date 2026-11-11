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
    "bez-aplikace": ("/bez-aplikace/", "/en/without-the-app/"),
}

L = {
    "cs": {
        "home_nav": [("#funkce", "Funkce"), ("#apple", "Pro Apple"), ("#pribehy", "Příběhy"), ("#ai", "AI asistent"), ("#cenik", "Ceník"), ("/mcp/", "MCP")],
        "doc_nav": [("/#funkce", "Funkce"), ("/#pribehy", "Příběhy"), ("/#cenik", "Ceník"), ("/bez-aplikace/", "V Claude a ChatGPT"), ("/mcp/", "MCP server"), ("/podpora/", "Podpora")],
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
        <ul><li><a href="/#funkce">Funkce</a></li><li><a href="/#pribehy">Příběhy</a></li><li><a href="/#cenik">Ceník</a></li><li><a href="/bez-aplikace/">V Claude a ChatGPT</a></li><li><a href="/mcp/">MCP server</a></li></ul>
      </div>
      <div>
        <h4>Informace</h4>
        <ul><li><a href="/podpora/">Podpora</a></li><li><a href="/podminky/">Podmínky použití</a></li><li><a href="/soukromi/">Ochrana soukromí</a></li><li><a href="mailto:support@iucetni.com">support@iucetni.com</a></li></ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 NEMOSERVIS Praha s.r.o. NEMOSERVIS® je registrovaná ochranná známka společnosti NEMOSERVIS Praha s.r.o. Apple, iPhone, iPad, Mac, Siri a App Store jsou ochranné známky Apple Inc. Claude je ochranná známka Anthropic PBC, OpenAI a ChatGPT jsou ochranné známky OpenAI.</span>
      <span class="foot-tools"><a class="lang-link" href="{other}" hreflang="en" lang="en">English</a><button class="theme-btn" id="theme" type="button" aria-label="Přepnout motiv">Motiv: auto</button></span>
    </div>
  </div>
</footer>""",
    },
    "en": {
        "home_nav": [("#features", "Features"), ("#apple", "Made for Apple"), ("#use-cases", "Use cases"), ("#ai", "AI assistant"), ("#pricing", "Pricing"), ("/en/mcp/", "MCP")],
        "doc_nav": [("/en/#features", "Features"), ("/en/#use-cases", "Use cases"), ("/en/#pricing", "Pricing"), ("/en/without-the-app/", "In Claude & ChatGPT"), ("/en/mcp/", "MCP server"), ("/en/support/", "Support")],
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
        <ul><li><a href="/en/#features">Features</a></li><li><a href="/en/#use-cases">Use cases</a></li><li><a href="/en/#pricing">Pricing</a></li><li><a href="/en/without-the-app/">In Claude &amp; ChatGPT</a></li><li><a href="/en/mcp/">MCP server</a></li></ul>
      </div>
      <div>
        <h4>Information</h4>
        <ul><li><a href="/en/support/">Support</a></li><li><a href="/en/terms/">Terms of Use</a></li><li><a href="/en/privacy/">Privacy Policy</a></li><li><a href="mailto:support@iucetni.com">support@iucetni.com</a></li></ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 NEMOSERVIS Praha s.r.o. NEMOSERVIS® is a registered trademark of NEMOSERVIS Praha s.r.o. Apple, iPhone, iPad, Mac, Siri and App Store are trademarks of Apple Inc. Claude is a trademark of Anthropic PBC; OpenAI and ChatGPT are trademarks of OpenAI.</span>
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


# ---------- pro vyhledávače a AI: robots.txt, llms.txt, llms-full.txt ----------
from html.parser import HTMLParser

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai",
           "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "CCBot",
           "Meta-ExternalAgent", "Amazonbot", "DuckAssistBot", "MistralAI-User", "Bingbot"]

ROBOTS = "# iucetni.com – vyhledávače i AI crawleři jsou vítáni / search engines and AI crawlers are welcome\n" \
    "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS) + \
    f"Sitemap: {SITE}/sitemap.xml\n# LLM summary: {SITE}/llms.txt · full text: {SITE}/llms-full.txt\n"

LLMS = f"""# iÚčetní

> iÚčetní is a native invoicing and tax-records app for iPhone, iPad and Mac, built for Czech sole traders and small businesses. It issues invoices with QR payments and ISDOC e-invoices, reads receipts from photos and PDFs, exports to POHODA, Money S3 and ABRA Flexi, and provides an MCP server so Claude, ChatGPT and other AI agents can work with invoices, customers and expenses. Free for one user on one device with data in the EU cloud; iÚčetní Pro (CZK 99/month or CZK 749/year, 7-day free trial) adds unlimited devices, up to 5 more people per company (edit or read-only roles; no Apple Family Sharing), on-device storage and an in-app AI assistant with the Claude Haiku model included (10 invoices and 20 receipts every 30 days, counted per saved invoice or receipt; AI credit (Small, Medium, Large), also available in the Free plan, lasts until used up: CZK 49 10 invoices + 20 receipts, CZK 299 80 invoices + 150 receipts, CZK 999 300 invoices + 600 receipts with Haiku or about a tenth of that with Sonnet; or the user's own Claude/OpenAI key). The app shows AI usage and a personal estimate of remaining invoices. AI over MCP runs in the user's own Claude/ChatGPT subscription and is free on the iÚčetní side (no allowance or credit used, except server-side receipt reading via read_receipt, which counts as one receipt in Pro or uses the limited trial in Free), so users can work day to day only in Claude or ChatGPT without opening the app; a limited free trial AI is available in the Free plan. Operated by NEMOSERVIS Praha s.r.o., Czech Republic.

Key facts:
- Platforms: iOS 26, iPadOS 26, macOS 26 – one App Store app (coming soon). The app UI is in Czech.
- MCP server: `https://mcp.iucetni.com/mcp/` (Streamable HTTP). Auth: OAuth 2.1 (Authorization Code + PKCE S256, dynamic client registration, scope `mcp`) or a Bearer AI key issued in the app. Free in every plan.
- MCP tools include list_invoices, get_invoice, get_invoice_pdf, create_draft, update_invoice, issue_invoice, mark_invoice_paid, list_customers, create_customer, lookup_ares, list_catalog, create_catalog_item, list_expenses, create_expense, update_expense, read_receipt, list_companies, list_bank_accounts.
- Data is stored on servers in the EU. No ads, no third-party tracking.
- Czech specifics: ARES company registry lookup, Czech National Bank exchange rates, VAT 21/12/0 %, reverse charge, flat-rate expenses (80/60/40/30 %).
- Support: support@iucetni.com

## Docs

- [Invoicing in Claude or ChatGPT without the app (EN)]({SITE}/en/without-the-app/): use iÚčetní only from Claude/ChatGPT over MCP; free in every plan, AI runs in the user's own subscription and uses no iÚčetní AI allowance or credit; the app is needed once to set up the account and company
- [Fakturace v Claude a ChatGPT bez aplikace (CS)]({SITE}/bez-aplikace/)
- [MCP server – how to connect (EN)]({SITE}/en/mcp/): Claude, ChatGPT, Claude Code, own agents; OAuth details; tools; security
- [MCP server – návod (CS)]({SITE}/mcp/)
- [Product overview (EN)]({SITE}/en/): features, use cases, pricing, FAQ
- [Přehled aplikace (CS)]({SITE}/): funkce, příběhy, ceník, časté otázky

## Policies

- [Privacy Policy (EN)]({SITE}/en/privacy/) · [Ochrana soukromí (CS)]({SITE}/soukromi/)
- [Terms of Use (EN)]({SITE}/en/terms/) · [Podmínky použití (CS)]({SITE}/podminky/)
- [Support (EN)]({SITE}/en/support/) · [Podpora (CS)]({SITE}/podpora/)

## Optional

- [Full text of the website]({SITE}/llms-full.txt)
- [OAuth protected resource metadata](https://mcp.iucetni.com/.well-known/oauth-protected-resource/mcp/)
- [OAuth authorization server metadata](https://mcp.iucetni.com/.well-known/oauth-authorization-server)
"""


class _Text(HTMLParser):
    """Převod stránky na čistý text (Markdown-like) – bez SVG, skriptů, hlavičky, patičky a ilustrativních náhledů."""
    SKIP = {"script", "style", "svg", "header", "footer", "nav", "button", "head"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "summary", "details", "section", "article", "div", "ol", "ul", "table"}

    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0; self.stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        hidden = a.get("aria-hidden") == "true"
        if tag in ("br", "img", "meta", "link", "input"):
            if tag == "br" and not self.skip: self.out.append("\n")
            return
        self.stack.append((tag, hidden or tag in self.SKIP))
        if hidden or tag in self.SKIP: self.skip += 1; return
        if self.skip: return
        if tag in self.BLOCK: self.out.append("\n")
        if tag in ("h1", "h2", "h3"): self.out.append("#" * int(tag[1]) + " ")
        if tag == "li": self.out.append("- ")
        if tag == "td": self.out.append(" | ")
        if tag in ("span", "small", "b", "a", "code"): self.out.append(" ")

    def handle_endtag(self, tag):
        while self.stack:
            t, sk = self.stack.pop()
            if sk: self.skip -= 1
            if t == tag: break
        if not self.skip and tag in self.BLOCK and tag != "li": self.out.append("\n")
        if not self.skip and tag in ("span", "small"): self.out.append(" ")

    def handle_data(self, data):
        if not self.skip: self.out.append(data)

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = re.sub(r"\n\n(?=- )", "\n", t)
        t = re.sub(r" ([.,:;!?])", r"\1", t)
        return re.sub(r"\n{3,}", "\n\n", t).strip()


def write_ai_files():
    (PUB / "robots.txt").write_text(ROBOTS)
    (PUB / "llms.txt").write_text(LLMS)
    parts = [f"# iÚčetní – full website text\n\nSource: {SITE} · generated by src/build.py\n"]
    for lang_i, lang in ((1, "en"), (0, "cs")):
        for key, paths in ROUTES.items():
            f = PUB / paths[lang_i].lstrip("/") / "index.html"
            p = _Text(); p.feed(f.read_text())
            parts.append(f"\n\n---\n\nURL: {SITE}{paths[lang_i]}\n\n" + p.text())
    (PUB / "llms-full.txt").write_text("".join(parts) + "\n")
    print("ok public/robots.txt, llms.txt, llms-full.txt")


if __name__ == "__main__":
    main()
    write_ai_files()
