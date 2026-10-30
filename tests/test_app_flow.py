"""End-to-end UI test of the offline demo — no API keys, no network."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).resolve().parent.parent / "app.py"


def _button(at: AppTest, prefix: str):
    for button in at.button:
        if prefix in button.label:
            return button
    raise AssertionError(f"no button starting with {prefix!r}: {[b.label for b in at.button]}")


def test_offline_demo_flow_and_language_switch() -> None:
    at = AppTest.from_file(str(APP_PATH), default_timeout=120)
    at.run()
    assert not at.exception

    # Hero is shown before any analysis.
    assert any("LipiSetu" in md.value for md in at.markdown)

    at.segmented_control[0].set_value("sample").run()
    assert not at.exception

    _button(at, "বিশ্লেষণ").click().run()
    assert not at.exception
    assert len(at.get("audio")) == 1
    assert any("ব্যাংক ঋণ আদায়ের নোটিশ" in md.value for md in at.markdown)
    downloads = at.get("download_button")
    assert len(downloads) >= 2
    assert any("PDF" in button.label for button in downloads)
    assert len(at.tabs) == 2
    assert len(at.text_area) == 1

    # Prefill helper fills every placeholder field.
    _button(at, "নমুনা তথ্য").click().run()
    assert not at.exception
    assert len(at.text_input) >= 3
    assert all(field.value for field in at.text_input)

    # Switching language keeps the old result and offers re-analysis.
    language = at.selectbox[0]
    language.set_value(language.options[1]).run()
    assert not at.exception
    assert any("हिन्दी" in info.value for info in at.info)
    reanalyze = _button(at, "फिर से विश्लेषण")
    reanalyze.click().run()
    assert not at.exception
    assert any("सारांश" in tab.label for tab in at.tabs)

    # A new language gets its own placeholder widget state without errors.
    assert len(at.text_input) >= 3
    assert any("नया दस्तावेज़" in button.label for button in at.button)


def test_offline_demo_in_english() -> None:
    at = AppTest.from_file(str(APP_PATH), default_timeout=120)
    at.run()
    assert not at.exception

    at.selectbox[0].set_value("English").run()
    assert not at.exception
    assert any("Plain-English" in md.value or "understand" in md.value.lower() for md in at.markdown)

    at.segmented_control[0].set_value("sample").run()
    assert not at.exception
    _button(at, "Analyze").click().run()
    assert not at.exception
    assert len(at.get("audio")) == 1
    assert any("Bank loan recovery notice" in md.value for md in at.markdown)
    assert any("Summary & audio" in tab.label for tab in at.tabs)
    assert all("English summary" not in expander.label for expander in at.expander)
