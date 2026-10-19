#!/usr/bin/env python3
"""Generate PTS intro handout PDF in the style of the reference document."""

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("Body", FONT_REG))
pdfmetrics.registerFont(TTFont("BodyBold", FONT_BOLD))

OUT = Path("/workspace/PTS_Obshchiy_kurs_vvodnoe.pdf")


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleRU",
            parent=base["Normal"],
            fontName="BodyBold",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleRU",
            parent=base["Normal"],
            fontName="Body",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "h_theses": ParagraphStyle(
            "ThesesH",
            parent=base["Normal"],
            fontName="Body",
            fontSize=12,
            leading=16,
            spaceBefore=2,
            spaceAfter=4,
        ),
        "part": ParagraphStyle(
            "PartH",
            parent=base["Normal"],
            fontName="Body",
            fontSize=12,
            leading=16,
            spaceBefore=2,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "BodyRU",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "body_left": ParagraphStyle(
            "BodyLeft",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=15,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "BulletRU",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=15,
            leftIndent=14,
            firstLineIndent=0,
            spaceAfter=3,
        ),
        "subhead": ParagraphStyle(
            "Subhead",
            parent=base["Normal"],
            fontName="Body",
            fontSize=11,
            leading=15,
            spaceBefore=4,
            spaceAfter=4,
        ),
    }


def u(text: str) -> str:
    return f"<u>{text}</u>"


def b(text: str) -> str:
    return f"<b>{text}</b>"


def dash(term: str, desc: str, s) -> Paragraph:
    # Em dash as list marker (Liberation Sans has no U+23AF ⎯)
    return Paragraph(f"— {b(term)} – {desc}", s["bullet"])


def plain_dash(text: str, s) -> Paragraph:
    return Paragraph(f"— {text}", s["bullet"])


def hr():
    return HRFlowable(
        width="100%",
        thickness=0.6,
        color=(0.55, 0.55, 0.55),
        spaceBefore=8,
        spaceAfter=8,
    )


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Вводное занятие по теме ПТС",
        author="ТЕХ ГУАП · направление ПТС",
    )

    story = []

    # Title
    story.append(Paragraph("ВВОДНОЕ ЗАНЯТИЕ ПО ТЕМЕ ПТС", s["title"]))
    story.append(Paragraph("Трансляции: зачем и с чем едят", s["subtitle"]))

    story.append(Paragraph("Тезисы на занятие:", s["h_theses"]))
    for t in [
        "Что такое трансляция и чем занимается ПТС?",
        "Зачем нужны трансляции и какими они бывают?",
        "Пайплайн эфира: от источника до зрителя.",
        "Железо, софт и команда на трансляции.",
        "Площадки работы и как устроен курс дальше.",
    ]:
        story.append(plain_dash(t, s))

    story.append(hr())

    # Part 1
    story.append(Paragraph("Часть 1. Введение в трансляции и ПТС", s["part"]))
    story.append(
        Paragraph(
            f"{u(b('Трансляция'))} – это процесс передачи аудио- и видеосигнала "
            f"от места события к аудитории за пределами зала: в прямой эфир, "
            f"в запись, в онлайн-встречу или в удалённое помещение.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            f"{u(b('ПТС (Передвижная телевизионная станция)'))} – направление "
            f"студии ТЕХ ГУАП и одновременно вся цепочка, которая увозит событие "
            f"за пределы площадки: камеры, сигнал, микшер, доставка и зритель.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "Мы <b>не видеооператоры</b> по основной роли. Иногда выходим "
            "видеооператорами на эфир и с камерами работаем не хуже. "
            "Суперсила ПТС – связать камеру, сигнал, микшер и доставку до зрителя.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            f"{u('Куда уходит картинка:')}",
            s["subhead"],
        )
    )
    for term, desc in [
        ("Прямой эфир", "VK, YouTube и другие платформы."),
        ("Онлайн-встреча", "Zoom, TrueConf и похожие сервисы."),
        ("Запись", "архив, нарезки, отчётность."),
        ("Удалённый зал", "трансляция в другое помещение."),
    ]:
        story.append(dash(term, desc, s))

    story.append(hr())

    # Part 2
    story.append(Paragraph("Часть 2. Зачем нужны трансляции", s["part"]))
    story.append(
        Paragraph(
            f"{u('Трансляция нужна не «для галочки», а как отдельный продукт рядом с живым залом:')}",
            s["subhead"],
        )
    )
    for term, desc in [
        ("Доступность", "событие видят те, кто не попал в зал. Live сейчас — и архив потом."),
        ("Расширение аудитории", "эфир выносит мероприятие за стены площадки: университет, город, партнёры, выпускники."),
        (
            "Удалённые команды и конференции",
            "когда спикеры и слушатели в разных городах, трансляция — общий «зал».",
        ),
        (
            "Качество события",
            "контроль картинки и звука, фиксация «как было», ответственность за эфир.",
        ),
    ]:
        story.append(dash(term, desc, s))

    story.append(hr())

    # Part 3
    story.append(Paragraph("Часть 3. Какими бывают трансляции", s["part"]))
    story.append(Paragraph(f"{u('Основные форматы:')}", s["subhead"]))
    for term, desc in [
        ("Live", "онлайн-эфир в реальном времени."),
        ("Гибрид", "зал плюс удалённые спикеры и зрители."),
        ("Запись / IMAG", "фиксация на диск и/или показ на экранах зала."),
        ("Студийная", "подкасты, интервью, ток-шоу."),
    ]:
        story.append(dash(term, desc, s))
    story.append(Paragraph(f"{u('По количеству камер:')}", s["subhead"]))
    story.append(dash("Однокамерная", "простой эфир, лекция, дисциплина кадра.", s))
    story.append(
        dash(
            "Многокамерная",
            "режиссёр переключает планы в эфире: общий, средний, детали, реакция зала.",
            s,
        )
    )

    story.append(hr())

    # Part 4
    story.append(Paragraph("Часть 4. Пайплайн трансляции", s["part"]))
    story.append(
        Paragraph(
            f"{u('Базовая цепочка от сцены до зрителя почти всегда одна и та же:')}",
            s["subhead"],
        )
    )
    for term, desc in [
        ("Источник", "камеры, ПК, презентации, графика."),
        ("Сигнал", "кабели, конвертеры, матрицы."),
        ("Микшер", "vMix / пульты, переключения."),
        ("Доставка", "RTMP / SRT / NDI, стрим."),
        ("Зритель", "платформа, экран, архив."),
    ]:
        story.append(dash(term, desc, s))
    story.append(
        Paragraph(
            "Если ломается эфир — ищите разрыв в этой цепочке.",
            s["body"],
        )
    )

    story.append(hr())

    # Part 5
    story.append(Paragraph("Часть 5. Железо и софт", s["part"]))
    story.append(Paragraph(f"{u('Железо:')}", s["subhead"]))
    for term, desc in [
        ("Камеры", "точки съёмки и вход сигнала в тракт."),
        ("Коммутация", "кабели, сплиттеры, матрицы, конвертеры."),
        ("Микшер", "железный или программный пульт, куда всё сходится."),
    ]:
        story.append(dash(term, desc, s))
    story.append(Paragraph(f"{u('Софт:')}", s["subhead"]))
    for term, desc in [
        ("vMix", "основной программный микшер: входы, выходы, стрим, запись."),
        ("Контент", "титры, бамперы, стингеры, презентации."),
        ("Кодеки и доставка", "как пишем материал и как отдаём зрителю."),
        ("Сети и стандарты", "NDI, Dante, RTMP/SRT и передача «по кабелю»."),
    ]:
        story.append(dash(term, desc, s))

    story.append(hr())

    # Part 6
    story.append(Paragraph("Часть 6. Команда трансляции", s["part"]))
    story.append(
        Paragraph(
            f"{u('Для успешного проведения трансляции нужна понятная смена ролей:')}",
            s["subhead"],
        )
    )
    for term, desc in [
        ("Выпускающий режиссёр", "отвечает за эфир целиком и финальное «можно в эфир»."),
        ("Режиссёр трансляции", "решает, что в программе: переключения, темп, крупности."),
        ("Инженер ПТС", "коммутация, сигналы, железо, стрим."),
        ("Оператор", "строит кадр, держит фокус, слушает команды."),
        ("Виджей трансляции", "графика в эфире: слои, переходы, визуальный ритм."),
        ("Звук / продюсер", "звук в программу и связь с организаторами по сценарию."),
    ]:
        story.append(dash(term, desc, s))
    story.append(
        Paragraph(
            "Один человек может закрывать несколько постов — но зоны ответственности должны быть понятны.",
            s["body"],
        )
    )

    story.append(hr())

    # Part 7
    story.append(Paragraph("Часть 7. Где мы работаем", s["part"]))
    story.append(Paragraph(f"{u('Основные площадки направления ПТС:')}", s["subhead"]))
    for term, desc in [
        ("Актовый зал", "крупные мероприятия и полноценные эфиры."),
        ("ПТСКА", "наша рабочая зона: сборка, учебка, железо."),
        ("Внешние площадки", "выезды, типовые схемы, быстрый разворот, полевые условия."),
    ]:
        story.append(dash(term, desc, s))
    story.append(
        Paragraph(
            "На разных площадках одна логика пайплайна — разный темп и запас по времени.",
            s["body"],
        )
    )

    story.append(hr())

    # Part 8
    story.append(Paragraph("Часть 8. Как устроен курс дальше", s["part"]))
    story.append(
        Paragraph(
            "Деление условное: жёстких рамок «ты только инженер / только режиссёр» нет. "
            "Темы пересекаются.",
            s["body"],
        )
    )
    story.append(Paragraph(f"{u('Инженерные темы:')}", s["subhead"]))
    story.append(
        Paragraph(
            "сигналы и коммутация; оборудование и стандарты по кабелю; кодеки и доставка; "
            "vMix; сети (NDI, Dante, SRT, RTMP); типовые схемы и «нулевая» трансляция.",
            s["body"],
        )
    )
    story.append(Paragraph(f"{u('Режиссёрские темы:')}", s["subhead"]))
    story.append(
        Paragraph(
            "монтаж в трансляции; построение кадра и крупности; операторские приёмы; "
            "свет и цвет; камера; дизайн в эфире и работа с контентом.",
            s["body"],
        )
    )
    story.append(Paragraph(f"{u('Форматы обучения:')}", s["subhead"]))
    for term, desc in [
        ("Лекции", "теория."),
        ("Практики", "работа руками на железе и в vMix."),
        ("Нулевая трансляция", "эфир с нуля как проверка, что всё сложилось."),
    ]:
        story.append(dash(term, desc, s))
    story.append(
        Paragraph(
            "Цель курса — не сдать теорию, а уметь поднять трансляцию.",
            s["body"],
        )
    )

    story.append(hr())

    # Part 9
    story.append(Paragraph("Часть 9. Итоги", s["part"]))
    story.append(
        Paragraph(
            "Успешная трансляция — это понятный пайплайн, исправное железо и софт, "
            "слаженная команда и ответственность за картинку до зрителя. "
            "ПТС делает событие видимым за пределами зала.",
            s["body"],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "<b>Лектор:</b> Тоскин Вадим — руководитель направления ПТС<br/>"
            "<b>Студия:</b> ТЕХ ГУАП",
            s["body_left"],
        )
    )

    doc.build(story)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
