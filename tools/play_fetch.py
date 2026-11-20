# Play'deki herkese açık mağaza sayfalarından başlık, açıklama ve ekran görüntüsü adreslerini okur (yalnız okuma).
import json, re, sys, html, urllib.request, pathlib
APPS = ["idletok", "idledropshippingtycoon", "tekirexpress", "pearltopower"]
out = {}
for a in APPS:
    for l in ("en", "tr"):
        u = f"https://play.google.com/store/apps/details?id=com.eraistudio.{a}&hl={l}&gl=US"
        h = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": l})).read().decode("utf-8")
        title = html.unescape(re.search(r'<meta property="og:title" content="([^"]+)"', h).group(1)).split(" - ")[0]
        m = re.search(r'data-g-id="description"[^>]*>(.*?)</div>', h, re.S)
        desc = html.unescape(re.sub(r"<br\s*/?>", "\n", m.group(1))) if m else ""
        desc = re.sub(r"<[^>]+>", "", desc).strip()
        shots = re.findall(r'<img[^>]+src="(https://play-lh\.googleusercontent\.com/[^"=]+)=w526[^"]*"[^>]*alt="[^"]*"', h)
        out[f"{a}/{l}"] = {"title": title, "desc": desc, "shots": list(dict.fromkeys(shots))}
        print(a, l, title, len(desc), len(out[f"{a}/{l}"]["shots"]))
pathlib.Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
