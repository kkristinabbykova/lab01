# Lab01 · Прикладная статистика · осень 2026

**Сайт работы:** https://kkristinabbykova.github.io/lab01/

Лабораторная работа из двух частей в одном репозитории и на одном сайте.

| Часть | Папка | На сайте |
|---|---|---|
| Основная работа: белое вино как случайный эксперимент (спринты 1 и 2) | [`wine/`](wine/) | [отчёт на marimo](https://kkristinabbykova.github.io/lab01/wine/) |
| Доп. задание КТвД: шрифт как случайная величина | [`fonts/`](fonts/) | [сайт про шрифты](https://kkristinabbykova.github.io/lab01/fonts/) · [отчёт на marimo](https://kkristinabbykova.github.io/lab01/fonts/report/) · [датчик](https://kkristinabbykova.github.io/lab01/fonts/datchik/) |

Ноутбуки: [`wine/lab01.ipynb`](wine/lab01.ipynb) и [`fonts/fonts.ipynb`](fonts/fonts.ipynb).

## Авторы (команда 27)

- Нефедьева Антонина Сергеевна, ИСУ 502335, трек «Инфохимия»: спринт 1, пакет `labstat`.
- Быкова Кристина Денисовна, ИСУ 501322, трек КТвД: спринты 1 и 2, оформление, доп. задание КТвД, сайт.

## Сайт

Отчёты и сайт про шрифты сделаны на **marimo** и работают прямо в браузере (WebAssembly), ничего ставить не нужно.
В каждом: оглавление в боковой панели, «Код этого раздела» под каждым разделом, живые блоки с ползунками.
Тексты, таблицы и рисунки берутся из выполненных ноутбуков; рисунки вина собраны в серой теме
(`LAB_THEME=gray`), в самих ноутбуках стиль прежний.

| Путь | Что это |
|---|---|
| `site/blocks_common.py` | общие функции приложений: рисунки, таблицы, код раздела, карточки, стиль |
| `site/blocks_wine.py`, `site/blocks_fonts.py` | обложка, тема и живые блоки каждого отчёта |
| `site/blocks_fonts_site.py` | сайт про шрифты на marimo: витрина, «попробуй сам», датчик новых шрифтов |
| `site/wine_app.py`, `site/fonts_app.py`, `site/fonts_site_app.py` | готовые marimo-приложения (собираются, руками не правятся) |
| `tools/build_apps.py` | ноутбук → marimo-приложение |
| `tools/build_site.py` | весь сайт в `docs/`: общая страница, оба приложения, сайт про шрифты |
| `.github/workflows/site.yml` | на каждый push: тесты обеих частей → сборка → GitHub Pages |

## Запуск у себя

```bash
pip install -r requirements.txt
(cd wine && python -m pytest -q)     # тесты основной работы
(cd fonts && python -m pytest -q)    # тесты доп. задания
marimo run site/wine_app.py          # отчёт по вину локально
marimo run site/fonts_app.py         # отчёт по шрифтам
python tools/build_site.py           # собрать весь сайт в docs/
```

## Публикация (один раз)

1. На GitHub: **Settings → Pages → Source: GitHub Actions**.
2. После каждого `git push` вкладка **Actions** собирает сайт за 3–5 минут.
