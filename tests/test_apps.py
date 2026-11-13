"""Проверки marimo-приложений сайта (site/*_app.py)."""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
APPS = ["wine_app.py", "fonts_app.py"]


@pytest.mark.parametrize("name", APPS)
def test_app_is_valid_python(name):
    compile((ROOT / "site" / name).read_text(encoding="utf-8"), name, "exec")


@pytest.mark.parametrize("name", APPS)
def test_app_has_toc_code_and_live_blocks(name):
    src = (ROOT / "site" / name).read_text(encoding="utf-8")
    assert "mo.sidebar" in src                # оглавление
    assert src.count("code_block(") > 5       # код под разделами
    assert src.count("live(") > 5             # живые блоки


@pytest.mark.parametrize("name", APPS)
def test_app_figures_exist(name):
    import re
    src = (ROOT / "site" / name).read_text(encoding="utf-8")
    folder = "wine" if name.startswith("wine") else "fonts"
    figs = re.findall(r'fig\("([^"]+\.png)"\)', src)
    assert figs
    for f in figs:
        assert (ROOT / "site" / "public" / folder / f).exists(), f


def test_public_generators_in_sync():
    assert (ROOT / "site" / "public" / "generators.py").read_text() == (ROOT / "fonts" / "labrng" / "generators.py").read_text()
