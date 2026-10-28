#!/usr/bin/env python3
"""Convert a PTS HTML slide deck into a branded PowerPoint (.pptx) copy."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

BG = RGBColor(0x12, 0x08, 0x1C)
ACCENT = RGBColor(0xCC, 0x0C, 0x5E)
ACCENT_SOFT = RGBColor(0xFF, 0x4D, 0x8D)
TEXT = RGBColor(0xF7, 0xEE, 0xF5)
MUTED = RGBColor(0xC4, 0xA8, 0xBC)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


class SlideText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._buf: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "br":
            self._buf.append("\n")
        if tag in ("p", "h1", "h2", "h3", "li", "div") and self._buf and self._buf[-1] != "\n":
            self._buf.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if tag in ("p", "h1", "h2", "h3", "li", "section"):
            self._buf.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        t = data.strip()
        if t:
            self._buf.append(t + " ")

    def lines(self) -> list[str]:
        raw = "".join(self._buf)
        lines = [re.sub(r"\s+", " ", line).strip() for line in raw.splitlines()]
        lines = [line for line in lines if line]
        drop_exact = {"←", "→"}
        out: list[str] = []
        for line in lines:
            if line in drop_exact:
                continue
            if "шаг / слайд" in line.lower():
                continue
            if re.fullmatch(r"\d+\s*/\s*\d+", line):
                continue
            if line.startswith("ТЕХ ГУАП · ПТС") and len(line) < 20:
                continue
            out.append(line)
        return out


def extract_slides(html_path: Path) -> list[tuple[str, list[str]]]:
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    html = re.sub(r"<style[\s\S]*?</style>", "", html, flags=re.I)
    html = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.I)
    parts = re.split(r"(?=<section\b)", html)
    slides: list[tuple[str, list[str]]] = []
    for part in parts:
        if "<section" not in part:
            continue
        m = re.search(r'data-title="([^"]+)"', part)
        title = m.group(1) if m else "Слайд"
        body = re.search(r"(<section[\s\S]*?</section>)", part)
        chunk = body.group(1) if body else part
        chunk = re.sub(r"<img[^>]*>", "", chunk)
        parser = SlideText()
        parser.feed(chunk)
        lines = parser.lines()
        # Drop footer brand leftovers
        lines = [ln for ln in lines if ln != "ТЕХ ГУАП · ПТС"]
        slides.append((title, lines))
    return slides


def set_slide_bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)


def style_run(run, *, size_pt: float, bold: bool = False, color: RGBColor = TEXT) -> None:
    run.font.name = "Arial"
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = color


def build_pptx(html_path: Path, out_path: Path, deck_title: str) -> None:
    slides = extract_slides(html_path)
    if not slides:
        raise SystemExit(f"No slides found in {html_path}")

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    margin = Inches(0.7)
    content_w = SLIDE_W - margin * 2

    for idx, (title, lines) in enumerate(slides):
        slide = prs.slides.add_slide(blank)
        set_slide_bg(slide, BG)

        # Accent bar
        bar = slide.shapes.add_shape(
            1,  # rectangle
            Inches(0),
            Inches(0),
            SLIDE_W,
            Inches(0.08),
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT
        bar.line.fill.background()

        # Eyebrow / title
        is_title = idx == 0
        body_lines = list(lines)

        # Prefer data-title as heading unless title slide
        heading = title if not is_title else (body_lines[0] if body_lines else title)
        if not is_title:
            # Remove first occurrences that duplicate the heading/eyebrow
            cleaned: list[str] = []
            seen_heading = False
            for ln in body_lines:
                if not seen_heading and (ln == title or ln.lower() == title.lower()):
                    seen_heading = True
                    continue
                cleaned.append(ln)
            body_lines = cleaned

        if is_title:
            # Brand line
            box = add_textbox(slide, margin, Inches(1.6), content_w, Inches(0.5))
            p = box.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            run = p.add_run()
            run.text = "ТЕХ ГУАП · направление ПТС"
            style_run(run, size_pt=16, bold=True, color=ACCENT_SOFT)

            # Main title from lines
            title_text = " ".join(body_lines[1:3]) if len(body_lines) >= 3 else " ".join(body_lines[1:]) or title
            if len(body_lines) >= 2 and body_lines[0].startswith("ТЕХ ГУАП"):
                # use remaining lines as title/subtitle
                main = []
                sub = []
                for ln in body_lines[1:]:
                    if not main or sum(len(x) for x in main) < 40:
                        main.append(ln)
                    else:
                        sub.append(ln)
                title_text = " ".join(main)
                subtitle = " ".join(sub)
            else:
                subtitle = ""

            box = add_textbox(slide, margin, Inches(2.3), content_w, Inches(2.2))
            tf = box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = title_text
            style_run(run, size_pt=40, bold=True, color=TEXT)

            if subtitle:
                box = add_textbox(slide, margin, Inches(4.8), content_w, Inches(1.2))
                p = box.text_frame.paragraphs[0]
                run = p.add_run()
                run.text = subtitle
                style_run(run, size_pt=18, color=MUTED)
        else:
            # Section heading
            box = add_textbox(slide, margin, Inches(0.35), content_w, Inches(0.9))
            p = box.text_frame.paragraphs[0]
            run = p.add_run()
            run.text = heading
            style_run(run, size_pt=28, bold=True, color=TEXT)

            # Body bullets / paragraphs
            box = add_textbox(slide, margin, Inches(1.35), content_w, Inches(5.5))
            tf = box.text_frame
            tf.word_wrap = True
            first = True
            for ln in body_lines:
                if first:
                    p = tf.paragraphs[0]
                    first = False
                else:
                    p = tf.add_paragraph()
                p.space_after = Pt(8)
                # Treat short labels / list-like lines as bullets
                text = ln
                if ln.startswith("— "):
                    text = ln
                elif len(ln) < 48 and not ln.endswith("."):
                    text = f"— {ln}"
                run = p.add_run()
                run.text = text
                # Slightly emphasize very short headings inside body
                emphasize = len(ln) <= 28 and not ln.endswith(".")
                style_run(run, size_pt=16 if not emphasize else 17, bold=emphasize, color=TEXT if emphasize else MUTED)

        # Footer
        foot = add_textbox(slide, margin, SLIDE_H - Inches(0.45), content_w * 0.7, Inches(0.3))
        p = foot.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = "ТЕХ ГУАП · ПТС"
        style_run(run, size_pt=10, color=MUTED)

        num = add_textbox(slide, SLIDE_W - margin - Inches(1.2), SLIDE_H - Inches(0.45), Inches(1.2), Inches(0.3))
        p = num.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        run = p.add_run()
        run.text = f"{idx + 1} / {len(slides)}"
        style_run(run, size_pt=10, color=MUTED)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    print(f"Wrote {out_path} ({out_path.stat().st_size // 1024} KiB), slides={len(slides)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", type=Path, help="Source HTML deck")
    ap.add_argument("-o", "--output", type=Path, required=True, help="Output .pptx path")
    ap.add_argument("--title", default="ПТС", help="Deck title metadata")
    args = ap.parse_args()
    build_pptx(args.html, args.output, args.title)


if __name__ == "__main__":
    main()
