# iucetni.com

Statický web aplikace **iÚčetní** (iPhone, iPad, Mac). Hostuje se přes Cloudflare Workers (static assets).

## Struktura
| Cesta | Obsah |
|---|---|
| `src/pages/cs/`, `src/pages/en/` | **zdroj všech stránek** (úvod, MCP, podpora, podmínky, soukromí) |
| `src/ill/` | ilustrace a ikony (SVG), vkládají se značkou `{{ill:název}}`; text `[[česky|english]]` |
| `src/build.py` | sestaví `public/` – po každé úpravě spustit `python3 src/build.py` |
| `public/` | hotový web (generovaný, needitovat ručně kromě `assets/`, `img/`, `404.html`, `_headers`) |
| `public/assets/` | sdílené CSS a JS, bez externích závislostí |
| `public/404.html` | stránka „nenalezeno“ |
| `public/_headers` | bezpečnostní hlavičky a cache |
| `public/img/` | logo a ikony (malé PNG) |
| `wrangler.jsonc` | konfigurace Workeru a domén iucetni.com, www.iucetni.com |

## Lokální náhled
    npx wrangler dev        # http://localhost:8787
nebo jen `python3 -m http.server -d public`.

## Nasazení
Cloudflare → Workers & Pages → Create → Import a repository → `facilitygo/iucetni`.
Build command nechat prázdný, deploy command `npx wrangler deploy`. Každý push do `main` se nasadí sám.
Domény z `routes` se napojí automaticky, pokud je zóna iucetni.com ve stejném účtu Cloudflare.

Ručně: `npx wrangler deploy`.

## Adresy pro App Store Connect a adresáře MCP konektorů
| | česky | anglicky |
|---|---|---|
| Marketing | https://iucetni.com/ | https://iucetni.com/en/ |
| Support | https://iucetni.com/podpora/ | https://iucetni.com/en/support/ |
| Privacy Policy | https://iucetni.com/soukromi/ | https://iucetni.com/en/privacy/ |
| Terms of Use | https://iucetni.com/podminky/ | https://iucetni.com/en/terms/ |
| MCP dokumentace | https://iucetni.com/mcp/ | https://iucetni.com/en/mcp/ |
