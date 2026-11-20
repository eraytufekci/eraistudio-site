# eraistudio.com statik sitesini üretir: python -X utf8 tools/build.py
# Metinler Play mağaza sayfalarından (tools/play.json, tools/play_fetch.py ile yenilenir); sitede yeni iddia yazılmaz.
import html, json, pathlib, re

R = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://eraistudio.com"
EMAIL = "eraistudiogames@gmail.com"
PLAY = json.loads((R / "tools/play.json").read_text(encoding="utf-8"))
SOCIAL = [
    ("YouTube", "https://www.youtube.com/@eraistudiogames"),
    ("Instagram", "https://www.instagram.com/eraistudiogames/"),
    ("TikTok", "https://www.tiktok.com/@eraistudio_games"),
    ("Facebook", "https://www.facebook.com/profile.php?id=61594981989212"),
    ("Google Play", "https://play.google.com/store/apps/dev?id=8369372898684036857"),
]

GAMES = [
    dict(slug="tekir-express", key="tekirexpress", name="Tekir Express", pkg="com.eraistudio.tekirexpress",
         genre={"en": "Family board game · Dice", "tr": "Aile masa oyunu · Zar"}, schema_genre=["Board game", "Family"],
         privacy="https://sites.google.com/view/tekirexpressgizlilik"),
    dict(slug="pearl-to-power", key="pearltopower", name="Pearl to Power", pkg="com.eraistudio.pearltopower",
         genre={"en": "City builder · Strategy", "tr": "Şehir kurma · Strateji"}, schema_genre=["City builder", "Strategy"],
         privacy="https://sites.google.com/view/pearl-to-power-privacy-policy"),
    dict(slug="idle-tok", key="idletok", name="Idle Tok: Influencer Tycoon", pkg="com.eraistudio.idletok",
         genre={"en": "Idle tycoon · Simulation", "tr": "Idle tycoon · Simülasyon"}, schema_genre=["Idle", "Simulation"],
         privacy="https://sites.google.com/view/idletokgizlilikpolitikasi"),
    dict(slug="idle-dropshipping-tycoon", key="idledropshippingtycoon", name="Idle Dropshipping Tycoon", pkg="com.eraistudio.idledropshippingtycoon",
         genre={"en": "Business simulation · Tycoon", "tr": "İşletme simülasyonu · Tycoon"}, schema_genre=["Simulation", "Tycoon"],
         privacy="https://sites.google.com/view/idledropshippingtycoongizlilik"),
]

T = {
    "en": dict(home="/", game="/games/{}/", press="/press/", games="Games", press_n="Press", contact="Contact",
               other="TR", kicker='<span lang="en">ErAI Studio</span> · Istanbul',
               h1="Small mobile games, each with a world of its own.",
               intro="ErAI Studio is an independent mobile game studio in Istanbul. Our games are on Google Play for Android.",
               more="Read more", play="Get it on Google Play", privacy="Privacy policy", support="Support",
               about="About the game", shots="Screenshots", platform="Platform", platform_v="Android (Google Play)",
               dev="Developer", back="All games", contact_h="Get in touch",
               contact_p="Questions, bug reports, press or business: write to us.",
               follow="Follow us", foot="Independent mobile game studio · Istanbul",
               press_h="Press kit", press_p="Logos, game icons and store art for articles and videos. You may use them to write about ErAI Studio and our games.",
               studio_h="About ErAI Studio", logos="Studio logo", game_art="Game art", download="Download",
               nf_h="Page not found", nf_p="The page you are looking for does not exist.", lang="en", hreflang="en"),
    "tr": dict(home="/tr/", game="/tr/oyunlar/{}/", press="/tr/basin/", games="Oyunlar", press_n="Basın", contact="İletişim",
               other="EN", kicker='<span lang="en">ErAI Studio</span> · İstanbul',
               h1="Her biri kendi dünyasını anlatan küçük mobil oyunlar.",
               intro="ErAI Studio, İstanbul'da bağımsız bir mobil oyun stüdyosu. Oyunlarımız Android için Google Play'de.",
               more="Devamını oku", play="Google Play'den indir", privacy="Gizlilik politikası", support="Destek",
               about="Oyun hakkında", shots="Ekran görüntüleri", platform="Platform", platform_v="Android (Google Play)",
               dev="Geliştirici", back="Tüm oyunlar", contact_h="Bize ulaşın",
               contact_p="Soru, hata bildirimi, basın ya da iş birliği için bize yazın.",
               follow="Bizi takip edin", foot="Bağımsız mobil oyun stüdyosu · İstanbul",
               press_h="Basın kiti", press_p="Yazı ve videolar için logolar, oyun simgeleri ve mağaza görselleri. ErAI Studio ve oyunlarımız hakkında yazarken kullanabilirsiniz.",
               studio_h="ErAI Studio hakkında", logos="Stüdyo logosu", game_art="Oyun görselleri", download="İndir",
               nf_h="Sayfa bulunamadı", nf_p="Aradığınız sayfa yok.", lang="tr", hreflang="tr"),
}

e = lambda s: html.escape(s, quote=True)
play_url = lambda g, l: f"https://play.google.com/store/apps/details?id={g['pkg']}&hl={l}"
title = lambda g, l: g["name"]
store_title = lambda g, l: PLAY[f"{g['key']}/{l}"]["title"]
desc = lambda g, l: PLAY[f"{g['key']}/{l}"]["desc"]
lead = lambda g, l: desc(g, l).split("\n\n")[0].strip()
feat = lambda g, l: f"/img/{g['slug']}/feature-{l if (R / 'img' / g['slug'] / f'feature-{l}.webp').exists() else 'en'}.webp"


def meta_desc(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


CSS = (R / "tools/style.css").read_text(encoding="utf-8")


def page(l, path, alt_path, ttl, description, body, ld=None, img="/img/brand/icon-512.png"):
    t = T[l]
    o = "tr" if l == "en" else "en"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    alt = "" if alt_path is None else (
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{path}"><link rel="alternate" hreflang="{o}" href="{SITE}{alt_path}">'
        f'<link rel="alternate" hreflang="x-default" href="{SITE}{path if l == "en" else alt_path}">')
    switch = f'<a class="lang" href="{alt_path or T[o]["home"]}" hreflang="{o}" lang="{o}">{t["other"]}</a>'
    return f"""<!doctype html>
<html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(ttl)}</title><meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE}{path}">{alt}
<meta property="og:type" content="website"><meta property="og:site_name" content="ErAI Studio"><meta property="og:title" content="{e(ttl)}">
<meta property="og:description" content="{e(description)}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}{img}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#faf8f3">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/img/brand/apple-touch-icon.png">
<link rel="stylesheet" href="/fonts/fonts.css"><style>{CSS}</style>{lds}</head>
<body><header class="top"><a class="logo" href="{t['home']}" lang="en">ErAI Studio</a>
<nav><a href="{t['home']}#games">{t['games']}</a><a href="{t['press']}">{t['press_n']}</a><a href="{t['home']}#contact">{t['contact']}</a>{switch}</nav></header>
<main>{body}</main>
<footer class="foot"><div><strong>ErAI Studio</strong> · {t['foot']}</div>
<div class="soc">{' '.join(f'<a href="{u}" rel="me noopener">{n}</a>' for n, u in SOCIAL)}</div>
<div><a href="mailto:{EMAIL}">{EMAIL}</a> · © 2026 ErAI Studio</div></footer></body></html>"""


def render_desc(s):
    out, ul = [], False
    for para in s.split("\n\n"):
        for line in [x.strip() for x in para.split("\n") if x.strip()]:
            letters = re.sub(r"[^A-Za-zÇĞİÖŞÜçğıöşüÂâ]", "", line)
            is_head = len(line) < 70 and letters and letters == letters.upper() and len(letters) > 3
            if line.startswith("• "):
                if not ul: out.append("<ul>"); ul = True
                out.append(f"<li>{e(line[2:])}</li>"); continue
            if ul: out.append("</ul>"); ul = False
            out.append(f"<h3>{e(line)}</h3>" if is_head else f"<p>{e(line)}</p>")
    if ul: out.append("</ul>")
    return "\n".join(out)


org_ld = {"@context": "https://schema.org", "@type": "Organization", "name": "ErAI Studio", "url": SITE + "/",
          "logo": SITE + "/img/brand/icon-512.png", "email": EMAIL, "sameAs": [u for _, u in SOCIAL],
          "address": {"@type": "PostalAddress", "addressLocality": "Istanbul", "addressCountry": "TR"}}


def game_ld(g, l):
    return {"@context": "https://schema.org", "@type": ["VideoGame", "MobileApplication"], "name": title(g, l), "alternateName": store_title(g, l),
            "description": meta_desc(lead(g, l), 300), "url": SITE + T[l]["game"].format(g["slug"]),
            "image": SITE + feat(g, l), "genre": g["schema_genre"], "gamePlatform": "Android",
            "operatingSystem": "Android", "applicationCategory": "GameApplication", "inLanguage": l,
            "installUrl": play_url(g, l), "sameAs": [play_url(g, l).split("&")[0]],
            "author": {"@type": "Organization", "name": "ErAI Studio", "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": "ErAI Studio", "url": SITE + "/"}}


def write(path, s):
    p = R / path.lstrip("/")
    if path.endswith("/"): p = p / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


urls = []
for l in ("en", "tr"):
    t, o = T[l], ("tr" if l == "en" else "en")
    # ana sayfa
    rows = ""
    for g in GAMES:
        gp = t["game"].format(g["slug"])
        rows += f"""<article class="row"><a class="img" href="{gp}"><img src="{feat(g, l)}" width="1024" height="500" alt="{e(title(g, l))}" loading="lazy"></a>
<div><div class="kicker">{e(g['genre'][l])}</div><h2><a href="{gp}">{e(title(g, l))}</a></h2><p>{e(lead(g, l))}</p>
<p class="links"><a href="{gp}">{t['more']} →</a> <a class="play" href="{play_url(g, l)}">{t['play']}</a></p></div></article>"""
    body = f"""<section class="intro"><div class="kicker">{t['kicker']}</div><h1>{t['h1']}</h1><p class="lede">{t['intro']}</p></section>
<section id="games">{rows}</section>
<section id="contact" class="contact"><h2>{t['contact_h']}</h2><p>{t['contact_p']}</p><p><a class="mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
<p class="soc">{t['follow']}: {' · '.join(f'<a href="{u}" rel="me noopener">{n}</a>' for n, u in SOCIAL)}</p></section>"""
    write(t["home"], page(l, t["home"], T[o]["home"], "ErAI Studio" + (" · Mobile games" if l == "en" else " · Mobil oyunlar"),
                          t["intro"], body, [org_ld]))
    urls.append((t["home"], T[o]["home"]))
    # oyun sayfaları
    for g in GAMES:
        gp, ap = t["game"].format(g["slug"]), T[o]["game"].format(g["slug"])
        shots = "".join(f'<img src="/img/{g["slug"]}/shot-{l}-{i}.webp" alt="{e(title(g, l))} – {t["shots"].lower()} {i}" loading="lazy">'
                        for i in range(1, 5) if (R / f"img/{g['slug']}/shot-{l}-{i}.webp").exists())
        body = f"""<article class="game"><p class="crumb"><a href="{t['home']}#games">← {t['back']}</a></p>
<header class="ghead"><img class="icon" src="/img/{g['slug']}/icon.webp" width="96" height="96" alt="">
<div><div class="kicker">{e(g['genre'][l])}</div><h1>{e(title(g, l))}</h1>
<p><a class="play" href="{play_url(g, l)}">{t['play']}</a></p></div></header>
<img class="hero" src="{feat(g, l)}" width="1024" height="500" alt="{e(title(g, l))}">
<div class="cols"><div class="text"><h2>{t['about']}</h2>{render_desc(desc(g, l))}</div>
<aside class="facts"><dl><dt>{t['platform']}</dt><dd>{t['platform_v']}</dd><dt>{t['dev']}</dt><dd>ErAI Studio</dd>
<dt>Google Play</dt><dd><a href="{play_url(g, l)}">{g['pkg']}</a></dd><dt>{t['support']}</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>{t['privacy']}</dt><dd><a href="{g['privacy']}">{t['privacy']} ↗</a></dd></dl></aside></div>
<h2>{t['shots']}</h2><div class="shots">{shots}</div></article>"""
        write(gp, page(l, gp, ap, f"{title(g, l)} · ErAI Studio", meta_desc(lead(g, l)), body, [game_ld(g, l)],
                       img=feat(g, l).replace(".webp", ".png")))
        urls.append((gp, ap))
    # basın kiti
    logos = "".join(f'<figure class="dl {c}"><img src="/img/brand/{f}" alt="ErAI Studio"><figcaption><a href="/img/brand/{f}" download>{f}</a></figcaption></figure>'
                    for f, c in [("wordmark_dark.png", "dark"), ("wordmark_light.png", ""), ("icon_1024.png", "")])
    arts = "".join(f"""<div class="pk"><h3><a href="{t['game'].format(g['slug'])}">{e(title(g, l))}</a></h3><p class="kicker">{e(g['genre'][l])}</p>
<div class="pkimg"><img src="/img/{g['slug']}/icon-512.png" alt="" loading="lazy"><img src="{feat(g, l)}" alt="" loading="lazy"></div>
<p><a href="/img/{g['slug']}/icon-512.png" download>{t['download']}: icon 512×512</a> · <a href="{feat(g, l).replace('.webp', '.png')}" download>{t['download']}: 1024×500</a> · <a href="{play_url(g, l)}">Google Play</a></p></div>"""
                   for g in GAMES)
    body = f"""<section class="intro"><div class="kicker" lang="en">ErAI Studio</div><h1>{t['press_h']}</h1><p class="lede">{t['press_p']}</p></section>
<section class="press"><h2>{t['studio_h']}</h2><p>{t['intro']}</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>{t['logos']}</h2><div class="logos">{logos}</div><h2>{t['game_art']}</h2>{arts}</section>"""
    write(t["press"], page(l, t["press"], T[o]["press"], f"{t['press_h']} · ErAI Studio", t["press_p"], body))
    urls.append((t["press"], T[o]["press"]))

nf = page("en", "/404.html", None, "404 · ErAI Studio", T["en"]["nf_p"],
          f"""<section class="intro"><h1>{T['en']['nf_h']}</h1><p class="lede">{T['en']['nf_p']} <a href="/">ErAI Studio →</a></p>
<p lang="tr">{T['tr']['nf_p']} <a href="/tr/">Türkçe ana sayfa →</a></p></section>""")
write("/404.html", nf.replace('<link rel="canonical" href="https://eraistudio.com/404.html">', '<meta name="robots" content="noindex">'))

sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for p, a in urls:
    la, lb = ("en", "tr") if not p.startswith("/tr/") else ("tr", "en")
    sm.append(f'<url><loc>{SITE}{p}</loc><xhtml:link rel="alternate" hreflang="{la}" href="{SITE}{p}"/>'
              f'<xhtml:link rel="alternate" hreflang="{lb}" href="{SITE}{a}"/></url>')
sm.append("</urlset>")
(R / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
(R / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
print("sayfa:", len(urls) + 1)
