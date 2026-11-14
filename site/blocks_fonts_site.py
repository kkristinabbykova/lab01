"""Сайт про шрифты на marimo: витрина доп. задания КТвД (раньше была страница на HTML + JavaScript).

Разделы: заголовок со случайной толщиной букв, коллекция шрифтов с приближением, «как читать ρ»,
«попробуй сам» (вариативный Roboto Flex), сравнение шрифтов, датчик «новых» шрифтов.
"""
import json

import blocks_common as C
import blocks_fonts as F

CSS_FILE = F.CSS_FILE
TITLE = "Шрифт как случайная величина · Lab01 · КТвД"


def _cell(params, body, returns=""):
    ret = f"    return ({returns},)\n" if returns else "    return\n"
    return f"@app.cell(hide_code=True)\ndef _({params}):\n{body.rstrip()}\n{ret}"


SETUP = '''@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = ''' + json.dumps(F.THEME) + '''
''' + C.HELPERS + r'''
    fonts_all = pd.read_csv(io.StringIO(read_text(PUB / "fonts.csv")))
    fonts = fonts_all[~fonts_all["no_lowercase"].astype(str).eq("True")].copy().reset_index(drop=True)
    CAT = {"sans": ("гротески", "#2a78d6"), "serif": ("антиквы", "#eb6834"), "display": ("акцидентные", "#1baf7a"),
           "handwriting": ("рукописные", "#9b59b6"), "mono": ("моноширинные", "#5c6170")}
    CAT_RU = {v[0]: k for k, v in CAT.items()}
    C1, C2 = T["c1"], T["c2"]

    def gfont(family, text="", wght=400):
        """Подключить шрифт Google Fonts (только нужные буквы, чтобы грузилось быстро)."""
        q = family.replace(" ", "+")
        t = ("&text=" + "".join(sorted(set(text))).replace("&", "")) if text else ""
        return f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={q}{t}&display=swap">'

    def to_wght(stem):
        """Толщина штриха (доли кегля) → ось wght Roboto Flex: 0.09 ≈ Regular 400."""
        return float(np.clip(np.interp(stem, [0.02, 0.09, 0.22], [100, 400, 1000]), 100, 1000))

    def to_ytlc(xh):
        """x-height (доли кегля) → ось YTLC Roboto Flex (высота строчных, 416…570)."""
        return float(np.clip(xh * 1000, 416, 570))

    def flex(text, wght=400, wdth=100, size=64, ytlc=514, color=None):
        return (f'<div style="font-family:\'Roboto Flex\',sans-serif;font-size:{size}px;line-height:1.05;'
                f'font-variation-settings:\'wght\' {wght:.0f},\'wdth\' {wdth:.0f},\'YTLC\' {ytlc:.0f};'
                f'color:{color or T["ink"]};overflow-wrap:anywhere">{text}</div>')

    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (C1, C2, CAT, CAT_RU, G, T, flex, fonts, gfont, to_wght, to_ytlc,
            Path, PUB, base64, cards, code_block, df_html, fig, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, section, stats, table_html, types)
'''

HERO = [
    _cell("mo", '''    reroll = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Перебросить толщину букв")''', "reroll"),
    _cell("T, fonts, mo, np, reroll, to_wght", r'''    _rng = np.random.default_rng(int(reroll.value) + 7)
    _stems = _rng.choice(fonts["stem"].to_numpy(float), size=40)
    _title = "".join(
        f'<span style="font-variation-settings:\'wght\' {to_wght(s):.0f};transition:font-variation-settings .5s">{ch}</span>'
        for ch, s in zip("Шрифт как случайная величина", _stems))
    mo.vstack([mo.Html(f"""
<div class="lab-cover fonts-hero">
  <div class="kicker">Lab01 · команда 27 · доп. задание КТвД · Быкова Кристина Денисовна</div>
  <h1 style="font-family:'Roboto Flex',sans-serif;font-size:clamp(2.4rem,7vw,5rem);line-height:1;margin:.6rem 0 1rem">{_title}</h1>
  <p>Доп. задание КТвД к лабораторной по прикладной статистике. Я собрала датасет шрифтов с Google Fonts
  (в анализе {len(fonts)}: часть выбрана мной, остальные добавлены случайным отбором, по 20 в каждой категории)
  и измерила у каждого две вещи: высоту строчных букв (x-height) и толщину штриха. Эти размеры нельзя вычислить
  по формуле, у каждого шрифта они свои, поэтому их можно изучать как случайные величины.</p>
  <p>Нажми кнопку: толщина каждой буквы в заголовке выпадет случайно, из тех же значений, что у настоящих шрифтов.</p>
  <div class="lab-stats"><div><b>{len(fonts)}</b><span>шрифтов</span></div><div><b>5</b><span>категорий</span></div>
  <div><b>2</b><span>случайные величины</span></div><div><b>6</b><span>методов датчика</span></div></div>
</div>"""), reroll,
        mo.Html('<div class="lab-guide"><h4>Что здесь</h4><ul>'
                '<li><a href="#collection">Шрифты</a>: коллекция, что измерено, как читать ρ.</li>'
                '<li><a href="#play">Попробуй сам</a>: толщина и ширина вариативного шрифта, сравнение шрифтов.</li>'
                '<li><a href="#rng">Датчик</a>: случайные «новые» шрифты, похожие на настоящие.</li>'
                '<li>Полный отчёт с кодом и формулами: <a href="report/" target="_top">отчёт</a> · '
                '<a href="../" target="_top">← Lab01: обе части работы</a>.</li></ul></div>')], gap=0.8)'''),
]

COLLECTION = [
    _cell("CAT, fonts, mo, np, section, stats", r'''    _rho = stats.spearmanr(fonts.x_height, fonts.stem)[0]
    _med = fonts.groupby("category").x_height.median()
    section(
        mo.md("""<a id="collection"></a>
## Шрифты: высота строчных и толщина штриха

Датасет собран самостоятельно: шрифтовые семейства из Google Fonts, по 20 гротесков, антикв, акцидентных,
рукописных и моноширинных. У каждого измерено начертание Regular прямо по контурам букв. Все размеры даны в долях
кегля, то есть не зависят от размера, которым набран текст."""),
        mo.Html('<figure class="lab-fig"><img src="public/fonts_measure.png" alt="Буквы H x l n o с линиями измерений">'
                '<figcaption style="font-size:.85rem;color:#5c6170;padding:.3rem">Что измеряется: x-height (верх строчной «x»), '
                'высота прописных, толщина вертикали «l» и контраст «o».</figcaption></figure>'),
        mo.Html(f"""<div class="lab-cards">
  <div class="lab-card"><span>гротески</span><b>{_med["sans"]:.3f}</b><small>медианная x-height</small></div>
  <div class="lab-card"><span>антиквы</span><b>{_med["serif"]:.3f}</b><small>строчные ниже: Манн–Уитни подтверждает</small></div>
  <div class="lab-card"><span>связь</span><b>ρ = {_rho:.2f}</b><small>чем выше строчные, тем толще штрих</small></div>
</div>"""),
    )'''),
    _cell("CAT, live, mo", r'''    sc_cats = mo.ui.multiselect(options=[v[0] for v in CAT.values()], value=[v[0] for v in CAT.values()], label="Категории")
    sc_x = mo.ui.range_slider(start=0.15, stop=0.65, step=0.01, value=[0.15, 0.65], label="x-height от и до", show_value=True)
    sc_y = mo.ui.range_slider(start=0.0, stop=0.44, step=0.01, value=[0.0, 0.44], label="толщина штриха от и до", show_value=True)
    sc_find = mo.ui.text(placeholder="например, Roboto", label="Найти шрифт")
    live("Коллекция шрифтов с приближением",
         "Сузьте диапазоны ползунками, и график приблизится. Когда точек на экране немного, у них появляются названия.",
         sc_cats, sc_x, sc_y, sc_find)''', "sc_cats, sc_find, sc_x, sc_y"),
    _cell("CAT, CAT_RU, T, cards, fonts, mo, plot_html, plt, sc_cats, sc_find, sc_x, sc_y", r'''    _d = fonts[fonts.category.isin([CAT_RU[c] for c in sc_cats.value])]
    _d = _d[_d.x_height.between(*sc_x.value) & _d.stem.between(*sc_y.value)]
    _q = (sc_find.value or "").strip().lower()
    _f, _ax = plt.subplots(figsize=(8.5, 4.8))
    for _k, (_ru, _col) in CAT.items():
        _p = _d[_d.category == _k]
        if len(_p):
            _ax.scatter(_p.x_height, _p.stem, s=46, color=_col, alpha=.85, edgecolor="white", linewidth=.7, label=f"{_ru} ({len(_p)})")
    _lab = len(_d) <= 30
    for _, _r in _d.iterrows():
        _hit = bool(_q) and _q in _r.family.lower()
        if _lab or _hit:
            _ax.annotate(_r.family, (_r.x_height, _r.stem), xytext=(4, 3), textcoords="offset points",
                         fontsize=9 if _hit else 7.5, color=T["c2"] if _hit else T["ink2"], weight="bold" if _hit else "normal")
        if _hit:
            _ax.scatter([_r.x_height], [_r.stem], s=160, facecolor="none", edgecolor=T["c2"], linewidth=2)
    _ax.set(xlim=sc_x.value, ylim=sc_y.value, xlabel="x-height, доли кегля", ylabel="толщина штриха, доли кегля",
            title="Каждая точка — шрифт")
    if len(_d):
        _ax.legend(fontsize=8, ncol=3, loc="upper left")
    mo.vstack([cards([("на графике", f"{len(_d)}", "шрифтов"),
                      ("x-height", f"{_d.x_height.median():.3f}" if len(_d) else "—", "медиана"),
                      ("штрих", f"{_d.stem.median():.3f}" if len(_d) else "—", "медиана")]), plot_html(_f)])'''),
    _cell("live, mo", r'''    rho_s = mo.ui.slider(start=-1, stop=1, step=0.05, value=0.4, label="Сила связи ρ", show_value=True)
    live("Как читать ρ",
         "ρ Спирмена показывает, насколько согласованно растут две величины: 0 значит связи нет, 1 значит чем больше одна, "
         "тем больше другая, без исключений. Слева облако из 100 случайных точек с выбранной силой связи, справа наши шрифты в рангах.",
         rho_s)''', "rho_s"),
    _cell("C1, C2, fonts, mo, np, plot_html, plt, rho_s, stats", r'''    _r = float(rho_s.value)
    _rp = 2 * np.sin(np.pi * _r / 6)          # корреляция Пирсона, при которой ρ Спирмена равна _r
    _z = np.random.default_rng(1).standard_normal((100, 2))
    _y = _rp * _z[:, 0] + np.sqrt(max(1 - _rp ** 2, 0)) * _z[:, 1]
    _f, _ax = plt.subplots(1, 2, figsize=(9, 3.6))
    _ax[0].scatter(stats.rankdata(_z[:, 0]), stats.rankdata(_y), s=14, color=C2, alpha=.8)
    _ax[0].set(title=f"случайное облако, ρ = {stats.spearmanr(_z[:, 0], _y)[0]:.2f}", xlabel="ранг X", ylabel="ранг Y")
    _ax[1].scatter(stats.rankdata(fonts.x_height), stats.rankdata(fonts.stem), s=14, color=C1, alpha=.8)
    _ax[1].set(title=f"наши шрифты, ρ = {stats.spearmanr(fonts.x_height, fonts.stem)[0]:.2f}",
               xlabel="место по x-height", ylabel="место по толщине")
    _f.tight_layout()
    plot_html(_f)'''),
]

PLAY = [
    _cell("mo, section", r'''    section(mo.md("""<a id="play"></a>
## Попробуй сам

### Толщина и ширина

Этот текст набран вариативным шрифтом Roboto Flex: толщину штриха, ширину букв и даже высоту строчных у него можно
менять плавно. Подвигай ползунки и посмотри, как меняется характер текста."""))'''),
    _cell("live, mo", r'''    pl_text = mo.ui.text(value="Шрифт как случайная величина", label="Текст", full_width=True)
    pl_wght = mo.ui.slider(start=100, stop=1000, step=10, value=400, label="Толщина (вес)", show_value=True)
    pl_wdth = mo.ui.slider(start=25, stop=151, step=1, value=100, label="Ширина, %", show_value=True)
    pl_ytlc = mo.ui.slider(start=416, stop=570, step=2, value=514, label="Высота строчных", show_value=True)
    pl_size = mo.ui.slider(start=16, stop=140, step=2, value=72, label="Кегль, px", show_value=True)
    live("Вариативный шрифт", "Все оси меняются плавно, как в настоящем шрифтовом редакторе.",
         pl_text, pl_wght, pl_wdth, pl_ytlc, pl_size)''', "pl_size, pl_text, pl_wdth, pl_wght, pl_ytlc"),
    _cell("T, flex, fonts, mo, np, pl_size, pl_text, pl_wdth, pl_wght, pl_ytlc", r'''    _stem = float(np.interp(pl_wght.value, [100, 400, 1000], [0.02, 0.09, 0.22]))
    _share = float((fonts.stem <= _stem).mean())
    mo.vstack([
        mo.Html(f'<div class="lab-fig" style="padding:1.2rem 1.4rem">{flex(pl_text.value or " ", pl_wght.value, pl_wdth.value, pl_size.value, pl_ytlc.value)}</div>'),
        mo.md(f"При весе {pl_wght.value} толщина штриха примерно **{_stem:.3f}** кегля: тоньше или так же у "
              f"**{_share:.0%}** шрифтов коллекции. Высота строчных {pl_ytlc.value / 1000:.3f} кегля."),
    ])'''),
    _cell("fonts, live, mo", r'''    _names = sorted(fonts.family)
    cmp1 = mo.ui.dropdown(options=_names, value="Roboto" if "Roboto" in _names else _names[0], label="Шрифт 1", searchable=True)
    cmp2 = mo.ui.dropdown(options=_names, value="Playfair Display" if "Playfair Display" in _names else _names[1], label="Шрифт 2", searchable=True)
    cmp3 = mo.ui.dropdown(options=_names, value="Caveat" if "Caveat" in _names else _names[2], label="Шрифт 3", searchable=True)
    cmp_text = mo.ui.text(value="Hxlno шрифт", label="Текст", max_length=40)
    mo.vstack([mo.md("### Сравнение шрифтов"),
               live("Три шрифта одним кеглем", "Сразу видно, у какого шрифта строчные выше и штрих толще. "
                    "Справа наши измерения этого шрифта.", cmp1, cmp2, cmp3, cmp_text)])''', "cmp1, cmp2, cmp3, cmp_text"),
    _cell("CAT, T, cmp1, cmp2, cmp3, cmp_text, fonts, gfont, mo", r'''    _rows = []
    _txt = cmp_text.value or "Hxlno"
    for _name in (cmp1.value, cmp2.value, cmp3.value):
        _r = fonts[fonts.family == _name].iloc[0]
        _ru, _col = CAT[_r.category]
        _rows.append(f"""{gfont(_name, _txt)}
<div style="display:grid;grid-template-columns:1fr 13rem;gap:1rem;align-items:center;border-top:1px solid {T['line']};padding:.7rem 0">
  <div style="font-family:'{_name}',serif;font-size:64px;line-height:1.15;overflow-wrap:anywhere">{_txt}</div>
  <div style="font-size:.85rem;color:{T['ink2']}"><b style="color:{T['ink']};font-size:1rem">{_name}</b><br>
  <span style="color:{_col}">● {_ru}</span><br>x-height {_r.x_height:.3f} · прописные {_r.cap_height:.3f}<br>
  штрих {_r.stem:.3f} · контраст {_r.contrast:.2f}</div></div>""")
    mo.Html('<div class="lab-fig" style="padding:.4rem 1.2rem">' + "".join(_rows) + "</div>")'''),
]

RNG = [
    _cell("mo, section", r'''    section(mo.md(r"""<a id="rng"></a>
## Датчик: случайный шрифт, похожий на настоящий

Датчик случайных чисел выдаёт значения, распределённые так же, как пропорции моих шрифтов. Сначала базовый датчик даёт
равномерное число $U$ от 0 до 1, потом метод превращает его в нужную величину:
$U \sim U(0, 1) \xrightarrow{\text{метод}} X \sim F_{\text{данных}}$.

**Полярный метод Марсальи:** точка бросается в квадрат, остаются только точки внутри круга, и из них получаются
нормальные числа $Z$. Дальше $Z$ переводится в модель: для x-height это скошенное нормальное распределение, для толщины
штриха логнормальное $X = \theta + e^{\mu + \sigma Z}$. **Квантильный метод** модель не использует: он берёт $U$ и
находит значение, ниже которого лежит такая же доля шрифтов."""))'''),
    _cell("G, live, mo", r'''    rg_var = mo.ui.radio(options={"x-height": "x_height", "толщина штриха": "stem"}, value="x-height", label="Величина", inline=True)
    rg_method = mo.ui.dropdown(options={v: k for k, v in G.METHOD_RU.items()}, value=G.METHOD_RU["polar"], label="Метод")
    rg_base = mo.ui.dropdown(options={v: k for k, v in G.BASE_RU.items()}, value=G.BASE_RU["pcg64"], label="Базовый датчик")
    rg_n = mo.ui.slider(start=100, stop=20000, step=100, value=1000, label="Сколько чисел", show_value=True)
    rg_go = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Сгенерировать заново")
    live("Датчик вживую", "Справа точки базового датчика: у RANDU тройки чисел ложатся на прямые, у хороших датчиков облако ровное.",
         rg_var, rg_method, rg_base, rg_n, rg_go)''', "rg_base, rg_go, rg_method, rg_n, rg_var"),
    _cell("C1, C2, G, cards, fonts, mo, np, plot_html, plt, rg_base, rg_go, rg_method, rg_n, rg_var", r'''    _real = fonts[rg_var.value].to_numpy(float)
    _fam = "skewnorm" if rg_var.value == "x_height" else "lognorm"
    _seed = 2026 + int(rg_go.value)
    rg_x, _info = G.generate(_real, rg_n.value, method=rg_method.value, family=_fam, base=rg_base.value, seed=_seed)
    _c = G.compare(_real, rg_x)
    _u = G.Uniform(rg_base.value, _seed)(3002)
    _f, _ax = plt.subplots(1, 2, figsize=(9.5, 3.6), gridspec_kw={"width_ratios": [2.2, 1]})
    _lo, _hi = np.quantile(np.concatenate([_real, rg_x]), [0.005, 0.995])
    _e = np.linspace(_lo, _hi, 28)
    _ax[0].hist(_real, bins=_e, density=True, color="#bcd6f3", label="мои шрифты")
    _ax[0].hist(rg_x, bins=_e, density=True, histtype="step", color=C2, linewidth=1.8, label="датчик")
    _ax[0].set(xlabel=("x-height" if rg_var.value == "x_height" else "толщина штриха") + ", доли кегля", ylabel="плотность",
               title=G.METHOD_RU[rg_method.value])
    _ax[0].legend()
    _ax[1].plot((6 * _u[1:-1] - 9 * _u[:-2]) % 1.0, _u[2:], ".", ms=1.5, color=C2 if rg_base.value == "randu" else C1)
    _ax[1].set(aspect="equal", xlim=(0, 1), ylim=(0, 1), title="тройки базового датчика")
    _f.tight_layout()
    mo.vstack([cards([("среднее", f"{_c['gen']['среднее']:.3f}", f"шрифты {_c['real']['среднее']:.3f}"),
                      ("СКО", f"{_c['gen']['СКО']:.3f}", f"шрифты {_c['real']['СКО']:.3f}"),
                      ("КС p", f"{_c['ks_p']:.3f}", "> 0.05: не отличается от шрифтов"),
                      ("принято точек", f"{_info['accept']:.3f}", "у полярного метода π/4 ≈ 0.785")]), plot_html(_f)])''', "rg_x"),
    _cell("G, T, flex, fonts, mo, np, rg_base, rg_go, section, to_wght, to_ytlc", r'''    _seed = 99 + int(rg_go.value)
    _xs = G.generate(fonts.x_height.to_numpy(float), 6, method="polar", family="skewnorm", base=rg_base.value, seed=_seed)[0]
    _ss = G.generate(fonts.stem.to_numpy(float), 6, method="polar", family="lognorm", base=rg_base.value, seed=_seed + 1)[0]
    _cardsf = "".join(
        f'<div class="lab-card" style="gap:.4rem">{flex("Hxlno", to_wght(s), 100, 54, to_ytlc(x))}'
        f'<small>x-height {x:.3f} · штрих {s:.3f}</small></div>' for x, s in zip(_xs, _ss))
    section(mo.md("### Шесть «новых» шрифтов\n\nДатчик выдал шесть пар (x-height, толщина штриха), и они наложены на "
                  "вариативный Roboto Flex: толщина задаёт вес, x-height задаёт высоту строчных. Кнопка «Сгенерировать заново» "
                  "выше даёт новые шрифты."),
            mo.Html(f'<div class="lab-cards" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">{_cardsf}</div>'))'''),
    _cell("mo", r'''    mo.Html("""<div style="color:#5c6170;font-size:.85rem;padding:1rem 0 2rem">
Быкова Кристина Денисовна, ИСУ 501322, трек КТвД, команда 27. Lab01, прикладная статистика, осень 2026.
Полный отчёт с кодом: <a href="report/" target="_top">отчёт</a>. Шрифты: Google Fonts (SIL Open Font License).</div>""")'''),
]


def app_text() -> str:
    head = C.header(TITLE, CSS_FILE).replace('import marimo\n', 'import marimo\n', 1)
    flex_css = _cell("mo", '''    mo.Html('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wdth,wght,YTLC@8..144,25..151,100..1000,416..570&display=swap">')''')
    cells = [SETUP, flex_css] + HERO + COLLECTION + PLAY + RNG
    return head + "\n\n".join(cells) + '\n\nif __name__ == "__main__":\n    app.run()\n'
