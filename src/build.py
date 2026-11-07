#!/usr/bin/env python3
"""Sestaví podstránky (soukromi, podminky, podpora) z public/index.html (hlavička, patička) a src/*.body.html."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
pub = root / "public"
index = (pub / "index.html").read_text()
footer = re.search(r"<!--FOOTER-->.*?<!--/FOOTER-->", index, re.S).group(0)
pages = {
    "soukromi": ("Ochrana soukromí", "Zásady ochrany osobních údajů aplikace iÚčetní a webu iucetni.com."),
    "podminky": ("Podmínky použití", "Podmínky používání aplikace iÚčetní, včetně předplatného iÚčetní Pro a AI funkcí."),
    "podpora": ("Podpora", "Podpora aplikace iÚčetní: kontakt, předplatné, smazání účtu a časté dotazy."),
}
tpl = """<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} – iÚčetní</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://iucetni.com/{slug}/">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script>try{{var t=localStorage.getItem('theme');if(t&&t!=='auto')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="iÚčetní – úvod"><img src="/img/logo.png" alt="" width="32" height="32">iÚčetní</a>
    <ul id="menu">
      <li><a href="/#funkce">Funkce</a></li>
      <li><a href="/#cenik">Ceník</a></li>
      <li><a href="/podpora/">Podpora</a></li>
      <li><a href="/podminky/">Podmínky</a></li>
      <li><a href="/soukromi/">Soukromí</a></li>
    </ul>
    <a class="btn btn-primary btn-sm" href="/#stahnout">Brzy v App Store</a>
    <button class="menu-btn" type="button" aria-label="Menu" aria-controls="menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>
<main class="wrap"><article class="doc">
{body}
</article></main>
{footer}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
for slug, (title, desc) in pages.items():
    body = (root / "src" / f"{slug}.body.html").read_text().strip()
    out = pub / slug / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(tpl.format(title=title, desc=desc, slug=slug, body=body, footer=footer))
    print("ok", out.relative_to(root))
