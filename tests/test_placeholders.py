"""Placeholder extraction and substitution — the reply form's contract."""

from __future__ import annotations

from datetime import date

import app


def test_detects_punctuated_tokens_from_the_prompt() -> None:
    assert app.unique_placeholders("[Reference No.]") == ["Reference No."]
    assert app.unique_placeholders("[A/C No.]") == ["A/C No."]
    assert app.unique_placeholders("[Amount (INR)]") == ["Amount (INR)"]


def test_detects_indic_script_tokens() -> None:
    assert app.unique_placeholders("[আপনার নাম]") == ["আপনার নাম"]
    assert app.unique_placeholders("[आपका पता]") == ["आपका पता"]
    assert app.unique_placeholders("[உங்கள் பெயர்]") == ["உங்கள் பெயர்"]


def test_deduplicates_case_insensitively_and_keeps_first_spelling() -> None:
    text = "Dear [Your Name], [YOUR NAME], [your name] and [Reference No.]"
    assert app.unique_placeholders(text) == ["Your Name", "Reference No."]


def test_ignores_empty_and_overlong_brackets() -> None:
    assert app.unique_placeholders("[] [   ] [ok]") == ["ok"]
    assert app.unique_placeholders("[" + "x" * 61 + "]") == []


def test_fill_is_case_insensitive_and_handles_punctuation() -> None:
    text = "To [Your Name], ref [REFERENCE NO.]."
    result = app.fill_placeholders(text, {"Your Name": "Ananya", "Reference No.": "ABC/1"})
    assert result == "To Ananya, ref ABC/1."


def test_blank_values_keep_the_placeholder_visible() -> None:
    text = "Dear [Your Name],"
    assert app.fill_placeholders(text, {"Your Name": "   "}) == text


def test_values_are_not_regex_replacement_templates() -> None:
    result = app.fill_placeholders("[Name]", {"Name": r"\1 \\g<0>"})
    assert result == r"\1 \\g<0>"


def test_slug_is_stable_and_distinguishes_punctuation() -> None:
    assert app.placeholder_slug("Your Name") == app.placeholder_slug("your name")
    assert app.placeholder_slug("Reference No.") != app.placeholder_slug("Reference No")
    assert all(char.isalnum() or char == "-" for char in app.placeholder_slug("[আপনার নাম]"))


def test_every_demo_placeholder_is_detected_and_fillable() -> None:
    import json
    from pathlib import Path

    data = json.loads(Path(app.DEMO_ANALYSES_PATH).read_text(encoding="utf-8"))
    for sample, per_lang in data.items():
        if sample.startswith("_"):
            continue
        for code, entry in per_lang.items():
            reply = entry["official_english_reply"]
            tokens = app.unique_placeholders(reply)
            assert tokens, f"{sample}/{code} has no placeholders"
            filled = app.fill_placeholders(reply, dict.fromkeys(tokens, "VALUE"))
            assert app.unique_placeholders(filled) == []
            assert "VALUE" in filled


def test_sample_values_cover_demo_tokens() -> None:
    assert app.sample_value_for("Your Name") == "Ananya Sen"
    assert app.sample_value_for("Bank Name") == "State Bank of Citizens"
    assert app.sample_value_for("Reference No.") == "SBC/LOAN-REC/2026/0942"
    assert app.sample_value_for("Date", today=date(2026, 10, 15)) == "15 October 2026"
    assert app.sample_value_for("Something Unmapped") == ""
