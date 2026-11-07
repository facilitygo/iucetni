# iucetni.com

Statický web aplikace **iÚčetní** (iPhone, iPad, Mac). Hostuje se přes Cloudflare Workers (static assets).

## Struktura
| Cesta | Obsah |
|---|---|
| `public/index.html` | celá úvodní stránka (CSS a JS inline, bez závislostí) |
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
