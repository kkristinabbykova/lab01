"""Приложение «Белое вино»: настройка, обложка и живые блоки (серая тема)."""
import json
from pathlib import Path

import blocks_common as C

THEME = dict(head_font="Unbounded, Onest, sans-serif", bg="#ffffff", card="#ffffff", ink="#111111", ink2="#555555", line="#111111",
             acc="#8e1b2e", acc2="#111111", soft="#f4f4f4", grid="#e2e2e2", c1="#4a5160", c2="#8e3b46", c3="#9aa1ab",
             cover="#ffffff", cover_ink="#111111",
             section_style={"background": "#ffffff", "border-top": "2px solid #111111", "padding": "1.2rem 0 1rem"},
             live_style={"background": "#f4f4f4", "border": "2px solid #111111", "border-left": "8px solid #8e1b2e",
                         "padding": "1rem 1.2rem 1.1rem"},
             extra_css='\n/* стиль «Плакат»: белый фон, чёрные линии, Unbounded, винно-красный акцент */\n.markdown h1, .markdown h2 {{ font-family: Unbounded, Onest, sans-serif !important; text-transform: uppercase; letter-spacing: -.01em; }}\n.markdown h1 {{ font-size: 2.6rem !important; line-height: 1 !important; border-top: 6px solid #111111; padding-top: .8rem; }}\n.markdown h2 {{ font-size: 1.9rem !important; line-height: 1.05 !important; }}\n.markdown h3 {{ font-family: Onest, sans-serif !important; font-size: .95rem !important; text-transform: uppercase; letter-spacing: .1em;\n               border-left: 0 !important; padding-left: 0 !important; border-top: 2px solid #111111; padding-top: .55rem; margin-top: 1.4rem; }}\n.markdown h4 {{ font-size: 1rem !important; color: #111111 !important; }}\n.markdown a {{ color: #8e1b2e; }}\n.markdown table {{ border-top: 2px solid #111111; border-bottom: 2px solid #111111; }}\n.lab-cover {{ background: #ffffff !important; color: #111111 !important; border-radius: 0 !important; padding: 0 0 1.4rem !important;\n             border-bottom: 2px solid #111111; }}\n.lab-cover h1 {{ font-family: Unbounded, Onest, sans-serif; text-transform: uppercase; font-size: clamp(2.2rem, 5.6vw, 4.4rem) !important;\n                line-height: .98 !important; letter-spacing: -.02em; font-weight: 700; margin: .4rem 0 1rem !important; }}\n.lab-cover .kicker {{ color: #8e1b2e; opacity: 1 !important; font-weight: 600; border-top: 6px solid #8e1b2e; padding-top: .6rem; display: inline-block; }}\n.lab-cover p {{ opacity: 1 !important; font-size: 1.05rem; }}\n.lab-stats {{ display: grid !important; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 0 !important;\n             border-top: 2px solid #111111; border-bottom: 2px solid #111111; margin-top: 1.4rem !important; }}\n.lab-stats div {{ padding: .9rem 0 .9rem .9rem; border-left: 1px solid #111111; }}\n.lab-stats div:first-child {{ border-left: 0; padding-left: 0; }}\n.lab-stats div b {{ font-family: Unbounded, Onest, sans-serif; font-size: 2.1rem !important; font-weight: 600 !important; }}\n.lab-stats div span {{ opacity: 1 !important; font-size: .82rem !important; }}\n.lab-cover .meta {{ opacity: 1 !important; }}\n.lab-guide {{ border: 0 !important; border-radius: 0 !important; border-top: 2px solid #111111 !important; padding: .9rem 0 0 !important; }}\n.lab-guide h4 {{ font-family: Unbounded, Onest, sans-serif; text-transform: uppercase; font-size: 1rem; }}\n.lab-fig {{ background: #f4f4f4 !important; border: 0 !important; border-radius: 0 !important; padding: .8rem !important; }}\n.lab-fig img {{ background: #ffffff; }}\n.lab-fig.live {{ border-left: 6px solid #8e1b2e !important; }}\n.lab-cards {{ gap: 2px !important; background: #111111; border: 2px solid #111111; }}\n.lab-card {{ border: 0 !important; border-radius: 0 !important; background: #ffffff !important; }}\n.lab-card:first-child {{ background: #8e1b2e !important; }}\n.lab-card:first-child span, .lab-card:first-child b, .lab-card:first-child small {{ color: #ffffff !important; }}\n.lab-card b {{ font-family: Unbounded, Onest, sans-serif; font-weight: 600; }}\n.lab-live .tag {{ background: #111111 !important; border-radius: 0 !important; }}\n.lab-live h4 {{ font-family: Unbounded, Onest, sans-serif; text-transform: uppercase; font-size: 1.05rem !important; }}\n.lab-tbl table {{ border: 0 !important; border-top: 2px solid #111111 !important; border-bottom: 2px solid #111111 !important; }}\n.lab-tbl th {{ background: #ffffff !important; text-transform: uppercase; font-size: .75rem; letter-spacing: .06em; }}\n.lab-out {{ border-radius: 0 !important; background: #f4f4f4 !important; border: 0 !important; }}\n')


CSS_FILE = "wine.css"


def header(title):
    return C.header(title, CSS_FILE)


SETUP = '''@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = ''' + json.dumps(THEME) + '''
    STYLE = ''' + json.dumps(C.css_body(THEME).split("\n", 1)[1], ensure_ascii=False) + '''
    ASSETS = "wine"
''' + C.HELPERS + r'''
    # ---- данные: белые и красные вина (Wine Quality, UCI) ----
    white = pd.read_csv(io.StringIO(read_text(PUB / "winequality-white.csv")), sep=";")
    red = pd.read_csv(io.StringIO(read_text(PUB / "winequality-red.csv")), sep=";")
    # столбец: (русское название, единицы, шаг записи)
    COLS = {
        "pH": ("pH", "ед. pH", 0.01), "fixed acidity": ("фиксированная кислотность", "г/дм³", 0.1),
        "alcohol": ("спирт", "% об.", 0.1), "volatile acidity": ("летучая кислотность", "г/дм³", 0.01),
        "citric acid": ("лимонная кислота", "г/дм³", 0.01), "residual sugar": ("остаточный сахар", "г/дм³", 0.05),
        "chlorides": ("хлориды", "г/дм³", 0.001), "free sulfur dioxide": ("свободный SO₂", "мг/дм³", 1.0),
        "total sulfur dioxide": ("общий SO₂", "мг/дм³", 1.0), "density": ("плотность", "г/см³", 0.0001),
        "sulphates": ("сульфаты", "г/дм³", 0.01), "quality": ("оценка качества", "балл", 1.0),
    }
    RU2COL = {v[0]: k for k, v in COLS.items()}
    C1, C2, C3 = T["c1"], T["c2"], T["c3"]

    def grid_edges(x, n_bins, step):
        """Интервалы, кратные шагу записи: иначе на гистограмме появляются ложные зубцы."""
        lo, hi = float(np.min(x)), float(np.max(x))
        w = max(step, round((hi - lo) / n_bins / step) * step)
        return np.arange(lo - step / 2, hi + w, w)

    def describe_cards(x, unit):
        return cards([("среднее", nf(np.mean(x)), unit), ("медиана", nf(np.median(x)), unit),
                      ("СКО", nf(np.std(x, ddof=1)), unit), ("асимметрия", nf(stats.skew(x), 2), "0 у симметричного"),
                      ("эксцесс", nf(stats.kurtosis(x), 2), "0 у нормального"), ("N", f"{len(x)}", "вин")])

    def hist_view(x, n_bins, step, label, unit):
        f, ax = plt.subplots(figsize=(8, 3.4))
        ax.hist(x, bins=grid_edges(x, n_bins, step), color=C1, alpha=0.55, edgecolor="white", linewidth=0.4)
        ax.axvline(np.mean(x), color=C2, linestyle="--", label=f"среднее {np.mean(x):.3f}")
        ax.axvline(np.median(x), color=C3, linestyle=":", label=f"медиана {np.median(x):.3f}")
        ax.set(xlabel=f"{label}, {unit}", ylabel="число вин", title=f"{label}: гистограмма")
        ax.legend()
        return plot_html(f)

    FAMS = {"нормальное": "norm", "логнормальное": "lognorm", "скошенное нормальное": "skewnorm",
            "гамма": "gamma", "Вейбулла": "weibull_min"}
    _fits = {}

    def fit_family(x, fam, key):
        if (key, fam) not in _fits:
            d = getattr(stats, fam)
            p = d.fit(x)
            ll = float(np.sum(d.logpdf(x, *p)))
            _fits[(key, fam)] = (p, 2 * len(p) - 2 * ll, float(stats.kstest(x, d.cdf, args=p).statistic))
        return _fits[(key, fam)]

    def fit_view(x, chosen, n_bins, step, label, unit, key):
        f, ax = plt.subplots(figsize=(8, 3.6))
        ax.hist(x, bins=grid_edges(x, n_bins, step), density=True, color=C3, alpha=0.45, edgecolor="white",
                linewidth=0.4, label="данные")
        g = np.linspace(np.min(x), np.max(x), 400)
        rows = []
        styles = [(C1, "-"), (C2, "-"), ("#16181d", (0, (5, 3))), ("#7a7f88", ":"), (C2, (0, (2, 2)))]
        for (ru, (col, ls)) in zip(chosen, styles):
            p, aic, ks = fit_family(x, FAMS[ru], key)
            ax.plot(g, getattr(stats, FAMS[ru]).pdf(g, *p), color=col, linestyle=ls, label=ru)
            rows.append({"распределение": ru, "AIC": round(aic, 1), "D Колмогорова": round(ks, 4)})
        ax.set(xlabel=f"{label}, {unit}", ylabel="плотность", title=f"{label}: данные и модели")
        ax.legend()
        tab = pd.DataFrame(rows).sort_values("AIC") if rows else pd.DataFrame()
        return plot_html(f), tab

    EST = {"среднее": np.mean, "медиана": np.median, "дисперсия": lambda a: np.var(a, ddof=1)}

    def cons_view(x, est, n, reps=400, seed=1):
        rng = np.random.default_rng(seed)
        fn = EST[est]
        true = fn(x)
        eps = 0.1 * (np.std(x) ** 2 if est == "дисперсия" else np.std(x))
        vals = np.array([fn(rng.choice(x, n, replace=True)) for _ in range(reps)])
        far = np.mean(np.abs(vals - true) > eps)
        f, ax = plt.subplots(figsize=(8, 3.2))
        ax.hist(vals, bins=40, color=C1, alpha=0.6, edgecolor="white", linewidth=0.4)
        ax.axvspan(true - eps, true + eps, color=C3, alpha=0.25, label=f"±ε вокруг значения по всем винам")
        ax.axvline(true, color=C2, label=f"по всем винам: {true:.4f}")
        ax.set(xlabel=f"{est} по выборке из {n} вин", ylabel=f"число выборок из {reps}", title="Как разбросаны оценки")
        ax.legend(loc="upper right")
        return plot_html(f), far, eps

    def sample_view(x, n, repl, reps=600, seed=2):
        rng = np.random.default_rng(seed)
        N = len(x)
        means = np.array([rng.choice(x, n, replace=repl).mean() for _ in range(reps)])
        se_theory = np.std(x) / np.sqrt(n) * (1.0 if repl else np.sqrt((N - n) / (N - 1)))
        f, ax = plt.subplots(1, 2, figsize=(9, 3.2))
        s = np.sort(rng.choice(x, n, replace=repl))
        xs = np.sort(x)
        ax[0].step(xs, np.arange(1, N + 1) / N, color=C1, label=f"все вина, N={N}", where="post")
        ax[0].step(s, np.arange(1, n + 1) / n, color=C2, label=f"одна выборка, n={n}", where="post")
        ax[0].set(ylabel="F(x)", title="Функции распределения")
        ax[0].legend(loc="lower right")
        ax[1].hist(means, bins=35, color=C1, alpha=0.6, edgecolor="white", linewidth=0.4)
        ax[1].axvline(np.mean(x), color=C2, label="среднее по всем винам")
        ax[1].set(title=f"Средние {reps} выборок", ylabel="число выборок")
        ax[1].legend(loc="upper right")
        f.tight_layout()
        return plot_html(f), means.std(ddof=1), se_theory

    def dep_view(x, y, q, xl, yl):
        bx = pd.qcut(x, q, labels=False, duplicates="drop")
        by = pd.qcut(y, q, labels=False, duplicates="drop")
        tab = pd.crosstab(by, bx)
        chi2, p, dof, _ = stats.chi2_contingency(tab)
        v = np.sqrt(chi2 / (tab.values.sum() * (min(tab.shape) - 1)))
        rho, prho = stats.spearmanr(x, y)
        f, ax = plt.subplots(1, 2, figsize=(9.5, 3.8))
        ax[0].hexbin(x, y, gridsize=30, cmap="Greys", mincnt=1, linewidths=0.2)
        ax[0].set(xlabel=xl, ylabel=yl, title="Облако вин")
        im = ax[1].imshow(tab.values[::-1], cmap="Greys")
        for i in range(tab.shape[0]):
            for j in range(tab.shape[1]):
                val = tab.values[::-1][i, j]
                ax[1].text(j, i, str(val), ha="center", va="center", fontsize=8,
                           color="white" if val > tab.values.max() * 0.6 else T["ink"])
        ax[1].set(xticks=range(tab.shape[1]), yticks=range(tab.shape[0]),
                  xticklabels=[f"Q{j + 1}" for j in range(tab.shape[1])],
                  yticklabels=[f"Q{i + 1}" for i in range(tab.shape[0])][::-1],
                  xlabel=f"группы по: {xl}", ylabel=f"группы по: {yl}", title="Сколько вин в каждой паре групп")
        ax[1].grid(False)
        f.tight_layout()
        return plot_html(f), rho, chi2, p, v, dof

    # ---- датчик pH (спринт 2): те же числа и формулы, что в ph_generator.py ----
    SIGMA, THETA, MU = 0.1363, 2.0877, float(np.log(1.0904))
    ph = white["pH"].to_numpy(float)

    def polar_normal(n, rng):
        out, tried, pts = [], 0, None
        while sum(len(o) for o in out) < n:
            v = 2 * rng.random((n, 2)) - 1
            s = (v ** 2).sum(axis=1)
            ok = (s > 0) & (s < 1)
            tried += n
            if pts is None:
                pts = (v[:1500], ok[:1500])
            out.append((v[ok] * np.sqrt(-2 * np.log(s[ok]) / s[ok])[:, None]).ravel())
        z = np.concatenate(out)[:n]
        return z, sum(len(o) for o in out) / 2 / tried, pts

    def gen_ph(method, n, seed):
        rng = np.random.default_rng(seed)
        if method == "полярный":
            z, acc, pts = polar_normal(n, rng)
        else:
            z, acc, pts = stats.norm.ppf(rng.random(n)), 1.0, None
        return THETA + np.exp(MU + SIGMA * z), acc, pts

    # ---- 10 алгоритмов: код пакета labrng (копия в public/) ----
    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (C1, C2, C3, COLS, EST, FAMS, G, RU2COL, T, cons_view, dep_view, describe_cards, fit_view, gen_ph,
            grid_edges, hist_view, ph, red, sample_view, white,
            Path, PUB, base64, cards, code_block, df_html, fig, section, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, stats, table_html, types)
'''


def cover_art() -> str:
    """Рисунок для обложки: облако настоящих вин, pH против фиксированной кислотности."""
    import numpy as np
    import pandas as pd
    w = pd.read_csv(Path(__file__).resolve().parent.parent / "wine" / "data" / "winequality-white.csv", sep=";")
    rng = np.random.default_rng(7)
    d = w.sample(1400, random_state=7)
    x = (d["fixed acidity"].clip(4, 10) - 4) / 6 * 440 + 20 + rng.uniform(-2, 2, len(d))
    y = 300 - (d["pH"].clip(2.8, 3.7) - 2.8) / 0.9 * 270 + rng.uniform(-2, 2, len(d))
    good = (d["quality"] >= 7).to_numpy()
    dots = "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="2.1" fill="{"#8e1b2e" if g else "#111111"}" fill-opacity="{0.8 if g else 0.18}"/>'
                   for a, b, g in zip(x, y, good))
    return (f'<svg class="art" viewBox="0 0 480 320" aria-hidden="true">{dots}'
            '<text x="470" y="312" text-anchor="end" font-size="15" fill="#111111" fill-opacity=".7">'
            'точка = вино (кислотность и pH), красные: оценка 7+</text></svg>')


def cover(head_md: str) -> str:
    html = C.css(THEME) + '''
<div class="lab-cover">''' + cover_art() + '''
  <div class="kicker">Прикладная статистика · Lab01 · команда 27 · основная работа</div>
  <h1>Белое вино как случайный эксперимент</h1>
  <p>4898 португальских белых вин Vinho Verde. Три случайные величины: pH, фиксированная кислотность и спирт.
  Почему их нельзя вычислить заранее, как они распределены и как связаны между собой. Во втором спринте датчик,
  который выдаёт новые «вина» с правильным pH, и исследование 10 алгоритмов датчиков.</p>
  <div class="lab-stats">
    <div><b>4 898</b><span>белых вин</span></div><div><b>3</b><span>случайные величины</span></div>
    <div><b>2</b><span>спринта</span></div><div><b>10</b><span>алгоритмов датчика</span></div>
    <div><b>12</b><span>живых блоков</span></div>
  </div>
  <div class="meta"><span><b>Спринт 1:</b> Нефедьева А. С. (Инфохимия)</span>
  <span><b>Спринт 2, оформление, выводы спринта 1:</b> Быкова К. Д. (КТвД)</span>
  <span><b>Проверка и правка текстов обоих спринтов:</b> Нефедьева А. С.</span>
  <span><b>Данные:</b> Wine Quality, UCI</span></div>
</div>
<div class="lab-guide"><h4>Как читать отчёт</h4><ul>
  <li><b>☰ Содержание</b> в панели слева (на телефоне кнопка вверху): переход к любому разделу.</li>
  <li><b>«Код этого раздела»</b> под каждым разделом: код, которым посчитаны таблицы и рисунки.</li>
  <li><b>Живые блоки</b> с полоской слева: ползунки и переключатели, графики пересчитываются прямо в браузере.</li>
  <li>Тексты, рисунки и таблицы взяты из выполненного ноутбука <code>wine/lab01.ipynb</code>.</li>
  <li><a href="../" target="_top">← Lab01: обе части работы</a> · <a href="../fonts/" target="_top">доп. задание КТвД (шрифты)</a></li>
</ul></div>'''
    return f'''@app.cell(hide_code=True)
def _(mo):
    mo.vstack([mo.Html({C.pystr(html)}), mo.md({C.pystr(head_md.strip())})])
    return
'''


EXTRA_TOC = """**Живые блоки**

- [Любая величина датасета](#live-explore)
- [Подбор распределения: pH](#live-fit-ph)
- [Состоятельность оценок](#live-cons)
- [Выборка и совокупность](#live-sample)
- [Зависимость: таблица групп](#live-dep)
- [Датчик pH](#live-gen)
- [Шесть методов и четыре базовых датчика](#live-algo)
"""


def _cells(*parts):
    return [p.strip("\n") + "\n" for p in parts]


EXPLORE = _cells('''
@app.cell(hide_code=True)
def _(COLS, live, mo):
    explore_var = mo.ui.dropdown(options=[v[0] for v in COLS.values()], value="pH", label="Величина")
    explore_bins = mo.ui.slider(start=10, stop=80, step=5, value=40, label="Число столбиков", show_value=True)
    explore_wine = mo.ui.radio(options=["белые", "красные"], value="белые", label="Вина", inline=True)
    mo.vstack([mo.Html('<a id="live-explore"></a>'),
               live("Любая величина датасета", "Выберите измерение и число столбиков: карточки и гистограмма пересчитаются. "
                    "Можно сравнить белые и красные вина.", explore_var, explore_bins, explore_wine)])
    return explore_bins, explore_var, explore_wine
''', '''
@app.cell(hide_code=True)
def _(COLS, RU2COL, describe_cards, explore_bins, explore_var, explore_wine, hist_view, mo, red, white):
    _col = RU2COL[explore_var.value]
    _label, _unit, _step = COLS[_col]
    _x = (white if explore_wine.value == "белые" else red)[_col].to_numpy(float)
    mo.vstack([describe_cards(_x, _unit), hist_view(_x, explore_bins.value, _step, _label, _unit)])
    return
''')


def fit_block(sfx, col, default):
    ui = f'''
@app.cell(hide_code=True)
def _(FAMS, live, mo):
    fit_fams_{sfx} = mo.ui.multiselect(options=list(FAMS), value={json.dumps(default, ensure_ascii=False)}, label="Модели")
    fit_bins_{sfx} = mo.ui.slider(start=15, stop=80, step=5, value=45, label="Столбики", show_value=True)
    mo.vstack([mo.Html('<a id="live-fit-{sfx}"></a>'),
               live("Подбор распределения вживую", "Включайте и выключайте модели: на графике их плотности, в таблице AIC "
                    "(чем меньше, тем лучше) и расстояние Колмогорова D до данных.", fit_fams_{sfx}, fit_bins_{sfx})])
    return fit_bins_{sfx}, fit_fams_{sfx}
'''
    view = f'''
@app.cell(hide_code=True)
def _(COLS, df_html, fit_bins_{sfx}, fit_fams_{sfx}, fit_view, mo, white):
    _label, _unit, _step = COLS[{json.dumps(col)}]
    _img, _tab = fit_view(white[{json.dumps(col)}].to_numpy(float), fit_fams_{sfx}.value, fit_bins_{sfx}.value, _step, _label, _unit, {json.dumps(sfx)})
    mo.vstack([_img, df_html(_tab) if len(_tab) else mo.md("_Выберите хотя бы одну модель._")])
    return
'''
    return _cells(ui, view)


def cons_block(sfx, default_ru):
    ui = f'''
@app.cell(hide_code=True)
def _(EST, live, mo):
    cons_var_{sfx} = mo.ui.dropdown(options=["pH", "фиксированная кислотность", "спирт"], value={json.dumps(default_ru, ensure_ascii=False)}, label="Величина")
    cons_est_{sfx} = mo.ui.radio(options=list(EST), value="среднее", label="Оценка", inline=True)
    cons_n_{sfx} = mo.ui.dropdown(options=["10", "30", "100", "300", "1000", "3000"], value="30", label="Объём выборки n")
    mo.vstack([mo.Html('<a id="live-cons{'' if sfx == 'ph' else '-' + sfx}"></a>'),
               live("Состоятельность: увеличьте n", "Из всех вин 400 раз берётся выборка объёма n и считается оценка. "
                    "Чем больше n, тем уже разброс и тем реже оценка выходит за полосу ±ε.", cons_var_{sfx}, cons_est_{sfx}, cons_n_{sfx})])
    return cons_est_{sfx}, cons_n_{sfx}, cons_var_{sfx}
'''
    view = f'''
@app.cell(hide_code=True)
def _(RU2COL, cards, cons_est_{sfx}, cons_n_{sfx}, cons_var_{sfx}, cons_view, mo, white):
    _img, _far, _eps = cons_view(white[RU2COL[cons_var_{sfx}.value]].to_numpy(float), cons_est_{sfx}.value, int(cons_n_{sfx}.value))
    mo.vstack([cards([("доля «далёких» оценок", f"{{_far:.3f}}", "должна стремиться к 0"), ("ε", f"{{_eps:.4f}}", "0.1·СКО (для дисперсии 0.1·σ²)")]), _img])
    return
'''
    return _cells(ui, view)


def sample_block(sfx, default_ru):
    ui = f'''
@app.cell(hide_code=True)
def _(live, mo):
    smp_var_{sfx} = mo.ui.dropdown(options=["pH", "фиксированная кислотность", "спирт"], value={json.dumps(default_ru, ensure_ascii=False)}, label="Величина")
    smp_n_{sfx} = mo.ui.slider(start=50, stop=4500, step=50, value=300, label="Объём выборки n", show_value=True)
    smp_repl_{sfx} = mo.ui.switch(value=True, label="с возвращением")
    mo.vstack([mo.Html('<a id="live-sample{'' if sfx == 'ph' else '-' + sfx}"></a>'),
               live("Выборка против всех вин", "Сдвиньте n к 4500 и выключите «с возвращением»: разброс средних станет "
                    "меньше формулы σ/√n: работает поправка на конечность совокупности.", smp_var_{sfx}, smp_n_{sfx}, smp_repl_{sfx})])
    return smp_n_{sfx}, smp_repl_{sfx}, smp_var_{sfx}
'''
    view = f'''
@app.cell(hide_code=True)
def _(RU2COL, cards, mo, sample_view, smp_n_{sfx}, smp_repl_{sfx}, smp_var_{sfx}, white):
    _img, _se, _th = sample_view(white[RU2COL[smp_var_{sfx}.value]].to_numpy(float), smp_n_{sfx}.value, smp_repl_{sfx}.value)
    mo.vstack([cards([("СКО средних, опыт", f"{{_se:.4f}}", "по 600 выборкам"),
                      ("по формуле", f"{{_th:.4f}}", "σ/√n" + ("" if smp_repl_{sfx}.value else " · √((N−n)/(N−1))"))]), _img])
    return
'''
    return _cells(ui, view)


def dep_block(sfx, default_pair):
    pairs = ["pH и фиксированная кислотность", "pH и спирт", "фиксированная кислотность и спирт",
             "спирт и плотность", "спирт и остаточный сахар"]
    ui = f'''
@app.cell(hide_code=True)
def _(live, mo):
    dep_pair_{sfx} = mo.ui.dropdown(options={json.dumps(pairs, ensure_ascii=False)}, value={json.dumps(default_pair, ensure_ascii=False)}, label="Пара")
    dep_q_{sfx} = mo.ui.slider(start=2, stop=6, step=1, value=4, label="Групп по каждой величине", show_value=True)
    mo.vstack([mo.Html('<a id="live-dep{'' if sfx == 'ph' else '-' + sfx}"></a>'),
               live("Зависимость: таблица групп", "Вина делятся на равные группы по каждой величине. Если величины независимы, "
                    "все клетки таблицы были бы примерно одинаковыми; хи-квадрат проверяет, насколько это не так.", dep_pair_{sfx}, dep_q_{sfx})])
    return dep_pair_{sfx}, dep_q_{sfx}
'''
    view = f'''
@app.cell(hide_code=True)
def _(COLS, RU2COL, cards, dep_pair_{sfx}, dep_q_{sfx}, dep_view, mo, white):
    _a, _b = dep_pair_{sfx}.value.split(" и ")
    _ca, _cb = RU2COL[_a], RU2COL[_b]
    _img, _rho, _chi2, _p, _v, _dof = dep_view(white[_ca].to_numpy(float), white[_cb].to_numpy(float), dep_q_{sfx}.value,
                                              f"{{_a}}, {{COLS[_ca][1]}}", f"{{_b}}, {{COLS[_cb][1]}}")
    mo.vstack([cards([("ρ Спирмена", f"{{_rho:+.2f}}", "сила и направление"), ("χ²", f"{{_chi2:.0f}}", f"df = {{_dof}}"),
                      ("p", f"{{_p:.1e}}", "меньше 0.05: связь есть"), ("V Крамера", f"{{_v:.2f}}", "0 нет связи, 1 полная")]), _img])
    return
'''
    return _cells(ui, view)


GEN = _cells('''
@app.cell(hide_code=True)
def _(live, mo):
    gen_method = mo.ui.radio(options=["полярный", "обратных функций"], value="полярный", label="Метод", inline=True)
    gen_n = mo.ui.slider(start=500, stop=20000, step=500, value=4898 // 500 * 500, label="Сколько значений", show_value=True)
    gen_seed = mo.ui.number(start=0, stop=10**6, value=2026, label="seed")
    gen_round = mo.ui.switch(value=True, label="округлять до 0.01, как прибор")
    mo.vstack([mo.Html('<a id="live-gen"></a>'),
               live("Датчик pH вживую", "Тот же датчик, что в разделе 6: θ + e^(μ + σZ). Меняйте метод, объём, seed и "
                    "округление и посмотрите, как меняется критерий Колмогорова–Смирнова.", gen_method, gen_n, gen_seed, gen_round)])
    return gen_method, gen_n, gen_round, gen_seed
''', '''
@app.cell(hide_code=True)
def _(C1, C2, cards, gen_method, gen_n, gen_ph, gen_round, gen_seed, grid_edges, mo, np, ph, plot_html, plt, stats):
    _x, _acc, _pts = gen_ph(gen_method.value, gen_n.value, int(gen_seed.value or 0))
    if gen_round.value:
        _x = np.round(_x, 2)
    _ks = stats.ks_2samp(_x, ph)
    _f, _ax = plt.subplots(1, 2 if _pts is not None else 1, figsize=(9.5 if _pts is not None else 8, 3.6),
                           gridspec_kw={"width_ratios": [2.2, 1]} if _pts is not None else None)
    _a0 = _ax[0] if _pts is not None else _ax
    _e = grid_edges(ph, 45, 0.01)
    _a0.hist(ph, bins=_e, density=True, color=C1, alpha=0.35, label="данные, 4898 вин")
    _a0.hist(_x, bins=_e, density=True, histtype="step", color=C2, linewidth=1.8, label="датчик")
    _a0.set(xlabel="pH, ед. pH", ylabel="плотность", title="Данные и датчик")
    _a0.legend()
    if _pts is not None:
        _v, _ok = _pts
        _ax[1].plot(_v[_ok, 0], _v[_ok, 1], ".", ms=2, color=C1)
        _ax[1].plot(_v[~_ok, 0], _v[~_ok, 1], ".", ms=2, color=C2)
        _t = np.linspace(0, 2 * np.pi, 200)
        _ax[1].plot(np.cos(_t), np.sin(_t), color="#16181d", linewidth=1)
        _ax[1].set(aspect="equal", xlim=(-1.05, 1.05), ylim=(-1.05, 1.05), title="Точки полярного метода")
    _f.tight_layout()
    mo.vstack([cards([("среднее", f"{_x.mean():.3f}", f"данные {ph.mean():.3f}"), ("СКО", f"{_x.std(ddof=1):.3f}", f"данные {ph.std(ddof=1):.3f}"),
                      ("КС p", f"{_ks.pvalue:.3f}", "больше 0.05: не отличается"), ("принято точек", f"{_acc:.3f}", "теория π/4 = 0.785" if _pts is not None else "без отбора")]),
               plot_html(_f)])
    return
''')

ALGO = _cells('''
@app.cell(hide_code=True)
def _(G, live, mo):
    algo_method = mo.ui.dropdown(options={v: k for k, v in G.METHOD_RU.items()}, value=G.METHOD_RU["polar"], label="Метод")
    algo_base = mo.ui.dropdown(options={v: k for k, v in G.BASE_RU.items()}, value=G.BASE_RU["pcg64"], label="Базовый датчик")
    algo_seed = mo.ui.number(start=0, stop=10**6, value=2026, label="seed")
    mo.vstack([mo.Html('<a id="live-algo"></a>'),
               live("Любой из шести методов на любом базовом датчике", "Код всех алгоритмов лежит в пакете labrng. Модель для методов "
                    "«через модель» логнормальная со сдвигом, как в разделе 6.", algo_method, algo_base, algo_seed)])
    return algo_base, algo_method, algo_seed
''', '''
@app.cell(hide_code=True)
def _(C1, C2, G, algo_base, algo_method, algo_seed, cards, grid_edges, mo, np, ph, plot_html, plt, stats):
    _x, _info = G.generate(ph, len(ph), method=algo_method.value, family="lognorm", base=algo_base.value,
                           seed=int(algo_seed.value or 0), step=0.01)
    _ks = stats.ks_2samp(_x, ph)
    _u = G.Uniform(algo_base.value, int(algo_seed.value or 0))(3002)
    _f, _ax = plt.subplots(1, 2, figsize=(9.5, 3.6), gridspec_kw={"width_ratios": [2.2, 1]})
    _e = grid_edges(ph, 45, 0.01)
    _ax[0].hist(ph, bins=_e, density=True, color=C1, alpha=0.35, label="данные")
    _ax[0].hist(_x, bins=_e, density=True, histtype="step", color=C2, linewidth=1.8, label="датчик")
    _ax[0].set(xlabel="pH, ед. pH", ylabel="плотность", title=G.METHOD_RU[algo_method.value])
    _ax[0].legend()
    _ax[1].plot((6 * _u[1:-1] - 9 * _u[:-2]) % 1.0, _u[2:], ".", ms=1.5, color=C2 if algo_base.value == "randu" else C1)
    _ax[1].set(aspect="equal", xlim=(0, 1), ylim=(0, 1), title="Тройки базового датчика")
    _f.tight_layout()
    mo.vstack([cards([("КС p", f"{_ks.pvalue:.3f}", "больше 0.05: не отличается от данных"),
                      ("принято точек", f"{_info['accept']:.3f}", "1 значит метод ничего не выбрасывает")]), plot_html(_f)])
    return
''')

BLOCKS = {
    "dataset": EXPLORE,
    "rv01-eda": fit_block("ph", "pH", ["нормальное", "логнормальное", "скошенное нормальное"]),
    "rv02-eda": fit_block("acid", "fixed acidity", ["нормальное", "логнормальное", "скошенное нормальное"]),
    "rv03-eda": fit_block("alc", "alcohol", ["нормальное", "гамма", "скошенное нормальное"]),
    "rv01-dep": dep_block("ph", "pH и фиксированная кислотность"),
    "rv03-dep": dep_block("alc", "спирт и плотность"),
    "rv01-cons": cons_block("ph", "pH"),
    "rv02-cons": cons_block("acid", "фиксированная кислотность"),
    "rv01-sample": sample_block("ph", "pH"),
    "rv03-sample": sample_block("alc", "спирт"),
    "sp2-tests": GEN,
    "sp2-algo-ph": ALGO,
}
