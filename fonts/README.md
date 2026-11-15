# Lab01 · КТвД: шрифты, интерактивный датчик, сайт

Быкова Кристина Денисовна (ИСУ 501322), команда 27, трек «Компьютерные технологии в дизайне».
Прикладная статистика, осень 2026. Доп. задание КТвД к лабораторной работе 01.

Это папка доп. задания КТвД: собственный датасет шрифтов, датчик случайных чисел для их пропорций,
интерактив на marimo и сайт. Основная часть лабораторной (вино) лежит рядом, в папке `wine/`.

**Сайт про шрифты:** https://kkristinabbykova.github.io/lab01/fonts/  
**Отчёт (marimo, живые блоки):** https://kkristinabbykova.github.io/lab01/fonts/report/  
**Открыть в Colab:** https://colab.research.google.com/github/kkristinabbykova/lab01/blob/main/fonts/fonts.ipynb  
**Вся работа:** https://kkristinabbykova.github.io/lab01/

## Что здесь

| Файл | Что это |
|---|---|
| [`fonts.ipynb`](fonts.ipynb) | доп. задание: собственный датасет шрифтов, две случайные величины (x-height и толщина штриха), EDA, (не)зависимость, гипотеза |
| `docs/index.html` | лендинг сайта: график шрифтов с приближением, «Попробуй сам», живой датчик x-height и толщины штриха (собирается `tools/build_landing.py`) |
| `labfont/` | измерение пропорций шрифтов по контурам букв (fontTools), схема измерений |
| `labrng/` | датчики: PCG64, вихрь Мерсенна, ЛКГ, RANDU; квантильный, обратная функция, Бокс–Мюллер, полярный, отношений, Неймана |
| `labstat/` | статистические функции и стиль графиков из основной части (автор Нефедьева А. С.) |
| `tests/` | автотесты: датчики, измеритель шрифтов, сборка сайта |
| `data/` | `fonts.csv` (измерения 106 семейств, 100 в анализе — по 20 в каждой категории), `font_categories.csv` (категория и источник: выбор автора или случайный отбор), образец шрифта для схемы |
| `tools/` | сборка: случайный отбор шрифтов (`sample_google_fonts.py`), ноутбук шрифтов, исполнитель ноутбуков, сайт |
| `docs/` | сайт этой части: лендинг и `fonts.html`; в общий сайт копируется корневым `tools/build_site.py` |

## Критерии КТвД

| Критерий | Где |
|---|---|
| Структура, индексы разделов, якорные ссылки | `fonts.ipynb`: нумерация 1 → 1.1, оглавление, «↑ к содержанию» |
| Скрытие кода | код-ячейки свёрнуты, тег `hide-input` для HTML-экспорта |
| Масштабы, единицы, единый стиль графиков | все графики в стиле `labstat.plots`, единицы на осях, подписи «Рис. N» |
| Формулы в LaTeX | весь текст ноутбуков |
| Доп. задание: датасет, 2 величины, случайность, (не)зависимость, EDA | `fonts.ipynb`, разделы 1–4 |
| Интерактивность для генератора, marimo | сайт про шрифты `site/fonts_site_app.py` и отчёт `site/fonts_app.py` (в корне репозитория) |
| Доп. баллы: автотесты генератора, таблицы метрик, итеративные коммиты, литература | `tests/`, таблицы в ноутбуке и датчике, история git |

Тексты в `fonts.ipynb` (природа событий, что видно на графиках, вывод о зависимости, общие выводы) написаны автором;
литература — раздел 5.3 ноутбука (в том числе книги, найденные в каталоге РГБ).

## Запуск у себя

```bash
cd fonts
pip install -r requirements.txt
python -m pytest -q              # автотесты
jupyter notebook fonts.ipynb     # ноутбук (нужен pip install jupyter)
python ../tools/build_site.py    # собрать весь сайт (из корня репозитория)
```

## Публикация

Сайт собирается и публикуется для всего репозитория сразу: см. `README.md` в корне.

## Как добавить шрифты

На fonts.google.com добавь шрифты в подборку и нажми «Download all» **один раз** в конце.
Если семейства нет в `data/font_categories.csv`, допиши строку с категорией из каталога. Дальше:

```bash
python tools/unpack_fonts.py ПАПКА_С_ZIP fonts/
python -m labfont.collect fonts/ data/fonts.csv
python tools/build_fonts_nb.py && python tools/run_nb.py fonts.ipynb
python tools/build_site.py
git add -A && git commit -m "Шрифты: +N семейств" && git push
```

## Литература

1. Брингхерст Р. Основы стиля в типографике. М.: Д. Аронов, 2006.
2. Королькова А. Живая типографика. М.: IndexMarket, 2007.
3. Microsoft. OpenType specification (таблицы head, OS/2, hmtx, fvar).
4. Кнут Д. Э. Искусство программирования. Т. 2. Получисленные алгоритмы. 3-е изд. М.: Вильямс (ЛКГ, RANDU, § 3.3.4).
5. Box G. E. P., Muller M. E. A note on the generation of random normal deviates // Ann. Math. Statist. 1958. Vol. 29. P. 610–611.
6. Marsaglia G., Bray T. A. A convenient method for generating normal variables // SIAM Review. 1964. Vol. 6, № 3. P. 260–264.
7. Kinderman A. J., Monahan J. F. Computer generation of random variables using the ratio of uniform deviates // ACM TOMS. 1977. Vol. 3, № 3. P. 257–260.
8. Azzalini A. A class of distributions which includes the normal ones // Scand. J. Statist. 1985. Vol. 12. P. 171–178 (скошенное нормальное).
9. Matsumoto M., Nishimura T. Mersenne Twister // ACM TOMACS. 1998. Vol. 8, № 1. P. 3–30.
10. O'Neill M. E. PCG: A family of simple fast space-efficient statistically good algorithms for random number generation. HMC-CS-2014-0905, 2014.
11. Феличи Дж. Типографика: шрифт, верстка, дизайн / пер. с англ. — 2-е изд., перераб. и доп. — СПб. : БХВ-Петербург, 2014. — 496 с. — ISBN 978-5-9775-0908-4.
12. Соболь И. М. Численные методы Монте-Карло. — М. : Наука, 1973.
13. Ермаков С. М. Метод Монте-Карло в вычислительной математике : вводный курс. — М. : БИНОМ ; СПб. : Невский диалект, 2009.
14. Савелова Т. И. Метод Монте-Карло : учебное пособие. — М. : НИЯУ МИФИ, 2011.
15. Гордон Ю. Книга про буквы от Аа до Яя. — М. : Издательство Студии Артемия Лебедева, 2006. — ISBN 5-98062-006-0.
