# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "numpy", "pandas", "matplotlib", "scipy", "anywidget", "traitlets"]
# ///
import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium", app_title="Lab01 КТвД: шрифт как случайная величина", css_file="fonts_site.css", html_head_file="head.html")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    T = {"bg": "#f6f7f5", "card": "#ffffff", "ink": "#1a1d24", "ink2": "#5c6170", "line": "#dcdfd8", "acc": "#2a78d6", "acc2": "#a9c8ef", "soft": "#eceee9", "grid": "#e6e5e0", "c1": "#2a78d6", "c2": "#eb6834", "c3": "#1baf7a", "cover": "", "cover_ink": "", "head_font": "Golos Text"}
    STYLE = ":root{ --paper:#f6f7f5; --ink:#1a1d24; --muted:#5c6170; --rule:#dcdfd8;\n  --blue:#2a78d6; --orange:#eb6834; --straw:#d8c56a; --green:#1baf7a; --measure:68ch;\n  --marimo-text-font:Onest,system-ui,sans-serif; --marimo-heading-font:Unbounded,Onest,sans-serif; }\nbody, #App, .mo-app, [data-testid=\"app\"]{background:var(--paper) !important;color:var(--ink)}\nbody, .markdown, .prose{font-family:Onest,system-ui,-apple-system,\"Segoe UI\",sans-serif}\n.fs a{color:var(--blue);text-underline-offset:.18em}\n.fs code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em;background:#e9ebe6;padding:.08em .35em;border-radius:3px}\n.fs{font-size:1.0625rem;line-height:1.6;color:var(--ink)}\n.fs .text{max-width:var(--measure)}\n.fs p{margin:0 0 1rem !important}\n.fs, .fs p, .fs a, .fs li, .fs b, .fs i, .fs .note, .fs .lede, .fs .bar, .fs .cmp-head, .fs figcaption, .fs .readout, .fs .legend{font-family:Onest,system-ui,sans-serif}\n.fs-hero h1 .l{font-family:\"Roboto Flex\",sans-serif}\n.fs-hero{padding-top:clamp(2rem,6vw,5rem);padding-bottom:1rem}\n.fs-hero h1{font-family:\"Roboto Flex\",sans-serif !important;font-size:clamp(2.9rem,9.2vw,7.4rem) !important;line-height:.98 !important;letter-spacing:-.02em;margin:.4rem 0 1.6rem !important;font-weight:400}\n.fs-hero h1 .w{display:block !important}\n.fs-hero h1 span.l{transition:font-weight .5s cubic-bezier(.2,.7,.2,1)}\n.fs .lede{font-size:clamp(1.1rem,1.6vw,1.3rem);color:var(--muted);margin:0 0 1.4rem;max-width:var(--measure)}\n.fs .note{color:var(--muted);font-size:.95rem}\n.fs-sec{padding-top:3rem;border-top:1px solid var(--rule);margin-top:2rem}\n.fs h2{font-family:Unbounded,Onest,sans-serif !important;font-size:clamp(1.6rem,3.2vw,2.4rem) !important;line-height:1.15 !important;font-weight:600 !important;letter-spacing:-.01em;margin:0 0 1rem !important;color:var(--ink)}\n.fs h3{font-family:Unbounded,Onest,sans-serif !important;font-size:1.1rem !important;font-weight:550 !important;margin:1.6rem 0 .5rem !important;color:var(--ink)}\n.fs figure{margin:1.4rem 0}\n.fs figure img{width:100%;height:auto;background:#fff;border-radius:6px}\n.fs figcaption{color:var(--muted);font-size:.92rem;margin-top:.5rem;max-width:var(--measure)}\n.fs .chart{background:#fff;border-radius:8px;padding:.6rem}\n.fs .chart svg{display:block;width:100%;height:auto}\n.fs .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1.4rem 2rem;margin:1.6rem 0;max-width:900px}\n.fs .fact strong{display:block;font-family:Unbounded,Onest,sans-serif;font-size:2.2rem;line-height:1.1;font-weight:600;font-variant-numeric:tabular-nums}\n.fs .fact span{color:var(--muted);font-size:.95rem}\n.fs .legend{display:flex;flex-wrap:wrap;gap:.4rem 1rem;font-size:.88rem;color:var(--muted);margin:.5rem 0 0}\n.fs .sw{display:inline-block;width:.8em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}\n.fs .rho-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;max-width:820px}\n.fs .lab{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:1.6rem;align-items:start;margin-top:.6rem}\n.fs .readout{font-variant-numeric:tabular-nums;margin-top:.7rem;font-size:.95rem}\n.fs .readout b{font-weight:650}\n.fs .specimen{background:#fff;border-radius:8px;padding:1.2rem 1.4rem;overflow:hidden}\n.fs .cmp-row{background:#fff;border-radius:8px;padding:.8rem 1rem 1rem;margin:0 0 1rem}\n.fs .cmp-head{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;margin-bottom:.3rem}\n.fs .cmp-head b{font-weight:650}\n.fs .bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.6rem 1.4rem;margin-top:.6rem}\n.fs .bar{font-size:.85rem;color:var(--muted)}\n.fs .bar .track{position:relative;height:8px;border-radius:4px;background:#eceee9;margin-top:.25rem}\n.fs .bar .fill{position:absolute;left:0;top:0;bottom:0;border-radius:4px}\n.fs .bar .med{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--ink);opacity:.7}\n.fs .newfonts{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-top:.8rem}\n.fs .newfonts div.c{background:#fff;border-radius:8px;padding:.8rem 1rem}\n.fs .newfonts small{color:var(--muted);font-size:.82rem}\n.fs-foot{border-top:1px solid var(--rule);margin-top:2.5rem;padding:2rem 0 3rem;color:var(--muted);font-size:.95rem}\n.fs-foot p{max-width:var(--measure)}\n.fs-ctrl{font-size:.9rem;color:var(--muted)}\n@media (max-width:640px){.fs .rho-grid,.fs .lab{grid-template-columns:1fr}}\n"

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
        return mo.Html(ST + f'<figure class="lab-fig" tabindex="0" title="Нажмите, чтобы увеличить"><img src="{src}" alt="" loading="lazy"></figure>')

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
        return mo.Html(ST + f'<figure class="lab-fig live" tabindex="0" title="Нажмите, чтобы увеличить"><img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}" alt=""></figure>')

    def cards(items):
        """Карточки с числами: [(подпись, значение, пояснение), ...]."""
        cells = "".join(f'<div class="lab-card"><span>{a}</span><b>{b}</b><small>{c}</small></div>' for a, b, c in items)
        return mo.Html(ST + f'<div class="lab-cards">{cells}</div>')

    def section(*items):
        """Раздел отчёта в рамке-карточке."""
        return mo.vstack([mo.Html(ST)] + list(items), gap=0.6).style(T.get("section_style") or {
            "background": T["card"], "border": f"1px solid {T['line']}", "border-radius": "18px",
            "padding": "1.3rem 1.5rem 1.1rem", "box-shadow": "0 1px 2px rgba(0,0,0,.04), 0 6px 22px rgba(0,0,0,.05)"})

    def live(title, note, *controls):
        """Заголовок живого блока и его элементы управления, в цветной рамке."""
        acc = T["acc"]
        return mo.vstack([mo.Html(ST + f'<div class="lab-live"><span class="tag">живой блок</span><h4>{title}</h4><p>{note}</p></div>'),
                          mo.hstack(list(controls), wrap=True, justify="start", gap=1.2)], gap=0.5).style(T.get("live_style") or {
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

    # свои элементы (anywidget): большая кнопка и график с приближением и щелчком; без anywidget всё работает на элементах marimo
    _WJ = {"scatter": "// Точечный график шрифтов для marimo (anywidget): приближение, сдвиг, подсказки, щелчок по точке выбирает шрифт.\nfunction render({ model, el }) {\n  const NS = \"http://www.w3.org/2000/svg\", SW = 640, SH = 390, pad = { l: 58, r: 16, t: 14, b: 50 };\n  const P = model.get(\"points\"), CAT = model.get(\"cats\");\n  const XL = model.get(\"xlabel\") || \"x-height, доли кегля\", YL = model.get(\"ylabel\") || \"толщина штриха, доли кегля\";\n  const XN = model.get(\"xname\") || \"x-height\", YN = model.get(\"yname\") || \"штрих\", ALWAYS = !!model.get(\"labels\"), PICK = model.get(\"pickable\") !== false;\n  const nf = (v, d = 3) => v.toFixed(d).replace(\".\", \",\");\n  const mk = (tag, attrs = {}) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };\n  const h = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt) e.textContent = txt; return e; };\n\n  const root = h(\"div\", \"fsc\");\n  const bar = h(\"div\", \"zoombar\");\n  const bIn = h(\"button\", \"\", \"+\"), bOut = h(\"button\", \"\", \"−\"), bAll = h(\"button\", \"\", \"Весь график\"), info = h(\"span\", \"note\");\n  bIn.title = \"Приблизить\"; bOut.title = \"Отдалить\";\n  bar.append(bIn, bOut, bAll, info);\n  const box = h(\"div\", \"box\"), sc = mk(\"svg\", { viewBox: `0 0 ${SW} ${SH}` }), tip = h(\"div\", \"tip\"), hint = h(\"div\", \"hint\", \"Чтобы приблизить, держите Ctrl (⌘) и крутите колесо\");\n  box.append(sc, tip, hint);\n  const legend = h(\"div\", \"legend\");\n  root.append(bar, box, legend);\n  el.append(root);\n\n  const xs = P.map(p => p.x), ys = P.map(p => p.s), xr = Math.max(...xs) - Math.min(...xs) || 1, yr = Math.max(...ys) - Math.min(...ys) || 1;\n  const FULL = P.length ? { x: [Math.min(...xs) - xr * .04, Math.max(...xs) + xr * .04],\n                            y: [Math.min(0, Math.min(...ys) - yr * .04), Math.max(...ys) + yr * .08] } : { x: [0, 1], y: [0, 1] };\n  let V = { x: [...FULL.x], y: [...FULL.y] };\n  const X = v => pad.l + (v - V.x[0]) / (V.x[1] - V.x[0]) * (SW - pad.l - pad.r);\n  const Y = v => SH - pad.b - (v - V.y[0]) / (V.y[1] - V.y[0]) * (SH - pad.t - pad.b);\n  const invX = px => V.x[0] + (px - pad.l) / (SW - pad.l - pad.r) * (V.x[1] - V.x[0]);\n  const invY = py => V.y[0] + (SH - pad.b - py) / (SH - pad.t - pad.b) * (V.y[1] - V.y[0]);\n  function niceTicks(a, b, n = 5) {\n    const raw = (b - a) / n, p = 10 ** Math.floor(Math.log10(raw)), m = raw / p;\n    const st = (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p, out = [];\n    for (let t = Math.ceil(a / st) * st; t <= b + 1e-12; t += st) out.push(+t.toFixed(10));\n    return [out, Math.max(0, -Math.floor(Math.log10(st) + 1e-9))];\n  }\n  const zoomK = () => (FULL.x[1] - FULL.x[0]) / (V.x[1] - V.x[0]);\n  function clampView() {\n    [\"x\", \"y\"].forEach(a => { const w = Math.min(V[a][1] - V[a][0], FULL[a][1] - FULL[a][0]);\n      const lo = Math.max(FULL[a][0], Math.min(V[a][0], FULL[a][1] - w)); V[a] = [lo, lo + w]; });\n  }\n  function zoomAt(f, px = (pad.l + SW - pad.r) / 2, py = (pad.t + SH - pad.b) / 2) {\n    const cx = invX(px), cy = invY(py), minW = (FULL.x[1] - FULL.x[0]) / 40, minH = (FULL.y[1] - FULL.y[0]) / 40;\n    const w = Math.max(minW, (V.x[1] - V.x[0]) / f), hh = Math.max(minH, (V.y[1] - V.y[0]) / f);\n    const fx = (cx - V.x[0]) / (V.x[1] - V.x[0]), fy = (cy - V.y[0]) / (V.y[1] - V.y[0]);\n    V = { x: [cx - fx * w, cx - fx * w + w], y: [cy - fy * hh, cy - fy * hh + hh] }; clampView(); draw();\n  }\n  function focusOn(name) {\n    const p = P.find(q => q.f === name); if (!p) return;\n    const w = (FULL.x[1] - FULL.x[0]) / 4, hh = (FULL.y[1] - FULL.y[0]) / 4;\n    V = { x: [p.x - w / 2, p.x + w / 2], y: [p.s - hh / 2, p.s + hh / 2] }; clampView();\n  }\n  function axes() {\n    const [xt, xd] = niceTicks(V.x[0], V.x[1]), [yt, yd] = niceTicks(V.y[0], V.y[1]);\n    xt.filter(t => t > V.x[0] && t < V.x[1]).forEach(t => {\n      sc.append(mk(\"line\", { x1: X(t), x2: X(t), y1: pad.t, y2: SH - pad.b, stroke: \"#e6e5e0\" }));\n      const tx = mk(\"text\", { x: X(t), y: SH - pad.b + 18, \"text-anchor\": \"middle\", \"font-size\": 12, fill: \"#5c6170\" }); tx.textContent = nf(t, Math.max(2, xd)); sc.append(tx); });\n    yt.filter(t => t >= V.y[0] && t < V.y[1]).forEach(t => {\n      sc.append(mk(\"line\", { x1: pad.l, x2: SW - pad.r, y1: Y(t), y2: Y(t), stroke: \"#e6e5e0\" }));\n      const ty = mk(\"text\", { x: pad.l - 8, y: Y(t) + 4, \"text-anchor\": \"end\", \"font-size\": 12, fill: \"#5c6170\" }); ty.textContent = nf(t, Math.max(2, yd)); sc.append(ty); });\n    sc.append(mk(\"line\", { x1: pad.l, x2: SW - pad.r, y1: SH - pad.b, y2: SH - pad.b, stroke: \"#5c6170\" }));\n    const lx = mk(\"text\", { x: (pad.l + SW - pad.r) / 2, y: SH - 8, \"text-anchor\": \"middle\", \"font-size\": 13, fill: \"#1a1d24\" }); lx.textContent = XL; sc.append(lx);\n    const cy = (pad.t + SH - pad.b) / 2;\n    const ly = mk(\"text\", { x: 15, y: cy, \"text-anchor\": \"middle\", \"font-size\": 13, fill: \"#1a1d24\", transform: `rotate(-90 15 ${cy})` }); ly.textContent = YL; sc.append(ly);\n  }\n  function draw() {\n    sc.replaceChildren(); tip.style.opacity = 0; axes();\n    const defs = mk(\"defs\"), cp = mk(\"clipPath\", { id: \"fscClip\" });\n    cp.append(mk(\"rect\", { x: pad.l, y: pad.t, width: SW - pad.l - pad.r, height: SH - pad.t - pad.b })); defs.append(cp); sc.append(defs);\n    const g = mk(\"g\", { \"clip-path\": \"url(#fscClip)\" }); sc.append(g);\n    const k = zoomK(), r = Math.min(10, 6 * Math.sqrt(Math.sqrt(k))), sel = model.get(\"selected\");\n    const vis = P.filter(p => p.x >= V.x[0] && p.x <= V.x[1] && p.s >= V.y[0] && p.s <= V.y[1]);\n    vis.forEach(p => {\n      const on = p.f === sel;\n      const c = mk(\"circle\", { cx: X(p.x), cy: Y(p.s), r: on ? r + 3 : r, fill: (CAT[p.c] || [\"\", \"#999\"])[1], \"fill-opacity\": .88,\n        stroke: on ? \"#1a1d24\" : \"#fff\", \"stroke-width\": on ? 2.5 : 1.2, tabindex: 0, style: PICK ? \"cursor:pointer\" : \"\" });\n      const show = () => { tip.textContent = `${p.f}: ${XN} ${nf(p.x)}, ${YN} ${nf(p.s)}` + (PICK ? \" · нажмите, чтобы открыть\" : \"\");\n        const b = sc.getBoundingClientRect(), kk = b.width / SW;\n        tip.style.left = `${X(p.x) * kk + 12}px`; tip.style.top = `${Y(p.s) * kk - 12}px`; tip.style.opacity = 1; };\n      const hide = () => { tip.style.opacity = 0; };\n      const pick = e => { if (!PICK) return; e.stopPropagation(); model.set(\"selected\", p.f); model.save_changes(); draw(); };\n      c.addEventListener(\"mouseenter\", show); c.addEventListener(\"focus\", show);\n      c.addEventListener(\"mouseleave\", hide); c.addEventListener(\"blur\", hide);\n      c.addEventListener(\"click\", pick); c.addEventListener(\"keydown\", e => { if (e.key === \"Enter\" || e.key === \" \") pick(e); });\n      c.addEventListener(\"pointerdown\", e => e.stopPropagation());\n      g.append(c);\n    });\n    const boxes = [];\n    const labelled = (ALWAYS || (k > 1.5 && vis.length <= 30)) ? [...vis] : vis.filter(p => p.f === sel);\n    labelled.sort((a, b) => (b.f === sel) - (a.f === sel) || b.s - a.s).forEach(p => {\n      const t = mk(\"text\", { x: X(p.x) + r + 4, y: Y(p.s) + 4, \"font-size\": p.f === sel ? 13 : 11, \"font-weight\": p.f === sel ? 650 : 400,\n        fill: \"#1a1d24\", \"pointer-events\": \"none\", stroke: \"#fff\", \"stroke-width\": 3, \"paint-order\": \"stroke\" });\n      t.textContent = p.f; g.append(t);\n      const bb = t.getBBox(), hit = boxes.some(o => bb.x < o.x + o.width + 2 && o.x < bb.x + bb.width + 2 && bb.y < o.y + o.height && o.y < bb.y + bb.height);\n      if (p.f !== sel && (hit || bb.x + bb.width > SW - pad.r)) t.remove(); else boxes.push(bb);\n    });\n    info.textContent = k > 1.02 ? `×${nf(k, 1)} · видно точек: ${vis.length} из ${P.length}` : `весь график · ${P.length} точек`;\n    sc.style.cursor = k > 1.02 ? \"grab\" : \"zoom-in\";\n    sc.style.touchAction = k > 1.02 ? \"none\" : \"pan-y\";\n  }\n  const svgPt = e => { const b = sc.getBoundingClientRect(); return [(e.clientX - b.left) * SW / b.width, (e.clientY - b.top) * SW / b.width]; };\n  let hintT;\n  sc.addEventListener(\"wheel\", e => {\n    if (!(e.ctrlKey || e.metaKey)) { hint.style.opacity = 1; clearTimeout(hintT); hintT = setTimeout(() => hint.style.opacity = 0, 1200); return; }\n    e.preventDefault(); const [x, y] = svgPt(e); zoomAt(Math.exp(-e.deltaY * 0.002), x, y);\n  }, { passive: false });\n  sc.addEventListener(\"dblclick\", e => { const [x, y] = svgPt(e); zoomAt(e.shiftKey ? 1 / 2 : 2, x, y); });\n  const ptrs = new Map(); let pinch0 = null;\n  sc.addEventListener(\"pointerdown\", e => { ptrs.set(e.pointerId, svgPt(e));\n    if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; pinch0 = Math.hypot(a[0] - b[0], a[1] - b[1]); }\n    if (zoomK() > 1.02 || ptrs.size === 2) { sc.setPointerCapture(e.pointerId); sc.style.cursor = \"grabbing\"; } });\n  sc.addEventListener(\"pointermove\", e => {\n    if (!ptrs.has(e.pointerId)) return; const prev = ptrs.get(e.pointerId), cur = svgPt(e); ptrs.set(e.pointerId, cur);\n    if (ptrs.size === 2 && pinch0) { const [a, b] = [...ptrs.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]);\n      zoomAt(d / pinch0, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); pinch0 = d; return; }\n    if (zoomK() <= 1.02) return;\n    const dx = invX(prev[0]) - invX(cur[0]), dy = invY(prev[1]) - invY(cur[1]);\n    V.x = V.x.map(v => v + dx); V.y = V.y.map(v => v + dy); clampView(); draw();\n  });\n  const up = e => { ptrs.delete(e.pointerId); if (ptrs.size < 2) pinch0 = null; sc.style.cursor = zoomK() > 1.02 ? \"grab\" : \"zoom-in\"; };\n  sc.addEventListener(\"pointerup\", up); sc.addEventListener(\"pointercancel\", up);\n  const med = a => { const b = [...a].sort((u, v) => u - v); return b[b.length >> 1]; };\n  const MX = med(P.map(p => p.x)), MY = med(P.map(p => p.s));\n  bIn.addEventListener(\"click\", () => zoomK() > 1.02 ? zoomAt(1.6) : zoomAt(1.6, X(MX), Y(MY)));\n  bOut.addEventListener(\"click\", () => zoomAt(1 / 1.6));\n  bAll.addEventListener(\"click\", () => { V = { x: [...FULL.x], y: [...FULL.y] }; draw(); });\n  const present = [...new Set(P.map(p => p.c))];\n  legend.innerHTML = Object.entries(CAT).filter(([k]) => present.includes(k))\n    .map(([k, [name, col]]) => `<span><i class=\"sw\" style=\"background:${col}\"></i>${name} (${P.filter(p => p.c === k).length})</span>`).join(\"\");\n  if (model.get(\"selected\")) focusOn(model.get(\"selected\"));\n  model.on(\"change:selected\", () => draw());\n  draw();\n}\nexport default { render };\n", "pill": "// Большая чёрная кнопка-«таблетка», как на прежнем сайте. Каждый щелчок увеличивает count.\nfunction render({ model, el }) {\n  const b = document.createElement(\"button\");\n  b.className = \"pill\"; b.type = \"button\"; b.textContent = model.get(\"label\");\n  b.addEventListener(\"click\", () => { model.set(\"count\", model.get(\"count\") + 1); model.save_changes(); });\n  el.append(b);\n}\nexport default { render };\n", "controls": "// Панель элементов управления в стиле прежнего сайта про шрифты: «таблетки», круглые списки, ползунки с подписью.\n// spec: [{type: \"seg\"|\"select\"|\"range\"|\"text\"|\"button\"|\"reset\", name, label, ...}], значения в model.values.\nfunction render({ model, el }) {\n  const spec = model.get(\"spec\");\n  const init = JSON.parse(JSON.stringify(model.get(\"values\")));\n  let vals = JSON.parse(JSON.stringify(init));\n  const nf = (v, d) => Number(v).toFixed(d).replace(\".\", \",\").replace(\"-\", \"−\");\n  const decs = st => { const s = String(st); return s.includes(\".\") ? s.split(\".\")[1].length : 0; };\n  let timer = null;\n  const push = (now) => {\n    clearTimeout(timer);\n    const send = () => { model.set(\"values\", JSON.parse(JSON.stringify(vals))); model.save_changes(); };\n    if (now) send(); else timer = setTimeout(send, 90);\n  };\n  const root = document.createElement(\"div\");\n  root.className = \"fctl\";\n  const refreshers = {};\n  for (const c of spec) {\n    const lab = document.createElement(\"label\");\n    if (c.wide) lab.classList.add(\"wide\");\n    if (c.grow) lab.style.flex = `${c.grow} 1 0`;\n    const cap = document.createElement(\"span\");\n    cap.className = \"cap\";\n    if (c.type === \"seg\") {\n      cap.textContent = c.label || \"\"; lab.append(cap);\n      const seg = document.createElement(\"span\"); seg.className = \"seg\"; seg.setAttribute(\"role\", \"radiogroup\");\n      const btns = c.options.map(([text, v]) => {\n        const b = document.createElement(\"button\"); b.type = \"button\"; b.textContent = text; b.setAttribute(\"role\", \"radio\");\n        b.addEventListener(\"click\", () => {\n          if (c.sets) { vals[c.sets] = v; (refreshers[c.sets] || (() => {}))(); }\n          else vals[c.name] = v;\n          sync(); push(true);\n        });\n        seg.append(b); return [b, v];\n      });\n      const sync = () => btns.forEach(([b, v]) => {\n        const on = c.sets ? Math.abs(Number(vals[c.sets]) - Number(v)) < 1e-9 : vals[c.name] === v;\n        b.setAttribute(\"aria-checked\", on);\n      });\n      refreshers[c.name] = sync;\n      if (c.sets) { const prev = refreshers[c.sets]; refreshers[\"__after_\" + c.sets] = sync; }\n      sync(); lab.append(seg);\n    } else if (c.type === \"select\") {\n      cap.textContent = c.label || \"\"; lab.append(cap);\n      const sel = document.createElement(\"select\"); sel.className = \"fancy\";\n      const add = (parent, [text, v]) => { const o = document.createElement(\"option\"); o.value = JSON.stringify(v); o.textContent = text; parent.append(o); };\n      if (c.groups) for (const [g, opts] of c.groups) { const og = document.createElement(\"optgroup\"); og.label = g; opts.forEach(o => add(og, o)); sel.append(og); }\n      else c.options.forEach(o => add(sel, o));\n      sel.value = JSON.stringify(vals[c.name]);\n      sel.addEventListener(\"change\", () => { vals[c.name] = JSON.parse(sel.value); push(true); });\n      refreshers[c.name] = () => { sel.value = JSON.stringify(vals[c.name]); };\n      lab.append(sel);\n    } else if (c.type === \"range\") {\n      const d = c.decimals ?? decs(c.step ?? 1);\n      const out = document.createElement(\"output\"); out.className = \"val\";\n      const unit = c.unit ? ` ${c.unit}` : \"\";\n      cap.append(document.createTextNode(`${c.label}: `), out, document.createTextNode(unit));\n      const inp = document.createElement(\"input\"); inp.type = \"range\";\n      inp.min = c.min; inp.max = c.max; inp.step = c.step ?? 1; inp.value = vals[c.name];\n      const show = () => { out.textContent = c.thousands ? Number(inp.value).toLocaleString(\"ru-RU\") : nf(inp.value, d); };\n      inp.addEventListener(\"input\", () => { show(); vals[c.name] = Number(inp.value);\n        (refreshers[\"__after_\" + c.name] || (() => {}))(); if (c.live) push(false); });\n      inp.addEventListener(\"change\", () => { vals[c.name] = Number(inp.value); push(true); });\n      refreshers[c.name] = () => { inp.value = vals[c.name]; show(); (refreshers[\"__after_\" + c.name] || (() => {}))(); };\n      show(); lab.append(cap, inp);\n    } else if (c.type === \"text\") {\n      cap.textContent = c.label || \"\"; lab.append(cap);\n      const inp = document.createElement(\"input\"); inp.type = \"text\"; inp.value = vals[c.name] ?? \"\";\n      if (c.maxlength) inp.maxLength = c.maxlength;\n      if (c.placeholder) inp.placeholder = c.placeholder;\n      inp.addEventListener(\"input\", () => { vals[c.name] = inp.value; push(false); });\n      refreshers[c.name] = () => { inp.value = vals[c.name]; };\n      lab.append(inp);\n    } else if (c.type === \"button\" || c.type === \"reset\") {\n      lab.classList.add(\"btn\");\n      const b = document.createElement(\"button\"); b.type = \"button\"; b.className = \"pill\"; b.textContent = c.label;\n      b.addEventListener(\"click\", () => {\n        if (c.type === \"reset\") { const keep = vals; vals = JSON.parse(JSON.stringify(init));\n          for (const k in keep) if (!(k in vals)) vals[k] = keep[k];\n          spec.filter(x => x.type === \"button\").forEach(x => { vals[x.name] = keep[x.name]; });\n          Object.keys(refreshers).filter(k => !k.startsWith(\"__\")).forEach(k => refreshers[k]()); }\n        else vals[c.name] = (vals[c.name] || 0) + 1;\n        push(true);\n      });\n      lab.append(b);\n    }\n    root.append(lab);\n  }\n  el.append(root);\n}\nexport default { render };\n"}
    _WC = {"scatter": ".fsc{font-family:Onest,\"Golos Text\",system-ui,sans-serif;color:#1a1d24;background:#fff;border-radius:10px;padding:.7rem .7rem .6rem;max-width:860px}\n.fsc .zoombar{display:flex;gap:.4rem;align-items:center;margin:0 0 .4rem;flex-wrap:wrap}\n.fsc .zoombar button{font:inherit;font-size:.95rem;min-width:2.3rem;height:2.3rem;padding:0 .8rem;border-radius:999px;border:1px solid #d6d4cc;background:#fff;color:#1a1d24;cursor:pointer}\n.fsc .zoombar button:hover{background:#f3f2ee}\n.fsc .note{color:#5c6170;font-size:.92rem;margin-left:.4rem}\n.fsc .box{position:relative}\n.fsc svg{display:block;width:100%;height:auto;user-select:none;-webkit-user-select:none;font-family:inherit}\n.fsc .tip{position:absolute;pointer-events:none;background:#1a1d24;color:#f6f7f5;font-size:.85rem;padding:.3rem .55rem;border-radius:5px;opacity:0;transition:opacity .12s;white-space:nowrap}\n.fsc .hint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:rgba(26,29,36,.82);color:#fff;padding:.5rem .8rem;border-radius:6px;font-size:.9rem;pointer-events:none;opacity:0;transition:opacity .25s}\n.fsc .legend{display:flex;flex-wrap:wrap;gap:.4rem 1rem;font-size:.88rem;color:#5c6170;margin:.5rem 0 0}\n.fsc .sw{display:inline-block;width:.8em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}\n", "pill": ".pill{font-family:Onest,\"Golos Text\",system-ui,sans-serif;font-weight:600;font-size:1.02rem;background:#1a1d24;color:#f6f7f5;border:0;border-radius:999px;padding:.78rem 1.35rem;cursor:pointer;transition:background .15s,transform .15s}\n.pill:hover{background:#353a46}\n.pill:active{transform:scale(.97)}\n", "controls": ".fctl{display:flex;flex-wrap:wrap;gap:1rem 1.4rem;align-items:flex-end;margin:.6rem 0 .5rem;font-family:Onest,\"Golos Text\",system-ui,sans-serif;color:#1a1d24}\n.fctl label{display:flex;flex-direction:column;gap:.35rem;font-size:.92rem;color:#5c6170;min-width:11rem}\n.fctl label.wide{flex:1 1 100%}\n.fctl label.btn{min-width:0}\n.fctl .cap .val{color:#1a1d24;font-weight:600;font-variant-numeric:tabular-nums}\n.fctl .seg{display:inline-flex;flex-wrap:wrap;gap:2px;background:#e6e8e3;border-radius:999px;padding:3px;width:max-content;max-width:100%}\n.fctl .seg button{font:inherit;background:transparent;color:#1a1d24;font-weight:500;font-size:.95rem;padding:.48rem 1rem;border:0;border-radius:999px;cursor:pointer;transition:background .15s}\n.fctl .seg button:hover{background:#f2f3f0}\n.fctl .seg button[aria-checked=\"true\"]{background:#fff;font-weight:650;box-shadow:0 1px 3px rgba(26,29,36,.18)}\n.fctl .fancy{appearance:none;-webkit-appearance:none;font:inherit;font-size:.98rem;color:#1a1d24;background:#fff url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%231a1d24' stroke-width='1.6'/%3E%3C/svg%3E\") no-repeat right .95rem center;border:1px solid #c9cdc5;border-radius:999px;padding:.6rem 2.4rem .6rem 1rem;min-width:13rem;width:100%;cursor:pointer;transition:border-color .15s,box-shadow .15s}\n.fctl .fancy:hover,.fctl input[type=text]:hover{border-color:#9aa0a8}\n.fctl .fancy:focus,.fctl input[type=text]:focus{outline:none;border-color:#2a78d6;box-shadow:0 0 0 3px rgba(42,120,214,.18)}\n.fctl input[type=text]{font:inherit;font-size:.98rem;color:#1a1d24;padding:.6rem 1rem;border:1px solid #c9cdc5;border-radius:999px;background:#fff;min-width:13rem;width:100%;box-sizing:border-box}\n.fctl input[type=range]{width:100%;min-width:13rem;accent-color:#2a78d6;height:1.4rem;cursor:pointer}\n.fctl .pill{font-family:inherit;font-weight:600;font-size:1rem;background:#1a1d24;color:#f6f7f5;border:0;border-radius:999px;padding:.78rem 1.35rem;cursor:pointer;transition:background .15s,transform .15s;white-space:nowrap}\n.fctl .pill:hover{background:#353a46}\n.fctl .pill:active{transform:scale(.97)}\n"}
    try:
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


    G = types.ModuleType("generators")
    exec(read_text(PUB / "generators.py"), G.__dict__)
    return (CAT, CAT_RU, G, GRIDC, H, HAS_AW, INK, MUTED, T, clicks, esc, font_row, fonts, frame, gfont, legend, nfc, panel, pill, vals,
            scatter_widget, selected_of, svg, to_wght, to_ytlc,
            Path, PUB, base64, cards, code_block, df_html, fig, io, live, mo, nf, np, out_text, pd, plot_html, plt,
            read_text, scipy, section, stats, table_html, types)


@app.cell(hide_code=True)
def _(mo):
    mo.Html("<style>@import url('https://fonts.googleapis.com/css2?family=Onest:wght@300..900&family=Unbounded:wght@300..900&family=Roboto+Flex:opsz,wdth,wght,YTLC@8..144,25..151,100..1000,416..570&display=swap');\n:root{ --paper:#f6f7f5; --ink:#1a1d24; --muted:#5c6170; --rule:#dcdfd8;\n  --blue:#2a78d6; --orange:#eb6834; --straw:#d8c56a; --green:#1baf7a; --measure:68ch;\n  --marimo-text-font:Onest,system-ui,sans-serif; --marimo-heading-font:Unbounded,Onest,sans-serif; }\nbody, #App, .mo-app, [data-testid=\"app\"]{background:var(--paper) !important;color:var(--ink)}\nbody, .markdown, .prose{font-family:Onest,system-ui,-apple-system,\"Segoe UI\",sans-serif}\n.fs a{color:var(--blue);text-underline-offset:.18em}\n.fs code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em;background:#e9ebe6;padding:.08em .35em;border-radius:3px}\n.fs{font-size:1.0625rem;line-height:1.6;color:var(--ink)}\n.fs .text{max-width:var(--measure)}\n.fs p{margin:0 0 1rem !important}\n.fs, .fs p, .fs a, .fs li, .fs b, .fs i, .fs .note, .fs .lede, .fs .bar, .fs .cmp-head, .fs figcaption, .fs .readout, .fs .legend{font-family:Onest,system-ui,sans-serif}\n.fs-hero h1 .l{font-family:\"Roboto Flex\",sans-serif}\n.fs-hero{padding-top:clamp(2rem,6vw,5rem);padding-bottom:1rem}\n.fs-hero h1{font-family:\"Roboto Flex\",sans-serif !important;font-size:clamp(2.9rem,9.2vw,7.4rem) !important;line-height:.98 !important;letter-spacing:-.02em;margin:.4rem 0 1.6rem !important;font-weight:400}\n.fs-hero h1 .w{display:block !important}\n.fs-hero h1 span.l{transition:font-weight .5s cubic-bezier(.2,.7,.2,1)}\n.fs .lede{font-size:clamp(1.1rem,1.6vw,1.3rem);color:var(--muted);margin:0 0 1.4rem;max-width:var(--measure)}\n.fs .note{color:var(--muted);font-size:.95rem}\n.fs-sec{padding-top:3rem;border-top:1px solid var(--rule);margin-top:2rem}\n.fs h2{font-family:Unbounded,Onest,sans-serif !important;font-size:clamp(1.6rem,3.2vw,2.4rem) !important;line-height:1.15 !important;font-weight:600 !important;letter-spacing:-.01em;margin:0 0 1rem !important;color:var(--ink)}\n.fs h3{font-family:Unbounded,Onest,sans-serif !important;font-size:1.1rem !important;font-weight:550 !important;margin:1.6rem 0 .5rem !important;color:var(--ink)}\n.fs figure{margin:1.4rem 0}\n.fs figure img{width:100%;height:auto;background:#fff;border-radius:6px}\n.fs figcaption{color:var(--muted);font-size:.92rem;margin-top:.5rem;max-width:var(--measure)}\n.fs .chart{background:#fff;border-radius:8px;padding:.6rem}\n.fs .chart svg{display:block;width:100%;height:auto}\n.fs .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1.4rem 2rem;margin:1.6rem 0;max-width:900px}\n.fs .fact strong{display:block;font-family:Unbounded,Onest,sans-serif;font-size:2.2rem;line-height:1.1;font-weight:600;font-variant-numeric:tabular-nums}\n.fs .fact span{color:var(--muted);font-size:.95rem}\n.fs .legend{display:flex;flex-wrap:wrap;gap:.4rem 1rem;font-size:.88rem;color:var(--muted);margin:.5rem 0 0}\n.fs .sw{display:inline-block;width:.8em;height:.8em;border-radius:2px;margin-right:.35em;vertical-align:-.05em}\n.fs .rho-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;max-width:820px}\n.fs .lab{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:1.6rem;align-items:start;margin-top:.6rem}\n.fs .readout{font-variant-numeric:tabular-nums;margin-top:.7rem;font-size:.95rem}\n.fs .readout b{font-weight:650}\n.fs .specimen{background:#fff;border-radius:8px;padding:1.2rem 1.4rem;overflow:hidden}\n.fs .cmp-row{background:#fff;border-radius:8px;padding:.8rem 1rem 1rem;margin:0 0 1rem}\n.fs .cmp-head{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap;margin-bottom:.3rem}\n.fs .cmp-head b{font-weight:650}\n.fs .bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.6rem 1.4rem;margin-top:.6rem}\n.fs .bar{font-size:.85rem;color:var(--muted)}\n.fs .bar .track{position:relative;height:8px;border-radius:4px;background:#eceee9;margin-top:.25rem}\n.fs .bar .fill{position:absolute;left:0;top:0;bottom:0;border-radius:4px}\n.fs .bar .med{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--ink);opacity:.7}\n.fs .newfonts{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-top:.8rem}\n.fs .newfonts div.c{background:#fff;border-radius:8px;padding:.8rem 1rem}\n.fs .newfonts small{color:var(--muted);font-size:.82rem}\n.fs-foot{border-top:1px solid var(--rule);margin-top:2.5rem;padding:2rem 0 3rem;color:var(--muted);font-size:.95rem}\n.fs-foot p{max-width:var(--measure)}\n.fs-ctrl{font-size:.9rem;color:var(--muted)}\n@media (max-width:640px){.fs .rho-grid,.fs .lab{grid-template-columns:1fr}}\n</style>")
    return


@app.cell(hide_code=True)
def _(pill):
    reroll = pill("Перебросить толщину букв")
    return (reroll,)


@app.cell(hide_code=True)
def _(H, clicks, fonts, mo, np, reroll, to_wght):
    _rng = np.random.default_rng(clicks(reroll) * 7 + 3)
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
def _(panel):
    rho_p = panel([{"type": "range", "name": "rho", "label": "Сила связи ρ", "min": -1, "max": 1, "step": 0.05, "decimals": 2, "live": True},
                   {"type": "seg", "name": "preset", "sets": "rho", "options": [["нет связи", 0], ["как у нас", 0.4], ["сильная", 0.9]]}],
                  {"rho": 0.4})
    rho_p
    return (rho_p,)


@app.cell(hide_code=True)
def _(H, MUTED, fonts, nfc, np, rho_p, stats, svg, vals):
    _r = float(vals(rho_p).get("rho", 0.4))
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
def _(CAT, fonts, mo, panel):
    sc_find = panel([{"type": "select", "name": "f", "label": "Найти шрифт", "grow": 0,
                      "groups": [[CAT[k][0], [[f, f] for f in sorted(fonts[fonts.category == k].family)]] for k in CAT]}],
                    {"f": "Inter"})
    mo.vstack([mo.md("Приближайте кнопками «+ / −» или двойным щелчком по месту; приближенный график можно "
                     "двигать мышью. **Нажмите на кружок**, и ниже откроется этот шрифт. Шрифт можно и найти по названию "
                     "в списке.").style({"color": "#5c6170", "font-size": ".95rem", "max-width": "68ch"}),
               sc_find], gap=0.3)
    return (sc_find,)


@app.cell(hide_code=True)
def _(sc_find, scatter_widget, vals):
    sc_find_v = vals(sc_find).get("f") or "Inter"
    sc_plot = scatter_widget(sc_find_v)
    sc_plot
    return (sc_find_v, sc_plot,)


@app.cell(hide_code=True)
def _(H, fonts, font_row, mo, sc_find_v, sc_plot, selected_of):
    _name = selected_of(sc_plot, sc_find_v) if sc_plot is not None else sc_find_v
    _r = fonts[fonts.family == _name]
    if sc_plot is None:
        _out = mo.md("_Интерактивный график загружается…_")
    elif not len(_r):
        _out = mo.md("")
    else:
        _out = H('<p class="note" style="margin:.4rem 0">Выбранный шрифт:</p>' + font_row(_r.iloc[0], "Hxlno шрифт") +
                 '<p class="note">Исследование целиком: <a href="report/" target="_top">отчёт</a> (код и формулы).</p>')
    _out
    return


@app.cell(hide_code=True)
def _(H):
    H("""<div class="fs-sec" id="play"><h2>Попробуй сам</h2><h3>Толщина и ширина</h3>
<div class="text"><p>Этот текст набран вариативным шрифтом Roboto Flex: у него толщину штриха, ширину букв и даже высоту
строчных можно менять плавно. Подвигай ползунки и посмотри, как меняется характер текста. Текст можно исправить в поле.</p></div></div>""")
    return


@app.cell(hide_code=True)
def _(panel):
    pl = panel([{"type": "text", "name": "t", "label": "Текст", "wide": True},
                {"type": "range", "name": "wght", "label": "Толщина (вес)", "min": 100, "max": 1000, "step": 10, "live": True},
                {"type": "range", "name": "wdth", "label": "Ширина", "unit": "%", "min": 25, "max": 151, "step": 1, "live": True},
                {"type": "range", "name": "ytlc", "label": "Высота строчных", "min": 416, "max": 570, "step": 2, "live": True},
                {"type": "range", "name": "size", "label": "Кегль", "unit": "px", "min": 16, "max": 160, "step": 2, "live": True},
                {"type": "reset", "label": "Сбросить"}],
               {"t": "Шрифт как случайная величина", "wght": 400, "wdth": 100, "ytlc": 514, "size": 72})
    pl
    return (pl,)


@app.cell(hide_code=True)
def _(H, esc, fonts, nfc, pl, vals):
    _s = fonts.stem
    _v = vals(pl)
    H(f"""<div class="specimen"><div style="font-family:'Roboto Flex','Golos Text',sans-serif;line-height:1.05;word-break:break-word;
font-size:{_v['size']}px;font-variation-settings:'wght' {_v['wght']},'wdth' {_v['wdth']},'YTLC' {_v['ytlc']}">{esc(_v['t'] or " ")}</div></div>
<p class="note">Для сравнения: у шрифтов из датасета (начертание Regular, вес 400) толщина штриха от {nfc(_s.min())} до {nfc(_s.max())} кегля,
медиана {nfc(_s.median())}. При кегле {_v['size']} px это от {nfc(_s.min() * _v['size'], 1)} до {nfc(_s.max() * _v['size'], 1)} px.</p>""")
    return


@app.cell(hide_code=True)
def _(CAT, H, fonts, mo, panel):
    _g = [[CAT[k][0], [[f, f] for f in sorted(fonts[fonts.category == k].family)]] for k in CAT]
    _has = set(fonts.family)
    _def = [n if n in _has else sorted(_has)[i * 7] for i, n in enumerate(("Inter", "Playfair", "Indie Flower"))]
    cmp = panel([{"type": "select", "name": f"f{i}", "label": f"Шрифт {i + 1}", "groups": _g, "grow": 1} for i in range(3)]
                + [{"type": "text", "name": "t", "label": "Текст", "maxlength": 40, "grow": 1}],
                {"f0": _def[0], "f1": _def[1], "f2": _def[2], "t": "Hxlno шрифт"})
    mo.vstack([H("""<h3>Сравнение шрифтов</h3><div class="text"><p>Выбери до трёх шрифтов из датасета
и введи любой текст. Все строки набраны одним кеглем: сразу видно, у какого шрифта строчные выше и штрих толще.
Пунктир показывает наши измерения: высоту строчных (x-height) и прописных.</p></div>"""), cmp], gap=0.2)
    return (cmp,)


@app.cell(hide_code=True)
def _(H, cmp, font_row, fonts, vals):
    _v = vals(cmp)
    _txt = (_v.get("t") or "Hxlno").strip() or "Hxlno"
    H("".join(font_row(fonts[fonts.family == _v[f"f{i}"]].iloc[0], _txt) for i in range(3))
      + '<p class="note">Чёрная риска на полоске показывает медиану по всем шрифтам датасета.</p>')
    return


@app.cell(hide_code=True)
def _(H):
    H("""<div class="fs-sec" id="rng"><h2>Датчик: случайный шрифт, похожий на настоящий</h2>
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
распределения, но большая часть бросков уходит впустую: принимается около 29 %.</p></div></div>""")
    return


@app.cell(hide_code=True)
def _(G, panel):
    rg = panel([{"type": "seg", "name": "var", "label": "Величина", "options": [["x-height", "x_height"], ["толщина штриха", "stem"]]},
                {"type": "select", "name": "method", "label": "Метод", "options": [[v, k] for k, v in G.METHOD_RU.items()], "grow": 1},
                {"type": "seg", "name": "base", "label": "Базовый датчик", "options": [[v.split(" (")[0], k] for k, v in G.BASE_RU.items()]},
                {"type": "range", "name": "n", "label": "Сколько чисел", "min": 100, "max": 20000, "step": 100, "thousands": True},
                {"type": "button", "name": "go", "label": "Сгенерировать заново"}],
               {"var": "x_height", "method": "polar", "base": "pcg64", "n": 1000, "go": 0})
    rg
    return (rg,)


@app.cell(hide_code=True)
def _(G, H, MUTED, fonts, frame, legend, nfc, np, rg, svg, vals):
    _v = vals(rg)
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
Доля принятых точек <b>{nfc(_info["accept"])}</b>{" (теория π/4 = 0,785)" if rg_method == "polar" else ""}.</p>""")
    return


@app.cell(hide_code=True)
def _(H):
    H("""<div class="fs-foot"><p>Быкова Кристина Денисовна, ИСУ 501322, команда 27, трек КТвД. Lab01, прикладная статистика, осень 2026:
доп. задание КТвД, датасет шрифтов, датчик случайных чисел, интерактив и этот сайт.
Отчёт: <a href="report/" target="_top">ноутбук со скрытым кодом</a>.</p><p>Шрифты: Google Fonts (SIL Open Font License).</p></div>""")
    return


if __name__ == "__main__":
    app.run()
