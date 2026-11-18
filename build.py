# Zostaví landing page sprievodcu matematikou (index.html) z výkladu s vopred vykreslenými vzorcami (src/vyklad.html).
# Vzorce sú SVG z MathJaxu priamo v stránke, preto stránka nepotrebuje žiadny skript ani internet (okrem webového písma).
#   python build.py
import re
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / 'src' / 'vyklad.html').read_text(encoding='utf-8')

# štýly MathJaxu (rozmery a zarovnanie SVG vzorcov) a globálna knižnica tvarov písmen
mjx_styles = ''.join(m.group(0) for m in re.finditer(r'<style (?:type="text/css"|id="MJX-SVG-styles")>[\s\S]*?</style>', src))
cache = re.search(r'<svg id="MJX-SVG-global-cache"[\s\S]*?</svg>', src).group(0)
main = re.search(r'<main>([\s\S]*?)</main>', src).group(1)
# bez skriptu MathJaxu nemá kontextové menu zmysel: vzorce nebudú zastávkou pre Tab
main = re.sub(r' tabindex="0"| ctxtmenu_counter="\d+"| class="MathJax CtxtMenu_Attached_0"', lambda m: ' class="MathJax"' if 'class' in m.group(0) else '', main)
# dlhé vzorce (nad 18 ex) sa na úzkom displeji posúvajú do strany: posuvná oblasť musí byť dostupná klávesnicou
def _wide(m):
    return m.group(1) + (' tabindex="0"' if float(m.group(3)) > 18 else '') + m.group(2)
main = re.sub(r'(<mjx-container class="MathJax"[^>]*?)(><svg[^>]*?width="([\d.]+)ex")', _wide, main)
main = main.replace('<section id="s0">', '<div id="blok-a" class="anchor"></div>\n<section id="s0">', 1)
main = main.replace('<section id="s10">', '<div id="blok-b" class="anchor"></div>\n<section id="s10">', 1)

s9 = re.search(r'<section id="s9">([\s\S]*?)</section>', main).group(1)
leontief = re.search(r'<mjx-container class="MathJax"[^>]*display="true"[^>]*>[\s\S]*?</mjx-container>', s9).group(0)
leontief = leontief.replace(' tabindex="0"', '').replace('<mjx-assistive-mml', '<mjx-assistive-mml aria-hidden="true"', 1)
KAP = [
    ('s0', 'Načo sú matice ekonómovi', 'Leontief, ekonometria, lineárne programovanie'),
    ('s1', 'Vektory', 'sčítanie, násobenie číslom, skalárny súčin'),
    ('s2', 'Lineárna kombinácia a závislosť', 'kedy vektor nenesie novú informáciu'),
    ('s3', 'Matice a operácie s nimi', 'súčin „riadok krát stĺpec“, transponovanie'),
    ('s4', 'Hodnosť matice', 'Gaussova eliminácia, stupňovitý tvar'),
    ('s5', 'Determinant', 'Sarrusovo pravidlo, rozvoj podľa riadku'),
    ('s6', 'Inverzná matica', 'vzorec pre 2×2, Jordanova metóda'),
    ('s7', 'Maticové rovnice', 'prečo záleží, z ktorej strany násobíš'),
    ('s8', 'Sústavy lineárnych rovníc', 'Frobeniova veta, parametre, Gauss'),
    ('s9', 'Leontiefov model', 'celý blok A v jednej ekonomickej úlohe'),
    ('s10', 'Definičný obor', 'zlomok, odmocnina, logaritmus'),
    ('s11', 'Inverzná funkcia', 'z ceny množstvo a z množstva cena'),
    ('s12', 'Ekonomické funkcie', 'náklady, príjmy, zisk, rentabilita'),
    ('s13', 'Derivácia', 'tabuľka, súčin, podiel, zložená funkcia'),
    ('s14', 'Dotyčnica a normála', 'smernica priamky z derivácie'),
    ('s15', 'Diferenciál, marginálna veličina, elasticita', 'o koľko sa zmení výstup pri zmene vstupu'),
    ('s16', 'Monotónnosť a extrémy', 'kde funkcia rastie a kde má vrchol'),
    ('s17', 'Konvexnosť a inflexné body', 'druhá derivácia a zakrivenie'),
    ('s18', 'Optimalizácia zisku a nákladov', 'maximálny zisk, minimálne priemerné náklady'),
    ('s19', 'Ťahák a zoznam materiálov', 'pravidlá naspamäť a kde čo nájdeš'),
]
def card(i, k):
    sid, t, d = k
    return f'<li><a class="card" href="#{sid}"><span class="card-n">{i}</span><span class="card-t">{t}</span><span class="card-d">{d}</span></a></li>'
cards_a = ''.join(card(i, k) for i, k in enumerate(KAP[:10]))
cards_b = ''.join(card(i + 10, k) for i, k in enumerate(KAP[10:]))

ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230d6e66'/%3E"
        "%3Ctext x='32' y='44' font-family='Georgia,serif' font-size='34' font-weight='700' fill='white' text-anchor='middle'%3E%E2%88%AB%3C/text%3E%3C/svg%3E")

CSS = """
:root{
  --bg:#f6f8f8; --panel:#fff; --ink:#132429; --muted:#566a70; --line:#d8e0e2;
  --accent:#0d6e66; --accent-d:#095650; --accent-soft:#dff1ee; --warn-soft:#fff3dc; --warn:#7f5300; --econ-soft:#e9edf7; --econ:#2f4a8f;
  --hero1:#0d6e66; --hero2:#0b4f5c;
  --font-body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --font-head:"IBM Plex Serif",Georgia,"Times New Roman",serif;
  --font-mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0e171a; --panel:#152125; --ink:#e5edef; --muted:#9db0b6; --line:#273a40;
  --accent:#5fd1c4; --accent-d:#7fe0d5; --accent-soft:#143633; --warn-soft:#382b12; --warn:#f0c26b; --econ-soft:#1b2540; --econ:#a8bcf3;
  --hero1:#0b4a45; --hero2:#0a2f38; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0e171a; --panel:#152125; --ink:#e5edef; --muted:#9db0b6; --line:#273a40;
  --accent:#5fd1c4; --accent-d:#7fe0d5; --accent-soft:#143633; --warn-soft:#382b12; --warn:#f0c26b; --econ-soft:#1b2540; --econ:#a8bcf3;
  --hero1:#0b4a45; --hero2:#0a2f38; color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{scroll-padding-top:72px}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 var(--font-body);-webkit-text-size-adjust:100%}
a{color:var(--accent)}
.skip{position:absolute;left:-9999px;top:8px;background:var(--panel);color:var(--ink);padding:12px 14px;min-height:44px;border-radius:6px;z-index:20}
.skip:focus{left:12px}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}

/* horná lišta */
.bar{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar-in{max-width:1120px;margin:0 auto;padding:0 16px;display:flex;align-items:center;gap:16px;min-height:56px}
.brand{font:600 1.05rem/1 var(--font-head);color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:10px;min-height:44px;min-width:44px}
.brand i{display:grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--accent);color:var(--bg);font:700 1.1rem/1 var(--font-head);font-style:normal}
.bar nav{margin-left:auto;display:flex;gap:4px}
.bar nav a{display:flex;align-items:center;min-height:44px;padding:0 10px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:.9375rem;font-weight:500;white-space:nowrap}
.bar nav a:hover{background:var(--accent-soft)}
.bar nav .short{display:none}
@media (max-width:560px){.bar nav .long{display:none}.bar nav .short{display:inline}.brand span{display:none}}

/* úvod */
.hero{background:linear-gradient(135deg,var(--hero1),var(--hero2));color:#fff}
.hero-in{max-width:1120px;margin:0 auto;padding:64px 16px 72px;display:grid;gap:40px;align-items:center}
@media (min-width:1000px){.hero-in{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr)}}
.hero-card{display:none;background:rgba(255,255,255,.96);color:#132429;border-radius:16px;padding:26px 28px;box-shadow:0 20px 50px rgba(0,0,0,.25)}
@media (min-width:1000px){.hero-card{display:block}}
.hero-card .k{font:500 .75rem/1.4 var(--font-mono);letter-spacing:.1em;text-transform:uppercase;color:#0d6e66;margin:0 0 12px}
.hero-card mjx-container{display:block;margin:8px 0 16px!important}
.hero-card mjx-container svg{display:block;max-width:100%;height:auto}
.hero-card p{margin:0;color:#4a5d63;font-size:.9375rem}
.hero-card a{color:#0d6e66;font-weight:600}
@media (min-width:900px){.hero-in{padding:96px 16px 104px}}
.eyebrow{font:500 .8125rem/1.4 var(--font-mono);letter-spacing:.1em;text-transform:uppercase;color:#bfeae4;margin:0 0 16px}
.hero h1{font:600 clamp(2.1rem,6vw,3.9rem)/1.08 var(--font-head);margin:0 0 20px;max-width:18ch;text-wrap:balance}
.hero .lead{font-size:clamp(1.05rem,2.2vw,1.25rem);max-width:58ch;color:#e3f4f1;margin:0 0 28px}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 36px}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 20px;border-radius:10px;font-weight:600;text-decoration:none}
.btn--main{background:#fff;color:#0b4f5c}
.btn--main:hover{background:#e6f6f3}
.btn--ghost{color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.7)}
.btn--ghost:hover{background:rgba(255,255,255,.12)}
.stats{display:flex;flex-wrap:wrap;gap:12px 36px;margin:0;padding:0;list-style:none}
.stats b{display:block;font:600 1.9rem/1 var(--font-head)}
.stats span{font-size:.875rem;color:#cdeee9}

/* prehľad kapitol */
.overview{max-width:1120px;margin:0 auto;padding:56px 16px 24px}
.sec-k{font:500 .8125rem/1.4 var(--font-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 6px}
.overview h2{font:600 clamp(1.6rem,3.4vw,2.2rem)/1.15 var(--font-head);margin:0 0 8px}
.overview .sub{color:var(--muted);margin:0 0 28px;max-width:62ch}
.blocks{display:grid;gap:32px}
@media (min-width:900px){.blocks{grid-template-columns:1fr 1fr;gap:40px}}
.blocks h3{font:600 1.15rem/1.3 var(--font-body);margin:0 0 12px}
.cards{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.card{display:grid;grid-template-columns:40px minmax(0,1fr);column-gap:12px;align-items:start;padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);text-decoration:none;min-height:56px}
.card:hover{border-color:var(--accent);box-shadow:0 1px 0 var(--accent)}
.card-n{grid-row:1/3;font:500 1rem/1.6 var(--font-mono);color:var(--accent)}
.card-t{font-weight:600;line-height:1.35}
.card-d{font-size:.875rem;color:var(--muted);line-height:1.4}

/* výklad */
.content{max-width:760px;margin:0 auto;padding:8px 16px 48px}
.content > section{padding:44px 0;border-bottom:1px solid var(--line)}
.anchor{position:relative;top:-72px}
.blok{font:500 .8125rem/1.4 var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
.content h2{font:600 clamp(1.5rem,3.2vw,1.9rem)/1.2 var(--font-head);margin:0 0 14px;text-wrap:balance}
.content h2 .n{color:var(--accent);margin-right:10px;font:500 1.2rem/1 var(--font-mono)}
.content h3{font:600 1.0625rem/1.4 var(--font-body);margin:26px 0 8px}
.content p{margin:0 0 12px}
.content ul,.content ol{margin:0 0 12px;padding-left:22px}
.content li{margin-bottom:5px}
.box{border:1px solid var(--line);background:var(--panel);padding:14px 16px;margin:16px 0;border-radius:10px}
.box .t{font:500 .75rem/1.4 var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}
.box.preco{background:var(--warn-soft)} .box.preco .t{color:var(--warn)}
.box.ekon{background:var(--econ-soft)} .box.ekon .t{color:var(--econ)}
.box.priklad{background:var(--accent-soft)}
.box p:last-child,.box ol:last-child,.box ul:last-child{margin-bottom:0}
.krok{counter-reset:k;list-style:none;padding-left:0!important}
.krok li{counter-increment:k;position:relative;padding-left:34px;margin-bottom:8px}
.krok li::before{content:counter(k);position:absolute;left:0;top:2px;width:22px;height:22px;border-radius:50%;background:var(--accent);color:var(--bg);font:500 .75rem/22px var(--font-mono);text-align:center}
.content table{border-collapse:collapse;width:100%;font-size:.875rem;margin:10px 0 14px;font-variant-numeric:tabular-nums}
.content th,.content td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
.content th{background:var(--panel);font-weight:600}
.scroll{overflow-x:auto;max-width:100%}
@media (max-width:760px){.content table{display:block;max-width:100%;overflow-x:auto}}
code{font-family:var(--font-mono);font-size:.92em;background:var(--panel);padding:1px 5px;border-radius:4px;border:1px solid var(--line)}
.files td:first-child{font-family:var(--font-mono);font-size:.8125rem}
mjx-container[tabindex]:focus-visible{outline-offset:1px;border-radius:4px}
mjx-container[display="true"]{display:block;margin:10px 0!important}
mjx-container[display="true"][tabindex]{max-width:100%;overflow-x:auto;overflow-y:hidden;padding:2px 0}
@media (max-width:760px){mjx-container[tabindex]:not([display="true"]){display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle;padding:2px 0}}

/* tlačidlo hore a päta */
.totop{position:fixed;right:16px;bottom:16px;z-index:9;display:grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--accent);color:var(--bg);text-decoration:none;font-size:1.3rem;box-shadow:0 4px 14px rgba(0,0,0,.18)}
.totop:hover{background:var(--accent-d)}
@supports (animation-timeline: scroll()){.totop{animation:totop linear both;animation-timeline:scroll();animation-range:0 480px}@keyframes totop{from{opacity:0;visibility:hidden}to{opacity:1;visibility:visible}}}
.foot{border-top:1px solid var(--line);color:var(--muted);font-size:.875rem}
.foot-in{max-width:760px;margin:0 auto;padding:28px 16px 88px}
.foot p{margin:0 0 8px}
"""

html = f"""<!doctype html>
<html lang="sk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Matematika NHF – celý semester</title>
<meta name="description" content="Výklad celého semestra matematiky na NHF EUBA v poradí cvičení: vektory, matice, determinanty, sústavy rovníc, Leontiefov model, funkcie, derivácie, extrémy a optimalizácia, s riešenými príkladmi.">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0d6e66">
<link rel="icon" href="{ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&amp;family=IBM+Plex+Serif:wght@600&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap">
{mjx_styles}
<style>{CSS}</style>
</head>
<body id="top">
<a class="skip" href="#obsah">Preskočiť na obsah</a>
<header class="bar"><div class="bar-in">
  <a class="brand" href="#top" aria-label="Matematika NHF, späť na začiatok"><i aria-hidden="true">∫</i><span>Matematika NHF</span></a>
  <nav aria-label="Rýchla navigácia"><a href="#blok-a"><span class="long">Lineárna algebra</span><span class="short">Algebra</span></a><a href="#blok-b">Funkcie</a><a href="#s19">Ťahák</a></nav>
</div></header>

<section class="hero" aria-labelledby="h1"><div class="hero-in">
  <div>
  <p class="eyebrow">Matematika · EUBA NHF · zimný semester</p>
  <h1 id="h1">Celý semester matematiky v poradí, v akom ide na cvičeniach</h1>
  <p class="lead">Každá kapitola má štyri časti: čo to je, prečo to funguje, postup krok za krokom a riešený príklad zo skrípt s overeným výsledkom. Modré rámčeky ukazujú, na čo sa to používa v ekonómii.</p>
  <p class="cta"><a class="btn btn--main" href="#s0">Začať od úvodu</a><a class="btn btn--ghost" href="#obsah">Prehľad kapitol</a></p>
  <ul class="stats"><li><b>20</b><span>kapitol</span></li><li><b>2</b><span>bloky: lineárna algebra a funkcie</span></li><li><b>30+</b><span>riešených príkladov</span></li></ul>
  </div>
  <aside class="hero-card" aria-label="Ukážka: Leontiefov model">
    <p class="k">Kam to celé smeruje</p>
    {leontief}
    <p>Leontiefov model medziodvetvových vzťahov spojí vektory, matice, determinant aj inverznú maticu do jednej ekonomickej úlohy. <a href="#s9">Kapitola 9</a></p>
  </aside>
</div></section>

<section class="overview" id="obsah" aria-labelledby="ov-h">
  <p class="sec-k">Obsah</p>
  <h2 id="ov-h">Kapitoly idú v poradí, v akom na seba nadväzujú</h2>
  <p class="sub">Keď niečomu nerozumieš, vráť sa o kapitolu späť, väčšinou tam je chýbajúci kúsok.</p>
  <div class="blocks">
    <div><h3>Blok A · Lineárna algebra</h3><ol class="cards">{cards_a}</ol></div>
    <div><h3>Blok B · Funkcie jednej premennej</h3><ol class="cards">{cards_b}</ol></div>
  </div>
</section>

<main class="content" id="vyklad">
{main}
</main>

<footer class="foot"><div class="foot-in">
  <p>Výklad zostavený zo skrípt a príkladov k cvičeniam z matematiky na NHF EUBA, zimný semester 2026/27. Všetky vzorové výsledky sú prepočítané a porovnané s výsledkami v skriptách.</p>
  <p>Študijná pomôcka, nie oficiálny materiál univerzity.</p>
</div></footer>
<a class="totop" href="#top" aria-label="Späť na začiatok">↑</a>
{cache}
</body>
</html>
"""
(ROOT / 'index.html').write_text(html, encoding='utf-8', newline='\n')
print('index.html', round(len(html.encode('utf-8')) / 1024), 'KB')
