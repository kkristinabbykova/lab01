"""Собрать marimo-приложения сайта из выполненных ноутбуков.

    python tools/build_apps.py

1. Основная работа (wine/lab01.ipynb) выполняется в серой теме (LAB_THEME=gray) во временной копии,
   чтобы не трогать сам ноутбук; из неё собирается site/wine_app.py.
2. Доп. задание КТвД (fonts/fonts.ipynb) берётся как есть; из него собирается site/fonts_app.py.

Каждый раздел ноутбука становится ячейкой marimo: текст, таблицы и рисунки как в ноутбуке, а код
раздела прячется под «Код этого раздела». В заданные места вставляются живые блоки (site/blocks_*.py):
ползунки и переключатели, которые пересчитывают графики прямо в браузере.
"""
from __future__ import annotations

import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PUB = SITE / "public"

sys.path.insert(0, str(SITE))
import blocks_common  # noqa: E402
import blocks_fonts  # noqa: E402
import blocks_fonts_site  # noqa: E402
import blocks_wine  # noqa: E402

UP = re.compile(r"\n*<sub>\[↑ к содержанию\]\(#toc\)</sub>\n*")
HEAD = re.compile(r"^(#{1,4}) (.+)$", re.M)


def lit(s: str) -> str:
    """Строка для кода приложения: в base64, чтобы при экспорте не потерялись обратные слеши (формулы LaTeX)."""
    return blocks_common.pystr(s)


def sections(nb: dict):
    """Разбить ноутбук на разделы: новый раздел начинается с markdown-ячейки с заголовком."""
    out, cur = [], None
    for c in nb["cells"][1:]:                       # ячейка 0 — шапка и оглавление, её собираем отдельно
        src = "".join(c["source"])
        if c["cell_type"] == "markdown" and HEAD.search(src):
            cur = {"anchors": re.findall(r'<a id="([^"]+)"', src), "items": [], "code": []}
            out.append(cur)
        if cur is None:
            cur = {"anchors": [], "items": [], "code": []}
            out.append(cur)
        if c["cell_type"] == "markdown":
            cur["anchors"] += [a for a in re.findall(r'<a id="([^"]+)"', src) if a not in cur["anchors"]]
            text = UP.sub("\n", src).strip()
            if text:
                cur["items"].append(("md", text))
        else:
            cur["code"].append("".join(c["source"]).strip())
            for o in c.get("outputs", []):
                cur["items"].append(("out", o))
    return out


def out_item(o: dict, asset_dir: Path, prefix: str, key: str) -> str | None:
    """Python-выражение marimo для одного вывода ячейки."""
    d = o.get("data", {})
    if "image/png" in d:
        png = d["image/png"]
        png = "".join(png) if isinstance(png, list) else png
        name = f"{prefix}{key}.png"
        (asset_dir / name).write_bytes(base64.b64decode(png))
        return f"fig({lit(name)})"
    if "text/html" in d:
        return f"table_html({lit(''.join(d['text/html']))})"
    text = o.get("text") or d.get("text/plain")
    if text:
        text = "".join(text)
        if text.strip().startswith("<Figure size") or not text.strip():
            return None
        return f"out_text({lit(text.rstrip())})"
    return None


def build(nb_path: Path, out_py: Path, asset_dir: Path, prefix: str, module, title: str) -> None:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    asset_dir.mkdir(parents=True, exist_ok=True)
    for f in asset_dir.glob(f"{prefix}*.png"):
        f.unlink()
    head = "".join(nb["cells"][0]["source"])
    toc = head[head.index('<a id="toc">'):] if '<a id="toc">' in head else ""
    head = head[:head.index('<a id="toc">')] if '<a id="toc">' in head else head

    cells = [module.SETUP, module.cover(head)]
    cells.append(blocks_common.toc_cell(toc, module.EXTRA_TOC))
    n_img = 0
    for si, sec in enumerate(sections(nb)):
        exprs = []
        for kind, val in sec["items"]:
            if kind == "md":
                exprs.append(f"mo.md({lit(val)})")
            else:
                e = out_item(val, asset_dir, prefix, f"{si:03d}_{n_img:02d}")
                n_img += 1
                if e:
                    exprs.append(e)
        code = "\n\n".join(c for c in sec["code"] if c)
        if code:
            exprs.append(f"code_block({lit(code)})")
        if not exprs:
            continue
        if len(exprs) == 1 and exprs[0].startswith("mo.md("):   # только заголовок части: без рамки, как разделитель
            cells.append(f"@app.cell(hide_code=True)\ndef _(mo):\n    {exprs[0]}\n    return\n")
            for a in sec["anchors"]:
                cells.extend(module.BLOCKS.get(a, []))
            continue
        body = ",\n        ".join(exprs)
        cells.append(f'''@app.cell(hide_code=True)
def _(code_block, fig, mo, out_text, section, table_html):
    section(
        {body},
    )
    return
''')
        for a in sec["anchors"]:
            cells.extend(module.BLOCKS.get(a, []))
    text = module.header(title) + "\n\n".join(cells) + '\n\nif __name__ == "__main__":\n    app.run()\n'
    out_py.write_text(text, encoding="utf-8")
    (out_py.parent / module.CSS_FILE).write_text(blocks_common.css(module.THEME, tags=False), encoding="utf-8")
    compile(text, str(out_py), "exec")
    print(f"{out_py.relative_to(ROOT)}: {text.count('@app.cell')} ячеек, рисунков {len(list(asset_dir.glob(prefix + '*.png')))}")


HEAD_HTML = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Onest:wght@300..900&family=Unbounded:wght@300..900&family=Roboto+Flex:opsz,wdth,wght,YTLC@8..144,25..151,100..1000,416..570&display=swap">
"""


def main() -> None:
    PUB.mkdir(parents=True, exist_ok=True)
    (SITE / "head.html").write_text(HEAD_HTML, encoding="utf-8")   # шрифты для всей страницы (в <head>)
    # данные и код для живых блоков
    for src, dst in ((ROOT / "wine/data/winequality-white.csv", "winequality-white.csv"),
                     (ROOT / "wine/data/winequality-red.csv", "winequality-red.csv"),
                     (ROOT / "fonts/data/fonts.csv", "fonts.csv"),
                     (ROOT / "fonts/labrng/generators.py", "generators.py")):
        shutil.copy(src, PUB / dst)

    # основная работа: выполнить копию ноутбука в серой теме
    with tempfile.TemporaryDirectory() as tmp:
        w = Path(tmp) / "wine"
        shutil.copytree(ROOT / "wine", w, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        env = dict(os.environ, LAB_THEME="gray")
        r = subprocess.run([sys.executable, "tools/run_nb.py", "lab01.ipynb"], cwd=w, env=env,
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout[-2000:] + r.stderr[-2000:])
        build(w / "lab01.ipynb", SITE / "wine_app.py", PUB / "wine", "w", blocks_wine,
              "Lab01 · Белое вино")

    build(ROOT / "fonts/fonts.ipynb", SITE / "fonts_app.py", PUB / "fonts", "f", blocks_fonts,
          "Lab01 · КТвД · Шрифт как случайная величина")

    # сайт про шрифты (витрина): написан прямо на marimo, без ноутбука
    shutil.copy(ROOT / "fonts/figures/fonts_measure.png", PUB / "fonts_measure.png")
    text = blocks_fonts_site.app_text()
    compile(text, "fonts_site_app.py", "exec")
    (SITE / "fonts_site_app.py").write_text(text, encoding="utf-8")
    (SITE / blocks_fonts_site.CSS_FILE).write_text(blocks_fonts_site.CSS, encoding="utf-8")
    print(f"site/fonts_site_app.py: {text.count('@app.cell')} ячеек")


if __name__ == "__main__":
    main()
