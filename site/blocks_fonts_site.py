"""Сайт про шрифты на marimo в том же виде, что и прежняя страница на HTML + JavaScript.

Вёрстка и стиль прежние (fonts_site.css взят со старой страницы). Графики рисуются как SVG прямо из Python,
поэтому выглядят как раньше; ползунки и переключатели теперь marimo, расчёты на Python в браузере.
"""
import json
from pathlib import Path

import blocks_common as C

WCODE = r'''    try:
        import anywidget
        import traitlets

        class _Pill(anywidget.AnyWidget):
            _esm = _WJ["pill"]
            _css = _WC["pill"]
            label = traitlets.Unicode("").tag(sync=True)
            count = traitlets.Int(0).tag(sync=True)

        class _Scatter(anywidget.AnyWidget):
            _esm = _WJ["scatter"]
            _css = _WC["scatter"]
            points = traitlets.List([]).tag(sync=True)
            cats = traitlets.Dict({}).tag(sync=True)
            selected = traitlets.Unicode("").tag(sync=True)

        class _Panel(anywidget.AnyWidget):
            _esm = _WJ["controls"]
            _css = _WC["controls"]
            spec = traitlets.List([]).tag(sync=True)
            values = traitlets.Dict({}).tag(sync=True)

        HAS_AW = True
    except Exception:
        HAS_AW = False

    def panel(spec, values):
        """Элементы управления в стиле прежнего сайта; без anywidget те же поля на стандартных элементах marimo."""
        if HAS_AW:
            return mo.ui.anywidget(_Panel(spec=spec, values=values))
        els = {}
        for c in spec:
            n, t = c.get("name"), c["type"]
            if t == "seg" and not c.get("sets"):
                o = {a: b for a, b in c["options"]}
                els[n] = mo.ui.radio(options=o, value=[a for a, b in c["options"] if b == values[n]][0], label=c.get("label", ""), inline=True)
            elif t == "select":
                opts = [o for g in c["groups"] for o in g[1]] if c.get("groups") else c["options"]
                o = {a: b for a, b in opts}
                els[n] = mo.ui.dropdown(options=o, value=[a for a, b in opts if b == values[n]][0], label=c.get("label", ""), searchable=True)
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

    def pill(label):
        if HAS_AW:
            return mo.ui.anywidget(_Pill(label=label))
        return mo.ui.button(value=0, on_click=lambda v: v + 1, label=label)

    def clicks(w):
        v = w.value
        return int(v.get("count", 0)) if isinstance(v, dict) else int(v or 0)

    def scatter_widget(selected=""):
        pts = [{"f": r.family, "c": r.category, "x": round(float(r.x_height), 4), "s": round(float(r.stem), 4)}
               for r in fonts.itertuples()]
        if HAS_AW:
            return mo.ui.anywidget(_Scatter(points=pts, cats={k: list(v) for k, v in CAT.items()}, selected=selected or ""))
        return None

    def selected_of(w, default=""):
        v = getattr(w, "value", None)
        return (v.get("selected") or default) if isinstance(v, dict) else default

    def font_row(r, txt):
        """Строка сравнения: текст шрифтом r, пунктиры наших измерений, полоски с медианой датасета."""
        keys = [("x_height", "x-height", 3), ("stem", "толщина штриха", 3), ("contrast", "контраст «o»", 2),
                ("width_o", "ширина «o» / x-height", 3)]

        def bar(k, lab, d):
            lo, hi, md = fonts[k].min(), fonts[k].max(), fonts[k].median()
            pos = lambda v: max(0, min(1, (v - lo) / (hi - lo))) * 100   # noqa: E731
            return (f'<div class="bar">{lab}: <b style="color:#1a1d24">{nfc(r[k], d)}</b><div class="track">'
                    f'<div class="fill" style="width:{pos(r[k]):.1f}%;background:{CAT[r.category][1]}"></div>'
                    f'<div class="med" style="left:{pos(md):.1f}%" title="медиана датасета"></div></div></div>')

        fs = max(14.0, min(72.0, 620 / (0.62 * max(len(txt), 1))))
        base = round(fs * max(1.0, r.cap_height) + 14)
        y_x, y_c = base - r.x_height * fs, base - r.cap_height * fs
        lines = [f'<line x1="0" x2="640" y1="{base}" y2="{base}" stroke="#5c6170"/>',
                 f'<line x1="0" x2="640" y1="{y_x:.1f}" y2="{y_x:.1f}" stroke="#eb6834" stroke-dasharray="5 4"/>',
                 f'<line x1="0" x2="640" y1="{y_c:.1f}" y2="{y_c:.1f}" stroke="#1baf7a" stroke-dasharray="5 4"/>',
                 f'<text x="8" y="{base}" font-size="{fs:.1f}" fill="#1a1d24" style="font-family:&quot;{esc(r.family)}&quot;,serif">{esc(txt)}</text>']
        head = (f'<div class="cmp-head"><b>{esc(r.family)}</b><span class="note"><span style="color:#eb6834">- - x-height {nfc(r.x_height)}</span>'
                f'&nbsp;&nbsp;<span style="color:#1baf7a">- - прописные {nfc(r.cap_height)}</span>&nbsp;&nbsp;{CAT[r.category][0]}</span></div>')
        return (gfont(r.family, txt) + '<div class="cmp-row">' + head + svg(640, base + 16, lines, txt + " шрифтом " + r.family)
                + '<div class="bars">' + "".join(bar(k, lab, d) for k, lab, d in keys) + "</div></div>")

'''

_W = Path(__file__).resolve().parent / "widgets"
WJ = {n: (_W / f"{n}.js").read_text(encoding="utf-8") for n in ("scatter", "pill", "controls")}
WC = {n: (_W / f"{n}.css").read_text(encoding="utf-8") for n in ("scatter", "pill", "controls")}
WIDGET_CODE = (
    "    # свои элементы (anywidget): большая кнопка и график с приближением и щелчком; без anywidget всё работает на элементах marimo\n"
    "    _WJ = " + json.dumps(WJ, ensure_ascii=False) + "\n"
    "    _WC = " + json.dumps(WC, ensure_ascii=False) + "\n"
    + WCODE)

CSS_FILE = "fonts_site.css"
TITLE = "Lab01 КТвД: шрифт как случайная величина"

CSS = r'''@import url('https://fonts.googleapis.com/css2?family=Onest:wght@300..900&family=Unbounded:wght@300..900&family=Roboto+Flex:opsz,wdth,wght,YTLC@8..144,25..151,100..1000,416..570&display=swap');
:root{ --paper:#f6f7f5; --ink:#1a1d24; --muted:#5c6170; --rule:#dcdfd8;
  --blue:#2a78d6; --orange:#eb6834; --straw:#d8c56a; --green:#1baf7a; --measure:68ch;
  --marimo-text-font:Onest,system-ui,sans-serif; --marimo-heading-font:Unbounded,Onest,sans-serif; }
body, #App, .mo-app, [data-testid="app"]{background:var(--paper) !important;color:var(--ink)}
body, .markdown, .prose{font-family:Onest,system-ui,-apple-system,"Segoe UI",sans-serif}
.fs a{color:var(--blue);text-underline-offset:.18em}
.fs code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em;background:#e9ebe6;padding:.08em .35em;border-radius:3px}
.fs{font-size:1.0625rem;line-height:1.6;color:var(--ink)}
.fs .text{max-width:var(--measure)}
.fs p{margin:0 0 1rem !important}
.fs, .fs p, .fs a, .fs li, .fs b, .fs i, .fs .note, .fs .lede, .fs .bar, .fs .cmp-head, .fs figcaption, .fs .readout, .fs .legend{font-family:Onest,system-ui,sans-serif}
.fs-hero h1 .l{font-family:"Roboto Flex",sans-serif}
.fs-hero{padding-top:clamp(2rem,6vw,5rem);padding-bottom:1rem}
.fs-hero h1{font-family:"Roboto Flex",sans-serif !important;font-size:clamp(2.9rem,9.2vw,7.4rem) !important;line-height:.98 !important;letter-spacing:-.02em;margin:.4rem 0 1.6rem !important;font-weight:400}
.fs-hero h1 .w{display:block !important}
.fs-hero h1 span.l{transition:font-weight .5s cubic-bezier(.2,.7,.2,1)}
.fs .lede{font-size:clamp(1.1rem,1.6vw,1.3rem);color:var(--muted);margin:0 0 1.4rem;max-width:var(--measure)}
.fs .note{color:var(--muted);font-size:.95rem}
.fs-sec{padding-top:3rem;border-top:1px solid var(--rule);margin-top:2rem}
.fs h2{font-family:Unbounded,Onest,sans-serif !important;font-size:clamp(1.6rem,3.2vw,2.4rem) !important;line-height:1.15 !important;font-weight:600 !important;letter-spacing:-.01em;margin:0 0 1rem !important;color:var(--ink)}
.fs h3{font-family:Unbounded,Onest,sans-serif !important;font-size:1.1rem !important;font-weight:550 !important;margin:1.6rem 0 .5rem !important;color:var(--ink)}
.fs figure{margin:1.4rem 0}
.fs figure img{width:100%;height:auto;background:#fff;border-radius:6px}
.fs figcaption{color:var(--muted);font-size:.92rem;margin-top:.5rem;max-width:var(--measure)}
.fs .chart{background:#fff;border-radius:8px;padding:.6rem}
.fs .chart svg{display:block;width:100%;height:auto}
.fs .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1.4rem 2rem;margin:1.6rem 0;max-width:900px}
.fs .fact strong{display:block;font-family:Unbounded,Onest,sans-serif;font-size:2.2rem;line-height:1.1;font-weight:600;font-variant-numeric:tabular-nums}
.fs .fact span{color:var(--muted);font-size:.95rem}
.fs .legend{display:flex;flex-wrap:wrap;gap:.4rem 1rem;font-size:.88rem;color:var(--muted);margin:.5rem 0 0}
.fs .sw{display:inline-block;width:.8em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}
.fs .rho-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;max-width:820px}
.fs .lab{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:1.6rem;align-items:start;margin-top:.6rem}
.fs .readout{font-variant-numeric:tabular-nums;margin-top:.7rem;font-size:.95rem}
.fs .readout b{font-weight:650}
.fs .specimen{background:#fff;border-radius:8px;padding:1.2rem 1.4rem;overflow:hidden}
.fs .cmp-row{background:#fff;border-radius:8px;padding:.8rem 1rem 1rem;margin:0 0 1rem}
.fs .cmp-head{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;margin-bottom:.3rem}
.fs .cmp-head b{font-weight:650}
.fs .bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.6rem 1.4rem;margin-top:.6rem}
.fs .bar{font-size:.85rem;color:var(--muted)}
.fs .bar .track{position:relative;height:8px;border-radius:4px;background:#eceee9;margin-top:.25rem}
.fs .bar .fill{position:absolute;left:0;top:0;bottom:0;border-radius:4px}
.fs .bar .med{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--ink);opacity:.7}
.fs .newfonts{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-top:.8rem}
.fs .newfonts div.c{background:#fff;border-radius:8px;padding:.8rem 1rem}
.fs .newfonts small{color:var(--muted);font-size:.82rem}
.fs-foot{border-top:1px solid var(--rule);margin-top:2.5rem;padding:2rem 0 3rem;color:var(--muted);font-size:.95rem}
.fs-foot p{max-width:var(--measure)}
.fs-ctrl{font-size:.9rem;color:var(--muted)}
@media (max-width:640px){.fs .rho-grid,.fs .lab{grid-template-columns:1fr}}
'''


def _cell(params, body, returns=""):
    ret = f"    return ({returns},)\n" if returns else "    return\n"
    return f"@app.cell(hide_code=True)\ndef _({params}):\n{body.rstrip()}\n{ret}"


SETUP = '''@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = ''' + json.dumps(dict(bg="#f6f7f5", card="#ffffff", ink="#1a1d24", ink2="#5c6170", line="#dcdfd8", acc="#2a78d6",
                              acc2="#a9c8ef", soft="#eceee9", grid="#e6e5e0", c1="#2a78d6", c2="#eb6834", c3="#1baf7a",
                              cover="", cover_ink="", head_font="Golos Text")) + '''
    STYLE = ''' + json.dumps(CSS, ensure_ascii=False) + '''
''' + C.HELPERS + r'''
    import html as htmlmod
    fonts_all = pd.read_csv(io.StringIO(read_text(PUB / "fonts.csv")))
    fonts = fonts_all[~fonts_all["no_lowercase"].astype(str).eq("True")].copy().reset_index(drop=True)
    CAT = {"sans": ("гротески", "#2a78d6"), "serif": ("антиквы", "#eb6834"), "display": ("акцидентные", "#1baf7a"),
           "handwriting": ("рукописные", "#9b59b6"), "mono": ("моноширинные", "#5c6170")}
    CAT_RU = {v[0]: k for k, v in CAT.items()}
    INK, MUTED, GRIDC = "#1a1d24", "#5c6170", "#e6e5e0"

    def nfc(v, d=3):
        """Число с запятой, как на прежней странице."""
        return f"{v:.{d}f}".replace(".", ",").replace("-", "−")

    def esc(s):
        return htmlmod.escape(str(s), quote=True)

    def ticks(lo, hi, n=6):
        step = 10 ** np.floor(np.log10((hi - lo) / n))
        for m in (1, 2, 2.5, 5, 10):
            if (hi - lo) / (step * m) <= n:
                step *= m
                break
        return np.arange(np.ceil(lo / step) * step, hi + step / 2, step)

    def dec(arr):
        """Сколько знаков после запятой нужно подписям делений."""
        st = arr[1] - arr[0] if len(arr) > 1 else 1
        txt = f"{st:.6g}"
        return len(txt.split(".")[1]) if "." in txt else 0

    def frame(W, H, L, R, Tp, B, xlim, ylim, xlabel, ylabel, xd=2, yd=2):
        """Оси и сетка SVG-графика в стиле прежней страницы. Возвращает (элементы, X(), Y())."""
        X = lambda v: L + (v - xlim[0]) / (xlim[1] - xlim[0]) * (W - L - R)      # noqa: E731
        Y = lambda v: H - B - (v - ylim[0]) / (ylim[1] - ylim[0]) * (H - Tp - B)  # noqa: E731
        out = []
        xt, yt = ticks(*xlim), ticks(*ylim, 5)
        xd, yd = max(xd, dec(xt)), max(yd, dec(yt))
        for t in xt:
            if xlim[0] - 1e-9 <= t <= xlim[1] + 1e-9:
                out.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{Tp}" y2="{H - B}" stroke="{GRIDC}"/>'
                           f'<text x="{X(t):.1f}" y="{H - B + 18}" text-anchor="middle" font-size="12" fill="{MUTED}">{nfc(t, xd)}</text>')
        for t in yt:
            if ylim[0] - 1e-9 <= t <= ylim[1] + 1e-9:
                out.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRIDC}"/>'
                           f'<text x="{L - 8}" y="{Y(t) + 4:.1f}" text-anchor="end" font-size="12" fill="{MUTED}">{nfc(t, yd)}</text>')
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{H - B}" y2="{H - B}" stroke="{MUTED}"/>')
        out.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 6}" text-anchor="middle" font-size="13" fill="{INK}">{xlabel}</text>')
        out.append(f'<text x="14" y="{(Tp + H - B) / 2:.0f}" text-anchor="middle" font-size="13" fill="{INK}" '
                   f'transform="rotate(-90 14 {(Tp + H - B) / 2:.0f})">{ylabel}</text>')
        return out, X, Y

    def svg(W, H, items, label=""):
        return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}" '
                f'style="font-family:Onest,system-ui,sans-serif">{"".join(items)}</svg>')

    def legend(items):
        return '<div class="legend">' + "".join(f'<span><i class="sw" style="background:{c}"></i>{t}</span>' for t, c in items) + "</div>"

    def gfont(family, text=""):
        q = family.replace(" ", "+")
        t = ("&text=" + "".join(sorted(set(text))).replace("&", "").replace("#", "")) if text else ""
        return f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={q}{t}&display=swap">'

    def to_wght(stem):
        """Толщина штриха (доли кегля) → вес Roboto Flex: 0.09 ≈ Regular 400."""
        return float(np.clip(np.interp(stem, [0.02, 0.09, 0.22], [100, 400, 1000]), 100, 1000))

    def to_ytlc(xh):
        """x-height (доли кегля) → ось YTLC Roboto Flex (высота строчных)."""
        return float(np.clip(xh * 1000, 416, 570))

    def H(s):
        """Кусок страницы в оформлении прежнего сайта."""
        return mo.Html(ST + f'<div class="fs">{s}</div>')

''' + WIDGET_CODE + r'''
    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (CAT, CAT_RU, G, GRIDC, H, HAS_AW, INK, MUTED, T, clicks, esc, font_row, fonts, frame, gfont, legend, nfc, panel, pill, vals,
            scatter_widget, selected_of, svg, to_wght, to_ytlc,
            Path, PUB, base64, cards, code_block, df_html, fig, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, section, stats, table_html, types)
'''

HERO = [
    _cell("pill", '''    reroll = pill("Перебросить толщину букв")''', "reroll"),
    _cell("H, clicks, fonts, mo, np, reroll, to_wght", r'''    _rng = np.random.default_rng(clicks(reroll) * 7 + 3)
    _pick = fonts[["stem", "width_o"]].dropna().to_numpy(float)

    def _letter(ch):   # каждая буква берёт толщину и ширину случайного настоящего шрифта
        if ch == " ":
            return " "
        _s, _w = _pick[_rng.integers(len(_pick))]
        _wd = float(np.clip(np.interp(_w, [0.75, 1.0, 1.25], [62, 100, 140]), 25, 151))
        return f'<span class="l" style="font-variation-settings:\'wght\' {to_wght(_s):.0f},\'wdth\' {_wd:.0f}">{ch}</span>'

    _words = "".join('<span class="w">' + "".join(_letter(c) for c in w) + "</span>" for w in ("Шрифт как", "случайная", "величина"))
    mo.vstack([H(f"""<div class="fs-hero">
  <p class="note" style="margin:0"><a href="../" target="_top">← Lab01: обе части работы</a> · <a href="report/" target="_top">отчёт</a></p>
  <h1 aria-label="Шрифт как случайная величина">{_words}</h1>
  <p class="lede">Это доп. задание КТвД к лабораторной по прикладной статистике. Я собрала датасет шрифтов
  с Google Fonts (в анализе их {len(fonts)}: часть выбрана мной, остальные добавлены случайным отбором, по 20 в каждой категории)
  и измерила у каждого две вещи: высоту строчных букв (x-height) и толщину штриха.
  Эти размеры нельзя вычислить по формуле: у каждого шрифта они свои, поэтому их можно изучать как случайные величины.</p>
  <p class="lede">Ниже то, что получилось, и интерактивный датчик, который выдаёт случайные числа, похожие на настоящие данные.
  Нажми кнопку: толщина и ширина каждой буквы в заголовке выпадут случайно, из тех же значений, что у настоящих шрифтов.</p>
</div>"""), reroll])'''),
]


FONTS = [
    _cell("H, fonts, nfc, stats", r'''    _rho = stats.spearmanr(fonts.x_height, fonts.stem)[0]
    _med = fonts.groupby("category").x_height.median()
    H(f"""<div class="fs-sec" id="fonts">
<h2>Шрифты: высота строчных и толщина штриха</h2>
<div class="text"><p>Датасет собран самостоятельно: {len(fonts)} шрифтовых семейств из Google Fonts, по 20 гротесков, антикв, акцидентных,
рукописных и моноширинных. У каждого измерено начертание Regular прямо по контурам букв. Все размеры даны в долях кегля,
то есть не зависят от размера, которым набран текст.</p></div>
<figure><img src="public/fonts_measure.png" alt="Буквы H x l n o шрифта Playfair с линиями измерений" loading="lazy">
<figcaption>Что измеряется: x-height (верх строчной «x»), высота прописных, толщина вертикали «l» и контраст «o».</figcaption></figure>
<div class="facts">
  <div class="fact"><strong>{nfc(_med["sans"])}</strong><span>медианная x-height гротесков</span></div>
  <div class="fact"><strong>{nfc(_med["serif"])}</strong><span>медианная x-height антикв: строчные ниже, критерий Манна–Уитни это подтверждает</span></div>
  <div class="fact"><strong>ρ = {nfc(_rho, 2)}</strong><span>связь x-height и толщины штриха: чем выше строчные, тем толще штрих</span></div>
</div>
<h3>Как читать ρ</h3>
<p class="note text">ρ Спирмена показывает, насколько согласованно растут две величины: 0 значит связи нет,
1 значит чем больше одна, тем больше другая, без исключений. Подвигай ползунок: слева облако из 100 случайных точек
с выбранной силой связи, справа наши шрифты (ρ = {nfc(_rho, 2)}).</p></div>""")'''),
    _cell("panel", r'''    rho_p = panel([{"type": "range", "name": "rho", "label": "Сила связи ρ", "min": -1, "max": 1, "step": 0.05, "decimals": 2, "live": True},
                   {"type": "seg", "name": "preset", "sets": "rho", "options": [["нет связи", 0], ["как у нас", 0.4], ["сильная", 0.9]]}],
                  {"rho": 0.4})
    rho_p''', "rho_p"),
    _cell("H, MUTED, fonts, nfc, np, rho_p, stats, svg, vals", r'''    _r = float(vals(rho_p).get("rho", 0.4))
    _rp = 2 * np.sin(np.pi * _r / 6)          # корреляция Пирсона, при которой ρ Спирмена ≈ _r
    _z = np.random.default_rng(7).standard_normal((100, 2))
    _ys = _rp * _z[:, 0] + np.sqrt(max(1 - _rp ** 2, 0)) * _z[:, 1]

    def _dots(xs, ys, color):
        _rx, _ry = stats.rankdata(xs) - 1, stats.rankdata(ys) - 1
        _n = len(xs)
        _it = [f'<rect x="14" y="14" width="272" height="212" fill="none" stroke="#e6e5e0"/>']
        _it += [f'<circle cx="{20 + a / (_n - 1) * 260:.1f}" cy="{220 - b / (_n - 1) * 200:.1f}" r="3.4" fill="{color}" fill-opacity=".8"/>'
                for a, b in zip(_rx, _ry)]
        _it.append(f'<text x="150" y="238" text-anchor="middle" font-size="11" fill="{MUTED}">x-height →</text>')
        _it.append(f'<text x="9" y="120" text-anchor="middle" font-size="11" fill="{MUTED}" transform="rotate(-90 9 120)">толщина штриха →</text>')
        return svg(300, 242, _it)

    H(f"""<div class="rho-grid">
  <div class="chart">{_dots(_z[:, 0], _ys, "#9aa0a8")}<p class="note" style="margin:.3rem 0 0">Случайные точки: ρ Спирмена получилось {nfc(stats.spearmanr(_z[:, 0], _ys)[0], 2)}.</p></div>
  <div class="chart">{_dots(fonts.x_height.to_numpy(), fonts.stem.to_numpy(), "#2a78d6")}<p class="note" style="margin:.3rem 0 0">Наши шрифты: место по x-height и место по толщине штриха (ранги, как у Спирмена).</p></div>
</div>""")'''),
    _cell("CAT, fonts, mo, panel", r'''    sc_find = panel([{"type": "select", "name": "f", "label": "Найти шрифт", "grow": 0,
                      "groups": [[CAT[k][0], [[f, f] for f in sorted(fonts[fonts.category == k].family)]] for k in CAT]}],
                    {"f": "Inter"})
    mo.vstack([mo.md("Приближайте кнопками «+ / −» или двойным щелчком по месту; приближенный график можно "
                     "двигать мышью. **Нажмите на кружок**, и ниже откроется этот шрифт. Шрифт можно и найти по названию "
                     "в списке.").style({"color": "#5c6170", "font-size": ".95rem", "max-width": "68ch"}),
               sc_find], gap=0.3)''', "sc_find"),
    _cell("sc_find, scatter_widget, vals", r'''    sc_find_v = vals(sc_find).get("f") or "Inter"
    sc_plot = scatter_widget(sc_find_v)
    sc_plot''', "sc_find_v, sc_plot"),
    _cell("H, fonts, font_row, mo, sc_find_v, sc_plot, selected_of", r'''    _name = selected_of(sc_plot, sc_find_v) if sc_plot is not None else sc_find_v
    _r = fonts[fonts.family == _name]
    if sc_plot is None:
        _out = mo.md("_Интерактивный график загружается…_")
    elif not len(_r):
        _out = mo.md("")
    else:
        _out = H('<p class="note" style="margin:.4rem 0">Выбранный шрифт:</p>' + font_row(_r.iloc[0], "Hxlno шрифт") +
                 '<p class="note">Исследование целиком: <a href="report/" target="_top">отчёт</a> (код и формулы).</p>')
    _out'''),
]

PLAY = [
    _cell("H", r'''    H("""<div class="fs-sec" id="play"><h2>Попробуй сам</h2><h3>Толщина и ширина</h3>
<div class="text"><p>Этот текст набран вариативным шрифтом Roboto Flex: у него толщину штриха, ширину букв и даже высоту
строчных можно менять плавно. Подвигай ползунки и посмотри, как меняется характер текста. Текст можно исправить в поле.</p></div></div>""")'''),
    _cell("panel", r'''    pl = panel([{"type": "text", "name": "t", "label": "Текст", "wide": True},
                {"type": "range", "name": "wght", "label": "Толщина (вес)", "min": 100, "max": 1000, "step": 10, "live": True},
                {"type": "range", "name": "wdth", "label": "Ширина", "unit": "%", "min": 25, "max": 151, "step": 1, "live": True},
                {"type": "range", "name": "ytlc", "label": "Высота строчных", "min": 416, "max": 570, "step": 2, "live": True},
                {"type": "range", "name": "size", "label": "Кегль", "unit": "px", "min": 16, "max": 160, "step": 2, "live": True},
                {"type": "reset", "label": "Сбросить"}],
               {"t": "Шрифт как случайная величина", "wght": 400, "wdth": 100, "ytlc": 514, "size": 72})
    pl''', "pl"),
    _cell("H, esc, fonts, nfc, pl, vals", r'''    _s = fonts.stem
    _v = vals(pl)
    H(f"""<div class="specimen"><div style="font-family:'Roboto Flex','Golos Text',sans-serif;line-height:1.05;word-break:break-word;
font-size:{_v['size']}px;font-variation-settings:'wght' {_v['wght']},'wdth' {_v['wdth']},'YTLC' {_v['ytlc']}">{esc(_v['t'] or " ")}</div></div>
<p class="note">Для сравнения: у шрифтов из датасета (начертание Regular, вес 400) толщина штриха от {nfc(_s.min())} до {nfc(_s.max())} кегля,
медиана {nfc(_s.median())}. При кегле {_v['size']} px это от {nfc(_s.min() * _v['size'], 1)} до {nfc(_s.max() * _v['size'], 1)} px.</p>""")'''),
    _cell("CAT, H, fonts, mo, panel", r'''    _g = [[CAT[k][0], [[f, f] for f in sorted(fonts[fonts.category == k].family)]] for k in CAT]
    _has = set(fonts.family)
    _def = [n if n in _has else sorted(_has)[i * 7] for i, n in enumerate(("Inter", "Playfair", "Indie Flower"))]
    cmp = panel([{"type": "select", "name": f"f{i}", "label": f"Шрифт {i + 1}", "groups": _g, "grow": 1} for i in range(3)]
                + [{"type": "text", "name": "t", "label": "Текст", "maxlength": 40, "grow": 1}],
                {"f0": _def[0], "f1": _def[1], "f2": _def[2], "t": "Hxlno шрифт"})
    mo.vstack([H("""<h3>Сравнение шрифтов</h3><div class="text"><p>Выбери до трёх шрифтов из датасета
и введи любой текст. Все строки набраны одним кеглем: сразу видно, у какого шрифта строчные выше и штрих толще.
Пунктир показывает наши измерения: высоту строчных (x-height) и прописных.</p></div>"""), cmp], gap=0.2)''', "cmp"),
    _cell("H, cmp, font_row, fonts, vals", r'''    _v = vals(cmp)
    _txt = (_v.get("t") or "Hxlno").strip() or "Hxlno"
    H("".join(font_row(fonts[fonts.family == _v[f"f{i}"]].iloc[0], _txt) for i in range(3))
      + '<p class="note">Чёрная риска на полоске показывает медиану по всем шрифтам датасета.</p>')'''),
]

RNG = [
    _cell("H", r'''    H("""<div class="fs-sec" id="rng"><h2>Датчик: случайный шрифт, похожий на настоящий</h2>
<div class="text"><p>Датчик случайных чисел выдаёт значения, распределённые так же, как пропорции моих 100 шрифтов.
Сначала базовый датчик даёт равномерное число <i>U</i> от 0 до 1, потом метод превращает его в нужную величину.</p>
<p>Методов шесть. Два из них работают прямо с данными, остальные сначала подбирают модель: для x-height это
скошенное нормальное распределение, для толщины штриха логнормальное.</p>
<p><b>Квантильное преобразование</b> модель не использует. Оно берёт <i>U</i> и находит значение, ниже которого лежит
такая же доля шрифтов: если <i>U</i> = 0,3, датчик выдаёт значение, у которого 30 % шрифтов меньше.</p>
<p><b>Метод обратной функции</b> делает то же самое, только не по самим шрифтам, а по формуле модели:
<i>X</i> = <i>F</i><sup>−1</sup>(<i>U</i>), где <i>F</i> это функция распределения модели.</p>
<p><b>Бокс–Мюллер</b> из двух равномерных чисел сразу делает два нормальных: <i>Z</i> = √(−2 ln <i>U</i><sub>1</sub>) · cos 2π<i>U</i><sub>2</sub>.
Синус и косинус считаются медленно, поэтому придумали полярный метод.</p>
<p><b>Полярный метод Марсальи</b> обходится без синуса и косинуса: точка бросается в квадрат, остаются только точки внутри
круга, и из них получаются нормальные числа <i>Z</i>. Принимается около 78,5 % точек (π/4).</p>
<p><b>Метод отношений</b> (Киндерман и Монахан) бросает точку (<i>u</i>, <i>v</i>) в прямоугольник и оставляет её, только если
она попала в особую фигуру. Тогда отношение <i>v</i>/<i>u</i> оказывается нормальным. Принимается около 73 % точек.</p>
<p>У этих трёх методов нормальное <i>Z</i> потом переводится в модель, например для толщины штриха
<i>X</i> = θ + e<sup>μ + σ<i>Z</i></sup>.</p>
<p><b>Метод Неймана</b> снова обходится без модели. Он бросает точку под гистограмму шрифтов: случайное значение и случайную
высоту. Если точка оказалась ниже столбика, значение остаётся, если выше, бросок повторяется. Работает с любой формой
распределения, но большая часть бросков уходит впустую: принимается около 29 %.</p></div></div>""")'''),
    _cell("G, panel", r'''    rg = panel([{"type": "seg", "name": "var", "label": "Величина", "options": [["x-height", "x_height"], ["толщина штриха", "stem"]]},
                {"type": "select", "name": "method", "label": "Метод", "options": [[v, k] for k, v in G.METHOD_RU.items()], "grow": 1},
                {"type": "seg", "name": "base", "label": "Базовый датчик", "options": [[v.split(" (")[0], k] for k, v in G.BASE_RU.items()]},
                {"type": "range", "name": "n", "label": "Сколько чисел", "min": 100, "max": 20000, "step": 100, "thousands": True},
                {"type": "button", "name": "go", "label": "Сгенерировать заново"}],
               {"var": "x_height", "method": "polar", "base": "pcg64", "n": 1000, "go": 0})
    rg''', "rg"),
    _cell("G, H, MUTED, fonts, frame, legend, nfc, np, rg, svg, vals", r'''    _v = vals(rg)
    rg_var, rg_method, rg_base, rg_n = _v["var"], _v["method"], _v["base"], int(_v["n"])
    _real = fonts[rg_var].to_numpy(float)
    _fam = "skewnorm" if rg_var == "x_height" else "lognorm"
    _seed = 2026 + int(_v.get("go", 0))
    _x, _info = G.generate(_real, rg_n, method=rg_method, family=_fam, base=rg_base, seed=_seed)
    _c = G.compare(_real, _x)
    _lo, _hi = (0.15, 0.65) if rg_var == "x_height" else (0.0, 0.22)
    _step = 0.025 if rg_var == "x_height" else 0.01
    _e = np.arange(_lo, _hi + _step / 2, _step)
    _hr = np.histogram(_real, _e, density=True)[0]
    _hg = np.histogram(_x, _e, density=True)[0]
    _ymax = max(_hr.max(), _hg.max()) * 1.12
    _it, _X, _Y = frame(640, 290, 52, 16, 12, 46, (_lo, _hi), (0, _ymax),
                        ("x-height" if rg_var == "x_height" else "толщина штриха") + ", доли кегля", "плотность", xd=2, yd=0)
    for _a, _b, _h in zip(_e[:-1], _e[1:], _hr):
        _it.append(f'<rect x="{_X(_a) + .5:.1f}" y="{_Y(_h):.1f}" width="{_X(_b) - _X(_a) - 1:.1f}" height="{_Y(0) - _Y(_h):.1f}" fill="#bcd6f3"/>')
    _pts = []
    for _a, _b, _h in zip(_e[:-1], _e[1:], _hg):
        _pts += [f"{_X(_a):.1f},{_Y(_h):.1f}", f"{_X(_b):.1f},{_Y(_h):.1f}"]
    _it.append(f'<polyline points="{" ".join(_pts)}" fill="none" stroke="#eb6834" stroke-width="2"/>')
    _hist = svg(640, 290, _it, "Гистограмма: шрифты и датчик")

    _u = G.Uniform(rg_base, _seed)(2400)
    if rg_method in ("polar", "ratio", "neumann"):
        _v = 2 * _u.reshape(-1, 2) - 1
        _ok = (_v ** 2).sum(1) < 1
        _side = [f'<rect x="10" y="10" width="300" height="300" fill="none" stroke="#e6e5e0"/>',
                 f'<circle cx="160" cy="160" r="150" fill="none" stroke="{MUTED}"/>']
        _side += [f'<circle cx="{160 + a * 150:.1f}" cy="{160 - b * 150:.1f}" r="1.3" fill="{"#2a78d6" if k else "#eb6834"}"/>'
                  for (a, b), k in zip(_v, _ok)]
        _cap = "Полярный метод: синие точки внутри круга приняты, оранжевые в углах отброшены."
    else:
        _side = [f'<rect x="10" y="10" width="300" height="300" fill="none" stroke="#e6e5e0"/>']
        _side += [f'<circle cx="{10 + a * 300:.1f}" cy="{310 - b * 300:.1f}" r="1.3" fill="{"#eb6834" if rg_base == "randu" else "#2a78d6"}"/>'
                  for a, b in zip((6 * _u[1:-1] - 9 * _u[:-2]) % 1.0, _u[2:])]
        _cap = "Тройки базового датчика: у RANDU они ложатся на прямые, у хороших датчиков облако ровное."
    _n, _m = len(_real), len(_x)
    _crit = 1.358 * np.sqrt((_n + _m) / (_n * _m))
    _same = _c["ks_D"] < _crit
    H(f"""<div class="lab">
  <div class="chart">{_hist}{legend([(f"мои шрифты, {len(_real)} семейств", "#bcd6f3"), ("датчик", "#eb6834")])}</div>
  <div><div class="chart">{svg(320, 320, _side, "Точки базового датчика")}</div><p class="note" style="margin-top:.5rem">{_cap}</p></div>
</div>
<p class="readout">Датчик: среднее <b>{nfc(_c["gen"]["среднее"])}</b>, СКО <b>{nfc(_c["gen"]["СКО"])}</b>;
шрифты: среднее <b>{nfc(_c["real"]["среднее"])}</b>, СКО <b>{nfc(_c["real"]["СКО"])}</b>.
Расстояние Колмогорова между функциями распределения <b>{nfc(_c["ks_D"])}</b> при пороге <b>{nfc(_crit)}</b> (α = 0,05):
{"датчик и шрифты статистически не различаются" if _same else "датчик и шрифты различаются"}.
Доля принятых точек <b>{nfc(_info["accept"])}</b>{" (теория π/4 = 0,785)" if rg_method == "polar" else ""}.</p>""")'''),
    _cell("H", r'''    H("""<div class="fs-foot"><p>Быкова Кристина Денисовна, ИСУ 501322, команда 27, трек КТвД. Lab01, прикладная статистика, осень 2026:
доп. задание КТвД, датасет шрифтов, датчик случайных чисел, интерактив и этот сайт.
Отчёт: <a href="report/" target="_top">ноутбук со скрытым кодом</a>.</p><p>Шрифты: Google Fonts (SIL Open Font License).</p></div>""")'''),
]


def app_text() -> str:
    head = C.header(TITLE, CSS_FILE).replace('"scipy"]', '"scipy", "anywidget", "traitlets"]')
    style = _cell("mo", "    mo.Html(" + json.dumps("<style>" + CSS + "</style>", ensure_ascii=False) + ")")
    cells = [SETUP, style] + HERO + FONTS + PLAY + RNG
    return head + "\n\n".join(cells) + '\n\nif __name__ == "__main__":\n    app.run()\n'
