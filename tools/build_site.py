"""Собрать весь сайт Lab01 в docs/ (GitHub Pages публикует эту папку).

    python tools/build_site.py

docs/                — общая страница: две части работы
docs/wine/           — основная работа (вино): marimo-приложение, серый стиль
docs/fonts/          — доп. задание КТвД: сайт про шрифты (лендинг, датчик)
docs/fonts/report/   — отчёт по шрифтам: marimo-приложение
docs/fonts/datchik/  — полный датчик на marimo

Без marimo (pip install marimo) собираются только страницы без приложений.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REPO = os.environ.get("LAB_REPO_URL", "").rstrip("/")


def export(app: Path, out: Path) -> int:
    if shutil.which("marimo") is None:
        print("marimo не установлен: пропускаю", app.name)
        return 0
    cmd = ["marimo", "export", "html-wasm", str(app), "-o", str(out), "--mode", "run"]
    print(" ".join(cmd))
    return subprocess.call(cmd)


def main() -> int:
    code = subprocess.call([sys.executable, str(ROOT / "tools" / "build_apps.py")])   # site/*_app.py + site/public/
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()

    # 1. шрифты: собственный сайт части (лендинг + датчик), ссылки ведут на marimo-отчёт и на общую страницу
    env = dict(os.environ, LAB_REPORT="report/", LAB_HUB="../", LAB_PATH_PREFIX="fonts/")
    code |= subprocess.call([sys.executable, str(ROOT / "fonts" / "tools" / "build_site.py")], env=env)
    shutil.copytree(ROOT / "fonts" / "docs", DOCS / "fonts")

    # 2. marimo-приложения: вино и отчёт по шрифтам
    code |= export(ROOT / "site" / "wine_app.py", DOCS / "wine")
    code |= export(ROOT / "site" / "fonts_app.py", DOCS / "fonts" / "report")

    # 3. общая страница
    (DOCS / "index.html").write_text(hub(), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("")
    print("docs/ собран")
    return code


def hub() -> str:
    white = pd.read_csv(ROOT / "wine" / "data" / "winequality-white.csv", sep=";")
    fonts = pd.read_csv(ROOT / "fonts" / "data" / "fonts.csv")
    n_fonts = int((~fonts["no_lowercase"]).sum())
    gh = (lambda p, t: f'<a href="{REPO}/blob/main/{p}">{t}</a>') if REPO else (lambda p, t: f"<code>{p}</code>")
    repo = f'<a class="repo" href="{REPO}">Репозиторий на GitHub</a>' if REPO else ""
    return (HUB.replace("__N_WINE__", f"{len(white):,}".replace(",", " "))
               .replace("__N_FONTS__", str(n_fonts))
               .replace("__NB_WINE__", gh("wine/lab01.ipynb", "lab01.ipynb"))
               .replace("__NB_FONTS__", gh("fonts/fonts.ipynb", "fonts.ipynb"))
               .replace("__REPO__", repo)
               .replace("__JSON__", json.dumps({"wine": len(white), "fonts": n_fonts})))


HUB = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab01 · Прикладная статистика</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&family=Roboto+Flex:opsz,wdth,wght@8..144,25..151,100..1000&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
html,body{margin:0}
body{font-family:"Golos Text",system-ui,sans-serif;color:#16181d;background:#f2f2f0;line-height:1.5}
a{color:inherit}
.top{max-width:1180px;margin:0 auto;padding:2.2rem 1.4rem 1.2rem}
.kicker{font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:#5a5f69}
h1{font-size:clamp(2rem,5.4vw,3.6rem);line-height:1.02;margin:.4rem 0 .8rem;font-weight:800;letter-spacing:-.02em}
.lede{max-width:52rem;color:#3b3f48;font-size:1.05rem;margin:0}
.authors{display:flex;flex-wrap:wrap;gap:.5rem 1.4rem;margin-top:1rem;font-size:.92rem;color:#5a5f69}
.authors b{color:#16181d;font-weight:600}
.repo{display:inline-block;margin-top:1rem;font-size:.9rem;padding:.35rem .8rem;border:1px solid #c9c9c4;border-radius:999px;text-decoration:none}
.repo:hover{background:#fff}
.parts{max-width:1180px;margin:0 auto;padding:0 1.4rem 2rem;display:grid;grid-template-columns:1fr 1fr;gap:1.2rem}
.part{position:relative;border-radius:22px;padding:1.8rem 1.7rem 1.6rem;overflow:hidden;display:flex;flex-direction:column;min-height:31rem}
.part h2{margin:.3rem 0 .6rem;font-size:clamp(1.6rem,3vw,2.3rem);line-height:1.05;letter-spacing:-.01em}
.part p{margin:.2rem 0 .8rem}
.tag{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;opacity:.75}
.nums{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem;margin:1rem 0 1.2rem}
.num strong{display:block;font-size:1.7rem;line-height:1;font-weight:700}
.num span{font-size:.78rem;opacity:.75}
.btns{margin-top:auto;display:flex;flex-wrap:wrap;gap:.5rem}
.btn{display:inline-flex;align-items:center;gap:.4rem;padding:.62rem 1rem;border-radius:12px;text-decoration:none;font-weight:600;font-size:.93rem;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}
.ghost{background:transparent;border:1px solid currentColor;font-weight:500}
.small{font-size:.82rem;opacity:.8;margin-top:.9rem}
/* вино: серый */
.wine{background:linear-gradient(160deg,#2b2f37 0%,#16181d 70%);color:#eceae6}
.wine .btn.main{background:#8e3b46;color:#fff}
.wine .num strong{color:#fff}
.wine canvas{position:absolute;right:-30px;top:-20px;width:300px;height:220px;opacity:.35;pointer-events:none}
/* шрифты: стиль сайта шрифтов */
.fonts{background:#fafaf7;color:#1a1d24;border:1px solid #e6e5e0}
.fonts h2{font-family:"Roboto Flex",sans-serif;font-variation-settings:"wght" 760,"wdth" 110}
.fonts .btn.main{background:#2a78d6;color:#fff}
.fonts .tag{color:#2a78d6;opacity:1}
.fonts .num strong{color:#eb6834}
.glyphs{position:absolute;right:1.2rem;top:.6rem;font-family:"Roboto Flex",sans-serif;font-size:5.2rem;line-height:1;color:#2a78d6;opacity:.16;pointer-events:none;letter-spacing:-.02em}
.what{max-width:1180px;margin:0 auto;padding:0 1.4rem 2.4rem;display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}
.what div{background:#fff;border:1px solid #e1e1de;border-radius:16px;padding:1rem 1.1rem;font-size:.9rem;color:#3b3f48}
.what b{display:block;color:#16181d;margin-bottom:.2rem}
footer{max-width:1180px;margin:0 auto;padding:1rem 1.4rem 2.5rem;color:#5a5f69;font-size:.85rem}
@media (max-width:860px){.parts{grid-template-columns:1fr}.part{min-height:0}.what{grid-template-columns:1fr 1fr}.glyphs{font-size:3.6rem}}
@media (max-width:520px){.what{grid-template-columns:1fr}.nums{grid-template-columns:repeat(3,1fr)}.num strong{font-size:1.35rem}}
</style>
</head>
<body>
<header class="top">
  <div class="kicker">Прикладная статистика · осень 2026 · Lab01</div>
  <h1>Случайные величины<br>в вине и в шрифтах</h1>
  <p class="lede">Лабораторная работа из двух частей. Основная работа команды: белое вино как случайный эксперимент,
  распределения, оценки, выборки и датчики случайных чисел. Доп. задание трека КТвД: собственный датасет шрифтов,
  где x-height и толщина штриха изучаются как случайные величины.</p>
  <div class="authors">
    <span><b>Нефедьева Антонина Сергеевна</b> · ИСУ 502335 · Инфохимия · спринт 1</span>
    <span><b>Быкова Кристина Денисовна</b> · ИСУ 501322 · группа 27 · КТвД · спринты 1–2 и доп. задание</span>
  </div>
  __REPO__
</header>

<main class="parts">
  <section class="part wine">
    <canvas id="cloud" width="600" height="440" aria-hidden="true"></canvas>
    <div class="tag">Основная работа · спринты 1 и 2</div>
    <h2>Белое вино как<br>случайный эксперимент</h2>
    <p>Wine Quality (UCI): у каждого вина измерены кислотность, pH, спирт и другие свойства.
    Три случайные величины, подбор распределений, состоятельность оценок, выборки, зависимость,
    датчик pH полярным методом и сравнение десяти алгоритмов.</p>
    <div class="nums">
      <div class="num"><strong>__N_WINE__</strong><span>белых вин</span></div>
      <div class="num"><strong>3</strong><span>случайные величины</span></div>
      <div class="num"><strong>10</strong><span>алгоритмов датчика</span></div>
    </div>
    <div class="btns">
      <a class="btn main" href="wine/">Открыть отчёт →</a>
    </div>
    <p class="small">Интерактивный отчёт на marimo: оглавление, код под каждым разделом, 12 живых блоков. Ноутбук: __NB_WINE__.</p>
  </section>

  <section class="part fonts">
    <div class="glyphs" aria-hidden="true">Hxo</div>
    <div class="tag">Доп. задание · трек КТвД</div>
    <h2>Шрифт как<br>случайная величина</h2>
    <p>Свой датасет: __N_FONTS__ семейств Google Fonts, измеренных по контурам букв. Распределения x-height и толщины
    штриха, их связь, гипотеза про гротески и антиквы, датчик «нового» шрифта.</p>
    <div class="nums">
      <div class="num"><strong>__N_FONTS__</strong><span>шрифтов, 5 категорий</span></div>
      <div class="num"><strong>2</strong><span>случайные величины</span></div>
      <div class="num"><strong>6</strong><span>методов датчика</span></div>
    </div>
    <div class="btns">
      <a class="btn main" href="fonts/">Сайт про шрифты →</a>
      <a class="btn ghost" href="fonts/report/">Отчёт</a>
      <a class="btn ghost" href="fonts/datchik/">Датчик</a>
    </div>
    <p class="small">Сайт с живыми шрифтами и датчиком, отчёт на marimo с живыми блоками. Ноутбук: __NB_FONTS__.</p>
  </section>
</main>

<section class="what" aria-label="Что внутри">
  <div><b>Без установки</b>Отчёты считаются прямо в браузере (marimo + WebAssembly), первый запуск 10–30 секунд.</div>
  <div><b>Код рядом</b>Под каждым разделом «Код этого раздела»: тем самым кодом посчитаны таблицы и рисунки.</div>
  <div><b>Живые блоки</b>Ползунки и переключатели: распределения, выборки, датчики пересчитываются на ходу.</div>
  <div><b>Проверено тестами</b>Автотесты пакетов labstat, labrng, labfont запускаются при каждой публикации.</div>
</section>

<footer>Данные: Wine Quality (P. Cortez и др., UCI Machine Learning Repository); шрифты Google Fonts (SIL Open Font License).</footer>

<script>
// облако «вин» на фоне карточки: случайные точки из двумерного нормального распределения (полярный метод)
(function(){
  const c=document.getElementById("cloud"); if(!c) return; const g=c.getContext("2d");
  function norm(){let u,v,s;do{u=2*Math.random()-1;v=2*Math.random()-1;s=u*u+v*v}while(s>=1||s===0);return u*Math.sqrt(-2*Math.log(s)/s)}
  for(let i=0;i<1400;i++){const a=norm(),b=norm();const x=300+a*95,y=220-(0.55*a+0.83*b)*70;
    g.fillStyle=i%9?"rgba(236,234,230,.55)":"rgba(201,120,132,.9)";g.beginPath();g.arc(x,y,2.1,0,7);g.fill()}
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
