"""LipiSetu AI (লিপি সেতু) - Bengali document comprehension + official English reply."""
from __future__ import annotations

import io
import logging
import os
import re
import time
from datetime import date
from typing import Literal, Optional

import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from google import genai
from google.genai import errors, types
from gtts import gTTS
from PIL import Image, ImageOps
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("lipisetu")

# ---------- Config (single place to tweak) ----------
MODEL_ID = "gemma-4-26b-a4b-it"
MAX_IMAGE_SIDE = 1600          # px; keeps payload small and latency low
MIN_IMAGE_SIDE = 400           # px; below this, text is rarely legible
MAX_UPLOAD_MB = 8
MAX_RETRIES = 3
API_TIMEOUT_MS = 60_000
MAX_TTS_CHARS = 1500


# ---------- Contract between the model and the UI ----------
class DocumentAnalysis(BaseModel):
    is_readable: bool = Field(
        description="False if the image is blurry, cropped, too dark, or not an official document."
    )
    quality_issue: Optional[str] = Field(
        default=None, description="If is_readable is false, a short reason in English."
    )
    document_type: str = Field(
        description="Short label, e.g. 'Bank loan notice', 'Electricity bill', 'College circular'."
    )
    urgency_level: Literal["High", "Medium", "Low"]
    key_deadline: Optional[str] = Field(
        default=None, description="Deadline exactly as printed in the document, or null if none is stated."
    )
    bengali_summary: str = Field(description="3-5 short sentences in simple spoken Bengali. Plain text only.")
    english_summary: str = Field(description="2-3 sentence English summary.")
    official_english_reply: str = Field(
        description="Formal English letter body: salutation through closing. Use [placeholders] for unknown details."
    )


class AnalysisError(Exception):
    """Raised with a message that is safe to show directly to the user."""