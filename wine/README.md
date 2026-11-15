# Lab01: исследование датасета и датчик случайных чисел

Прикладная статистика, осень 2026. Команда: трек «Инфохимия» (lab.ic.01) + трек КТвД. Готовы **спринт 1** (исследование) и **спринт 2** (датчик pH: полярный метод + метод обратных функций, раздел 6–7 ноутбука), ноутбук оформлен по критериям КТвД. Доп. задание КТвД (шрифты, датчик на marimo, сайт) — в папке `fonts/` этого репозитория.

Основной файл работы: **`lab01.ipynb`**. Структура разделов по условию лабораторной:

```
# Lab01 - sprint 1
## Dataset: Wine Quality (белые вина)
## Random Variable 01 (pH)
## Random Variable 02 (фиксированная кислотность)
## Random Variable 03 (спирт)
   ### Description · EDA & Distribution · Independence & Estimations
   ### Normalization · Sample vs Population · Hypotheses · Resume
## Lab resume
   ### Итоговые метрики · гипотезы · выводы · литература · cat_mark_table
# Lab01 - sprint 2
## Датчик pH: полярный метод и метод обратных функций · исследование 10 алгоритмов датчиков · метрики · литература
```

## Что где лежит

| Путь | Что это |
|---|---|
| `lab01.ipynb` | исследование, выполненный ноутбук с графиками |
| `ph_generator.py` | датчик pH (спринт 2): полярный метод и метод обратных функций; тесты `tests/test_ph_generator.py` |
| `labrng/` | 10 алгоритмов датчиков для раздела 7 (исследование алгоритмов): 6 методов и 4 базовых датчика; тесты `tests/test_labrng.py` |
| `labstat/` | личный пакет: громоздкий код вынесен сюда, чтобы ноутбук читался |
| `tests/` | автотесты пакета (pytest) |
| `figures/` | все графики ноутбука в PNG |
| `data/` | исходные CSV Wine Quality (белые и красные) |
| `tools/` | `run_nb.py` выполняет ноутбук без Jupyter, `ktvd_format.py` — оформление по критериям КТвД |

## Как запустить

```bash
pip install -r requirements.txt
python -m pytest -q          # 69 тестов (из папки wine/)
jupyter notebook lab01.ipynb # выполнить сверху вниз
```

Без Jupyter ноутбук можно выполнить так: `python tools/run_nb.py lab01.ipynb`.

Ноутбук запускается из папки `wine/`. В Colab: [открыть ноутбук](https://colab.research.google.com/github/kkristinabbykova/lab01/blob/main/wine/lab01.ipynb), первая ячейка с кодом сама скачает репозиторий и перейдёт в папку `wine/`. Если папки `data/` нет, данные скачаются с зеркала на GitHub, контрольная сумма SHA-256 проверяется.

## Данные

Wine Quality: Cortez P., Cerdeira A., Almeida F., Matos T., Reis J. Modeling wine preferences by data mining from physicochemical properties // Decision Support Systems. 2009. Vol. 47, № 4. P. 547–553. UCI Machine Learning Repository, DOI 10.24432/C56S3T. Файлы взяты с зеркала github.com/zygmuntz/wine-quality, размер совпадает с оригиналом UCI (264 426 и 84 199 байт).

## Авторы

Нефедьева Антонина Сергеевна, ИСУ 502335 (Инфохимия): исследование вин, пакет `labstat`, проверка и правка текстов обоих спринтов.
Быкова Кристина Денисовна, ИСУ 501322, команда 27 (КТвД): оформление ноутбука, тексты выводов спринта 1, спринт 2 (датчик pH); доп. задание в папке `fonts/`.
