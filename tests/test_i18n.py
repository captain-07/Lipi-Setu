"""Translation dictionaries must stay complete and format-safe."""

from __future__ import annotations

import string

import app


def test_every_language_has_the_same_keys() -> None:
    base = set(app.SUPPORTED_LANGUAGES[app.DEFAULT_LANGUAGE])
    for name, cfg in app.SUPPORTED_LANGUAGES.items():
        assert set(cfg) == base, f"{name} has a different key set"


def test_core_keys_exist_in_every_language() -> None:
    required = {
        "code",
        "native_name",
        "font_class",
        "text_class",
        "sentence_end",
        "results_title",
        "results_sub",
        "system_ready",
        "stale_results",
        "reanalyze_cta",
        "add_to_calendar",
        "fill_sample",
        "details_progress",
        "pdf_preview_note",
        "download_original",
        "err_key_missing",
        "err_key_rejected",
        "err_rate_limited",
        "err_service_unavailable",
        "err_analyze_failed",
        "err_pdf_unreadable",
    }
    for name, cfg in app.SUPPORTED_LANGUAGES.items():
        assert required <= set(cfg), f"{name} is missing {required - set(cfg)}"


def test_format_placeholders_are_known() -> None:
    allowed = {"mb", "count", "filled", "total", "lang", "old", "new"}
    for name, cfg in app.SUPPORTED_LANGUAGES.items():
        for key, value in cfg.items():
            for _, field, _, _ in string.Formatter().parse(value):
                if field:
                    assert field in allowed, f"{name}/{key} uses unknown {{{field}}}"


def test_language_metadata_is_consistent() -> None:
    codes = {cfg["code"] for cfg in app.SUPPORTED_LANGUAGES.values()}
    assert codes == {"bn", "hi", "ta", "mr", "en"}
    for cfg in app.SUPPORTED_LANGUAGES.values():
        assert cfg["native_name"]
        assert cfg["sentence_end"] in {".", "।"}


def test_new_keys_are_translated_not_english_copies() -> None:
    english_only = {"download_original", "add_to_calendar", "fill_sample"}
    for name, cfg in app.SUPPORTED_LANGUAGES.items():
        if cfg["code"] in {"bn", "en"}:
            continue
        for key in english_only:
            assert cfg[key] != app.SUPPORTED_LANGUAGES[app.DEFAULT_LANGUAGE][key], f"{name}/{key} was not translated"
