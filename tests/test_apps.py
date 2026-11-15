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
    import base64
    figs = [base64.b64decode(b).decode() for b in re.findall(r'fig\(__import__\("base64"\)\.b64decode\("([^"]+)"\)', src)]
    assert figs
    for f in figs:
        assert (ROOT / "site" / "public" / folder / f).exists(), f


def test_public_generators_in_sync():
    assert (ROOT / "site" / "public" / "generators.py").read_text() == (ROOT / "fonts" / "labrng" / "generators.py").read_text()


def test_fonts_site_app():
    src = (ROOT / "site" / "fonts_site_app.py").read_text(encoding="utf-8")
    compile(src, "fonts_site_app.py", "exec")
    for anchor in ("fonts", "play", "rng"):
        assert f'id="{anchor}"' in src
    assert (ROOT / "site" / "public" / "fonts_measure.png").exists()


@pytest.mark.parametrize("name", APPS + ["fonts_site_app.py"])
def test_no_double_backslashes(name):
    """При экспорте в WebAssembly «\\\\» в коде ячеек превращается в «\\» и ломает LaTeX: тексты хранятся в base64."""
    assert "\\\\" not in (ROOT / "site" / name).read_text(encoding="utf-8")
