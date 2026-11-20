# Görselleri ve yazı tiplerini indirir/kopyalar (bir kez; çıktılar depoya girer).
import json, re, shutil, urllib.request, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((R/"tools/play.json").read_text(encoding="utf-8"))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
def get(u, p):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(urllib.request.urlopen(urllib.request.Request(u, headers=UA)).read())
SLUG = {"idletok": "idle-tok", "idledropshippingtycoon": "idle-dropshipping-tycoon", "tekirexpress": "tekir-express", "pearltopower": "pearl-to-power"}
for k, v in d.items():
    app, lang = k.split("/")
    for i, u in enumerate(v["shots"][:4], 1):
        get(f"{u}=w540-rw", R/f"img/{SLUG[app]}/shot-{lang}-{i}.webp")
# simgeler (Play'deki canlı simge)
for app, s in SLUG.items():
    h = urllib.request.urlopen(urllib.request.Request(f"https://play.google.com/store/apps/details?id=com.eraistudio.{app}&hl=en", headers=UA)).read().decode()
    u = re.search(r'<meta property="og:image" content="([^"=]+)', h).group(1)
    get(f"{u}=s512", R/f"img/{s}/icon-512.png"); get(f"{u}=s192-rw", R/f"img/{s}/icon.webp")
# yazı tipleri (latin + latin-ext; Türkçe harfler için)
css_u = "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Source+Serif+4:wght@400;600&display=swap"
css = urllib.request.urlopen(urllib.request.Request(css_u, headers=UA)).read().decode()
out, n = [], 0
for block in re.findall(r"/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
    subset, ff = block
    if subset not in ("latin", "latin-ext"): continue
    url = re.search(r"url\((https://[^)]+)\)", ff).group(1)
    fam = re.search(r"font-family: '([^']+)'", ff).group(1).replace(" ", "")
    w = re.search(r"font-weight: (\d+)", ff).group(1)
    name = f"{fam}-{w}-{subset}.woff2"
    if not (R/"fonts"/name).exists(): get(url, R/"fonts"/name); n += 1
    out.append(ff.replace(url, f"/fonts/{name}"))
(R/"fonts/fonts.css").write_text("\n".join(out), encoding="utf-8")
print("tamam; yeni yazı tipi dosyası:", n)
