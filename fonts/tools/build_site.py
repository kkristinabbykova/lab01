"""Собрать файлы для marimo-ноутбука и сайта.

    python tools/build_site.py

1. Копирует код датчиков и данные в public/: в браузере (WASM) ноутбук берёт их оттуда.
3. Собирает лендинг docs/index.html (tools/build_landing.py), он ведёт на датчик.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"


def main():
    PUB.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "labrng" / "generators.py", PUB / "generators.py")
    shutil.copy(ROOT / "data" / "fonts.csv", PUB / "fonts.csv")
    print("public/ обновлена")
    code = 0
    subprocess.call([sys.executable, str(ROOT / "tools" / "build_landing.py")])   # лендинг docs/index.html
    # отчёт: ноутбук без кода, с работающими якорями и формулами (GitHub так не умеет)
    subprocess.call([sys.executable, str(ROOT / "tools" / "export_nb.py"), str(ROOT / "fonts.ipynb"), str(ROOT / "docs" / "fonts.html")])
    return code


if __name__ == "__main__":
    sys.exit(main())
