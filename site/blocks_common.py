"""Общие куски для marimo-приложений сайта: оформление, вывод таблиц и рисунков, оглавление."""
import json


def header(title: str) -> str:
    return f'''# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "numpy", "pandas", "matplotlib", "scipy"]
# ///
import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium", app_title={json.dumps(title, ensure_ascii=False)})


'''


# Код, общий для настроечной ячейки обоих приложений. Подставляется внутрь def _():
HELPERS = r'''
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
'''

HELPER_NAMES = ("Path PUB base64 cards code_block fig io live mo nf np out_text pd plot_html plt read_text scipy "
                "stats table_html types").split()


def css(t: dict) -> str:
    """Оформление страницы: общий каркас, цвета из темы t."""
    return f'''<style>
:root {{ --lab-bg:{t["bg"]}; --lab-card:{t["card"]}; --lab-ink:{t["ink"]}; --lab-ink2:{t["ink2"]};
        --lab-line:{t["line"]}; --lab-acc:{t["acc"]}; --lab-acc2:{t["acc2"]}; --lab-soft:{t["soft"]}; }}
body, #App, .mo-app, [data-testid="app"] {{ background: var(--lab-bg) !important; }}
.markdown h1, .markdown h2, .markdown h3, .markdown h4 {{ color: var(--lab-ink); letter-spacing: -.01em; }}
.markdown h2 {{ font-size: 1.6rem; margin-top: 2.4rem; padding-top: 1rem; border-top: 2px solid var(--lab-line); }}
.markdown h3 {{ font-size: 1.22rem; margin-top: 1.6rem; }}
.markdown a {{ color: var(--lab-acc); }}
.lab-cover {{ background: {t["cover"]}; color: {t["cover_ink"]}; border-radius: 18px; padding: 2.2rem 2rem 1.8rem;
             margin-bottom: .6rem; position: relative; overflow: hidden; }}
.lab-cover .kicker {{ text-transform: uppercase; letter-spacing: .14em; font-size: .75rem; opacity: .75; }}
.lab-cover h1 {{ font-size: clamp(1.8rem, 4.6vw, 3rem); line-height: 1.08; margin: .5rem 0 .8rem; color: inherit; border: 0; }}
.lab-cover p {{ max-width: 46rem; opacity: .9; margin: .3rem 0; }}
.lab-cover .meta {{ display: flex; flex-wrap: wrap; gap: .5rem 1.4rem; margin-top: 1.2rem; font-size: .88rem; opacity: .85; }}
.lab-cover .meta b {{ font-weight: 600; }}
.lab-guide {{ background: var(--lab-card); border: 1px solid var(--lab-line); border-radius: 14px; padding: 1rem 1.2rem; }}
.lab-guide h4 {{ margin: 0 0 .4rem; }}
.lab-guide ul {{ margin: .2rem 0 0 1.1rem; padding: 0; }}
.lab-fig {{ margin: .4rem 0; background: #fff; border: 1px solid var(--lab-line); border-radius: 12px; padding: .5rem; }}
.lab-fig img {{ display: block; width: 100%; height: auto; }}
.lab-fig.live {{ border-color: var(--lab-acc2); }}
.lab-tbl {{ overflow-x: auto; }}
.lab-tbl table {{ border-collapse: collapse; font-size: .86rem; background: #fff; border: 1px solid var(--lab-line); }}
.lab-tbl th, .lab-tbl td {{ border-bottom: 1px solid var(--lab-line); padding: .32rem .6rem; text-align: right; }}
.lab-tbl th {{ background: var(--lab-soft); color: var(--lab-ink); font-weight: 600; }}
.lab-out {{ background: #fff; border: 1px solid var(--lab-line); border-radius: 10px; padding: .6rem .8rem;
           font-size: .8rem; line-height: 1.45; overflow-x: auto; color: var(--lab-ink); margin: .2rem 0; }}
.lab-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: .6rem; margin: .3rem 0; }}
.lab-card {{ background: var(--lab-card); border: 1px solid var(--lab-line); border-radius: 12px; padding: .7rem .85rem;
            display: flex; flex-direction: column; gap: .1rem; }}
.lab-card span {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: var(--lab-ink2); }}
.lab-card b {{ font-size: 1.45rem; font-variant-numeric: tabular-nums; color: var(--lab-ink); }}
.lab-card small {{ color: var(--lab-ink2); font-size: .78rem; }}
.lab-live {{ border-left: 4px solid var(--lab-acc); padding: .2rem 0 .1rem .9rem; margin-top: 1rem; }}
.lab-live .tag {{ display: inline-block; font-size: .68rem; text-transform: uppercase; letter-spacing: .12em;
                  background: var(--lab-acc); color: #fff; border-radius: 999px; padding: .12rem .55rem; }}
.lab-live h4 {{ margin: .35rem 0 .15rem; font-size: 1.08rem; color: var(--lab-ink); }}
.lab-live p {{ margin: 0; color: var(--lab-ink2); font-size: .9rem; }}
.lab-toc a {{ text-decoration: none; }}
.lab-toc ul {{ padding-left: 1rem; }}
@media (max-width: 640px) {{ .lab-cover {{ padding: 1.5rem 1.2rem; }} }}
</style>'''


def toc_cell(toc_md: str, extra: str) -> str:
    """Оглавление в боковой панели marimo (кнопка ☰ на телефоне)."""
    toc = toc_md.replace('<a id="toc"></a>', "").replace("**Содержание**", "").strip()
    toc = "\n".join(l for l in toc.splitlines() if not l.startswith("**Часть КТвД") and not l.startswith("*Код в ячейках"))
    body = json.dumps("### Содержание\n\n" + toc + "\n\n" + extra, ensure_ascii=False)
    return f'''@app.cell(hide_code=True)
def _(mo):
    mo.sidebar([mo.md({body})])
    return
'''
