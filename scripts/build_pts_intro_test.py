#!/usr/bin/env python3
"""Generate intro PTS test DOCX in the style of ТЕСТ_ТЕХ_2025."""

from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

OUT = Path(__file__).resolve().parents[1] / "ТЕСТ_ПТС_вводное.docx"


def set_run_font(run, size=14):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)


def add_q(doc, num, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.space_before = Pt(8)
    r1 = p.add_run(str(num))
    set_run_font(r1)
    r2 = p.add_run(f". {text}")
    set_run_font(r2)


def build():
    doc = Document()
    sec = doc.sections[0]
    # A4-ish margins close to ТЕСТ_ТЕХ_2025
    sec.left_margin = Pt(85.5)  # ~30mm-ish via EMU below
    from docx.shared import Twips, Emu

    sec.page_width = Emu(7560310)
    sec.page_height = Emu(10692130)
    sec.left_margin = Emu(1080135)
    sec.right_margin = Emu(539750)
    sec.top_margin = Emu(720090)
    sec.bottom_margin = Emu(720090)

    h = doc.add_paragraph()
    r = h.add_run("ТЕСТ_ТЕХ · ПТС · вводное занятие")
    set_run_font(r, 14)
    r.bold = True

    add_q(doc, 1, "Соедините термин и его определение:")
    doc.add_paragraph()

    rows = [
        ("Выпускающий режиссёр", "А) строит кадр, держит фокус, слушает команды"),
        ("Режиссёр трансляции", "Б) звук в программу и связь с организаторами по сценарию"),
        ("Инженер ПТС", "В) отвечает за эфир целиком и финальное «можно в эфир»"),
        ("Оператор", "Г) графика в эфире: слои, переходы, визуальный ритм"),
        ("Виджей трансляции", "Д) решает, что в программе: переключения, темп, крупности"),
        ("Звук / продюсер", "Е) коммутация, сигналы, железо, стрим"),
    ]
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = "Table Grid"
    tbl_ind = OxmlElement("w:tblInd")
    tbl_ind.set(qn("w:w"), "775")
    tbl_ind.set(qn("w:type"), "dxa")
    table._tbl.tblPr.append(tbl_ind)
    for i, (left, right) in enumerate(rows):
        c0, c1 = table.rows[i].cells
        c0.text = ""
        c1.text = ""
        set_run_font(c0.paragraphs[0].add_run(left), 12)
        set_run_font(c1.paragraphs[0].add_run(right), 12)

    add_q(doc, 2, "Зачем нужны трансляции? Дайте определение «ПТС».")
    add_q(doc, 3, "Какими бывают трансляции? Назовите форматы и различие по числу камер.")
    add_q(doc, 4, "Опишите пайплайн трансляции от источника до зрителя.")
    add_q(doc, 5, "Что относится к железу, а что к софту на трансляции?")
    add_q(doc, 6, "Назовите площадки работы ПТС и форматы обучения на курсе.")

    sit = doc.add_paragraph()
    sit.paragraph_format.space_before = Pt(12)
    r = sit.add_run("Ситуация: ")
    set_run_font(r, 14)
    set_run_font(
        sit.add_run(
            "Вы — инженер прямой трансляции мероприятия. Во время эфира режиссёр "
            "сообщает, что картинка от одной из ключевых камер резко пропала и в "
            'мониторе вместо изображения — ошибка "No Signal". При этом другие камеры '
            "работают нормально. Ваши действия?"
        ),
        14,
    )

    doc.save(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
