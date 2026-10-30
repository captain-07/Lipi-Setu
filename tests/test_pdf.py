"""PDF rendering, deadline parsing, and calendar export."""

from __future__ import annotations

from datetime import date

import pytest

import app


def _analysis(reply: str = "Dear Sir,\n\nThank you.\n\nYours faithfully,\nAnanya Sen") -> app.DocumentAnalysis:
    return app.DocumentAnalysis(
        is_readable=True,
        document_type="Bank loan notice",
        urgency_level="High",
        key_deadline="15 October 2026",
        local_summary="এটি একটি ব্যাংক নোটিশ।",
        english_summary="A bank notice.",
        official_english_reply=reply,
    )


def test_builds_a_valid_pdf() -> None:
    data = app.build_reply_pdf(_analysis())
    assert data.startswith(b"%PDF")
    assert len(data) > 1000


def test_pdf_embeds_indic_fonts_for_mixed_script_values() -> None:
    if not app.pdf_unicode_available():
        pytest.skip("bundled PDF fonts are not available")
    reply = "Dear Sir,\n\nName: অর্ণব মুখার্জি / अर्जुन शर्मा / முருகன்\n\nYours faithfully,\nAnanya"
    data = app.build_reply_pdf(_analysis(reply))
    assert b"NotoSansBengali" in data
    assert b"NotoSansDevanagari" in data
    assert b"NotoSansTamil" in data


def test_pdf_safe_maps_typographic_characters() -> None:
    assert app._pdf_safe("₹1,200 – “paid”…") == 'Rs. 1,200 - "paid"...'
    assert app._pdf_safe("অ") == "?"


def test_has_non_latin1() -> None:
    assert not app.has_non_latin1("Plain English 123.")
    assert app.has_non_latin1("অর্ণব")
    assert not app.has_non_latin1("Rs. 1,200 – paid…")


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("15 October 2026", date(2026, 10, 15)),
        ("on or before 15th Oct 2026", date(2026, 10, 15)),
        ("October 15, 2026", date(2026, 10, 15)),
        ("15/10/2026", date(2026, 10, 15)),
        ("15-10-2026", date(2026, 10, 15)),
        ("2026-10-15", date(2026, 10, 15)),
        ("before 5:00 PM on 15 October 2026", date(2026, 10, 15)),
    ],
)
def test_parse_deadline_formats(text: str, expected: date) -> None:
    assert app.parse_deadline(text) == expected


@pytest.mark.parametrize("text", [None, "", "no deadline stated", "31/02/2026", "sometime soon"])
def test_parse_deadline_rejects_unclear_values(text: str | None) -> None:
    assert app.parse_deadline(text) is None


def test_build_ics_is_an_all_day_event_with_a_reminder() -> None:
    data = app.build_ics(date(2026, 10, 15), "Deadline: Bank notice", "Bring the documents")
    text = data.decode("utf-8")
    assert text.startswith("BEGIN:VCALENDAR\r\n")
    assert "DTSTART;VALUE=DATE:20261015\r\n" in text
    assert "DTEND;VALUE=DATE:20261016\r\n" in text
    assert "TRIGGER:-P2D\r\n" in text
    assert text.endswith("END:VCALENDAR\r\n")
    assert "Deadline: Bank notice" in text


def test_build_ics_escapes_special_characters() -> None:
    text = app.build_ics(date(2026, 10, 15), "Pay, now; please", "line one\nline two").decode("utf-8")
    assert r"Pay\, now\; please" in text
    assert r"line one\nline two" in text
