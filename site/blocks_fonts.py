"""Приложение «Шрифты» (доп. задание КТвД): настройка, обложка и живые блоки в стиле сайта шрифтов."""
import json

from pathlib import Path

import blocks_common as C

_W = Path(__file__).resolve().parent / "widgets"
_SJ = (_W / "scatter.js").read_text(encoding="utf-8")
_PJ = (_W / "controls.js").read_text(encoding="utf-8")
_PC = (_W / "controls.css").read_text(encoding="utf-8")
PANEL_CODE = ("    _PJ = " + json.dumps(_PJ, ensure_ascii=False) + "\n    _PC = " + json.dumps(_PC, ensure_ascii=False) + "\n" + r'''    try:
        import anywidget as _aw
        import traitlets as _tl

        class _Panel(_aw.AnyWidget):
            _esm = _PJ
            _css = _PC
            spec = _tl.List([]).tag(sync=True)
            values = _tl.Dict({}).tag(sync=True)

        _HAS_PANEL = True
    except Exception:
        _HAS_PANEL = False

    def panel(spec, values):
        """Элементы управления в стиле сайта про шрифты; без anywidget те же поля на стандартных элементах marimo."""
        if _HAS_PANEL:
            return mo.ui.anywidget(_Panel(spec=spec, values=values))
        els = {}
        for c in spec:
            n, t = c.get("name"), c["type"]
            if t == "seg" and not c.get("sets"):
                els[n] = mo.ui.radio(options={o[0]: o[1] for o in c["options"]},
                                     value=[o[0] for o in c["options"] if o[1] == values[n]][0], label=c.get("label", ""), inline=True)
            elif t == "chips":
                els[n] = mo.ui.multiselect(options={o[0]: o[1] for o in c["options"]},
                                           value=[o[0] for o in c["options"] if o[1] in values[n]], label=c.get("label", ""))
            elif t == "select":
                opts = [o for g in c["groups"] for o in g[1]] if c.get("groups") else c["options"]
                els[n] = mo.ui.dropdown(options={o[0]: o[1] for o in opts},
                                        value=[o[0] for o in opts if o[1] == values[n]][0], label=c.get("label", ""))
            elif t == "range":
                els[n] = mo.ui.slider(start=c["min"], stop=c["max"], step=c.get("step", 1), value=values[n], label=c["label"], show_value=True)
            elif t == "text":
                els[n] = mo.ui.text(value=values.get(n, ""), label=c.get("label", ""))
            elif t == "button":
                els[n] = mo.ui.button(value=0, on_click=lambda v: v + 1, label=c["label"])
        return mo.ui.dictionary(els)

    def vals(p):
        v = p.value
        return v.get("values", v) if isinstance(v, dict) else {}
''')
_SC = (_W / "scatter.css").read_text(encoding="utf-8")
SCATTER_CODE = (
    "    # график с приближением (anywidget); без anywidget остаётся картинка matplotlib\n"
    "    _SJ = " + json.dumps(_SJ, ensure_ascii=False) + "\n"
    "    _SC = " + json.dumps(_SC, ensure_ascii=False) + "\n" + r'''
    try:
        import anywidget
        import traitlets

        class _Scatter(anywidget.AnyWidget):
            _esm = _SJ
            _css = _SC
            points = traitlets.List([]).tag(sync=True)
            cats = traitlets.Dict({}).tag(sync=True)
            selected = traitlets.Unicode("").tag(sync=True)
            xlabel = traitlets.Unicode("").tag(sync=True)
            ylabel = traitlets.Unicode("").tag(sync=True)
            xname = traitlets.Unicode("").tag(sync=True)
            yname = traitlets.Unicode("").tag(sync=True)
            labels = traitlets.Bool(False).tag(sync=True)
            pickable = traitlets.Bool(False).tag(sync=True)

        HAS_AW = True
    except Exception:
        HAS_AW = False

    def zoom_scatter(df, xcol, ycol, cats, label_points):
        """Точечный график с приближением: кнопки + / −, двойной щелчок, перетаскивание, подсказки."""
        if not HAS_AW:
            return scatter_view(df, xcol, ycol, cats, label_points)
        d = df[df.category.isin([CAT_RU[c] for c in cats])].dropna(subset=[xcol, ycol])
        pts = [{"f": r.family, "c": r.category, "x": round(float(getattr(r, xcol)), 4), "s": round(float(getattr(r, ycol)), 4)}
               for r in d.itertuples()]
        if not pts:
            return mo.md("_Выберите хотя бы одну категорию._")
        return mo.ui.anywidget(_Scatter(points=pts, cats={k: list(v) for k, v in CAT.items()},
                                        xlabel=f"{FCOLS[xcol][0]}, {FCOLS[xcol][1]}", ylabel=f"{FCOLS[ycol][0]}, {FCOLS[ycol][1]}",
                                        xname=FCOLS[xcol][0], yname=FCOLS[ycol][0], labels=bool(label_points), pickable=False))
''')

THEME = dict(head_font="Unbounded, Onest, sans-serif", bg="#f6f7f5", card="#ffffff", ink="#1a1d24", ink2="#5c6170", line="#dcdfd8",
             acc="#2a78d6", acc2="#a9c8ef", soft="#ffffff", grid="#e6e5e0", c1="#2a78d6", c2="#eb6834", c3="#1baf7a",
             cover="transparent", cover_ink="#1a1d24",
             section_style={"border-top": "1px solid #dcdfd8", "padding": "2rem 0 1.2rem"},
             live_style={"background": "#ffffff", "border-radius": "10px", "padding": "1rem 1.2rem 1.1rem"},
             extra_css='\n/* стиль сайта про шрифты: светлая бумага, Onest, Unbounded, Roboto Flex, синий акцент, разделы через линию */\nbody, .markdown, .prose {{ color: #1a1d24; }}\n.markdown h1, .markdown h2, .markdown h3 {{ font-family: Unbounded, Onest, sans-serif !important; }}\n.markdown h1 {{ font-size: clamp(1.7rem, 3.4vw, 2.4rem) !important; font-weight: 600 !important; line-height: 1.12 !important; }}\n.markdown h2 {{ font-size: clamp(1.5rem, 3vw, 2.1rem) !important; font-weight: 600 !important; line-height: 1.15 !important; }}\n.markdown h3 {{ font-size: 1.1rem !important; font-weight: 550 !important; border-left: 0 !important; padding-left: 0 !important; }}\n.markdown h4 {{ font-family: Onest, sans-serif !important; font-size: 1rem !important; color: #5c6170 !important; }}\n.markdown a {{ color: #2a78d6; text-underline-offset: .18em; }}\n.markdown table th {{ color: #5c6170; font-weight: 600; }}\n.markdown table td, .markdown table th {{ border-bottom: 1px solid #dcdfd8; }}\n.lab-cover {{ background: transparent !important; color: #1a1d24 !important; border-radius: 0 !important; padding: 1.2rem 0 1.6rem !important; }}\n.lab-cover .kicker {{ color: #2a78d6; opacity: 1 !important; }}\n.lab-cover h1 {{ font-family: "Roboto Flex", Onest, sans-serif; font-size: clamp(2.8rem, 8vw, 6.4rem) !important; line-height: .98 !important;\n                letter-spacing: -.02em; font-weight: 400; margin: .5rem 0 1.4rem !important; max-width: none !important; }}\n.lab-cover h1 .w {{ display: block; }}\n.lab-cover p {{ color: #5c6170; opacity: 1 !important; font-size: clamp(1.05rem, 1.5vw, 1.25rem); line-height: 1.6; max-width: 68ch !important; }}\n.lab-stats {{ gap: 1.4rem 2.6rem !important; }}\n.lab-stats div b {{ font-family: Unbounded, Onest, sans-serif; font-size: 2.3rem !important; font-weight: 600 !important; }}\n.lab-stats div span {{ color: #5c6170; opacity: 1 !important; font-size: .92rem !important; }}\n.lab-guide {{ background: #ffffff !important; border: 0 !important; border-radius: 8px !important; }}\n.lab-guide h4 {{ font-family: Unbounded, Onest, sans-serif; font-size: .95rem; font-weight: 550; }}\n.lab-guide a {{ color: #2a78d6; }}\n.lab-fig {{ background: #ffffff !important; border: 0 !important; border-radius: 8px !important; padding: .6rem !important; }}\n.lab-fig.live {{ border: 0 !important; }}\n.lab-cards {{ gap: 1.2rem 2rem !important; margin: .8rem 0 !important; }}\n.lab-card {{ background: transparent !important; border: 0 !important; border-radius: 0 !important; padding: 0 !important; }}\n.lab-card span {{ text-transform: none !important; letter-spacing: 0 !important; font-size: .9rem !important; color: #5c6170 !important; order: 2; }}\n.lab-card b {{ font-family: Unbounded, Onest, sans-serif; font-size: 2rem !important; font-weight: 600; order: 1; }}\n.lab-card small {{ order: 3; }}\n.lab-live .tag {{ background: #2a78d6 !important; }}\n.lab-live h4 {{ font-family: Unbounded, Onest, sans-serif; font-size: 1.05rem !important; font-weight: 550; }}\n.lab-tbl table {{ background: transparent !important; border: 0 !important; }}\n.lab-tbl th {{ background: transparent !important; color: #5c6170 !important; }}\n.lab-tbl th, .lab-tbl td {{ border-bottom: 1px solid #dcdfd8 !important; }}\n.lab-out {{ background: #ffffff !important; border: 0 !important; border-radius: 8px !important; }}\n')


CSS_FILE = "fonts.css"


def header(title):
    return C.header(title, CSS_FILE).replace('"scipy"]', '"scipy", "anywidget", "traitlets"]')


SETUP = '''@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = ''' + json.dumps(THEME) + '''
    STYLE = ''' + json.dumps(C.css_body(THEME).split("\n", 1)[1], ensure_ascii=False) + '''
    ASSETS = "fonts"
''' + C.HELPERS + r'''
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

''' + SCATTER_CODE + PANEL_CODE + r'''
    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (C1, C2, C3, CAT, CAT_RU, FAMS, FCOLS, FRU, G, T, describe_cards, fit_view, fonts, panel, scatter_view, vals, zoom_scatter,
            Path, PUB, base64, cards, code_block, df_html, fig, section, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, stats, table_html, types)
'''


def hero_title() -> str:
    """Заголовок как на сайте про шрифты: у каждой буквы толщина и ширина случайного настоящего шрифта."""
    import numpy as np
    import pandas as pd
    f = pd.read_csv(Path(__file__).resolve().parent.parent / "fonts" / "data" / "fonts.csv")
    f = f[~f["no_lowercase"].astype(str).eq("True")][["stem", "width_o"]].dropna().to_numpy(float)
    rng = np.random.default_rng(27)
    out = []
    for word in ("Шрифт как", "случайная", "величина"):
        letters = []
        for ch in word:
            if ch == " ":
                letters.append(" ")
                continue
            stem, wid = f[rng.integers(len(f))]
            wght = float(np.clip(np.interp(stem, [0.02, 0.09, 0.22], [100, 400, 1000]), 100, 1000))
            wdth = float(np.clip(np.interp(wid, [0.75, 1.0, 1.25], [62, 100, 140]), 25, 151))
            letters.append(f'<span style="font-variation-settings:&#39;wght&#39; {wght:.0f},&#39;wdth&#39; {wdth:.0f}">{ch}</span>')
        out.append('<span class="w">' + "".join(letters) + "</span>")
    return "".join(out)


def cover(head_md: str) -> str:
    html = C.css(THEME) + '''
<div class="lab-cover">
  <div class="kicker">Lab01 · команда 27 · доп. задание КТвД · Быкова Кристина Денисовна</div>
  <h1 aria-label="Шрифт как случайная величина">''' + hero_title() + '''</h1>
  <p>Собственный датасет: 100 семейств Google Fonts, по 20 в каждой категории. Две случайные величины одной природы,
  высота строчных (x-height) и толщина основного штриха, измерены по контурам букв. Случайность, распределения,
  зависимость, гипотеза про гротески и датчик, который выдаёт пропорции «нового» шрифта.</p>
  <div class="lab-stats">
    <div><b>100</b><span>шрифтов</span></div><div><b>5</b><span>категорий</span></div>
    <div><b>2</b><span>случайные величины</span></div><div><b>6</b><span>методов датчика</span></div>
    <div><b>6</b><span>живых блоков</span></div>
  </div>
</div>
<div class="lab-guide"><h4>Как читать отчёт</h4><ul>
  <li><b>☰ Содержание</b> в панели слева (на телефоне кнопка вверху): переход к любому разделу.</li>
  <li><b>«Код этого раздела»</b> под каждым разделом: код, которым посчитаны таблицы и рисунки.</li>
  <li><b>Живые блоки</b> на белых панелях: фильтры по категориям, подбор моделей, датчик. Всё считается в браузере.</li>
  <li>Живая витрина шрифтов с ползунками толщины: <a href="../" target="_top">сайт про шрифты</a>.</li>
  <li><a href="../../" target="_top">← Lab01: обе части работы</a> · <a href="../../wine/" target="_top">основная работа (вино)</a></li>
</ul></div>'''
    return f'''@app.cell(hide_code=True)
def _(mo):
    mo.vstack([mo.Html({C.pystr(html)}), mo.md({C.pystr(head_md.strip())})])
    return
'''


EXTRA_TOC = """**Живые блоки**

- [Коллекция по категориям](#live-collection)
- [Подбор распределения: x-height](#live-fit-xh)
- [Подбор распределения: толщина штриха](#live-fit-stem)
- [Связь внутри категорий](#live-within)
- [Сравнение двух категорий](#live-compare)
- [Датчик: случайный шрифт](#live-gen)
"""


def _cells(*parts):
    return [p.strip("\n") + "\n" for p in parts]



COLLECTION = _cells('''
@app.cell(hide_code=True)
def _(CAT, FCOLS, live, mo, panel):
    coll = panel([{"type": "chips", "name": "cats", "label": "Категории", "options": [[v[0], v[0], v[1]] for v in CAT.values()]},
                  {"type": "select", "name": "x", "label": "По горизонтали", "options": [[v[0], k] for k, v in FCOLS.items()]},
                  {"type": "select", "name": "y", "label": "По вертикали", "options": [[v[0], k] for k, v in FCOLS.items()]},
                  {"type": "seg", "name": "names", "label": "Подписи", "options": [["без подписей", False], ["подписать шрифты", True]]}],
                 {"cats": [v[0] for v in CAT.values()], "x": "x_height", "y": "stem", "names": False})
    mo.vstack([mo.Html('<a id="live-collection"></a>'),
               live("Коллекция по категориям", "Выберите категории и любые две пропорции, каждая точка это шрифт. "
                    "График приближается кнопками «+ / −» и двойным щелчком, подписи помогают найти выбросы, например самые жирные акцидентные.", coll)])
    return (coll,)
''', '''
@app.cell(hide_code=True)
def _(CAT_RU, FCOLS, coll, describe_cards, fonts, mo, vals, zoom_scatter):
    _v = vals(coll)
    _d = fonts[fonts.category.isin([CAT_RU[c] for c in _v["cats"]])]
    _x = _d[_v["x"]].dropna().to_numpy(float)
    mo.vstack([describe_cards(_x, FCOLS[_v["x"]][1]) if len(_x) else mo.md("_Выберите хотя бы одну категорию._"),
               zoom_scatter(_d, _v["x"], _v["y"], _v["cats"], _v["names"])])
    return
''')


def fit_block(sfx, col, default):
    ui = f'''
@app.cell(hide_code=True)
def _(FAMS, live, mo, panel):
    fit_{sfx} = panel([{{"type": "chips", "name": "fams", "label": "Модели", "options": [[k, k] for k in FAMS]}},
                       {{"type": "range", "name": "bins", "label": "Столбики", "min": 8, "max": 40, "step": 2}}],
                      {{"fams": {json.dumps(default, ensure_ascii=False)}, "bins": 20}})
    mo.vstack([mo.Html('<a id="live-fit-{sfx}"></a>'),
               live("Подбор распределения вживую", "Включайте модели и меняйте число столбиков: на графике плотности моделей, "
                    "в таблице AIC (чем меньше, тем лучше) и расстояние Колмогорова D.", fit_{sfx})])
    return (fit_{sfx},)
'''
    view = f'''
@app.cell(hide_code=True)
def _(df_html, FCOLS, fit_{sfx}, fit_view, fonts, mo, vals):
    _v = vals(fit_{sfx})
    _label, _unit = FCOLS[{json.dumps(col)}]
    _img, _tab = fit_view(fonts[{json.dumps(col)}].dropna().to_numpy(float), _v["fams"], int(_v["bins"]), _label, _unit, {json.dumps(sfx)})
    mo.vstack([_img, df_html(_tab) if len(_tab) else mo.md("_Выберите хотя бы одну модель._")])
    return
'''
    return _cells(ui, view)


WITHIN = _cells('''
@app.cell(hide_code=True)
def _(CAT, live, mo, panel):
    within = panel([{"type": "seg", "name": "cat", "label": "Категория",
                     "options": [["все шрифты", "все шрифты"]] + [[v[0], v[0]] for v in CAT.values()]}], {"cat": "все шрифты"})
    mo.vstack([mo.Html('<a id="live-within"></a>'),
               live("Связь x-height и толщины внутри категории", "Общая связь может возникнуть просто из-за смеси категорий. "
                    "Проверьте каждую категорию отдельно: у акцидентных связи почти нет.", within)])
    return (within,)
''', '''
@app.cell(hide_code=True)
def _(CAT, CAT_RU, cards, fonts, mo, stats, vals, within, zoom_scatter):
    _c = vals(within)["cat"]
    _all = _c == "все шрифты"
    _d = fonts if _all else fonts[fonts.category == CAT_RU[_c]]
    _rho, _p = stats.spearmanr(_d.x_height, _d.stem)
    mo.vstack([cards([("ρ Спирмена", f"{_rho:+.2f}", "сила и направление связи"), ("p", f"{_p:.4f}", "меньше 0.05: связь есть"),
                      ("шрифтов", f"{len(_d)}", _c)]),
               zoom_scatter(_d, "x_height", "stem", [v[0] for v in CAT.values()] if _all else [_c], not _all)])
    return
''')

COMPARE = _cells('''
@app.cell(hide_code=True)
def _(CAT, FCOLS, live, mo, panel):
    cmp = panel([{"type": "select", "name": "a", "label": "Категория A", "options": [[v[0], v[0]] for v in CAT.values()]},
                 {"type": "select", "name": "b", "label": "Категория B", "options": [[v[0], v[0]] for v in CAT.values()]},
                 {"type": "select", "name": "var", "label": "Величина", "options": [[v[0], k] for k, v in FCOLS.items()]}],
                {"a": "гротески", "b": "антиквы", "var": "x_height"})
    mo.vstack([mo.Html('<a id="live-compare"></a>'),
               live("Сравните любые две категории", "Та же проверка, что в гипотезе 4.1, но для любой пары категорий и любой "
                    "пропорции: односторонний критерий Манна–Уитни, H₀: у A значения не больше, чем у B.", cmp)])
    return (cmp,)
''', '''
@app.cell(hide_code=True)
def _(C1, C2, CAT_RU, FCOLS, cards, cmp, fonts, mo, np, plot_html, plt, stats, vals):
    _v = vals(cmp)
    _a = fonts[fonts.category == CAT_RU[_v["a"]]][_v["var"]].dropna().to_numpy(float)
    _b = fonts[fonts.category == CAT_RU[_v["b"]]][_v["var"]].dropna().to_numpy(float)
    _mw = stats.mannwhitneyu(_a, _b, alternative="greater")
    _f, _ax = plt.subplots(figsize=(8, 3.2))
    _e = np.histogram_bin_edges(np.concatenate([_a, _b]), bins=16)
    _ax.hist(_a, bins=_e, color=C1, alpha=0.5, label=f"{_v['a']}: медиана {np.median(_a):.3f}")
    _ax.hist(_b, bins=_e, color=C2, alpha=0.5, label=f"{_v['b']}: медиана {np.median(_b):.3f}")
    _ax.set(xlabel=f"{FCOLS[_v['var']][0]}, {FCOLS[_v['var']][1]}", ylabel="шрифтов")
    _ax.legend()
    mo.vstack([cards([("p Манна–Уитни", f"{_mw.pvalue:.4f}", "меньше 0.05: у A больше"),
                      ("P(A > B)", f"{_mw.statistic / (len(_a) * len(_b)):.2f}", "доля пар, где A больше")]), plot_html(_f)])
    return
''')

GEN = _cells('''
@app.cell(hide_code=True)
def _(mo):
    mo.md(''' + C.pystr("<a id=\"live-gen\"></a>\n### Датчик: случайный шрифт\n\nДатчик выдаёт пропорции «нового» шрифта, распределённые так же, как у 100 шрифтов коллекции.\nСхема любого датчика: $U \\sim U(0, 1) \\xrightarrow{\\text{метод}} X \\sim F_{\\text{данных}}$.\nБазовый датчик даёт равномерные числа, метод превращает их в нужную величину. Код лежит в пакете `labrng`.") + ''')
    return
''', '''
@app.cell(hide_code=True)
def _(FCOLS, G, live, mo, panel):
    gen_p = panel([{"type": "select", "name": "var", "label": "Величина",
                    "options": [[v[0], k] for k, v in FCOLS.items() if k in ("x_height", "stem", "contrast", "width_o")]},
                   {"type": "select", "name": "method", "label": "Метод", "options": [[v, k] for k, v in G.METHOD_RU.items()]},
                   {"type": "seg", "name": "base", "label": "Базовый датчик", "options": [[v.split(" (")[0], k] for k, v in G.BASE_RU.items()]},
                   {"type": "select", "name": "family", "label": "Модель (для методов через модель)",
                    "options": [["логнормальное", "lognorm"], ["скошенное нормальное", "skewnorm"], ["нормальное", "norm"]]},
                   {"type": "range", "name": "n", "label": "Сколько значений", "min": 100, "max": 10000, "step": 100, "thousands": True},
                   {"type": "button", "name": "go", "label": "Сгенерировать заново"}],
                  {"var": "stem", "method": "quantile", "base": "pcg64", "family": "lognorm", "n": 1000, "go": 0})
    live("Датчик вживую", "Меняйте величину, метод, базовый датчик и модель. Справа тройки чисел базового датчика: "
         "у RANDU они ложатся на прямую.", gen_p)
    return (gen_p,)
''', '''
@app.cell(hide_code=True)
def _(C1, C2, FCOLS, G, cards, fonts, gen_p, mo, np, plot_html, plt, vals):
    _v = vals(gen_p)
    gen_var, gen_method, gen_base, gen_family, gen_n, gen_seed = _v["var"], _v["method"], _v["base"], _v["family"], int(_v["n"]), 2026 + int(_v.get("go", 0))
    _real = fonts[gen_var].dropna().to_numpy(float)
    _x, _info = G.generate(_real, gen_n, method=gen_method, family=gen_family, base=gen_base,
                           seed=gen_seed, step=0.0)
    _c = G.compare(_real, _x)
    _u = G.Uniform(gen_base, gen_seed)(3002)
    _f, _ax = plt.subplots(1, 2, figsize=(9.5, 3.6), gridspec_kw={"width_ratios": [2.2, 1]})
    _lo, _hi = np.quantile(np.concatenate([_real, _x]), [0.005, 0.995])
    _e = np.linspace(_lo, _hi, 26)
    _ax[0].hist(_real, bins=_e, density=True, color=C1, alpha=0.35, label="шрифты")
    _ax[0].hist(_x, bins=_e, density=True, histtype="step", color=C2, linewidth=1.8, label="датчик")
    _ax[0].set(xlabel=f"{FCOLS[gen_var][0]}, {FCOLS[gen_var][1]}", ylabel="плотность", title=G.METHOD_RU[gen_method])
    _ax[0].legend()
    _ax[1].plot((6 * _u[1:-1] - 9 * _u[:-2]) % 1.0, _u[2:], ".", ms=1.5, color=C2 if gen_base == "randu" else C1)
    _ax[1].set(aspect="equal", xlim=(0, 1), ylim=(0, 1), title="Тройки базового датчика")
    _f.tight_layout()
    mo.vstack([cards([("среднее", f"{_c['gen']['среднее']:.3f}", f"шрифты {_c['real']['среднее']:.3f}"),
                      ("СКО", f"{_c['gen']['СКО']:.3f}", f"шрифты {_c['real']['СКО']:.3f}"),
                      ("КС p", f"{_c['ks_p']:.3f}", "больше 0.05: не отличается"),
                      ("принято точек", f"{_info['accept']:.3f}", "1 значит без отбора")]), plot_html(_f)])
    return
''', '''
@app.cell(hide_code=True)
def _(df_html, fonts, G, gen_p, mo, pd, time_mod, vals):
    _v = vals(gen_p)
    gen_var, gen_base, gen_family, gen_n, gen_seed = _v["var"], _v["base"], _v["family"], int(_v["n"]), 2026 + int(_v.get("go", 0))
    _real = fonts[gen_var].dropna().to_numpy(float)
    _rows = []
    for _m in G.METHODS:
        _t = time_mod.perf_counter()
        _x, _i = G.generate(_real, gen_n, method=_m, family=gen_family, base=gen_base,
                            seed=gen_seed, step=0.0)
        _dt = (time_mod.perf_counter() - _t) * 1000
        _c = G.compare(_real, _x)
        _rows.append({"метод": G.METHOD_RU[_m], "Δ среднего": _c["gen"]["среднее"] - _c["real"]["среднее"],
                      "Δ СКО": _c["gen"]["СКО"] - _c["real"]["СКО"], "КС p": _c["ks_p"], "доля принятых": _i["accept"], "время, мс": _dt})
    mo.vstack([mo.md("**Все шесть методов на выбранной величине**"),
               df_html(pd.DataFrame(_rows))])
    return
''', '''
@app.cell(hide_code=True)
def _():
    import time as time_mod
    return (time_mod,)
''')

BLOCKS = {
    "ds-eda": COLLECTION,
    "rv1-eda": fit_block("xh", "x_height", ["нормальное", "скошенное нормальное", "Вейбулла"]),
    "rv2-eda": fit_block("stem", "stem", ["нормальное", "логнормальное", "скошенное нормальное"]),
    "dep": WITHIN,
    "hyp": COMPARE + GEN,
}
