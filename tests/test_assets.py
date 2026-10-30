"""Image/PDF validation and demo asset integrity."""

from __future__ import annotations

import io
import json

import pytest
from PIL import Image

import app


def _png(size: tuple[int, int]) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, "white").save(buf, format="PNG")
    return buf.getvalue()


def test_prepare_image_returns_a_bounded_jpeg() -> None:
    data, mime = app.prepare_image(_png((1200, 1600)))
    assert mime == "image/jpeg"
    assert data.startswith(b"\xff\xd8")
    with Image.open(io.BytesIO(data)) as image:
        assert max(image.size) <= app.MAX_IMAGE_SIDE


def test_prepare_image_rejects_tiny_images() -> None:
    with pytest.raises(app.AnalysisError) as excinfo:
        app.prepare_image(_png((100, 100)))
    assert "resolution" in str(excinfo.value).lower()


def test_prepare_image_rejects_non_images() -> None:
    with pytest.raises(app.AnalysisError):
        app.prepare_image(b"this is not an image")


def test_prepare_image_rejects_oversized_payloads() -> None:
    with pytest.raises(app.AnalysisError):
        app.prepare_image(b"x" * (app.MAX_UPLOAD_MB * 1024 * 1024 + 1))


def test_prepare_image_localises_errors() -> None:
    cfg = app.SUPPORTED_LANGUAGES["Hindi (हिन्दी)"]
    with pytest.raises(app.AnalysisError) as excinfo:
        app.prepare_image(_png((100, 100)), cfg)
    assert excinfo.value.args[0] == cfg["err_image_too_low"]


def test_prepare_document_passes_pdfs_through() -> None:
    payload = b"%PDF-1.7\n" + b"x" * 512
    data, mime = app.prepare_document(payload)
    assert data == payload
    assert mime == "application/pdf"


def test_prepare_document_rejects_truncated_pdf() -> None:
    with pytest.raises(app.AnalysisError) as excinfo:
        app.prepare_document(b"%PDF-1.7\n")
    assert excinfo.value.i18n_key == "err_pdf_unreadable"


def test_generated_sample_is_a_usable_image() -> None:
    for sample in ("bank", "electricity", "circular"):
        raw = app.generate_sample_document(sample)
        assert raw.startswith(b"\xff\xd8")
        prepared, mime = app.prepare_image(raw)
        assert mime == "image/jpeg"
        assert len(prepared) > 10_000


def test_demo_analysis_payload_is_complete_and_valid() -> None:
    data = json.loads(app.DEMO_ANALYSES_PATH.read_text(encoding="utf-8"))
    samples = {k: v for k, v in data.items() if not k.startswith("_")}
    assert set(samples) == {"bank", "electricity", "circular"}
    for sample, per_lang in samples.items():
        assert set(per_lang) == {"bn", "hi", "ta", "mr", "en"}, sample
        for code, entry in per_lang.items():
            analysis = app.DocumentAnalysis(**entry)
            assert analysis.is_readable, f"{sample}/{code}"
            assert analysis.document_type_local, f"{sample}/{code} has no localized document type"
            assert analysis.local_summary
            assert analysis.official_english_reply
            assert analysis.urgency_level in {"High", "Medium", "Low"}


def test_demo_audio_exists_for_every_pair() -> None:
    data = json.loads(app.DEMO_ANALYSES_PATH.read_text(encoding="utf-8"))
    for sample, per_lang in data.items():
        if sample.startswith("_"):
            continue
        for code in per_lang:
            path = app.DEMO_AUDIO_DIR / f"{sample}_{code}.mp3"
            assert path.exists(), path
            assert path.stat().st_size > 1000
