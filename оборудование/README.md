# Оборудование для трансляций

Какая задача → какое соединение → какое оборудование.

## Материалы

| Файл | Назначение |
|------|------------|
| `PTS-oborudovanie.html` | Презентация (фото вшиты) |
| `PTS-oborudovanie.pptx` | Копия для PowerPoint |
| `PTS-oborudovanie-tekst.md` | Подробный текст лектора |
| `PTS_Oborudovanie_konspekt.pdf` | Конспект для слушателей |
| `PTS_Oborudovanie_konspekt.md` | Тот же конспект в Markdown |
| `assets/equipment/` | Исходники фото + ATTRIBUTION.md |

## Сборка

```bash
python3 scripts/build_pts_equipment_deck.py      # пересборка HTML
python3 scripts/build_pts_equipment_handout.py   # конспект PDF + MD
python3 ../scripts/html_deck_to_pptx.py PTS-oborudovanie.html -o PTS-oborudovanie.pptx
```
