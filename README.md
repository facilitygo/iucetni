# iucetni.com

Statický web aplikace **iÚčetní** (iPhone, iPad, Mac). Hostuje se přes Cloudflare Workers (static assets).

## Struktura
| Cesta | Obsah |
|---|---|
| `public/index.html` | úvodní stránka (ilustrace jsou inline SVG) |
| `public/assets/` | sdílené CSS a JS, bez externích závislostí |
| `public/podpora/`, `podminky/`, `soukromi/` | podpora, podmínky použití, ochrana soukromí (URL pro App Store) |
| `src/*.body.html`, `src/build.py` | zdroj podstránek – po úpravě spustit `python3 src/build.py` (převezme patičku z index.html) |
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

## Adresy pro App Store Connect
- Support URL: https://iucetni.com/podpora/
- Privacy Policy URL: https://iucetni.com/soukromi/
- Terms of Use (EULA): https://iucetni.com/podminky/ (doplňuje standardní EULA Apple)
- Marketing URL: https://iucetni.com/
