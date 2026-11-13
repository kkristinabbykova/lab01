"""Экспорт ноутбука в HTML-отчёт для сайта: код скрыт, якоря работают, формулы через MathJax.

    python tools/export_nb.py fonts.ipynb docs/fonts.html

GitHub показывает .ipynb без скрытия кода и без внутренних якорных ссылок, поэтому для чтения
отчёта на сайте лежит эта страница. Код остаётся в самом ноутбуке.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

MD = MarkdownIt("commonmark", {"html": True}).enable("table")
MATH = re.compile(r"(\$\$.+?\$\$|\$[^$\n]+?\$)", re.S)

CSS = """
:root{--ink:#1a1d24;--muted:#5c6170;--line:#e6e5e0;--paper:#fafaf7;--blue:#2a78d6}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 -apple-system,"Segoe UI",Inter,Roboto,Arial,sans-serif}
main{max-width:980px;margin:0 auto;padding:2rem 1.25rem 4rem}
a{color:var(--blue)}
h1{font-size:1.9rem;line-height:1.25;margin:.2rem 0 1rem}
h2{font-size:1.45rem;margin:2.4rem 0 .6rem;padding-top:.6rem;border-top:1px solid var(--line)}
h3{font-size:1.15rem;margin:1.6rem 0 .4rem}
table{border-collapse:collapse;margin:.8rem 0;font-size:.92rem;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:.35rem .6rem;text-align:left;vertical-align:top}
th{background:#f1f0eb}
img{max-width:100%;height:auto;display:block;margin:.6rem auto}
pre.out{background:#fff;border:1px solid var(--line);border-radius:6px;padding:.6rem .8rem;overflow-x:auto;font-size:.82rem;line-height:1.45}
code{font-family:"JetBrains Mono",Menlo,Consolas,monospace;font-size:.9em}
sub a{font-size:.8rem}
.top{position:sticky;top:0;background:var(--paper);border-bottom:1px solid var(--line);padding:.5rem 1.25rem;font-size:.9rem;z-index:2}
.top a{margin-right:1rem}
:target{scroll-margin-top:3.5rem}
"""

HEAD = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{css}</style>
<script>window.MathJax={{tex:{{inlineMath:[["$","$"]],displayMath:[["$$","$$"]]}},svg:{{fontCache:"global"}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head><body>
<div class="top"><a href="./">← сайт</a><a href="#toc">Содержание</a><a href="{src}">ноутбук с кодом на GitHub</a></div>
<main>
"""


def md_to_html(text: str) -> str:
    """Markdown → HTML, формулы $…$ и $$…$$ не трогаем (их рисует MathJax)."""
    keep = []

    def stash(m):
        keep.append(m.group(0))
        return f"MATHPLACEHOLDER{len(keep) - 1}X"

    out = MD.render(MATH.sub(stash, text))
    return re.sub(r"MATHPLACEHOLDER(\d+)X", lambda m: html.escape(keep[int(m.group(1))], quote=False), out)


def output_html(o: dict) -> str:
    data = o.get("data", {})
    if "image/png" in data:
        png = data["image/png"]
        png = "".join(png) if isinstance(png, list) else png
        return f'<img alt="" src="data:image/png;base64,{png.strip()}">'
    if "text/html" in data:
        return "".join(data["text/html"])
    text = o.get("text") or data.get("text/plain")
    if text:
        text = "".join(text)
        if text.strip().startswith("<Figure size"):
            return ""
        return f'<pre class="out">{html.escape(text)}</pre>'
    return ""


def main(src: str, dst: str, repo_url: str = "") -> None:
    nb = json.loads(Path(src).read_text(encoding="utf-8"))
    parts = []
    for c in nb["cells"]:
        if c["cell_type"] == "markdown":
            parts.append(md_to_html("".join(c["source"])))
        elif c["cell_type"] == "code":   # сам код не показываем, только результаты
            parts.extend(output_html(o) for o in c.get("outputs", []))
    first = "".join(nb["cells"][0]["source"])
    title = re.search(r"^# (.+)$", first, re.M)
    link = f"{repo_url}/blob/main/{Path(src).name}" if repo_url else Path(src).name
    page = HEAD.format(title=html.escape(title.group(1) if title else Path(src).stem), css=CSS, src=link)
    page += "\n".join(p for p in parts if p) + "\n</main></body></html>\n"
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text(page, encoding="utf-8")
    print(f"{dst} собран из {src}")


if __name__ == "__main__":
    import os
    main(sys.argv[1], sys.argv[2], os.environ.get("LAB_REPO_URL", "").rstrip("/"))
