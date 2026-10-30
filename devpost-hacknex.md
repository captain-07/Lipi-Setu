---
title: "I Built LipiSetu AI at HackNex Season 2 — an App That Reads Official English Notices Back to You in Bengali, Hindi, Tamil, Marathi and English"
tags: ai, python, streamlit, hackathon
description: "A photo or PDF of an official notice goes in; a plain-language summary in four Indian languages (plus an English mode for reviewers), spoken audio, a calendar-ready deadline, and a ready-to-send English reply PDF come out. Here's what I built in 24 hours — and what I fixed afterwards."
cover_image: https://raw.githubusercontent.com/captain-07/Lipi-Setu/main/docs/cover.png
series: hackathon-2026
---

# I Built LipiSetu AI at HackNex Season 2

**Event:** HackNex Season 2, under InnovoCon Season 2
**Dates:** 25–26 September 2026
**Venue:** JIS College of Engineering, Kalyani, Nadia, West Bengal
**Track:** AI/ML
**Repo:** [github.com/captain-07/Lipi-Setu](https://github.com/captain-07/Lipi-Setu)

## The problem I actually saw

In West Bengal — and across India — the language of government is English, and the language
of people is not. A municipal corporation notice, a bank letter, a bill, a pension circular:
all of it arrives in formal English, dense with legal phrasing, and all of it carries a
**deadline**.

If you don't read English fluently, you don't just struggle to understand the notice. You
**don't know that you are the person being addressed**, so you don't know you need to act,
so you miss the deadline. That's the failure mode I wanted to close. Not "translate the
document" — translate it *and* tell me whether I'm in trouble, and then help me write back.

## What LipiSetu does

Give it a photo or a PDF of an official notice. It gives you back:

- **🗣️ A plain-language summary** in Bengali, Hindi, Tamil, or Marathi — plus an English
  mode for reviewers — with the whole interface translated, including labels, the hero,
  errors, and validation messages
- **🔊 Audio playback** of that summary, so literacy and eyesight aren't blockers
- **🔴🟠🟢 An urgency flag** with the printed deadline extracted, when there is one
- **📅 A one-click calendar event** for the deadline
- **✍️ A formal English reply letter** as fill-in-the-blanks, downloadable as a filled A4 PDF

The reply flow is the part I'm most pleased with. The model returns a letter containing
`[PLACEHOLDER]` tokens; the app turns every one into its own form field and substitutes the
values as you type:

```python
_PLACEHOLDER_RE = re.compile(r"\[([^\[\]\n]{1,60})\]")


def unique_placeholders(text: str) -> list[str]:
    """Return distinct [PLACEHOLDER] tokens, de-duplicated case-insensitively."""
    canonical: dict[str, str] = {}
    for match in _PLACEHOLDER_RE.finditer(text):
        token = match.group(1).strip()
        if token:
            canonical.setdefault(token.casefold(), token)
    return list(canonical.values())
```

Matched case-insensitively, so `[YOUR NAME]` and `[Your Name]` are the same field. Blank a
field deliberately and the `[PLACEHOLDER]` stays visible in the letter instead of silently
vanishing into a broken sentence — and the banner tells you how many remain. Small thing,
but it's the difference between a tool you trust and one that quietly loses your data.

## Tech stack

| Piece | Choice |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| Vision + reasoning | Gemma 4 (`gemma-4-26b-a4b-it`) via the Google GenAI SDK |
| Speech | [ElevenLabs](https://elevenlabs.io/) `eleven_multilingual_v2` |
| PDF | [fpdf2](https://github.com/py-pdf/fpdf2) + `uharfbuzz` + embedded Noto fonts |
| Imaging | Pillow |
| Validation | Pydantic |
| Tests / CI | pytest, Streamlit `AppTest`, Ruff, GitHub Actions |

One detail worth calling out: `eleven_multilingual_v2` **detects language from the script**,
so the same voice ID works for every supported language. No per-language voice mapping needed.

## The decision I'm happiest with: offline demo mode

The venue wifi died more than once, and judges' laptops don't have API keys. A demo that
needs the cloud is a demo that fails live.

So the **sample** mode **never calls Google or ElevenLabs**. It replays pre-bundled assets:

- `samples/demo_analyses.json` — 3 sample notices × 5 languages = 15 pre-written analyses
- `samples/audio/*.mp3` — 15 pre-generated speech files (~7 MB), regenerable via
  `scripts/generate_demo_audio.py --force`
- `static/fonts/*.woff2` and `assets/fonts/*.ttf` — self-hosted UI and PDF fonts

**No network. No API keys.** It works in a classroom, on a plane, or in an air-gapped lab.
That single decision is what made the demo reliable, and it was made *because* of the venue.

## What I fixed after the hackathon

The hackathon build proved the flow. The version in the repo now is the one I actually want
to hand to someone:

- **Unicode PDF output.** The first build could only render Latin-1 in the reply PDF, so an
  Indian name turned into `?`. The current version embeds Noto Sans, Noto Sans Bengali, Noto
  Sans Devanagari, and Noto Sans Tamil and shapes them with HarfBuzz. Bengali, Devanagari,
  and Tamil names and addresses now render correctly.
- **PDF input.** Multi-page notices can be passed to Gemini natively instead of requiring a
  photo of every page.
- **Calendar export.** A deadline becomes an all-day `.ics` event with a two-day reminder.
- **A result-first layout.** Once a document is analyzed, the input card collapses into a
  compact document bar, so the summary and reply are the first things on screen.
- **Language switching without losing work.** Change the language and the old result stays
  visible; one click re-analyzes it in the new language.
- **Native-language-first labels.** English is kept for product names and technical terms,
  not mixed into every button.
- **A real test suite.** 45 offline tests cover translations, placeholders, demo assets,
  image/PDF limits, Unicode PDFs, deadlines, and an end-to-end `AppTest` flow. CI runs them
  on Python 3.10 and 3.12.
- **An English mode for reviewers.** The four Indian languages remain the primary experience,
  but English lets recruiters and engineers test the complete flow without knowing one.
- **CI, deployment notes, and a browser-rendered cover** that shapes all supported scripts correctly.

## Being honest about the limitations

These are real and I left them in rather than papering over them:

- **One document at a time.** A multi-page PDF works, but separate loose images must be
  combined into a PDF first.
- **Urgency detection is model judgment**, not a rules engine. It errs toward flagging.
- **OCR quality caps everything.** Below 400 px on the shorter side, text is genuinely
  illegible and analysis is rejected outright rather than guessed at.
- **Audio depends on ElevenLabs.** If the key is missing or the quota is exhausted, the app
  degrades to text with a clear message.
- **The reply is a draft, not legal or financial advice.** The PDF footer says so too.
- **No authentication or per-user rate limiting.** This is a demo, not a multi-tenant
  service.

## What I'd do differently

24 hours is not much, and I spent some of it on things I'd have skipped with more time.
The UI polish was nearly a third of the build. I'd have wired the Unicode PDF font first and
done polish last, because "it renders my name wrong" undersells a tool whose entire job is
trust. That's exactly the first thing I fixed afterwards.

## Try it

```bash
git clone https://github.com/captain-07/Lipi-Setu.git
cd Lipi-Setu
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Then either add a Google AI key and an ElevenLabs key for real uploads — or choose the
**sample** mode and see the whole flow with neither. The sample path is offline by design.

Thanks to the JIS College of Engineering team and the InnovoCon organisers for running a
hackathon where the problems on the table were real ones from the town around it. That's a
rare kind of brief.
