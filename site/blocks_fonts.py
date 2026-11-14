"""Приложение «Шрифты» (доп. задание КТвД): настройка, обложка и живые блоки в стиле сайта шрифтов."""
import json

import blocks_common as C

THEME = dict(head_font='"Roboto Flex", "Golos Text", sans-serif', bg="#fafaf7", card="#ffffff", ink="#1a1d24", ink2="#5c6170", line="#e6e5e0", acc="#2a78d6",
             acc2="#a9c8ef", soft="#f1f0eb", grid="#e6e5e0", c1="#2a78d6", c2="#eb6834", c3="#1baf7a",
             cover="radial-gradient(120% 140% at 100% 0%,#2a78d6 0%,#1a1d24 55%)", cover_ink="#fafaf7")


CSS_FILE = "fonts.css"


def header(title):
    return C.header(title, CSS_FILE)


SETUP = '''@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = ''' + json.dumps(THEME) + '''
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

    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (C1, C2, C3, CAT, CAT_RU, FAMS, FCOLS, FRU, G, T, describe_cards, fit_view, fonts, scatter_view,
            Path, PUB, base64, cards, code_block, df_html, fig, section, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, stats, table_html, types)
'''


def cover(head_md: str) -> str:
    html = C.css(THEME) + '''
<div class="lab-cover">
  <div class="kicker">Lab01 · команда 27 · доп. задание КТвД · Быкова Кристина Денисовна</div>
  <h1>Шрифт как случайная величина</h1>
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
  <li><b>Живые блоки</b> с синей полоской: фильтры по категориям, подбор моделей, датчик. Всё считается в браузере.</li>
  <li>Живая витрина шрифтов с ползунками толщины: <a href="../" target="_top">сайт про шрифты</a>.</li>
  <li><a href="../../" target="_top">← Lab01: обе части работы</a> · <a href="../../wine/" target="_top">основная работа (вино)</a></li>
</ul></div>'''
    return f'''@app.cell(hide_code=True)
def _(mo):
    mo.vstack([mo.Html({json.dumps(html, ensure_ascii=False)}), mo.md({json.dumps(head_md.strip(), ensure_ascii=False)})])
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
def _(CAT, FCOLS, live, mo):
    coll_cats = mo.ui.multiselect(options=[v[0] for v in CAT.values()], value=[v[0] for v in CAT.values()], label="Категории")
    coll_x = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items()}, value="x-height", label="По горизонтали")
    coll_y = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items()}, value="толщина штриха", label="По вертикали")
    coll_names = mo.ui.switch(value=False, label="подписать шрифты")
    mo.vstack([mo.Html('<a id="live-collection"></a>'),
               live("Коллекция по категориям", "Выберите категории и любые две пропорции: точки — шрифты. "
                    "Подписи помогают найти выбросы — например, самые жирные акцидентные.", coll_cats, coll_x, coll_y, coll_names)])
    return coll_cats, coll_names, coll_x, coll_y
''', '''
@app.cell(hide_code=True)
def _(CAT_RU, FCOLS, coll_cats, coll_names, coll_x, coll_y, describe_cards, fonts, mo, scatter_view):
    _d = fonts[fonts.category.isin([CAT_RU[c] for c in coll_cats.value])]
    _x = _d[coll_x.value].dropna().to_numpy(float)
    mo.vstack([describe_cards(_x, FCOLS[coll_x.value][1]) if len(_x) else mo.md("_Выберите хотя бы одну категорию._"),
               scatter_view(_d, coll_x.value, coll_y.value, coll_cats.value, coll_names.value)])
    return
''')


def fit_block(sfx, col, default):
    ui = f'''
@app.cell(hide_code=True)
def _(FAMS, live, mo):
    fit_fams_{sfx} = mo.ui.multiselect(options=list(FAMS), value={json.dumps(default, ensure_ascii=False)}, label="Модели")
    fit_bins_{sfx} = mo.ui.slider(start=8, stop=40, step=2, value=20, label="Столбики", show_value=True)
    mo.vstack([mo.Html('<a id="live-fit-{sfx}"></a>'),
               live("Подбор распределения вживую", "Включайте модели и меняйте число столбиков: на графике плотности моделей, "
                    "в таблице AIC (меньше — лучше) и расстояние Колмогорова D.", fit_fams_{sfx}, fit_bins_{sfx})])
    return fit_bins_{sfx}, fit_fams_{sfx}
'''
    view = f'''
@app.cell(hide_code=True)
def _(df_html, FCOLS, fit_bins_{sfx}, fit_fams_{sfx}, fit_view, fonts, mo):
    _label, _unit = FCOLS[{json.dumps(col)}]
    _img, _tab = fit_view(fonts[{json.dumps(col)}].dropna().to_numpy(float), fit_fams_{sfx}.value, fit_bins_{sfx}.value, _label, _unit, {json.dumps(sfx)})
    mo.vstack([_img, df_html(_tab) if len(_tab) else mo.md("_Выберите хотя бы одну модель._")])
    return
'''
    return _cells(ui, view)


WITHIN = _cells('''
@app.cell(hide_code=True)
def _(CAT, live, mo):
    within_cat = mo.ui.dropdown(options=["все шрифты"] + [v[0] for v in CAT.values()], value="все шрифты", label="Категория")
    mo.vstack([mo.Html('<a id="live-within"></a>'),
               live("Связь x-height и толщины внутри категории", "Общая связь может возникнуть просто из-за смеси категорий. "
                    "Проверьте каждую категорию отдельно: у акцидентных связи почти нет.", within_cat)])
    return (within_cat,)
''', '''
@app.cell(hide_code=True)
def _(CAT, CAT_RU, cards, fonts, mo, scatter_view, stats, within_cat):
    _all = within_cat.value == "все шрифты"
    _d = fonts if _all else fonts[fonts.category == CAT_RU[within_cat.value]]
    _rho, _p = stats.spearmanr(_d.x_height, _d.stem)
    mo.vstack([cards([("ρ Спирмена", f"{_rho:+.2f}", "сила и направление связи"), ("p", f"{_p:.4f}", "< 0.05 — связь есть"),
                      ("шрифтов", f"{len(_d)}", within_cat.value)]),
               scatter_view(_d, "x_height", "stem", [v[0] for v in CAT.values()] if _all else [within_cat.value], not _all)])
    return
''')

COMPARE = _cells('''
@app.cell(hide_code=True)
def _(CAT, FCOLS, live, mo):
    cmp_a = mo.ui.dropdown(options=[v[0] for v in CAT.values()], value="гротески", label="Категория A")
    cmp_b = mo.ui.dropdown(options=[v[0] for v in CAT.values()], value="антиквы", label="Категория B")
    cmp_var = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items()}, value="x-height", label="Величина")
    mo.vstack([mo.Html('<a id="live-compare"></a>'),
               live("Сравните любые две категории", "Та же проверка, что в гипотезе 4.1, но для любой пары категорий и любой "
                    "пропорции: односторонний критерий Манна–Уитни, H₀: у A значения не больше, чем у B.", cmp_a, cmp_b, cmp_var)])
    return cmp_a, cmp_b, cmp_var
''', '''
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
''')

GEN = _cells('''
@app.cell(hide_code=True)
def _(mo):
    mo.md("""<a id="live-gen"></a>
### Датчик: случайный шрифт

Датчик выдаёт пропорции «нового» шрифта, распределённые так же, как у 100 шрифтов коллекции.
Схема любого датчика: $U \\\\sim U(0, 1) \\\\xrightarrow{\\\\text{метод}} X \\\\sim F_{\\\\text{данных}}$.
Базовый датчик даёт равномерные числа, метод превращает их в нужную величину. Код — пакет `labrng`.""")
    return
''', '''
@app.cell(hide_code=True)
def _(FCOLS, G, live, mo):
    gen_var = mo.ui.dropdown(options={v[0]: k for k, v in FCOLS.items() if k in ("x_height", "stem", "contrast", "width_o")},
                             value="толщина штриха", label="Величина")
    gen_method = mo.ui.dropdown(options={v: k for k, v in G.METHOD_RU.items()}, value=G.METHOD_RU["quantile"], label="Метод")
    gen_base = mo.ui.dropdown(options={v: k for k, v in G.BASE_RU.items()}, value=G.BASE_RU["pcg64"], label="Базовый датчик")
    gen_family = mo.ui.dropdown(options={"логнормальное": "lognorm", "скошенное нормальное": "skewnorm", "нормальное": "norm"},
                                value="логнормальное", label="Модель (для методов через модель)")
    gen_n = mo.ui.slider(start=100, stop=10000, step=100, value=1000, label="Сколько значений", show_value=True)
    gen_seed = mo.ui.number(start=0, stop=10**6, value=2026, label="seed")
    live("Датчик вживую", "Меняйте величину, метод, базовый датчик и модель. Справа — тройки чисел базового датчика: "
         "у RANDU они ложатся на прямую.", gen_var, gen_method, gen_base, gen_family, gen_n, gen_seed)
    return gen_base, gen_family, gen_method, gen_n, gen_seed, gen_var
''', '''
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
''', '''
@app.cell(hide_code=True)
def _(df_html, fonts, G, gen_base, gen_family, gen_n, gen_seed, gen_var, mo, pd, time_mod):
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
