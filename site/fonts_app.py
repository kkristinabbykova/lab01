# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "numpy", "pandas", "matplotlib", "scipy"]
# ///
import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium", app_title="Lab01 · КТвД · Шрифт как случайная величина")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = {"bg": "#fafaf7", "card": "#ffffff", "ink": "#1a1d24", "ink2": "#5c6170", "line": "#e6e5e0", "acc": "#2a78d6", "acc2": "#a9c8ef", "soft": "#f1f0eb", "grid": "#e6e5e0", "c1": "#2a78d6", "c2": "#eb6834", "c3": "#1baf7a", "cover": "radial-gradient(120% 140% at 100% 0%,#2a78d6 0%,#1a1d24 55%)", "cover_ink": "#fafaf7"}
    ASSETS = "fonts"

    import base64
    import io
    import types
    from pathlib import Path

    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import scipy                      # нужен и коду датчиков: явный импорт, чтобы marimo установил scipy в браузере
    from scipy import stats

    def read_text(p):
        """Файл из public/: локально это путь, в браузере (WebAssembly) это URL."""
        try:
            return Path(str(p)).read_text(encoding="utf-8")
        except Exception:
            from pyodide.http import open_url
            return open_url(str(p)).read()

    PUB = mo.notebook_location() / "public"

    def fig(name):
        """Рисунок из выполненного ноутбука: локально встраивается, в браузере грузится по ссылке."""
        p = PUB / ASSETS / name
        try:
            src = "data:image/png;base64," + base64.b64encode(Path(str(p)).read_bytes()).decode()
        except Exception:
            src = str(p)
        return mo.Html(f'<figure class="lab-fig"><img src="{src}" alt="" loading="lazy"></figure>')

    def table_html(h):
        return mo.Html(f'<div class="lab-tbl">{h}</div>')

    def out_text(t):
        return mo.Html(f'<pre class="lab-out">{t.replace("&", "&amp;").replace("<", "&lt;")}</pre>')

    def code_block(code):
        return mo.accordion({"Код этого раздела": mo.md(f"```python\n{code}\n```")})

    def plot_html(f):
        """Matplotlib → картинка; так рисунок одинаково выглядит локально и в браузере."""
        buf = io.BytesIO()
        f.savefig(buf, format="png", dpi=140, bbox_inches="tight")
        plt.close(f)
        return mo.Html(f'<figure class="lab-fig live"><img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}" alt=""></figure>')

    def cards(items):
        """Карточки с числами: [(подпись, значение, пояснение), ...]."""
        cells = "".join(f'<div class="lab-card"><span>{a}</span><b>{b}</b><small>{c}</small></div>' for a, b, c in items)
        return mo.Html(f'<div class="lab-cards">{cells}</div>')

    def live(title, note, *controls):
        """Заголовок живого блока и его элементы управления."""
        return mo.vstack([mo.Html(f'<div class="lab-live"><span class="tag">живой блок</span><h4>{title}</h4><p>{note}</p></div>'),
                          mo.hstack(list(controls), wrap=True, justify="start", gap=1.2)], gap=0.4)

    def nf(v, d=3):
        return f"{v:.{d}f}"

    plt.rcParams.update({
        "figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
        "grid.color": T["grid"], "grid.linewidth": 0.8, "axes.edgecolor": T["ink2"], "axes.labelcolor": T["ink"],
        "xtick.color": T["ink2"], "ytick.color": T["ink2"], "legend.frameon": False, "lines.linewidth": 2,
        "axes.titlesize": 11, "axes.labelsize": 10, "legend.fontsize": 9, "font.size": 10,
    })

    fonts_all = pd.read_csv(io.StringIO(read_text(PUB / "fonts.csv")))
    fonts = fonts_all[~fonts_all["no_lowercase"].astype(str).eq("True")].copy()
    CAT = {"sans": ("гротески", "#2a78d6"), "serif": ("антиквы", "#eb6834"), "display": ("акцидентные", "#1baf7a"),
           "handwriting": ("рукописные", "#9b59b6"), "mono": ("моноширинные", "#5c6170")}
    CAT_RU = {v[0]: k for k, v in CAT.items()}
    # столбец: (русское название, единицы)
    FCOLS = {"x_height": ("x-height", "доли кегля"), "stem": ("толщина штриха", "доли кегля"),
             "contrast": ("контраст «o»", "отношение"), "width_o": ("ширина «o»", "отношение"),
             "cap_height": ("высота прописных", "доли кегля"), "x_to_cap": ("x-height / высота прописных", "отношение")}
    FRU = {v[0]: k for k, v in FCOLS.items()}
    C1, C2, C3 = T["c1"], T["c2"], T["c3"]

    def describe_cards(x, unit):
        return cards([("среднее", nf(np.mean(x)), unit), ("медиана", nf(np.median(x)), unit),
                      ("СКО", nf(np.std(x, ddof=1)), unit), ("асимметрия", nf(stats.skew(x), 2), "0 у симметричного"),
                      ("эксцесс", nf(stats.kurtosis(x), 2), "0 у нормального"), ("N", f"{len(x)}", "шрифтов")])

    FAMS = {"нормальное": "norm", "логнормальное": "lognorm", "скошенное нормальное": "skewnorm",
            "гамма": "gamma", "Вейбулла": "weibull_min"}
    _fits = {}

    def fit_view(x, chosen, n_bins, label, unit, key):
        f, ax = plt.subplots(figsize=(8, 3.6))
        ax.hist(x, bins=n_bins, density=True, color=C1, alpha=0.3, edgecolor="white", linewidth=0.4, label="шрифты")
        g = np.linspace(np.min(x), np.max(x), 400)
        rows = []
        styles = [(C1, "-"), (C2, "-"), (C3, (0, (5, 3))), ("#1a1d24", ":"), ("#9b59b6", (0, (2, 2)))]
        for ru, (col, ls) in zip(chosen, styles):
            fam = FAMS[ru]
            if (key, fam) not in _fits:
                d = getattr(stats, fam)
                p = d.fit(x)
                _fits[(key, fam)] = (p, 2 * len(p) - 2 * float(np.sum(d.logpdf(x, *p))),
                                     float(stats.kstest(x, d.cdf, args=p).statistic))
            p, aic, ks = _fits[(key, fam)]
            ax.plot(g, getattr(stats, fam).pdf(g, *p), color=col, linestyle=ls, label=ru)
            rows.append({"распределение": ru, "AIC": round(aic, 1), "D Колмогорова": round(ks, 4)})
        ax.set(xlabel=f"{label}, {unit}", ylabel="плотность", title=f"{label}: шрифты и модели")
        ax.legend()
        return plot_html(f), (pd.DataFrame(rows).sort_values("AIC") if rows else pd.DataFrame())

    def scatter_view(df, xcol, ycol, cats, label_points):
        f, ax = plt.subplots(figsize=(8, 4.4))
        for k, (ru, col) in CAT.items():
            d = df[df.category == k]
            if ru not in cats or not len(d):
                continue
            ax.scatter(d[xcol], d[ycol], s=34, color=col, alpha=0.85, edgecolor="white", linewidth=0.6, label=f"{ru} ({len(d)})")
            if label_points:
                for _, r in d.iterrows():
                    ax.annotate(r.family, (r[xcol], r[ycol]), fontsize=6.5, xytext=(3, 2), textcoords="offset points", color=T["ink2"])
        ax.set(xlabel=f"{FCOLS[xcol][0]}, {FCOLS[xcol][1]}", ylabel=f"{FCOLS[ycol][0]}, {FCOLS[ycol][1]}",
               title=f"{FCOLS[xcol][0]} и {FCOLS[ycol][0]}")
        ax.legend(fontsize=8, ncol=2)
        return plot_html(f)

    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (C1, C2, C3, CAT, CAT_RU, FAMS, FCOLS, FRU, G, T, describe_cards, fit_view, fonts, scatter_view,
            Path, PUB, base64, cards, code_block, fig, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, stats, table_html, types)


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([mo.Html("<style>\n:root { --lab-bg:#fafaf7; --lab-card:#ffffff; --lab-ink:#1a1d24; --lab-ink2:#5c6170;\n        --lab-line:#e6e5e0; --lab-acc:#2a78d6; --lab-acc2:#a9c8ef; --lab-soft:#f1f0eb; }\nbody, #App, .mo-app, [data-testid=\"app\"] { background: var(--lab-bg) !important; }\n.markdown h1, .markdown h2, .markdown h3, .markdown h4 { color: var(--lab-ink); letter-spacing: -.01em; }\n.markdown h2 { font-size: 1.6rem; margin-top: 2.4rem; padding-top: 1rem; border-top: 2px solid var(--lab-line); }\n.markdown h3 { font-size: 1.22rem; margin-top: 1.6rem; }\n.markdown a { color: var(--lab-acc); }\n.lab-cover { background: radial-gradient(120% 140% at 100% 0%,#2a78d6 0%,#1a1d24 55%); color: #fafaf7; border-radius: 18px; padding: 2.2rem 2rem 1.8rem;\n             margin-bottom: .6rem; position: relative; overflow: hidden; }\n.lab-cover .kicker { text-transform: uppercase; letter-spacing: .14em; font-size: .75rem; opacity: .75; }\n.lab-cover h1 { font-size: clamp(1.8rem, 4.6vw, 3rem); line-height: 1.08; margin: .5rem 0 .8rem; color: inherit; border: 0; }\n.lab-cover p { max-width: 46rem; opacity: .9; margin: .3rem 0; }\n.lab-cover .meta { display: flex; flex-wrap: wrap; gap: .5rem 1.4rem; margin-top: 1.2rem; font-size: .88rem; opacity: .85; }\n.lab-cover .meta b { font-weight: 600; }\n.lab-guide { background: var(--lab-card); border: 1px solid var(--lab-line); border-radius: 14px; padding: 1rem 1.2rem; }\n.lab-guide h4 { margin: 0 0 .4rem; }\n.lab-guide ul { margin: .2rem 0 0 1.1rem; padding: 0; }\n.lab-fig { margin: .4rem 0; background: #fff; border: 1px solid var(--lab-line); border-radius: 12px; padding: .5rem; }\n.lab-fig img { display: block; width: 100%; height: auto; }\n.lab-fig.live { border-color: var(--lab-acc2); }\n.lab-tbl { overflow-x: auto; }\n.lab-tbl table { border-collapse: collapse; font-size: .86rem; background: #fff; border: 1px solid var(--lab-line); }\n.lab-tbl th, .lab-tbl td { border-bottom: 1px solid var(--lab-line); padding: .32rem .6rem; text-align: right; }\n.lab-tbl th { background: var(--lab-soft); color: var(--lab-ink); font-weight: 600; }\n.lab-out { background: #fff; border: 1px solid var(--lab-line); border-radius: 10px; padding: .6rem .8rem;\n           font-size: .8rem; line-height: 1.45; overflow-x: auto; color: var(--lab-ink); margin: .2rem 0; }\n.lab-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: .6rem; margin: .3rem 0; }\n.lab-card { background: var(--lab-card); border: 1px solid var(--lab-line); border-radius: 12px; padding: .7rem .85rem;\n            display: flex; flex-direction: column; gap: .1rem; }\n.lab-card span { font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: var(--lab-ink2); }\n.lab-card b { font-size: 1.45rem; font-variant-numeric: tabular-nums; color: var(--lab-ink); }\n.lab-card small { color: var(--lab-ink2); font-size: .78rem; }\n.lab-live { border-left: 4px solid var(--lab-acc); padding: .2rem 0 .1rem .9rem; margin-top: 1rem; }\n.lab-live .tag { display: inline-block; font-size: .68rem; text-transform: uppercase; letter-spacing: .12em;\n                  background: var(--lab-acc); color: #fff; border-radius: 999px; padding: .12rem .55rem; }\n.lab-live h4 { margin: .35rem 0 .15rem; font-size: 1.08rem; color: var(--lab-ink); }\n.lab-live p { margin: 0; color: var(--lab-ink2); font-size: .9rem; }\n.lab-toc a { text-decoration: none; }\n.lab-toc ul { padding-left: 1rem; }\n@media (max-width: 640px) { .lab-cover { padding: 1.5rem 1.2rem; } }\n</style>\n<div class=\"lab-cover\">\n  <div class=\"kicker\">Lab01 · доп. задание КТвД · Быкова Кристина Денисовна, группа 27</div>\n  <h1>Шрифт как случайная величина</h1>\n  <p>100 семейств Google Fonts, по 20 в каждой категории. Две случайные величины одной природы — высота строчных\n  (x-height) и толщина основного штриха — измерены по контурам букв. Случайность, распределения, зависимость,\n  гипотеза про гротески и датчик, который выдаёт пропорции «нового» шрифта.</p>\n  <div class=\"meta\"><span><b>Данные:</b> собственный датасет, 106 измерено, 100 в анализе</span>\n  <span><b>Код:</b> labfont (fontTools), labrng, labstat</span></div>\n</div>\n<div class=\"lab-guide\"><h4>Как читать отчёт</h4><ul>\n  <li><b>☰ Содержание</b> — панель слева (на телефоне — кнопка вверху): переход к любому разделу.</li>\n  <li><b>«Код этого раздела»</b> под каждым разделом — код, которым посчитаны таблицы и рисунки.</li>\n  <li><b>Живые блоки</b> с синей полоской — фильтры по категориям, подбор моделей, датчик: всё считается в браузере.</li>\n  <li>Интерактивная витрина шрифтов (ползунки толщины, сравнение шрифтов) — на <a href=\"../\" target=\"_top\">главной странице шрифтов</a>.</li>\n  <li><a href=\"../../\" target=\"_top\">← Lab01: все части работы</a> · <a href=\"../../wine/\" target=\"_top\">основная работа (вино)</a></li>\n</ul></div>"), mo.md("# Lab01 · КТвД · доп. задание: пропорции шрифтов\n\n**Две случайные величины одной природы: высота строчных (x-height) и толщина основного штриха.**\n\n| | |\n|---|---|\n| Датасет | собственный: шрифты Google Fonts, измерены по контурам букв скриптом `labfont` (fontTools) |\n| Генеральная совокупность | собранная коллекция, $N = 100$ семейств; одно начертание на семейство, ближайшее к Regular |\n| Категории | display 20, serif 20, mono 20, handwriting 20, sans 20 |\n| Случайные величины | RV01 **x-height**, RV02 **толщина штриха «l»**; обе в долях кегля |\n| Запуск | [открыть в Google Colab](https://colab.research.google.com/github/kkristinabbykova/lab01/blob/main/fonts/fonts.ipynb) (первая ячейка сама скачает репозиторий) или локально: `jupyter notebook fonts.ipynb` |\n| Автор | Быкова Кристина Денисовна (ИСУ 501322), группа 27, трек КТвД |\n| Код | `labfont/` (измерения, схема), `labstat/` (статистические функции из основной части, автор Нефедьева А. С.), тесты `tests/test_labfont.py` |")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.sidebar([mo.md("### Содержание\n\n- [1. Dataset: коллекция шрифтов](#ds)\n    - [1.1 Как измерено](#ds-how)\n    - [1.2 Обзор данных](#ds-eda)\n- [2. Random Variable 01 (x-height)](#rv1)\n    - [2.1 Description (природа события)](#rv1-desc)\n    - [2.2 EDA & Distribution](#rv1-eda)\n- [3. Random Variable 02 (толщина штриха)](#rv2)\n    - [3.1 Description (природа события)](#rv2-desc)\n    - [3.2 EDA & Distribution](#rv2-eda)\n- [4. Independence: x-height и толщина штриха](#dep)\n    - [4.1 Гипотеза: у гротесков x-height больше, чем у антикв](#hyp)\n- [5. Resume](#resume)\n    - [5.1 Итоговые метрики](#res-metrics)\n    - [5.2 Выводы](#res-concl)\n    - [5.3 Литература](#res-lit)\n    - [5.4 cat_mark_table](#res-marks)\n\n\n**Живые блоки**\n\n- [Коллекция по категориям](#live-collection)\n- [Подбор распределения: x-height](#live-fit-xh)\n- [Подбор распределения: толщина штриха](#live-fit-stem)\n- [Связь внутри категорий](#live-within)\n- [Сравнение двух категорий](#live-compare)\n- [Датчик: случайный шрифт](#live-gen)\n")])
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        out_text("Исключены (нет строчных букв): ['Alegreya SC', 'Cinzel Decorative', 'Cormorant SC', 'Rubik Mono One', 'Spectral SC', 'Yuji Hentaigana Akari']"),
        out_text("(100, 20)"),
        code_block("import os, subprocess, sys\nif \"google.colab\" in sys.modules and not os.path.exists(\"labfont\"):   # в Colab: скачать репозиторий с пакетами и данными\n    subprocess.run([\"git\", \"clone\", \"-q\", \"https://github.com/kkristinabbykova/lab01.git\"], check=True)\n    os.chdir(\"lab01/fonts\")\nsys.path.insert(0, \".\")   # пакеты labstat и labfont лежат в корне репозитория\nimport warnings\nimport numpy as np\nimport pandas as pd\nfrom pathlib import Path\nfrom scipy import stats\n\nfrom labstat import dependence, describe as dsc, distributions as dist, hypotheses as hyp, stochastic, plots\nfrom labfont import fontplots as fp\nfrom labfont.illustrate import measurement_figure\n\nwarnings.filterwarnings(\"ignore\", category=RuntimeWarning)\npd.set_option(\"display.precision\", 4)\nplots.style()\nSEED = 2026\nraw = pd.read_csv(\"data/fonts.csv\")\nraw[\"category\"] = raw[\"category\"].fillna(\"\")\n# Шрифты без настоящих строчных (капитель SC, униказ): их «x» — это капитель или прописная\nprint(\"Исключены (нет строчных букв):\", raw.family[raw.no_lowercase].tolist())\nfonts = raw[~raw.no_lowercase].reset_index(drop=True)\nOTHERS = ['cap_height', 'contrast', 'width_o', 'adv_mean', 'weight_class']\nfonts.shape"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"ds\"></a>\n## 1. Dataset: коллекция шрифтов\n\n<a id=\"ds-how\"></a>\n### 1.1 Как измерено\n\nШрифты взяты из двух источников: 37 семейств выбраны автором на fonts.google.com, ещё 69 добавлены\n**случайным отбором** из репозитория Google Fonts (github.com/google/fonts) так, чтобы в каждой категории было по 20\n(`tools/sample_google_fonts.py`, `random.Random(2026)`). Категории — по каталогу Google Fonts (`data/font_categories.csv`).\nСкрипт `python -m labfont.collect fonts/ data/fonts.csv` берёт из архива одно начертание, ближайшее к Regular\n(прямое, вес 400; у вариативного шрифта создаётся экземпляр с $\\mathrm{wght} = 400$), и меряет контуры букв.\n\nВсе длины делятся на размер кегля в единицах шрифта (UPM), поэтому величины **безразмерные, в долях кегля**:\nx-height $= 0.5$ значит, что при кегле 16 px строчные буквы высотой 8 px.\n\n- **x-height**: верхняя точка контура «x»;\n- **толщина штриха**: ширина вертикали «l» на линии $y = \\tfrac12\\,$x-height. Контур дробится в многоугольник,\n  по точкам пересечения с горизонталью находятся участки «чернил» (правило ненулевой обмотки, как у растеризатора шрифтов);\n- **контраст**: толщина боков «o» к толщине верха и низа; **ширина**: ширина «o» к x-height.\n  Даже у шрифтов, которые выглядят «без контраста», бока «o» обычно чуть толще: горизонтальные штрихи той же\n  толщины, что и вертикальные, кажутся глазу заметно толще, и дизайнеры это компенсируют [10, с. 38].\n\nТермины (основной штрих, рост строчных) — по таблицам шрифтовой терминологии В. Кричевского и В. Ефимова,\nприведённым у Ю. Гордона [10, с. 36–37].\n\n**Очистка.** Измерено семейств: 106. Исключены (6) шрифты без настоящих строчных букв\n(Alegreya SC, Cinzel Decorative, Cormorant SC, Rubik Mono One, Spectral SC, Yuji Hentaigana Akari): в капительных (SC) и декоративных шрифтах на месте «x» стоит капитель или прописная форма,\nи «x-height» у них — это не высота строчных. Признак: у «l» нет выносного элемента (она не выше «x» больше чем в 1.15 раза;\nу остальных шрифтов отношение от 1.25). Spectral SC вдобавок повторяет Spectral. Начертания оптических размеров\n(Inter 18pt, Fraunces 72pt) и ширин (Roboto SemiCondensed) объединены с основным семейством по папке Google Fonts.\n\n**Ограничение.** Выборка смешанная: часть шрифтов выбрана по вкусу, часть — случайно. Поэтому генеральная совокупность\nздесь — «эта коллекция», а не все шрифты мира; выводы о Google Fonts в целом делаются осторожно.\n\nПочему одно начертание на семейство: Bold, Italic и Regular одного семейства рисовал один дизайнер,\nэто зависимые наблюдения. Наблюдение здесь — семейство."),
        fig("f001_02.png"),
        mo.md("<a id=\"fig1\"></a>\n*Рис. 1. Схема измерений на контурах настоящего шрифта: x-height, высота прописных, толщина штриха «l» и контраст «o».*"),
        code_block("fig, m = measurement_figure(Path(\"data/fonts_sample/Playfair-VariableFont.ttf\").read_bytes())\nplots.save(fig, \"fonts_measure.png\");"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"ds-eda\"></a>\n### 1.2 Обзор данных"),
        out_text("Семейств: 100 | с кириллицей: 39 | вариативных: 32\nВес OS/2 у выбранных начертаний: {400: 100}"),
        table_html("<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>x_height</th>\n      <th>stem</th>\n      <th>contrast</th>\n      <th>width_o</th>\n    </tr>\n    <tr>\n      <th>category</th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>display</th>\n      <td>0.500</td>\n      <td>0.114</td>\n      <td>1.303</td>\n      <td>1.008</td>\n    </tr>\n    <tr>\n      <th>handwriting</th>\n      <td>0.471</td>\n      <td>0.065</td>\n      <td>1.028</td>\n      <td>0.889</td>\n    </tr>\n    <tr>\n      <th>mono</th>\n      <td>0.519</td>\n      <td>0.084</td>\n      <td>1.138</td>\n      <td>0.901</td>\n    </tr>\n    <tr>\n      <th>sans</th>\n      <td>0.521</td>\n      <td>0.087</td>\n      <td>1.202</td>\n      <td>0.941</td>\n    </tr>\n    <tr>\n      <th>serif</th>\n      <td>0.460</td>\n      <td>0.082</td>\n      <td>2.092</td>\n      <td>0.981</td>\n    </tr>\n  </tbody>\n</table>\n</div>"),
        fig("f002_05.png"),
        mo.md("<a id=\"fig2\"></a>\n*Рис. 2. Ранговые корреляции Спирмена $\\rho$ между измерениями шрифтов.*"),
        code_block("print(\"Семейств:\", len(fonts), \"| с кириллицей:\", int(fonts.has_cyrillic.sum()), \"| вариативных:\", int(fonts.is_variable.sum()))\nprint(\"Вес OS/2 у выбранных начертаний:\", fonts.weight_class.value_counts().sort_index().to_dict())\nfonts.groupby(\"category\")[[\"x_height\", \"stem\", \"contrast\", \"width_o\"]].median().round(3)\n\ncols = [\"x_height\", \"cap_height\", \"x_to_cap\", \"stem\", \"contrast\", \"width_o\", \"adv_mean\"]\nplots.corr_heatmap(fonts[cols].rename(columns=fp.COL_RU).corr(method=\"spearman\"), \"fonts_corr.png\", title=\"Связи между измерениями шрифтов\");"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(CAT, FCOLS, live, mo):
    coll_cats = mo.ui.multiselect(options=[v[0] for v in CAT.values()], value=[v[0] for v in CAT.values()], label="Категории")
    coll_x = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items()}, value="x-height", label="По горизонтали")
    coll_y = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items()}, value="толщина штриха", label="По вертикали")
    coll_names = mo.ui.switch(value=False, label="подписать шрифты")
    mo.vstack([mo.Html('<a id="live-collection"></a>'),
               live("Коллекция по категориям", "Выберите категории и любые две пропорции: точки — шрифты. "
                    "Подписи помогают найти выбросы — например, самые жирные акцидентные.", coll_cats, coll_x, coll_y, coll_names)])
    return coll_cats, coll_names, coll_x, coll_y


@app.cell(hide_code=True)
def _(CAT_RU, FCOLS, coll_cats, coll_names, coll_x, coll_y, describe_cards, fonts, mo, scatter_view):
    _d = fonts[fonts.category.isin([CAT_RU[c] for c in coll_cats.value])]
    _x = _d[coll_x.value].dropna().to_numpy(float)
    mo.vstack([describe_cards(_x, FCOLS[coll_x.value][1]) if len(_x) else mo.md("_Выберите хотя бы одну категорию._"),
               scatter_view(_d, coll_x.value, coll_y.value, coll_cats.value, coll_names.value)])
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"rv1\"></a>\n## 2. Random Variable 01 (x-height)"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"rv1-desc\"></a>\n### 2.1 Description (природа события)\n\n**Величина.** Высота строчных в долях кегля. В русской терминологии это «рост строчных знаков»: расстояние от линии шрифта до вершины строчной x [9, с. 49]. Точность измерения $1/\\mathrm{UPM}$ (у большинства шрифтов\n$1/1000$ или $1/2048$ кегля), то есть $\\le 0.001$.\n\n**Событие.** Из коллекции случайно выбирается семейство шрифтов, у его Regular измеряется высота строчных.\n\n**Что посчитано для проверки стохастической природы.** Прогноз величины по остальным измерениям\n(высота прописных, контраст, ширина «o», средняя ширина букв, вес OS/2 и вторая величина) на 5-кратной кросс-валидации: линейная регрессия и $k = 5$ ближайших\nсоседей. Если бы величина вычислялась формулой из остальных, $R^2 \\approx 1$, а остаток был бы порядка\nточности $0.001$. Плюс разброс внутри одной категории: если бы категория (гротеск, антиква…) задавала величину,\nвнутри категории разброса бы не было.\n\n**Природа события.** x-height — случайная величина, так как она зависит в первую очередь\nот создателя шрифта: именно тот, кто рисует шрифт, решает, какой она будет. Мы не можем заранее знать x-height\nслучайно выбранного шрифта, так как не знаем, какую высоту дал ему автор. Высоту можно предположить по категории\nшрифта, так как шрифты одной категории во многом похожи, и с помощью примерных подсчётов по другим размерам\n($R^2 = 0.67$). Но это только примерно: точно вычислить x-height нельзя, ошибка прогноза остаётся."),
        out_text("Линейная модель: R² = 0.671, СКО остатка 0.0377 кегля\n5 ближайших соседей: R² = 0.509, СКО остатка 0.0451 кегля\nНаблюдений в модели: 98 (без шрифтов с неизмеренным контрастом)\nСКО самой величины 0.0660; точность измерения ≤ 0.001"),
        fig("f004_07.png"),
        mo.md("<a id=\"fig_x_height_cat\"></a>\n*Рис. 3. x-height по категориям шрифтов: ящики с усами и сами наблюдения.*"),
        mo.md("**Результаты:**\n\n- Линейная модель по остальным измерениям: $R^2 = 0.671$, СКО остатка 0.0377 кегля.\n- 5 ближайших соседей: $R^2 = 0.509$, СКО остатка 0.0451 кегля.\n- СКО самой величины 0.0660 (шрифтов в модели: 98), точность измерения $\\le 0.001$: даже лучший остаток (0.0377) больше точности, отношение $\\approx 38$.\n- Средний по категориям разброс внутри категории составляет 82 % общего СКО."),
        code_block("full = fonts.dropna(subset=OTHERS + [\"x_height\", \"stem\"])   # без шрифтов с неизмеренным контрастом\ny = full[\"x_height\"].to_numpy()\nXo = full[[c for c in OTHERS + [\"x_height\", \"stem\"] if c != \"x_height\"]].to_numpy()\nlin = stochastic.cv_r2_linear(Xo, y, k=5, seed=SEED)\nknn = stochastic.cv_r2_knn(Xo, y, k_neighbors=5, k=5, seed=SEED)\nprint(f\"Линейная модель: R² = {lin['r2_cv']:.3f}, СКО остатка {lin['resid_std']:.4f} кегля\")\nprint(f\"5 ближайших соседей: R² = {knn['r2_cv']:.3f}, СКО остатка {knn['resid_std']:.4f} кегля\")\nprint(f\"Наблюдений в модели: {len(full)} (без шрифтов с неизмеренным контрастом)\")\nprint(f\"СКО самой величины {y.std(ddof=1):.4f}; точность измерения ≤ 0.001\")\nfp.box_by_category(fonts, \"x_height\", \"x-height\", \"доли кегля\", \"fonts_x_height_by_cat.png\");"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"rv1-eda\"></a>\n### 2.2 EDA & Distribution"),
        out_text("Выбросов по правилу 1.5·IQR: 4"),
        table_html("<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>n</th>\n      <th>mean</th>\n      <th>var</th>\n      <th>std</th>\n      <th>cv</th>\n      <th>min</th>\n      <th>q25</th>\n      <th>median</th>\n      <th>q75</th>\n      <th>max</th>\n      <th>iqr</th>\n      <th>mode</th>\n      <th>skew</th>\n      <th>kurt</th>\n      <th>n_unique</th>\n      <th>step</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>все</th>\n      <td>100.0</td>\n      <td>0.4807</td>\n      <td>0.0044</td>\n      <td>0.0663</td>\n      <td>0.1379</td>\n      <td>0.1512</td>\n      <td>0.4566</td>\n      <td>0.4985</td>\n      <td>0.5236</td>\n      <td>0.6401</td>\n      <td>0.0670</td>\n      <td>0.5000</td>\n      <td>-1.6591</td>\n      <td>5.5849</td>\n      <td>80.0</td>\n      <td>3.0428e-05</td>\n    </tr>\n    <tr>\n      <th>display</th>\n      <td>20.0</td>\n      <td>0.4899</td>\n      <td>0.0030</td>\n      <td>0.0548</td>\n      <td>0.1118</td>\n      <td>0.3890</td>\n      <td>0.4668</td>\n      <td>0.5000</td>\n      <td>0.5155</td>\n      <td>0.6401</td>\n      <td>0.0487</td>\n      <td>0.5000</td>\n      <td>0.4117</td>\n      <td>1.4950</td>\n      <td>19.0</td>\n      <td>6.0034e-04</td>\n    </tr>\n    <tr>\n      <th>handwriting</th>\n      <td>20.0</td>\n      <td>0.4345</td>\n      <td>0.0108</td>\n      <td>0.1040</td>\n      <td>0.2395</td>\n      <td>0.1512</td>\n      <td>0.3780</td>\n      <td>0.4709</td>\n      <td>0.5096</td>\n      <td>0.5859</td>\n      <td>0.1316</td>\n      <td>0.1512</td>\n      <td>-1.0056</td>\n      <td>0.8845</td>\n      <td>20.0</td>\n      <td>3.0428e-05</td>\n    </tr>\n    <tr>\n      <th>mono</th>\n      <td>20.0</td>\n      <td>0.5106</td>\n      <td>0.0012</td>\n      <td>0.0349</td>\n      <td>0.0683</td>\n      <td>0.4000</td>\n      <td>0.4990</td>\n      <td>0.5188</td>\n      <td>0.5287</td>\n      <td>0.5600</td>\n      <td>0.0297</td>\n      <td>0.5000</td>\n      <td>-1.6023</td>\n      <td>3.1958</td>\n      <td>17.0</td>\n      <td>1.3203e-03</td>\n    </tr>\n    <tr>\n      <th>sans</th>\n      <td>20.0</td>\n      <td>0.5100</td>\n      <td>0.0015</td>\n      <td>0.0393</td>\n      <td>0.0771</td>\n      <td>0.4140</td>\n      <td>0.4976</td>\n      <td>0.5206</td>\n      <td>0.5310</td>\n      <td>0.5780</td>\n      <td>0.0334</td>\n      <td>0.5000</td>\n      <td>-0.7973</td>\n      <td>0.4393</td>\n      <td>18.0</td>\n      <td>9.7656e-04</td>\n    </tr>\n    <tr>\n      <th>serif</th>\n      <td>20.0</td>\n      <td>0.4586</td>\n      <td>0.0016</td>\n      <td>0.0400</td>\n      <td>0.0872</td>\n      <td>0.3750</td>\n      <td>0.4309</td>\n      <td>0.4600</td>\n      <td>0.4840</td>\n      <td>0.5360</td>\n      <td>0.0531</td>\n      <td>0.3750</td>\n      <td>-0.1807</td>\n      <td>-0.4006</td>\n      <td>20.0</td>\n      <td>3.3594e-04</td>\n    </tr>\n  </tbody>\n</table>\n</div>"),
        table_html("<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>k</th>\n      <th>loglik</th>\n      <th>AIC</th>\n      <th>BIC</th>\n      <th>KS_D</th>\n      <th>params</th>\n    </tr>\n    <tr>\n      <th>dist</th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>weibull_min</th>\n      <td>3</td>\n      <td>140.3320</td>\n      <td>-274.6639</td>\n      <td>-266.8484</td>\n      <td>0.1047</td>\n      <td>(24.3521, -0.7798, 1.2879)</td>\n    </tr>\n    <tr>\n      <th>skewnorm</th>\n      <td>3</td>\n      <td>139.8473</td>\n      <td>-273.6945</td>\n      <td>-265.8790</td>\n      <td>0.1064</td>\n      <td>(-3.0913, 0.5507, 0.0961)</td>\n    </tr>\n    <tr>\n      <th>norm</th>\n      <td>2</td>\n      <td>130.0155</td>\n      <td>-256.0309</td>\n      <td>-250.8206</td>\n      <td>0.1357</td>\n      <td>(0.4807, 0.0659)</td>\n    </tr>\n    <tr>\n      <th>lognorm</th>\n      <td>3</td>\n      <td>130.0154</td>\n      <td>-254.0308</td>\n      <td>-246.2153</td>\n      <td>0.1357</td>\n      <td>(0.0, -65535.8488, 65536.3295)</td>\n    </tr>\n    <tr>\n      <th>gamma</th>\n      <td>3</td>\n      <td>126.1514</td>\n      <td>-246.3027</td>\n      <td>-238.4872</td>\n      <td>0.1516</td>\n      <td>(270.9875, -0.7014, 0.0044)</td>\n    </tr>\n  </tbody>\n</table>\n</div>"),
        fig("f005_11.png"),
        mo.md("<a id=\"fig_x_height_eda\"></a>\n*Рис. 4. x-height: гистограмма с подобранными плотностями, ящик с усами, Q-Q к нормальному.*"),
        mo.md("**Результаты:**\n\n- $N = 100$, среднее 0.481, медиана 0.499, СКО 0.0663, коэффициент вариации 13.8 %.\n- Асимметрия $-1.66$, эксцесс $+5.58$; диапазон 0.151–0.640; выбросов по $1.5\\cdot\\mathrm{IQR}$: 4.\n- Лучшее семейство по AIC: Вейбулла; D'Agostino $K^2$ для нормального: $p \\approx 10^{-11}$.\n\n**Что видно на графиках.** На гистограмме больше всего шрифтов около значения 0.5\n(медиана 0.499). Среднее немного меньше (0.481): его вниз тянет левый хвост. Хвост слева длиннее, потому что\nвстречаются отдельные шрифты с очень маленькой x-height (0.15–0.35), а выше 0.6 строчные почти не бывают, иначе\nони сравняются с прописными. На ящике с усами выбросы в основном снизу: три шрифта с необычно маленькой x-height\nи один с большой. Синий колокол нормального распределения повторяет столбики хуже: он симметричный, а данные нет.\nБлиже к столбикам несимметричные модели: Вейбулла и скошенное нормальное. Q-Q график это подтверждает: крайние\nточки уходят от прямой, и нормальное распределение отвергается ($p \\approx 10^{-11}$)."),
        code_block("x_x_height = fonts[\"x_height\"].to_numpy()\nprint(\"Выбросов по правилу 1.5·IQR:\", dsc.iqr_outliers(x_x_height).sum())\ndisplay(dsc.compare_table({\"все\": x_x_height} | {c: g[\"x_height\"] for c, g in fonts.groupby(\"category\")}).T)\nfit_x_height = dist.fit_candidates(x_x_height)\nfit_x_height\n\nbest_x_height = {nm: dist.fit(nm, x_x_height) for nm in [\"norm\"] + [d for d in fit_x_height.index if d != \"norm\"][:2]}\nplots.eda_panel(x_x_height, \"x-height\", \"доли кегля\", best_x_height, \"fonts_x_height_eda.png\", bins=\"fd\");"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(FAMS, live, mo):
    fit_fams_xh = mo.ui.multiselect(options=list(FAMS), value=["нормальное", "скошенное нормальное", "Вейбулла"], label="Модели")
    fit_bins_xh = mo.ui.slider(start=8, stop=40, step=2, value=20, label="Столбики", show_value=True)
    mo.vstack([mo.Html('<a id="live-fit-xh"></a>'),
               live("Подбор распределения вживую", "Включайте модели и меняйте число столбиков: на графике плотности моделей, "
                    "в таблице AIC (меньше — лучше) и расстояние Колмогорова D.", fit_fams_xh, fit_bins_xh)])
    return fit_bins_xh, fit_fams_xh


@app.cell(hide_code=True)
def _(FCOLS, fit_bins_xh, fit_fams_xh, fit_view, fonts, mo):
    _label, _unit = FCOLS["x_height"]
    _img, _tab = fit_view(fonts["x_height"].dropna().to_numpy(float), fit_fams_xh.value, fit_bins_xh.value, _label, _unit, "xh")
    mo.vstack([_img, mo.ui.table(_tab, selection=None, pagination=False) if len(_tab) else mo.md("_Выберите хотя бы одну модель._")])
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"rv2\"></a>\n## 3. Random Variable 02 (толщина штриха)"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"rv2-desc\"></a>\n### 3.1 Description (природа события)\n\n**Величина.** Толщина вертикали «l» в долях кегля. Толщина основных штрихов определяет насыщенность шрифта, от светлого до жирного [9, с. 61]. Точность измерения $1/\\mathrm{UPM}$ (у большинства шрифтов\n$1/1000$ или $1/2048$ кегля), то есть $\\le 0.001$.\n\n**Событие.** Из коллекции случайно выбирается семейство шрифтов, у его Regular измеряется толщина вертикали «l».\n\n**Что посчитано для проверки стохастической природы.** Прогноз величины по остальным измерениям\n(высота прописных, контраст, ширина «o», средняя ширина букв, вес OS/2 и вторая величина) на 5-кратной кросс-валидации: линейная регрессия и $k = 5$ ближайших\nсоседей. Если бы величина вычислялась формулой из остальных, $R^2 \\approx 1$, а остаток был бы порядка\nточности $0.001$. Плюс разброс внутри одной категории: если бы категория (гротеск, антиква…) задавала величину,\nвнутри категории разброса бы не было.\n\n**Природа события.** Толщина штриха — случайная величина: какой она будет, решает автор\nшрифта в зависимости от того, для чего шрифт нужен. Жирный шрифт делают, чтобы он был акцентным, а тонкий и лёгкий —\nчтобы он был не акцентным. Заранее предположить толщину случайно выбранного шрифта очень сложно, и угадать её\nпо категории и другим размерам тоже: прогноз объясняет только около половины разброса ($R^2 = 0.54$), а внутри\nодной категории остаётся 74 % разброса."),
        out_text("Линейная модель: R² = 0.539, СКО остатка 0.0332 кегля\n5 ближайших соседей: R² = 0.156, СКО остатка 0.0446 кегля\nНаблюдений в модели: 98 (без шрифтов с неизмеренным контрастом)\nСКО самой величины 0.0490; точность измерения ≤ 0.001"),
        fig("f007_13.png"),
        mo.md("<a id=\"fig_stem_cat\"></a>\n*Рис. 5. Толщина штриха по категориям шрифтов: ящики с усами и сами наблюдения.*"),
        mo.md("**Результаты:**\n\n- Линейная модель по остальным измерениям: $R^2 = 0.539$, СКО остатка 0.0332 кегля.\n- 5 ближайших соседей: $R^2 = 0.156$, СКО остатка 0.0446 кегля.\n- СКО самой величины 0.0490 (шрифтов в модели: 98), точность измерения $\\le 0.001$: даже лучший остаток (0.0332) больше точности, отношение $\\approx 33$.\n- Средний по категориям разброс внутри категории составляет 74 % общего СКО."),
        code_block("full = fonts.dropna(subset=OTHERS + [\"x_height\", \"stem\"])   # без шрифтов с неизмеренным контрастом\ny = full[\"stem\"].to_numpy()\nXo = full[[c for c in OTHERS + [\"x_height\", \"stem\"] if c != \"stem\"]].to_numpy()\nlin = stochastic.cv_r2_linear(Xo, y, k=5, seed=SEED)\nknn = stochastic.cv_r2_knn(Xo, y, k_neighbors=5, k=5, seed=SEED)\nprint(f\"Линейная модель: R² = {lin['r2_cv']:.3f}, СКО остатка {lin['resid_std']:.4f} кегля\")\nprint(f\"5 ближайших соседей: R² = {knn['r2_cv']:.3f}, СКО остатка {knn['resid_std']:.4f} кегля\")\nprint(f\"Наблюдений в модели: {len(full)} (без шрифтов с неизмеренным контрастом)\")\nprint(f\"СКО самой величины {y.std(ddof=1):.4f}; точность измерения ≤ 0.001\")\nfp.box_by_category(fonts, \"stem\", \"толщина штриха\", \"доли кегля\", \"fonts_stem_by_cat.png\");"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"rv2-eda\"></a>\n### 3.2 EDA & Distribution"),
        out_text("Выбросов по правилу 1.5·IQR: 16"),
        table_html("<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>n</th>\n      <th>mean</th>\n      <th>var</th>\n      <th>std</th>\n      <th>cv</th>\n      <th>min</th>\n      <th>q25</th>\n      <th>median</th>\n      <th>q75</th>\n      <th>max</th>\n      <th>iqr</th>\n      <th>mode</th>\n      <th>skew</th>\n      <th>kurt</th>\n      <th>n_unique</th>\n      <th>step</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>все</th>\n      <td>100.0</td>\n      <td>0.0915</td>\n      <td>2.3716e-03</td>\n      <td>0.0487</td>\n      <td>0.5320</td>\n      <td>0.0223</td>\n      <td>0.0727</td>\n      <td>0.0840</td>\n      <td>0.0931</td>\n      <td>0.4313</td>\n      <td>0.0204</td>\n      <td>0.0900</td>\n      <td>4.2790</td>\n      <td>24.7997</td>\n      <td>83.0</td>\n      <td>1.5625e-05</td>\n    </tr>\n    <tr>\n      <th>display</th>\n      <td>20.0</td>\n      <td>0.1272</td>\n      <td>6.7349e-03</td>\n      <td>0.0821</td>\n      <td>0.6454</td>\n      <td>0.0492</td>\n      <td>0.0809</td>\n      <td>0.1144</td>\n      <td>0.1408</td>\n      <td>0.4313</td>\n      <td>0.0599</td>\n      <td>0.1250</td>\n      <td>2.6643</td>\n      <td>7.6231</td>\n      <td>19.0</td>\n      <td>3.8415e-04</td>\n    </tr>\n    <tr>\n      <th>handwriting</th>\n      <td>20.0</td>\n      <td>0.0641</td>\n      <td>5.9992e-04</td>\n      <td>0.0245</td>\n      <td>0.3818</td>\n      <td>0.0223</td>\n      <td>0.0463</td>\n      <td>0.0653</td>\n      <td>0.0768</td>\n      <td>0.1145</td>\n      <td>0.0305</td>\n      <td>0.0223</td>\n      <td>0.3167</td>\n      <td>-0.6032</td>\n      <td>20.0</td>\n      <td>2.9893e-04</td>\n    </tr>\n    <tr>\n      <th>mono</th>\n      <td>20.0</td>\n      <td>0.0841</td>\n      <td>6.0857e-05</td>\n      <td>0.0078</td>\n      <td>0.0928</td>\n      <td>0.0670</td>\n      <td>0.0809</td>\n      <td>0.0840</td>\n      <td>0.0900</td>\n      <td>0.1010</td>\n      <td>0.0091</td>\n      <td>0.0900</td>\n      <td>-0.4659</td>\n      <td>0.8183</td>\n      <td>14.0</td>\n      <td>1.5625e-05</td>\n    </tr>\n    <tr>\n      <th>sans</th>\n      <td>20.0</td>\n      <td>0.0978</td>\n      <td>2.3984e-03</td>\n      <td>0.0490</td>\n      <td>0.5007</td>\n      <td>0.0670</td>\n      <td>0.0795</td>\n      <td>0.0869</td>\n      <td>0.0931</td>\n      <td>0.2931</td>\n      <td>0.0136</td>\n      <td>0.0879</td>\n      <td>3.4104</td>\n      <td>11.0725</td>\n      <td>19.0</td>\n      <td>1.0937e-04</td>\n    </tr>\n    <tr>\n      <th>serif</th>\n      <td>20.0</td>\n      <td>0.0845</td>\n      <td>2.8593e-04</td>\n      <td>0.0169</td>\n      <td>0.2001</td>\n      <td>0.0410</td>\n      <td>0.0773</td>\n      <td>0.0820</td>\n      <td>0.0931</td>\n      <td>0.1196</td>\n      <td>0.0158</td>\n      <td>0.0410</td>\n      <td>-0.2905</td>\n      <td>0.9405</td>\n      <td>20.0</td>\n      <td>4.8828e-04</td>\n    </tr>\n  </tbody>\n</table>\n</div>"),
        table_html("<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>k</th>\n      <th>loglik</th>\n      <th>AIC</th>\n      <th>BIC</th>\n      <th>KS_D</th>\n      <th>params</th>\n    </tr>\n    <tr>\n      <th>dist</th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>lognorm</th>\n      <td>3</td>\n      <td>200.2241</td>\n      <td>-394.4481</td>\n      <td>-386.6326</td>\n      <td>0.1572</td>\n      <td>(0.3889, 0.0001, 0.084)</td>\n    </tr>\n    <tr>\n      <th>skewnorm</th>\n      <td>3</td>\n      <td>185.8139</td>\n      <td>-365.6278</td>\n      <td>-357.8123</td>\n      <td>0.2471</td>\n      <td>(4.3596, 0.0474, 0.0655)</td>\n    </tr>\n    <tr>\n      <th>gamma</th>\n      <td>3</td>\n      <td>166.8052</td>\n      <td>-327.6103</td>\n      <td>-319.7948</td>\n      <td>0.3404</td>\n      <td>(0.978, 0.0223, 0.0694)</td>\n    </tr>\n    <tr>\n      <th>norm</th>\n      <td>2</td>\n      <td>160.8181</td>\n      <td>-317.6363</td>\n      <td>-312.4259</td>\n      <td>0.2497</td>\n      <td>(0.0915, 0.0485)</td>\n    </tr>\n    <tr>\n      <th>weibull_min</th>\n      <td>3</td>\n      <td>-inf</td>\n      <td>inf</td>\n      <td>inf</td>\n      <td>0.2986</td>\n      <td>(0.7583, 0.06, 0.0195)</td>\n    </tr>\n  </tbody>\n</table>\n</div>"),
        fig("f008_17.png"),
        mo.md("<a id=\"fig_stem_eda\"></a>\n*Рис. 6. Толщина штриха: гистограмма с подобранными плотностями, ящик с усами, Q-Q к нормальному.*"),
        mo.md("**Результаты:**\n\n- $N = 100$, среднее 0.092, медиана 0.084, СКО 0.0487, коэффициент вариации 53.2 %.\n- Асимметрия $+4.28$, эксцесс $+24.80$; диапазон 0.022–0.431; выбросов по $1.5\\cdot\\mathrm{IQR}$: 16.\n- Лучшее семейство по AIC: логнормальное; D'Agostino $K^2$ для нормального: $p \\approx 10^{-28}$.\n\n**Что видно на графиках.** Больше всего шрифтов с толщиной штриха около 0.08–0.09\n(медиана 0.084). Хвост длинный справа: толстых шрифтов мало, но они бывают очень толстыми, до 0.43, это в пять раз\nтолще обычного. Поэтому на ящике с усами выбросы в основном сверху: это самые жирные акцидентные шрифты, которые\nделают, чтобы они были акцентными. Лучше всего столбики повторяет оранжевая линия, логнормальное распределение:\nу неё такой же высокий узкий пик и длинный хвост вправо. Синий колокол нормального распределения симметричный\nи не подходит: на Q-Q графике правые точки резко уходят вверх от прямой, нормальное распределение отвергается\n($p \\approx 10^{-28}$)."),
        code_block("x_stem = fonts[\"stem\"].to_numpy()\nprint(\"Выбросов по правилу 1.5·IQR:\", dsc.iqr_outliers(x_stem).sum())\ndisplay(dsc.compare_table({\"все\": x_stem} | {c: g[\"stem\"] for c, g in fonts.groupby(\"category\")}).T)\nfit_stem = dist.fit_candidates(x_stem)\nfit_stem\n\nbest_stem = {nm: dist.fit(nm, x_stem) for nm in [\"norm\"] + [d for d in fit_stem.index if d != \"norm\"][:2]}\nplots.eda_panel(x_stem, \"толщина штриха\", \"доли кегля\", best_stem, \"fonts_stem_eda.png\", bins=\"fd\");"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(FAMS, live, mo):
    fit_fams_stem = mo.ui.multiselect(options=list(FAMS), value=["нормальное", "логнормальное", "скошенное нормальное"], label="Модели")
    fit_bins_stem = mo.ui.slider(start=8, stop=40, step=2, value=20, label="Столбики", show_value=True)
    mo.vstack([mo.Html('<a id="live-fit-stem"></a>'),
               live("Подбор распределения вживую", "Включайте модели и меняйте число столбиков: на графике плотности моделей, "
                    "в таблице AIC (меньше — лучше) и расстояние Колмогорова D.", fit_fams_stem, fit_bins_stem)])
    return fit_bins_stem, fit_fams_stem


@app.cell(hide_code=True)
def _(FCOLS, fit_bins_stem, fit_fams_stem, fit_view, fonts, mo):
    _label, _unit = FCOLS["stem"]
    _img, _tab = fit_view(fonts["stem"].dropna().to_numpy(float), fit_fams_stem.value, fit_bins_stem.value, _label, _unit, "stem")
    mo.vstack([_img, mo.ui.table(_tab, selection=None, pagination=False) if len(_tab) else mo.md("_Выберите хотя бы одну модель._")])
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"dep\"></a>\n## 4. Independence: x-height и толщина штриха\n\nОбе величины одной природы: пропорции одной и той же буквы, их задаёт один дизайнер. По условию для таких величин\nпроверяется независимость. $H_0$: x-height и толщина штриха независимы. Проверки: корреляции Пирсона, Спирмена,\nКендалла; $\\chi^2$ на таблице сопряжённости по квантилям; перестановочный тест для $\\rho$ Спирмена\n(2000 перестановок). Отдельно $\\rho$ внутри каждой категории: общая связь может возникать только из-за смеси\nкатегорий (парадокс Симпсона)."),
        table_html("<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>coef</th>\n      <th>p</th>\n    </tr>\n    <tr>\n      <th>method</th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>pearson</th>\n      <td>0.3137</td>\n      <td>1.4807e-03</td>\n    </tr>\n    <tr>\n      <th>spearman</th>\n      <td>0.4006</td>\n      <td>3.6211e-05</td>\n    </tr>\n    <tr>\n      <th>kendall</th>\n      <td>0.2851</td>\n      <td>2.9867e-05</td>\n    </tr>\n  </tbody>\n</table>\n</div>"),
        out_text("χ² = 23.7, df = 9, p = 0.00479, V Крамера = 0.281\nперестановочный тест: ρ = 0.401, p = 0.0005\nρ внутри категорий: {'display': np.float64(0.01), 'handwriting': np.float64(0.698), 'mono': np.float64(0.655), 'sans': np.float64(0.452), 'serif': np.float64(0.556)}"),
        fig("f009_20.png"),
        mo.md("<a id=\"fig7\"></a>\n*Рис. 7. x-height и толщина штриха; цвет — категория, чёрная линия — медиана толщины по квинтилям x-height.*"),
        mo.md("**Результаты:**\n\n- Пирсон +0.314, Спирмен +0.401, Кендалл +0.285\n  (для Спирмена $p \\approx 10^{-5}$).\n- $\\chi^2 = 23.7$ при $\\mathrm{df} = 9$, $p = 0.005$, $V$ Крамера 0.281.\n- Перестановочный тест: $\\rho = +0.401$, $p = 0.0005$. $H_0$ о независимости при $\\alpha = 0.05$ **отвергается**.\n- $\\rho$ Спирмена внутри категорий: display +0.01, handwriting +0.70, mono +0.65, sans +0.45, serif +0.56.\n\n**Вывод о зависимости.** Между x-height и толщиной штриха есть связь средней силы\n(ρ Спирмена = 0.40). Она значима: гипотеза о независимости отвергается ($p = 0.0005$). При увеличении высоты\nстрочных штрих тоже увеличивается, так как они соразмерны: если увеличивать только высоту, текст перестанет быть\nчитаемым. Связь сохраняется внутри\nвсех категорий, кроме акцидентных шрифтов: у рукописных ρ = 0.70, у моноширинных 0.65, у антикв 0.56, у гротесков\n0.45, а у акцидентных всего 0.01. Акцидентные шрифты зачастую предназначены для акцента и не подстраиваются\nни под какие правила: они дизайнерские и красивые, обычно не для чтения, а для акцента."),
        code_block("display(dependence.correlations(fonts.x_height, fonts.stem))\nchi = dependence.chi2_independence(fonts.x_height, fonts.stem, bins=4 if len(fonts) >= 80 else 2)\nperm = dependence.permutation_spearman(fonts.x_height, fonts.stem, n_perm=2000, seed=SEED)\nprint(f\"χ² = {chi['chi2']:.1f}, df = {chi['dof']}, p = {chi['p']:.3g}, V Крамера = {chi['cramer_v']:.3f}\")\nprint(f\"перестановочный тест: ρ = {perm['rho']:.3f}, p = {perm['p']:.4f}\")\nprint(\"ρ внутри категорий:\", {c: round(stats.spearmanr(g.x_height, g.stem)[0], 3) for c, g in fonts.groupby(\"category\") if len(g) >= 8})\nfp.scatter_by_category(fonts, \"x_height\", \"stem\", \"x-height, доли кегля\", \"толщина штриха, доли кегля\",\n                       \"x-height и толщина штриха\", \"fonts_dependence.png\");"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(CAT, live, mo):
    within_cat = mo.ui.dropdown(options=["все шрифты"] + [v[0] for v in CAT.values()], value="все шрифты", label="Категория")
    mo.vstack([mo.Html('<a id="live-within"></a>'),
               live("Связь x-height и толщины внутри категории", "Общая связь может возникнуть просто из-за смеси категорий. "
                    "Проверьте каждую категорию отдельно: у акцидентных связи почти нет.", within_cat)])
    return (within_cat,)


@app.cell(hide_code=True)
def _(CAT, CAT_RU, cards, fonts, mo, scatter_view, stats, within_cat):
    _all = within_cat.value == "все шрифты"
    _d = fonts if _all else fonts[fonts.category == CAT_RU[within_cat.value]]
    _rho, _p = stats.spearmanr(_d.x_height, _d.stem)
    mo.vstack([cards([("ρ Спирмена", f"{_rho:+.2f}", "сила и направление связи"), ("p", f"{_p:.4f}", "< 0.05 — связь есть"),
                      ("шрифтов", f"{len(_d)}", within_cat.value)]),
               scatter_view(_d, "x_height", "stem", [v[0] for v in CAT.values()] if _all else [within_cat.value], not _all)])
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"hyp\"></a>\n### 4.1 Гипотеза: у гротесков x-height больше, чем у антикв\n\nВ типографике принято считать, что у гротесков строчные выше, чем у антикв. Проверяем односторонним критерием\nМанна–Уитни: $H_0$: $P(X_{\\text{sans}} > X_{\\text{serif}}) \\le 1/2$, $\\alpha = 0.05$."),
        out_text("медиана x-height: гротески 0.521 (n = 20), антиквы 0.460 (n = 20)"),
        out_text("test        Mann–Whitney (greater)\nH0                  P(A > B) ≤ 1/2\nstat                         330.5\np                           0.0002\ndecision              отвергаем H0\np_a_gt_b                    0.8263\ndtype: object"),
        mo.md("**Результаты:** медиана x-height у гротесков 0.521, у антикв 0.460;\nкритерий Манна–Уитни $p = 0.0002$, $H_0$ **отвергается**."),
        code_block("sans, serif = fonts.x_height[fonts.category == \"sans\"], fonts.x_height[fonts.category == \"serif\"]\nh_sans = hyp.mann_whitney(sans, serif, alternative=\"greater\")\nprint(f\"медиана x-height: гротески {sans.median():.3f} (n = {len(sans)}), антиквы {serif.median():.3f} (n = {len(serif)})\")\npd.Series(h_sans)"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(CAT, FCOLS, live, mo):
    cmp_a = mo.ui.dropdown(options=[v[0] for v in CAT.values()], value="гротески", label="Категория A")
    cmp_b = mo.ui.dropdown(options=[v[0] for v in CAT.values()], value="антиквы", label="Категория B")
    cmp_var = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items()}, value="x-height", label="Величина")
    mo.vstack([mo.Html('<a id="live-compare"></a>'),
               live("Сравните любые две категории", "Та же проверка, что в гипотезе 4.1, но для любой пары категорий и любой "
                    "пропорции: односторонний критерий Манна–Уитни, H₀: у A значения не больше, чем у B.", cmp_a, cmp_b, cmp_var)])
    return cmp_a, cmp_b, cmp_var


@app.cell(hide_code=True)
def _(C1, C2, CAT_RU, FCOLS, cards, cmp_a, cmp_b, cmp_var, fonts, mo, np, plot_html, plt, stats):
    _a = fonts[fonts.category == CAT_RU[cmp_a.value]][cmp_var.value].dropna().to_numpy(float)
    _b = fonts[fonts.category == CAT_RU[cmp_b.value]][cmp_var.value].dropna().to_numpy(float)
    _mw = stats.mannwhitneyu(_a, _b, alternative="greater")
    _f, _ax = plt.subplots(figsize=(8, 3.2))
    _e = np.histogram_bin_edges(np.concatenate([_a, _b]), bins=16)
    _ax.hist(_a, bins=_e, color=C1, alpha=0.5, label=f"{cmp_a.value}: медиана {np.median(_a):.3f}")
    _ax.hist(_b, bins=_e, color=C2, alpha=0.5, label=f"{cmp_b.value}: медиана {np.median(_b):.3f}")
    _ax.set(xlabel=f"{FCOLS[cmp_var.value][0]}, {FCOLS[cmp_var.value][1]}", ylabel="шрифтов")
    _ax.legend()
    mo.vstack([cards([("p Манна–Уитни", f"{_mw.pvalue:.4f}", "< 0.05 — у A больше"),
                      ("P(A > B)", f"{_mw.statistic / (len(_a) * len(_b)):.2f}", "доля пар, где A больше")]), plot_html(_f)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""<a id="live-gen"></a>
### Датчик: случайный шрифт

Датчик выдаёт пропорции «нового» шрифта, распределённые так же, как у 100 шрифтов коллекции.
Схема любого датчика: $U \\sim U(0, 1) \\xrightarrow{\\text{метод}} X \\sim F_{\\text{данных}}$.
Базовый датчик даёт равномерные числа, метод превращает их в нужную величину. Код — пакет `labrng`.""")
    return


@app.cell(hide_code=True)
def _(FCOLS, G, live, mo):
    gen_var = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items() if k in ("x_height", "stem", "contrast", "width_o")},
                             value="толщина штриха", label="Величина")
    gen_method = mo.ui.dropdown(options={v: k for k, v in G.METHOD_RU.items()}, value=G.METHOD_RU["polar"], label="Метод")
    gen_base = mo.ui.dropdown(options={v: k for k, v in G.BASE_RU.items()}, value=G.BASE_RU["pcg64"], label="Базовый датчик")
    gen_family = mo.ui.dropdown(options={"логнормальное": "lognorm", "скошенное нормальное": "skewnorm", "нормальное": "norm"},
                                value="логнормальное", label="Модель (для методов через модель)")
    gen_n = mo.ui.slider(start=100, stop=10000, step=100, value=1000, label="Сколько значений", show_value=True)
    gen_seed = mo.ui.number(start=0, stop=10**6, value=2026, label="seed")
    live("Датчик вживую", "Меняйте величину, метод, базовый датчик и модель. Справа — тройки чисел базового датчика: "
         "у RANDU они ложатся на прямую.", gen_var, gen_method, gen_base, gen_family, gen_n, gen_seed)
    return gen_base, gen_family, gen_method, gen_n, gen_seed, gen_var


@app.cell(hide_code=True)
def _(C1, C2, FCOLS, G, cards, fonts, gen_base, gen_family, gen_method, gen_n, gen_seed, gen_var, mo, np, plot_html, plt):
    _real = fonts[gen_var.value].dropna().to_numpy(float)
    _x, _info = G.generate(_real, gen_n.value, method=gen_method.value, family=gen_family.value, base=gen_base.value,
                           seed=int(gen_seed.value or 0), step=0.0)
    _c = G.compare(_real, _x)
    _u = G.Uniform(gen_base.value, int(gen_seed.value or 0))(3002)
    _f, _ax = plt.subplots(1, 2, figsize=(9.5, 3.6), gridspec_kw={"width_ratios": [2.2, 1]})
    _lo, _hi = np.quantile(np.concatenate([_real, _x]), [0.005, 0.995])
    _e = np.linspace(_lo, _hi, 26)
    _ax[0].hist(_real, bins=_e, density=True, color=C1, alpha=0.35, label="шрифты")
    _ax[0].hist(_x, bins=_e, density=True, histtype="step", color=C2, linewidth=1.8, label="датчик")
    _ax[0].set(xlabel=f"{FCOLS[gen_var.value][0]}, {FCOLS[gen_var.value][1]}", ylabel="плотность", title=G.METHOD_RU[gen_method.value])
    _ax[0].legend()
    _ax[1].plot((6 * _u[1:-1] - 9 * _u[:-2]) % 1.0, _u[2:], ".", ms=1.5, color=C2 if gen_base.value == "randu" else C1)
    _ax[1].set(aspect="equal", xlim=(0, 1), ylim=(0, 1), title="Тройки базового датчика")
    _f.tight_layout()
    mo.vstack([cards([("среднее", f"{_c['gen']['среднее']:.3f}", f"шрифты {_c['real']['среднее']:.3f}"),
                      ("СКО", f"{_c['gen']['СКО']:.3f}", f"шрифты {_c['real']['СКО']:.3f}"),
                      ("КС p", f"{_c['ks_p']:.3f}", "> 0.05 — не отличается"),
                      ("принято точек", f"{_info['accept']:.3f}", "1 — без отбора")]), plot_html(_f)])
    return


@app.cell(hide_code=True)
def _(G, fonts, gen_base, gen_family, gen_n, gen_seed, gen_var, mo, pd, time_mod):
    _real = fonts[gen_var.value].dropna().to_numpy(float)
    _rows = []
    for _m in G.METHODS:
        _t = time_mod.perf_counter()
        _x, _i = G.generate(_real, gen_n.value, method=_m, family=gen_family.value, base=gen_base.value,
                            seed=int(gen_seed.value or 0), step=0.0)
        _dt = (time_mod.perf_counter() - _t) * 1000
        _c = G.compare(_real, _x)
        _rows.append({"метод": G.METHOD_RU[_m], "Δ среднего": _c["gen"]["среднее"] - _c["real"]["среднее"],
                      "Δ СКО": _c["gen"]["СКО"] - _c["real"]["СКО"], "КС p": _c["ks_p"], "доля принятых": _i["accept"], "время, мс": _dt})
    mo.vstack([mo.md("**Все шесть методов на выбранной величине**"),
               mo.ui.table(pd.DataFrame(_rows).round(4), selection=None, pagination=False)])
    return


@app.cell(hide_code=True)
def _():
    import time as time_mod
    return (time_mod,)


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"resume\"></a>\n## 5. Resume\n\n<a id=\"res-metrics\"></a>\n### 5.1 Итоговые метрики"),
        table_html("<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>N</th>\n      <th>среднее</th>\n      <th>СКО</th>\n      <th>медиана</th>\n      <th>асимметрия</th>\n      <th>эксцесс</th>\n      <th>R² по остальным</th>\n      <th>лучшая по AIC</th>\n    </tr>\n    <tr>\n      <th>величина</th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>x-height</th>\n      <td>100</td>\n      <td>0.4807</td>\n      <td>0.0663</td>\n      <td>0.4985</td>\n      <td>-1.6591</td>\n      <td>5.5849</td>\n      <td>0.6711</td>\n      <td>weibull_min</td>\n    </tr>\n    <tr>\n      <th>толщина штриха</th>\n      <td>100</td>\n      <td>0.0915</td>\n      <td>0.0487</td>\n      <td>0.0840</td>\n      <td>4.2790</td>\n      <td>24.7997</td>\n      <td>0.5391</td>\n      <td>lognorm</td>\n    </tr>\n  </tbody>\n</table>\n</div>"),
        code_block("rows = []\nfor col, nm in [(\"x_height\", \"x-height\"), (\"stem\", \"толщина штриха\")]:\n    v = fonts[col]\n    rows.append({\"величина\": nm, \"N\": len(v), \"среднее\": v.mean(), \"СКО\": v.std(), \"медиана\": v.median(),\n                 \"асимметрия\": stats.skew(v), \"эксцесс\": stats.kurtosis(v),\n                 \"R² по остальным\": stochastic.cv_r2_linear(full[[c for c in OTHERS + [\"x_height\", \"stem\"] if c != col]].to_numpy(), full[col].to_numpy(), k=5, seed=SEED)[\"r2_cv\"],\n                 \"лучшая по AIC\": dist.fit_candidates(v.to_numpy()).index[0]})\npd.DataFrame(rows).set_index(\"величина\").round(4)"),
    ], gap=0.6)
    return


@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, table_html):
    mo.vstack([
        mo.md("<a id=\"res-concl\"></a>\n### 5.2 Выводы\n\n1. x-height и толщина штриха — случайные величины: их выбирает автор шрифта, и заранее, до измерения,\n   их не узнать. По категории и другим размерам их можно угадать только примерно ($R^2 = 0.67$ и $0.54$).\n2. Распределения несимметричные. У x-height больше всего шрифтов около 0.5 и длинный хвост влево; лучше подходят\n   Вейбулла и скошенное нормальное. У толщины штриха больше всего шрифтов около 0.08–0.09 и длинный хвост вправо\n   из-за жирных акцидентных шрифтов; лучше подходит логнормальное. Нормальное распределение отвергается для обеих величин.\n3. Между x-height и толщиной штриха есть связь средней силы (ρ = 0.40, $p = 0.0005$): они соразмерны, иначе текст\n   перестанет быть читаемым. Связь есть во всех категориях, кроме акцидентных, которые делают для акцента, а не для чтения.\n4. Гипотеза подтвердилась: у гротесков x-height больше, чем у антикв (медианы 0.521 и 0.460, $p = 0.0002$).\n5. Ограничения: 33 шрифта из 100 я выбрала сама, потому что они мне понравились, остальные 67 отобраны случайно.\n   Кроме того, все шрифты взяты с Google Fonts, а в каждой категории их всего по 20. Поэтому выводы относятся\n   к этой коллекции и могут не совпасть для всех шрифтов вообще.\n\n<a id=\"res-lit\"></a>\n### 5.3 Литература\n\n1. Брингхерст Р. Основы стиля в типографике. М.: Д. Аронов, 2006 (Bringhurst R. The Elements of Typographic Style).\n2. Королькова А. Живая типографика. М.: IndexMarket, 2007.\n3. Microsoft. OpenType specification: таблицы `head` (unitsPerEm), `OS/2` (sxHeight, usWeightClass), `hmtx`, `fvar`.\n4. fontTools: библиотека для работы со шрифтами на Python. github.com/fonttools/fonttools.\n5. Google Fonts: каталог шрифтов с открытой лицензией (SIL OFL). fonts.google.com.\n\nДатчик случайных чисел (сайт и `datchik.py`):\n\n6. Соболь И. М. Численные методы Монте-Карло. — М. : Наука, 1973. Гл. 2: с. 44–48 (метод обратных функций),\n   с. 62–63 (полярные координаты), с. 74–76 (методы отбора).\n7. Ермаков С. М. Метод Монте-Карло в вычислительной математике : вводный курс. — М. : БИНОМ ; СПб. : Невский\n   диалект, 2009. — 192 с. — ISBN 978-5-7940-0140-2. *(найдено в каталоге РГБ)*\n8. Савелова Т. И. Метод Монте-Карло : учебное пособие. — М. : НИЯУ МИФИ, 2011. — 150 с. —\n   ISBN 978-5-7262-1546-4. Гл. 2 «Статистическое моделирование случайных величин», с. 58. *(найдено в каталоге РГБ)*\n\n9. Феличи Дж. Типографика: шрифт, верстка, дизайн / пер. с англ. С. И. Пономаренко. — 2-е изд., перераб. и доп. —\n   СПб. : БХВ-Петербург, 2014. — 496 с. — ISBN 978-5-9775-0908-4. С. 49 (рост строчных знаков, x-height),\n   с. 61 (насыщенность и толщина основных штрихов), с. 188–189 (влияние роста строчных на кажущийся размер шрифта).\n10. Гордон Ю. Книга про буквы от Аа до Яя. — М. : Издательство Студии Артемия Лебедева, 2006. — 384 с. —\n   ISBN 5-98062-006-0. С. 36–37 (шрифтовая терминология), с. 38 (оптические иллюзии и компенсация толщины штрихов).\n\n<a id=\"res-marks\"></a>\n### 5.4 cat_mark_table\n\n| cat_id | notebook_link | coeff | comment |\n|--------|---------------|-------|---------|\n| КТвД: доп. датасет | [1](#ds) | | собственный датасет, собран и измерен своим скриптом |\n| КТвД: случайная величина | [2.1](#rv1-desc), [3.1](#rv2-desc) | | $R^2$ по остальным измерениям и остаток против точности |\n| КТвД: (не)зависимость | [4](#dep) | | корреляции, $\\chi^2$, перестановочный тест, проверка внутри категорий |\n| КТвД: EDA | [1.2](#ds-eda), [2.2](#rv1-eda), [3.2](#rv2-eda) | | описательные статистики, категории, подбор семейств |\n| КТвД: гипотеза | [4.1](#hyp) | | гротески против антикв, Манн–Уитни |\n| КТвД: оформление | [содержание](#toc) | | нумерация, якоря, скрытый код, подписи рисунков, LaTeX |"),
    ], gap=0.6)
    return


if __name__ == "__main__":
    app.run()
