#!/usr/bin/env python3
"""Capture each presentation slide as a static PNG and zip them."""
from pathlib import Path
import zipfile
from playwright.sync_api import sync_playwright

ROOT = Path("/workspace")
HTML = ROOT / "PTS-vvodnoe.html"
OUT = ROOT / "slides-static"
ZIP = Path("/opt/cursor/artifacts/PTS-vvodnoe-slides.zip")
ZIP_REPO = ROOT / "PTS-vvodnoe-slides.zip"

OUT.mkdir(parents=True, exist_ok=True)
ZIP.parent.mkdir(parents=True, exist_ok=True)

# Clear old pngs
for p in OUT.glob("*.png"):
    p.unlink()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page.goto(HTML.as_uri(), wait_until="networkidle")

    # Freeze animations / force final state for clean static frames
    page.add_style_tag(content="""
      *, *::before, *::after {
        animation: none !important;
        transition: none !important;
      }
      .orb { display: none !important; }
      .scanline { display: none !important; }
      .reveal, .reveal-left, .reveal-scale, .fragment, .fragment.visible {
        opacity: 1 !important;
        transform: none !important;
        filter: none !important;
      }
      .pipe::after { opacity: 1 !important; }
    """)

    count = page.evaluate("document.querySelectorAll('.slide').length")
    print(f"Slides: {count}")

    for i in range(count):
        page.evaluate(
            """(idx) => {
              document.querySelectorAll('.slide').forEach((s, n) => {
                const on = n === idx;
                s.classList.toggle('active', on);
                // For static review: show all step-fragments fully revealed
                s.querySelectorAll('.fragment').forEach((f) => {
                  f.classList.toggle('visible', on);
                  f.classList.remove('hl');
                });
              });
              const counter = document.getElementById('counter');
              const progress = document.getElementById('progress');
              const total = document.querySelectorAll('.slide').length;
              if (counter) counter.textContent = `${idx + 1} / ${total}`;
              if (progress) progress.style.width = `${((idx + 1) / total) * 100}%`;
            }""",
            i,
        )
        page.wait_for_timeout(120)
        name = f"slide-{i+1:02d}.png"
        path = OUT / name
        page.screenshot(path=str(path), full_page=False, type="png")
        print(f"Wrote {path}")

    browser.close()

# Zip for the user
for target in (ZIP, ZIP_REPO):
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for png in sorted(OUT.glob("slide-*.png")):
            zf.write(png, arcname=png.name)
    print(f"Zip: {target} ({target.stat().st_size} bytes)")
