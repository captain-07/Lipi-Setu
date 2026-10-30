"""Render docs/cover.png from docs/cover.html with a real browser.

Why a browser: Pillow on Windows has no Raqm, so complex scripts such as Tamil
and Bengali are shaped incorrectly. Chrome/Edge shapes them correctly.

Setup (one time):

    pip install playwright
    playwright install chromium   # or use an installed Chrome/Edge

Run from the project root:

    python scripts/generate_cover.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "docs" / "cover.html"
OUT = ROOT / "docs" / "cover.png"


def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Install Playwright first: pip install playwright") from exc

    if not HTML.exists():
        raise SystemExit(f"Missing cover source: {HTML}")

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome", headless=True)
        except Exception:
            # Fall back to Playwright's bundled Chromium.
            browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
        page.goto(HTML.as_uri(), wait_until="load")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(OUT))
        browser.close()

    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
