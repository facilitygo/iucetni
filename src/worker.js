// iucetni.com – statický web + příjem žádostí o testovací přístup (POST /api/testovaci-pristup)
// Žádosti se ukládají do KV (binding BETA) pod klíčem = e-mail. Výpis: wrangler kv key list --binding BETA --remote
const PLATFORMS = ["ios", "mac", "android", "windows", "linux"];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/testovaci-pristup") {
      if (request.method !== "POST") return new Response("Method Not Allowed", { status: 405, headers: { Allow: "POST" } });
      return handleSignup(request, env, url);
    }
    return env.ASSETS.fetch(request);
  },
};

async function handleSignup(request, env, url) {
  const wantsJson = (request.headers.get("Accept") || "").includes("application/json");
  const origin = request.headers.get("Origin");
  if (origin && new URL(origin).host !== url.host) return reply(wantsJson, 403, "origin", url);
  if (Number(request.headers.get("Content-Length") || 0) > 8000) return reply(wantsJson, 413, "size", url);

  let form;
  try { form = await request.formData(); } catch { return reply(wantsJson, 400, "form", url); }
  const lang = form.get("lang") === "en" ? "en" : "cs";
  if (form.get("web")) return reply(wantsJson, 200, "ok", url, lang); // honeypot: tváříme se, že je hotovo

  const email = String(form.get("email") || "").trim().toLowerCase().slice(0, 200);
  const name = String(form.get("name") || "").trim().slice(0, 200);
  const note = String(form.get("note") || "").trim().slice(0, 2000);
  const platforms = form.getAll("platform").map(String).filter((p) => PLATFORMS.includes(p));
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return reply(wantsJson, 400, "email", url, lang);
  if (!platforms.length) return reply(wantsJson, 400, "platform", url, lang);
  if (form.get("consent") !== "1") return reply(wantsJson, 400, "consent", url, lang);

  const now = new Date().toISOString();
  const prev = await env.BETA.get(email, "json");
  const record = { email, name, platforms, note, lang, created: prev?.created || now, updated: now, country: request.cf?.country || null };
  await env.BETA.put(email, JSON.stringify(record), { metadata: { platforms: platforms.join(","), created: record.created } });
  return reply(wantsJson, 200, "ok", url, lang);
}

function reply(json, status, code, url, lang = "cs") {
  if (json) return Response.json({ ok: status === 200, code }, { status });
  const page = lang === "en" ? "/en/test-access/" : "/testovaci-pristup/";
  return Response.redirect(new URL(`${page}?${status === 200 ? "odeslano=1" : "chyba=" + code}#formular`, url), 303);
}
