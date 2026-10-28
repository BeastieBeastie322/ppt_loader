# Вводное занятие

Трансляции: зачем и с чем едят. Введение в направление ПТС.

## Материалы

| Файл | Назначение |
|------|------------|
| `PTS-vvodnoe.html` | Презентация (фото вшиты) |
| `PTS-vvodnoe.pptx` | Копия для PowerPoint |
| `PTS-vvodnoe-tekst.md` | Текст лектора к слайдам |
| `PTS_Obshchiy_kurs_vvodnoe.pdf` | Конспект / раздатка для слушателей |
| `ТЕСТ_ПТС_вводное.docx` | Тест (6 вопросов) |
| `ТЕСТ_ПТС_вводное_ключи.txt` | Ключи ответов |

## Сборка

```bash
python3 scripts/build_pts_handout.py      # конспект PDF
python3 scripts/build_pts_intro_test.py   # тест DOCX
python3 ../scripts/html_deck_to_pptx.py PTS-vvodnoe.html -o PTS-vvodnoe.pptx
```

> `presentation-legacy/` — старая копия презентации; актуальная — `PTS-vvodnoe.html`.
