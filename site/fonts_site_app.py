# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "numpy", "pandas", "matplotlib", "scipy"]
# ///
import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium", app_title="Lab01 КТвД: шрифт как случайная величина", css_file="fonts_site.css", html_head_file="head.html")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = {"bg": "#f6f7f5", "card": "#ffffff", "ink": "#1a1d24", "ink2": "#5c6170", "line": "#dcdfd8", "acc": "#2a78d6", "acc2": "#a9c8ef", "soft": "#eceee9", "grid": "#e6e5e0", "c1": "#2a78d6", "c2": "#eb6834", "c3": "#1baf7a", "cover": "", "cover_ink": "", "head_font": "Golos Text"}
    STYLE = "@import url('https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&family=Roboto+Flex:opsz,wdth,wght,YTLC@8..144,25..151,100..1000,416..570&display=swap');\n:root{ --paper:#f6f7f5; --ink:#1a1d24; --muted:#5c6170; --rule:#dcdfd8;\n  --blue:#2a78d6; --orange:#eb6834; --straw:#d8c56a; --green:#1baf7a; --measure:68ch;\n  --marimo-text-font:\"Golos Text\",system-ui,sans-serif; --marimo-heading-font:\"Golos Text\",system-ui,sans-serif; }\nbody, #App, .mo-app, [data-testid=\"app\"]{background:var(--paper) !important;color:var(--ink)}\nbody, .markdown, .prose{font-family:\"Golos Text\",system-ui,-apple-system,\"Segoe UI\",sans-serif}\n.fs a{color:var(--blue);text-underline-offset:.18em}\n.fs code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em;background:#e9ebe6;padding:.08em .35em;border-radius:3px}\n.fs{font-size:1.0625rem;line-height:1.6;color:var(--ink)}\n.fs .text{max-width:var(--measure)}\n.fs p{margin:0 0 1rem !important}\n.fs, .fs *{font-family:\"Golos Text\",system-ui,sans-serif}\n.fs-hero{padding-top:clamp(2rem,6vw,5rem);padding-bottom:1rem}\n.fs-hero h1{font-family:\"Golos Text\",sans-serif !important;font-size:clamp(2.9rem,9.2vw,7.4rem) !important;line-height:.98 !important;letter-spacing:-.02em;margin:.4rem 0 1.6rem !important;font-weight:400}\n.fs-hero h1 .w{display:block !important}\n.fs-hero h1 span.l{transition:font-weight .5s cubic-bezier(.2,.7,.2,1)}\n.fs .lede{font-size:clamp(1.1rem,1.6vw,1.3rem);color:var(--muted);margin:0 0 1.4rem;max-width:var(--measure)}\n.fs .note{color:var(--muted);font-size:.95rem}\n.fs-sec{padding-top:3rem;border-top:1px solid var(--rule);margin-top:2rem}\n.fs h2{font-family:\"Golos Text\",sans-serif !important;font-size:clamp(1.7rem,3.4vw,2.6rem) !important;line-height:1.1 !important;font-weight:750 !important;letter-spacing:-.01em;margin:0 0 1rem !important;color:var(--ink)}\n.fs h3{font-family:\"Golos Text\",sans-serif !important;font-size:1.15rem !important;font-weight:650 !important;margin:1.6rem 0 .5rem !important;color:var(--ink)}\n.fs figure{margin:1.4rem 0}\n.fs figure img{width:100%;height:auto;background:#fff;border-radius:6px}\n.fs figcaption{color:var(--muted);font-size:.92rem;margin-top:.5rem;max-width:var(--measure)}\n.fs .chart{background:#fff;border-radius:8px;padding:.6rem}\n.fs .chart svg{display:block;width:100%;height:auto}\n.fs .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1.4rem 2rem;margin:1.6rem 0;max-width:900px}\n.fs .fact strong{display:block;font-size:2.4rem;line-height:1.05;font-weight:800;font-variant-numeric:tabular-nums}\n.fs .fact span{color:var(--muted);font-size:.95rem}\n.fs .legend{display:flex;flex-wrap:wrap;gap:.4rem 1rem;font-size:.88rem;color:var(--muted);margin:.5rem 0 0}\n.fs .sw{display:inline-block;width:.8em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}\n.fs .rho-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;max-width:820px}\n.fs .lab{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:1.6rem;align-items:start;margin-top:.6rem}\n.fs .readout{font-variant-numeric:tabular-nums;margin-top:.7rem;font-size:.95rem}\n.fs .readout b{font-weight:650}\n.fs .specimen{background:#fff;border-radius:8px;padding:1.2rem 1.4rem;overflow:hidden}\n.fs .cmp-row{background:#fff;border-radius:8px;padding:.8rem 1rem 1rem;margin:0 0 1rem}\n.fs .cmp-head{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;margin-bottom:.3rem}\n.fs .cmp-head b{font-weight:650}\n.fs .bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.6rem 1.4rem;margin-top:.6rem}\n.fs .bar{font-size:.85rem;color:var(--muted)}\n.fs .bar .track{position:relative;height:8px;border-radius:4px;background:#eceee9;margin-top:.25rem}\n.fs .bar .fill{position:absolute;left:0;top:0;bottom:0;border-radius:4px}\n.fs .bar .med{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--ink);opacity:.7}\n.fs .newfonts{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-top:.8rem}\n.fs .newfonts div.c{background:#fff;border-radius:8px;padding:.8rem 1rem}\n.fs .newfonts small{color:var(--muted);font-size:.82rem}\n.fs-foot{border-top:1px solid var(--rule);margin-top:2.5rem;padding:2rem 0 3rem;color:var(--muted);font-size:.95rem}\n.fs-foot p{max-width:var(--measure)}\n.fs-ctrl{font-size:.9rem;color:var(--muted)}\n@media (max-width:640px){.fs .rho-grid,.fs .lab{grid-template-columns:1fr}}\n"

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
    # marimo показывает каждый вывод отдельно, и стиль из одной ячейки не доходит до другой:
    # поэтому оформление кладётся прямо в каждый кусок HTML
    ST = f"<style>{STYLE}</style>"

    def fig(name):
        """Рисунок из выполненного ноутбука: локально встраивается, в браузере грузится по ссылке."""
        p = PUB / ASSETS / name
        try:
            src = "data:image/png;base64," + base64.b64encode(Path(str(p)).read_bytes()).decode()
        except Exception:
            src = str(p)
        return mo.Html(ST + f'<figure class="lab-fig"><img src="{src}" alt="" loading="lazy"></figure>')

    def table_html(h):
        return mo.Html(ST + f'<div class="lab-tbl">{h}</div>')

    def df_html(df, digits=4):
        """Таблица pandas в оформлении отчёта (без служебных колонок интерактивной таблицы)."""
        return table_html(df.to_html(index=False, border=0, float_format=lambda v: f"{v:.{digits}g}" if abs(v) < 1e-3 and v else f"{v:.{digits}f}"))

    def out_text(t):
        return mo.Html(ST + f'<pre class="lab-out">{t.replace("&", "&amp;").replace("<", "&lt;")}</pre>')

    def code_block(code):
        return mo.accordion({"Код этого раздела": mo.md(f"```python\n{code}\n```")})

    def plot_html(f):
        """Matplotlib → картинка; так рисунок одинаково выглядит локально и в браузере."""
        buf = io.BytesIO()
        f.savefig(buf, format="png", dpi=140, bbox_inches="tight")
        plt.close(f)
        return mo.Html(ST + f'<figure class="lab-fig live"><img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}" alt=""></figure>')

    def cards(items):
        """Карточки с числами: [(подпись, значение, пояснение), ...]."""
        cells = "".join(f'<div class="lab-card"><span>{a}</span><b>{b}</b><small>{c}</small></div>' for a, b, c in items)
        return mo.Html(ST + f'<div class="lab-cards">{cells}</div>')

    def section(*items):
        """Раздел отчёта в рамке-карточке."""
        return mo.vstack([mo.Html(ST)] + list(items), gap=0.6).style({
            "background": T["card"], "border": f"1px solid {T['line']}", "border-radius": "18px",
            "padding": "1.3rem 1.5rem 1.1rem", "box-shadow": "0 1px 2px rgba(0,0,0,.04), 0 6px 22px rgba(0,0,0,.05)"})

    def live(title, note, *controls):
        """Заголовок живого блока и его элементы управления, в цветной рамке."""
        acc = T["acc"]
        return mo.vstack([mo.Html(ST + f'<div class="lab-live"><span class="tag">живой блок</span><h4>{title}</h4><p>{note}</p></div>'),
                          mo.hstack(list(controls), wrap=True, justify="start", gap=1.2)], gap=0.5).style({
            "background": T["soft"], "border": f"1px solid {T['acc2']}", "border-left": f"6px solid {acc}",
            "border-radius": "16px", "padding": ".9rem 1.2rem 1rem"})

    def nf(v, d=3):
        return f"{v:.{d}f}"

    plt.rcParams.update({
        "figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
        "grid.color": T["grid"], "grid.linewidth": 0.8, "axes.edgecolor": T["ink2"], "axes.labelcolor": T["ink"],
        "xtick.color": T["ink2"], "ytick.color": T["ink2"], "legend.frameon": False, "lines.linewidth": 2,
        "axes.titlesize": 10.5, "axes.labelsize": 9.5, "legend.fontsize": 8.5, "font.size": 9.5,
    })

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
                f'style="font-family:Golos Text,system-ui,sans-serif">{"".join(items)}</svg>')

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

    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (CAT, CAT_RU, G, GRIDC, H, INK, MUTED, T, esc, fonts, frame, gfont, legend, nfc, svg, to_wght, to_ytlc,
            Path, PUB, base64, cards, code_block, df_html, fig, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, section, stats, table_html, types)


@app.cell(hide_code=True)
def _(mo):
    mo.Html("<style>@import url('https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&family=Roboto+Flex:opsz,wdth,wght,YTLC@8..144,25..151,100..1000,416..570&display=swap');\n:root{ --paper:#f6f7f5; --ink:#1a1d24; --muted:#5c6170; --rule:#dcdfd8;\n  --blue:#2a78d6; --orange:#eb6834; --straw:#d8c56a; --green:#1baf7a; --measure:68ch;\n  --marimo-text-font:\"Golos Text\",system-ui,sans-serif; --marimo-heading-font:\"Golos Text\",system-ui,sans-serif; }\nbody, #App, .mo-app, [data-testid=\"app\"]{background:var(--paper) !important;color:var(--ink)}\nbody, .markdown, .prose{font-family:\"Golos Text\",system-ui,-apple-system,\"Segoe UI\",sans-serif}\n.fs a{color:var(--blue);text-underline-offset:.18em}\n.fs code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em;background:#e9ebe6;padding:.08em .35em;border-radius:3px}\n.fs{font-size:1.0625rem;line-height:1.6;color:var(--ink)}\n.fs .text{max-width:var(--measure)}\n.fs p{margin:0 0 1rem !important}\n.fs, .fs *{font-family:\"Golos Text\",system-ui,sans-serif}\n.fs-hero{padding-top:clamp(2rem,6vw,5rem);padding-bottom:1rem}\n.fs-hero h1{font-family:\"Golos Text\",sans-serif !important;font-size:clamp(2.9rem,9.2vw,7.4rem) !important;line-height:.98 !important;letter-spacing:-.02em;margin:.4rem 0 1.6rem !important;font-weight:400}\n.fs-hero h1 .w{display:block !important}\n.fs-hero h1 span.l{transition:font-weight .5s cubic-bezier(.2,.7,.2,1)}\n.fs .lede{font-size:clamp(1.1rem,1.6vw,1.3rem);color:var(--muted);margin:0 0 1.4rem;max-width:var(--measure)}\n.fs .note{color:var(--muted);font-size:.95rem}\n.fs-sec{padding-top:3rem;border-top:1px solid var(--rule);margin-top:2rem}\n.fs h2{font-family:\"Golos Text\",sans-serif !important;font-size:clamp(1.7rem,3.4vw,2.6rem) !important;line-height:1.1 !important;font-weight:750 !important;letter-spacing:-.01em;margin:0 0 1rem !important;color:var(--ink)}\n.fs h3{font-family:\"Golos Text\",sans-serif !important;font-size:1.15rem !important;font-weight:650 !important;margin:1.6rem 0 .5rem !important;color:var(--ink)}\n.fs figure{margin:1.4rem 0}\n.fs figure img{width:100%;height:auto;background:#fff;border-radius:6px}\n.fs figcaption{color:var(--muted);font-size:.92rem;margin-top:.5rem;max-width:var(--measure)}\n.fs .chart{background:#fff;border-radius:8px;padding:.6rem}\n.fs .chart svg{display:block;width:100%;height:auto}\n.fs .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1.4rem 2rem;margin:1.6rem 0;max-width:900px}\n.fs .fact strong{display:block;font-size:2.4rem;line-height:1.05;font-weight:800;font-variant-numeric:tabular-nums}\n.fs .fact span{color:var(--muted);font-size:.95rem}\n.fs .legend{display:flex;flex-wrap:wrap;gap:.4rem 1rem;font-size:.88rem;color:var(--muted);margin:.5rem 0 0}\n.fs .sw{display:inline-block;width:.8em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}\n.fs .rho-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;max-width:820px}\n.fs .lab{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:1.6rem;align-items:start;margin-top:.6rem}\n.fs .readout{font-variant-numeric:tabular-nums;margin-top:.7rem;font-size:.95rem}\n.fs .readout b{font-weight:650}\n.fs .specimen{background:#fff;border-radius:8px;padding:1.2rem 1.4rem;overflow:hidden}\n.fs .cmp-row{background:#fff;border-radius:8px;padding:.8rem 1rem 1rem;margin:0 0 1rem}\n.fs .cmp-head{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;margin-bottom:.3rem}\n.fs .cmp-head b{font-weight:650}\n.fs .bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.6rem 1.4rem;margin-top:.6rem}\n.fs .bar{font-size:.85rem;color:var(--muted)}\n.fs .bar .track{position:relative;height:8px;border-radius:4px;background:#eceee9;margin-top:.25rem}\n.fs .bar .fill{position:absolute;left:0;top:0;bottom:0;border-radius:4px}\n.fs .bar .med{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--ink);opacity:.7}\n.fs .newfonts{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-top:.8rem}\n.fs .newfonts div.c{background:#fff;border-radius:8px;padding:.8rem 1rem}\n.fs .newfonts small{color:var(--muted);font-size:.82rem}\n.fs-foot{border-top:1px solid var(--rule);margin-top:2.5rem;padding:2rem 0 3rem;color:var(--muted);font-size:.95rem}\n.fs-foot p{max-width:var(--measure)}\n.fs-ctrl{font-size:.9rem;color:var(--muted)}\n@media (max-width:640px){.fs .rho-grid,.fs .lab{grid-template-columns:1fr}}\n</style>")
    return


@app.cell(hide_code=True)
def _(mo):
    reroll = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Перебросить толщину букв")
    return (reroll,)


@app.cell(hide_code=True)
def _(H, fonts, mo, np, reroll):
    _rng = np.random.default_rng(int(reroll.value) * 7 + 3)
    _st = np.sort(fonts["stem"].to_numpy(float))

    def _wt(s):   # толщина штриха настоящего шрифта → вес Golos Text 400…900 по месту среди шрифтов
        return int(400 + 500 * np.searchsorted(_st, s) / len(_st))

    _words = []
    for _w in ("Шрифт как", "случайная", "величина"):
        _words.append('<span class="w">' + "".join(
            ch if ch == " " else f'<span class="l" style="font-weight:{_wt(_rng.choice(_st))}">{ch}</span>' for ch in _w) + "</span>")
    mo.vstack([H(f"""<div class="fs-hero">
  <p class="note" style="margin:0"><a href="../" target="_top">← Lab01: обе части работы</a> · <a href="report/" target="_top">отчёт</a></p>
  <h1 aria-label="Шрифт как случайная величина">{"".join(_words)}</h1>
  <p class="lede">Это доп. задание КТвД к лабораторной по прикладной статистике. Я собрала датасет шрифтов
  с Google Fonts (в анализе их {len(fonts)}: часть выбрана мной, остальные добавлены случайным отбором, по 20 в каждой категории)
  и измерила у каждого две вещи: высоту строчных букв (x-height) и толщину штриха.
  Эти размеры нельзя вычислить по формуле: у каждого шрифта они свои, поэтому их можно изучать как случайные величины.</p>
  <p class="lede">Ниже то, что получилось, и интерактивный датчик, который выдаёт случайные числа, похожие на настоящие данные.
  Нажми кнопку: толщина каждой буквы в заголовке выпадет случайно, из тех же значений, что у настоящих шрифтов.</p>
</div>"""), reroll])
    return


@app.cell(hide_code=True)
def _(H, fonts, nfc, stats):
    _rho = stats.spearmanr(fonts.x_height, fonts.stem)[0]
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
с выбранной силой связи, справа наши шрифты (ρ = {nfc(_rho, 2)}).</p></div>""")
    return


@app.cell(hide_code=True)
def _(mo):
    rho_s = mo.ui.slider(start=-1, stop=1, step=0.05, value=0.4, label="Сила связи ρ", show_value=True)
    rho_preset = mo.ui.radio(options={"нет связи": 0.0, "как у нас": 0.4, "сильная": 0.9, "свой (ползунок)": None},
                             value="свой (ползунок)", inline=True)
    mo.hstack([rho_s, rho_preset], justify="start", gap=2)
    return (rho_preset, rho_s,)


@app.cell(hide_code=True)
def _(H, MUTED, fonts, nfc, np, rho_preset, rho_s, stats, svg):
    _r = rho_preset.value if rho_preset.value is not None else float(rho_s.value)
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
</div>""")
    return


@app.cell(hide_code=True)
def _(CAT, mo):
    sc_cats = mo.ui.multiselect(options=[v[0] for v in CAT.values()], value=[v[0] for v in CAT.values()], label="Категории")
    sc_x = mo.ui.range_slider(start=0.15, stop=0.65, step=0.01, value=[0.15, 0.65], label="x-height: от и до", show_value=True)
    sc_y = mo.ui.range_slider(start=0.0, stop=0.44, step=0.01, value=[0.0, 0.44], label="толщина штриха: от и до", show_value=True)
    sc_find = mo.ui.text(placeholder="например, Inter", label="Найти шрифт")
    mo.vstack([mo.md("Приближайте график ползунками «от и до»: когда точек на экране немного, у них появляются названия шрифтов. "
                     "Наведите на точку, чтобы увидеть подробности.").style({"color": "#5c6170", "font-size": ".95rem"}),
               mo.hstack([sc_cats, sc_find], justify="start", gap=1.5, wrap=True),
               mo.hstack([sc_x, sc_y], justify="start", gap=1.5, wrap=True)], gap=0.5)
    return (sc_cats, sc_find, sc_x, sc_y,)


@app.cell(hide_code=True)
def _(CAT, CAT_RU, H, INK, esc, fonts, frame, legend, nfc, sc_cats, sc_find, sc_x, sc_y, svg):
    _d = fonts[fonts.category.isin([CAT_RU[c] for c in sc_cats.value])]
    _xl, _yl = tuple(sc_x.value), tuple(sc_y.value)
    if _xl[1] - _xl[0] < 0.02:
        _xl = (_xl[0] - 0.01, _xl[0] + 0.01)
    if _yl[1] - _yl[0] < 0.02:
        _yl = (_yl[0] - 0.01, _yl[0] + 0.01)
    _in = _d[_d.x_height.between(*_xl) & _d.stem.between(*_yl)]
    _items, _X, _Y = frame(640, 400, 64, 18, 14, 48, _xl, _yl, "x-height, доли кегля", "толщина штриха, доли кегля")
    _q = (sc_find.value or "").strip().lower()
    _lab = len(_in) <= 30
    for _, _r in _in.iterrows():
        _ru, _col = CAT[_r.category]
        _hit = bool(_q) and _q in _r.family.lower()
        _tip = f"{_r.family} · {_ru} · x-height {nfc(_r.x_height)} · штрих {nfc(_r.stem)}"
        _items.append(f'<circle cx="{_X(_r.x_height):.1f}" cy="{_Y(_r.stem):.1f}" r="{8 if _hit else 6}" fill="{_col}" '
                      f'stroke="{INK if _hit else "#fff"}" stroke-width="{2 if _hit else 1.2}"><title>{esc(_tip)}</title></circle>')
        if _lab or _hit:
            _items.append(f'<text x="{_X(_r.x_height) + 9:.1f}" y="{_Y(_r.stem) + 4:.1f}" font-size="{12 if _hit else 10.5}" '
                          f'fill="{INK}" font-weight="{600 if _hit else 400}">{esc(_r.family)}</text>')
    _counts = _d.category.value_counts()
    _info = "весь график" if (_xl, _yl) == ((0.15, 0.65), (0.0, 0.44)) else "приближено"
    H(f"""<div class="chart" style="max-width:820px">
  <p class="note" style="margin:.2rem .4rem">{_info} · {len(_in)} точек</p>
  {svg(640, 400, _items, "Точечный график: x-height и толщина штриха по шрифтам")}
  {legend([(f"{v[0]} ({_counts.get(k, 0)})", v[1]) for k, v in CAT.items() if v[0] in sc_cats.value])}
</div>
<p class="note">Исследование целиком: <a href="report/" target="_top">отчёт</a> (код и формулы).</p>""")
    return


@app.cell(hide_code=True)
def _(H):
    H("""<div class="fs-sec" id="play"><h2>Попробуй сам</h2><h3>Толщина и ширина</h3>
<div class="text"><p>Этот текст набран вариативным шрифтом Roboto Flex: у него толщину штриха, ширину букв и даже высоту
строчных можно менять плавно. Подвигай ползунки и посмотри, как меняется характер текста. Текст можно исправить в поле.</p></div></div>""")
    return


@app.cell(hide_code=True)
def _(mo):
    pl_text = mo.ui.text(value="Шрифт как случайная величина", label="Текст", full_width=True)
    pl_wght = mo.ui.slider(start=100, stop=1000, step=10, value=400, label="Толщина (вес)", show_value=True)
    pl_wdth = mo.ui.slider(start=25, stop=151, step=1, value=100, label="Ширина, %", show_value=True)
    pl_ytlc = mo.ui.slider(start=416, stop=570, step=2, value=514, label="Высота строчных", show_value=True)
    pl_size = mo.ui.slider(start=16, stop=160, step=2, value=72, label="Кегль, px", show_value=True)
    mo.vstack([pl_text, mo.hstack([pl_wght, pl_wdth, pl_ytlc, pl_size], justify="start", gap=1.5, wrap=True)], gap=0.5)
    return (pl_size, pl_text, pl_wdth, pl_wght, pl_ytlc,)


@app.cell(hide_code=True)
def _(H, esc, fonts, nfc, pl_size, pl_text, pl_wdth, pl_wght, pl_ytlc):
    _s = fonts.stem
    H(f"""<div class="specimen"><div style="font-family:'Roboto Flex','Golos Text',sans-serif;line-height:1.05;word-break:break-word;
font-size:{pl_size.value}px;font-variation-settings:'wght' {pl_wght.value},'wdth' {pl_wdth.value},'YTLC' {pl_ytlc.value}">{esc(pl_text.value or " ")}</div></div>
<p class="note">Для сравнения: у шрифтов из датасета (начертание Regular, вес 400) толщина штриха от {nfc(_s.min())} до {nfc(_s.max())} кегля,
медиана {nfc(_s.median())}. При кегле {pl_size.value} px это от {nfc(_s.min() * pl_size.value, 1)} до {nfc(_s.max() * pl_size.value, 1)} px.</p>""")
    return


@app.cell(hide_code=True)
def _(CAT, H, fonts, mo):
    _opts = {f"{r.family} · {CAT[r.category][0]}": r.family for r in fonts.sort_values(["category", "family"]).itertuples()}
    _key = {v: k for k, v in _opts.items()}
    _pick = lambda name, i: _key.get(name, list(_opts)[i * 7])   # noqa: E731
    cmp1 = mo.ui.dropdown(options=_opts, value=_pick("Inter", 0), label="Шрифт 1", searchable=True)
    cmp2 = mo.ui.dropdown(options=_opts, value=_pick("Playfair", 1), label="Шрифт 2", searchable=True)
    cmp3 = mo.ui.dropdown(options=_opts, value=_pick("Indie Flower", 2), label="Шрифт 3", searchable=True)
    cmp_text = mo.ui.text(value="Hxlno шрифт", label="Текст", max_length=40)
    mo.vstack([H("""<h3>Сравнение шрифтов</h3><div class="text"><p>Выбери до трёх шрифтов из датасета
и введи любой текст. Все строки набраны одним кеглем: сразу видно, у какого шрифта строчные выше и штрих толще.
Пунктир показывает наши измерения: высоту строчных (x-height) и прописных.</p></div>"""),
               mo.hstack([cmp1, cmp2, cmp3, cmp_text], justify="start", gap=1.2, wrap=True)], gap=0.4)
    return (cmp1, cmp2, cmp3, cmp_text,)


@app.cell(hide_code=True)
def _(CAT, H, cmp1, cmp2, cmp3, cmp_text, esc, fonts, gfont, nfc, svg):
    _txt = (cmp_text.value or "Hxlno").strip() or "Hxlno"
    _keys = [("x_height", "x-height", 3), ("stem", "толщина штриха", 3), ("contrast", "контраст «o»", 2), ("width_o", "ширина «o» / x-height", 3)]
    _rg = {k: (fonts[k].min(), fonts[k].max(), fonts[k].median()) for k, _, _ in _keys}

    def _bar(r, k, lab, d):
        lo, hi, med = _rg[k]
        pos = lambda v: max(0, min(1, (v - lo) / (hi - lo))) * 100   # noqa: E731
        return (f'<div class="bar">{lab}: <b style="color:#1a1d24">{nfc(r[k], d)}</b><div class="track">'
                f'<div class="fill" style="width:{pos(r[k]):.1f}%;background:{CAT[r.category][1]}"></div>'
                f'<div class="med" style="left:{pos(med):.1f}%" title="медиана датасета"></div></div></div>')

    _rows = []
    for _name in (cmp1.value, cmp2.value, cmp3.value):
        _r = fonts[fonts.family == _name].iloc[0]
        _fs = max(14.0, min(72.0, 72 * 620 / (0.62 * 72 * len(_txt))))
        _base = round(_fs * max(1.0, _r.cap_height) + 14)
        _h = _base + 16
        _lines = [f'<line x1="0" x2="640" y1="{_base}" y2="{_base}" stroke="#5c6170"/>',
                  f'<line x1="0" x2="640" y1="{_base - _r.x_height * _fs:.1f}" y2="{_base - _r.x_height * _fs:.1f}" stroke="#eb6834" stroke-dasharray="5 4"/>',
                  f'<line x1="0" x2="640" y1="{_base - _r.cap_height * _fs:.1f}" y2="{_base - _r.cap_height * _fs:.1f}" stroke="#1baf7a" stroke-dasharray="5 4"/>',
                  f'<text x="8" y="{_base}" font-family="\'{esc(_name)}\', serif" font-size="{_fs:.1f}" fill="#1a1d24" '
                  f'style="font-family:\'{esc(_name)}\',serif">{esc(_txt)}</text>']
        _rows.append(f"""{gfont(_name, _txt)}<div class="cmp-row"><div class="cmp-head"><b>{esc(_name)}</b>
<span class="note"><span style="color:#eb6834">- - x-height {nfc(_r.x_height)}</span>&nbsp;&nbsp;
<span style="color:#1baf7a">- - прописные {nfc(_r.cap_height)}</span>&nbsp;&nbsp;{CAT[_r.category][0]}</span></div>
{svg(640, _h, _lines, _txt + " шрифтом " + _name)}
<div class="bars">{"".join(_bar(_r, k, lab, d) for k, lab, d in _keys)}</div></div>""")
    H("".join(_rows) + '<p class="note">Чёрная риска на полоске показывает медиану по всем шрифтам датасета.</p>')
    return


@app.cell(hide_code=True)
def _(H):
    H("""<div class="fs-sec" id="rng"><h2>Датчик: случайный шрифт, похожий на настоящий</h2>
<div class="text"><p>Датчик случайных чисел выдаёт значения, распределённые так же, как пропорции моих 100 шрифтов.
Сначала базовый датчик даёт равномерное число <i>U</i> от 0 до 1, потом метод превращает его в нужную величину.</p>
<p><b>Полярный метод Марсальи:</b> точка бросается в квадрат, остаются только точки внутри круга, и из них
получаются нормальные числа <i>Z</i>. Дальше <i>Z</i> переводится в модель: для x-height это скошенное нормальное
распределение, для толщины штриха логнормальное <i>X</i> = θ + e<sup>μ + σ<i>Z</i></sup>.
<b>Квантильный метод</b> модель не использует: он берёт <i>U</i> и находит значение, ниже которого лежит
такая же доля шрифтов.</p></div></div>""")
    return


@app.cell(hide_code=True)
def _(G, mo):
    rg_var = mo.ui.radio(options={"x-height": "x_height", "толщина штриха": "stem"}, value="x-height", label="Величина", inline=True)
    rg_method = mo.ui.dropdown(options={v: k for k, v in G.METHOD_RU.items()}, value=G.METHOD_RU["polar"], label="Метод")
    rg_base = mo.ui.radio(options={v: k for k, v in G.BASE_RU.items()}, value=G.BASE_RU["pcg64"], label="Базовый датчик", inline=True)
    rg_n = mo.ui.slider(start=100, stop=20000, step=100, value=1000, label="Сколько чисел", show_value=True)
    rg_go = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Сгенерировать заново")
    mo.vstack([mo.hstack([rg_var, rg_method], justify="start", gap=2, wrap=True), rg_base,
               mo.hstack([rg_n, rg_go], justify="start", gap=2, align="end")], gap=0.6)
    return (rg_base, rg_go, rg_method, rg_n, rg_var,)


@app.cell(hide_code=True)
def _(G, H, MUTED, fonts, frame, legend, nfc, np, rg_base, rg_go, rg_method, rg_n, rg_var, svg):
    _real = fonts[rg_var.value].to_numpy(float)
    _fam = "skewnorm" if rg_var.value == "x_height" else "lognorm"
    _seed = 2026 + int(rg_go.value)
    _x, _info = G.generate(_real, rg_n.value, method=rg_method.value, family=_fam, base=rg_base.value, seed=_seed)
    _c = G.compare(_real, _x)
    _lo, _hi = (0.15, 0.65) if rg_var.value == "x_height" else (0.0, 0.22)
    _step = 0.025 if rg_var.value == "x_height" else 0.01
    _e = np.arange(_lo, _hi + _step / 2, _step)
    _hr = np.histogram(_real, _e, density=True)[0]
    _hg = np.histogram(_x, _e, density=True)[0]
    _ymax = max(_hr.max(), _hg.max()) * 1.12
    _it, _X, _Y = frame(640, 290, 52, 16, 12, 46, (_lo, _hi), (0, _ymax),
                        ("x-height" if rg_var.value == "x_height" else "толщина штриха") + ", доли кегля", "плотность", xd=2, yd=0)
    for _a, _b, _h in zip(_e[:-1], _e[1:], _hr):
        _it.append(f'<rect x="{_X(_a) + .5:.1f}" y="{_Y(_h):.1f}" width="{_X(_b) - _X(_a) - 1:.1f}" height="{_Y(0) - _Y(_h):.1f}" fill="#bcd6f3"/>')
    _pts = []
    for _a, _b, _h in zip(_e[:-1], _e[1:], _hg):
        _pts += [f"{_X(_a):.1f},{_Y(_h):.1f}", f"{_X(_b):.1f},{_Y(_h):.1f}"]
    _it.append(f'<polyline points="{" ".join(_pts)}" fill="none" stroke="#eb6834" stroke-width="2"/>')
    _hist = svg(640, 290, _it, "Гистограмма: шрифты и датчик")

    _u = G.Uniform(rg_base.value, _seed)(2400)
    if rg_method.value in ("polar", "ratio", "neumann"):
        _v = 2 * _u.reshape(-1, 2) - 1
        _ok = (_v ** 2).sum(1) < 1
        _side = [f'<rect x="10" y="10" width="300" height="300" fill="none" stroke="#e6e5e0"/>',
                 f'<circle cx="160" cy="160" r="150" fill="none" stroke="{MUTED}"/>']
        _side += [f'<circle cx="{160 + a * 150:.1f}" cy="{160 - b * 150:.1f}" r="1.3" fill="{"#2a78d6" if k else "#eb6834"}"/>'
                  for (a, b), k in zip(_v, _ok)]
        _cap = "Полярный метод: синие точки внутри круга приняты, оранжевые в углах отброшены."
    else:
        _side = [f'<rect x="10" y="10" width="300" height="300" fill="none" stroke="#e6e5e0"/>']
        _side += [f'<circle cx="{10 + a * 300:.1f}" cy="{310 - b * 300:.1f}" r="1.3" fill="{"#eb6834" if rg_base.value == "randu" else "#2a78d6"}"/>'
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
Доля принятых точек <b>{nfc(_info["accept"])}</b>{" (теория π/4 = 0,785)" if rg_method.value == "polar" else ""}.</p>""")
    return


@app.cell(hide_code=True)
def _(G, H, esc, fonts, nfc, rg_base, rg_go, to_wght, to_ytlc):
    _seed = 99 + int(rg_go.value)
    _xs = G.generate(fonts.x_height.to_numpy(float), 6, method="polar", family="skewnorm", base=rg_base.value, seed=_seed)[0]
    _ss = G.generate(fonts.stem.to_numpy(float), 6, method="polar", family="lognorm", base=rg_base.value, seed=_seed + 1)[0]
    _c = "".join(
        f'<div class="c"><div style="font-family:\'Roboto Flex\',sans-serif;font-size:58px;line-height:1.1;'
        f'font-variation-settings:\'wght\' {to_wght(s):.0f},\'YTLC\' {to_ytlc(x):.0f}">Hxlno</div>'
        f'<small>x-height {nfc(x)} · штрих {nfc(s)}</small></div>' for x, s in zip(_xs, _ss))
    H(f"""<h3>Шесть «новых» шрифтов</h3><div class="text"><p>Датчик выдал шесть пар (x-height, толщина штриха), и они наложены
на вариативный Roboto Flex: толщина задаёт вес, x-height задаёт высоту строчных. Кнопка «Сгенерировать заново» даёт новые шрифты.</p></div>
<div class="newfonts">{_c}</div>
<p class="note" style="margin-top:1rem">Полная версия датчика на marimo: шесть методов, четыре величины шрифтов и таблица сравнения:
<a href="datchik/" target="_top">датчик</a>.</p>
<div class="fs-foot"><p>Быкова Кристина Денисовна, ИСУ 501322, команда 27, трек КТвД. Lab01, прикладная статистика, осень 2026:
доп. задание КТвД, датасет шрифтов, датчик случайных чисел, интерактив и этот сайт.
Отчёт: <a href="report/" target="_top">ноутбук со скрытым кодом</a>.</p><p>Шрифты: Google Fonts (SIL Open Font License).</p></div>""")
    return


if __name__ == "__main__":
    app.run()
