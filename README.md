# 🌉 LipiSetu AI · লিপি সেতু

> **Bridge the language gap across India** — Understand any official English document in your native Indian language (Bengali, Hindi, Tamil, Marathi), and reply in official English.

LipiSetu AI is a Streamlit-powered web application that helps citizens comprehend official English documents (notices, bills, letters, circulars) by providing:

- **🗣️ Multilingual Summary** — Simple summary in Bengali, Hindi, Tamil, or Marathi
- **🔊 Audio playback** — Listen to the summary read aloud in your chosen language
- **✉️ Formal English reply** — A fill-in-the-blanks draft letter, downloadable as an already-completed PDF
- **📴 Offline demo** — Try the whole flow with no internet and no API keys

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌐 **Multilingual Support** | Choose between **Bengali (বাংলা)**, **Hindi (हिन्दी)**, **Tamil (தமிழ்)**, and **Marathi (मराठी)** — the whole interface, including labels, hero and error messages, is translated |
| 📄 **Document Analysis** | Upload, snapshot with camera, or test with sample official documents |
| 🗣️ **Local Language Summary** | 3–5 sentence summary in simple spoken native language, typeset with a script-matched webfont |
| 🔊 **Text-to-Speech** | Audio playback via **ElevenLabs** (`eleven_multilingual_v2`) for all 4 languages |
| 🔴🟠🟢 **Urgency Detection** | Automatically flags deadlines, penalties, and required actions |
| ✍️ **Fill-in-the-Blanks Reply** | Every `[PLACEHOLDER]` becomes its own form field; values are substituted into the letter automatically |
| 📥 **PDF Download** | Download the reply as a professional A4 PDF, already filled in |
| 📴 **Offline Demo Mode** | "Try Sample Document" replays bundled assets — no network, no API keys |
| 📷 **Camera & Sample Support** | Take photos directly or use pre-built sample notices for zero-friction testing |
| 🔒 **Privacy First** | Images are processed in-memory only — nothing is stored on disk |

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[Google Gemma 4](https://ai.google.dev/)** — Multimodal AI model (via Google GenAI SDK)
- **[ElevenLabs](https://elevenlabs.io/)** — Text-to-Speech for Bengali, Hindi, Tamil & Marathi audio
- **[fpdf2](https://github.com/py-pdf/fpdf2)** — PDF generation for reply letters
- **[Pillow](https://python-pillow.org/)** — Image preprocessing and sample document generation
- **[Pydantic](https://docs.pydantic.dev/)** — Structured output validation

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- A **[Google AI API key](https://aistudio.google.com/apikey)** (free tier works) — only for real uploads
- An **[ElevenLabs API key](https://elevenlabs.io/app/settings/api-keys)** — only for audio on real uploads

> **No keys needed to explore.** Sample mode runs entirely offline (see [Offline Demo Mode](#-offline-demo-mode)).

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/LipiSetu.git
   cd LipiSetu
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API keys**

   **Option A — Environment variables:**
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY = "your-gemini-key-here"
   $env:ELEVEN_LABS_API_KEY = "your-elevenlabs-key-here"

   # macOS / Linux
   export GEMINI_API_KEY="your-gemini-key-here"
   export ELEVEN_LABS_API_KEY="your-elevenlabs-key-here"
   ```

   **Option B — Streamlit secrets file:**
   Create `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-gemini-key-here"
   ELEVEN_LABS_API_KEY = "your-elevenlabs-key-here"
   ```

   Optionally pick a different voice:
   ```toml
   ELEVENLABS_VOICE_ID = "your-voice-id"
   ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

   The app will open at **http://localhost:8501**.

---

## 📸 How to Use

1. **Select your language** from the sidebar dropdown (Bengali, Hindi, Tamil, or Marathi). Your choice is remembered for the session.
2. Choose **Upload**, **Camera**, or **Try Sample Document**.
3. Click **🔍 Analyze Document**.
4. View the results:
   - **Summary tab** — Native language summary, urgency level, deadline, and audio playback.
   - **Reply tab** — The formal English reply letter.
5. **Fill in your details** — each `[PLACEHOLDER]` in the letter gets its own field. Values are substituted into the letter as you type.
6. Check the **preview** expander to see exactly what will be written to the PDF.
7. Click **⬇️ Download Reply as PDF**.

Placeholders are matched case-insensitively, so `[YOUR NAME]` and `[Your Name]` are treated as the same field. Leaving a field blank keeps the `[PLACEHOLDER]` visible in the letter rather than silently dropping it, and the banner tells you how many remain.

> **Note:** the PDF uses the Latin-1 core PDF font, so **write the placeholder values in English**. Filling them in an Indian script triggers a warning, because the PDF cannot render those glyphs.

---

## 🌐 Supported Languages

- 🇧🇩 / 🇮🇳 **Bengali (বাংলা)** — `code: bn`
- 🇮🇳 **Hindi (हिन्दी)** — `code: hi`
- 🇮🇳 **Tamil (தமிழ்)** — `code: ta`
- 🇮🇳 **Marathi (मराठी)** — `code: mr`

All UI strings live in the `SUPPORTED_LANGUAGES` dictionary at the top of `app.py`. Every language must define the **same set of keys** — add a language by copying an existing block and translating each value.

---

## 📴 Offline Demo Mode

Choosing **Try Sample Document** never calls Google or ElevenLabs. It replays pre-bundled assets, so the demo works with **no internet connection and no API keys** — useful for demos, classroom use, and air-gapped environments.

Bundled assets:

| Path | Contents |
|---|---|
| `samples/demo_analyses.json` | 3 sample notices × 4 languages = 12 pre-written analyses (summary, English summary, reply letter, urgency, deadline) |
| `samples/audio/*.mp3` | 12 pre-generated speech files (`<sample>_<lang>.mp3`, ~6 MB total) |
| `scripts/generate_demo_audio.py` | Regenerates the MP3s (requires network + `ELEVEN_LABS_API_KEY`) |

To regenerate the demo audio after editing `samples/demo_analyses.json`:

```bash
python scripts/generate_demo_audio.py            # only missing files
python scripts/generate_demo_audio.py --force    # regenerate everything
```

To add a new language, drop its 4 entries into `demo_analyses.json`, then run the script with `--force`.

---

## 📐 Image Requirements

| Limit | Value | Notes |
|---|---|---|
| **Minimum resolution** | 400 px (shorter side) | Below this the text is rarely legible and analysis is rejected |
| **Maximum resolution** | 1600 px | Larger images are downscaled; small images are never upscaled |
| **Maximum file size** | 5 MB | Checked before decoding |

Photos are auto-rotated using EXIF data, so sideways phone photos work as-is.

---

## 🔒 Privacy & Security

- **No data storage** — Images are processed in-memory and discarded after the session.
- **No server-side logging of document content**.
- **API key protection** — Keys are loaded from environment variables or Streamlit secrets.

### What leaves your machine

To be precise about the privacy guarantee: in **Upload** and **Camera** modes the document image is sent to Google's Gemini API, and the generated summary text is sent to ElevenLabs for speech synthesis. **Sample mode sends nothing anywhere.** No content is written to disk by the app.

---

<p align="center">
  Built with ❤️ for Indian language speakers<br>
  <strong>🌉 LipiSetu AI — The Bridge of Letters</strong>
</p>