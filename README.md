# 🌉 LipiSetu AI · লিপি সেতু

> **Bridge the language gap across India** — Understand any official English document in your native Indian language (Bengali, Hindi, Tamil, Marathi), and reply in official English.

LipiSetu AI is a Streamlit-powered web application that helps citizens comprehend official English documents (notices, bills, letters, circulars) by providing:

- **🗣️ Multilingual Summary** — Simple summary in Bengali, Hindi, Tamil, or Marathi
- **🔊 Audio playback** — Listen to the summary read aloud in your chosen language
- **✉️ Formal English reply** — An editable draft letter, downloadable as PDF

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌐 **Multilingual Support** | Choose between **Bengali (বাংলা)**, **Hindi (हिन्दी)**, **Tamil (தமிழ்)**, and **Marathi (मराठी)** |
| 📄 **Document Analysis** | Upload, snapshot with camera, or test with sample official documents |
| 🗣️ **Local Language Summary** | 3–5 sentence summary in simple spoken native language |
| 🔊 **Text-to-Speech** | Native voice audio playback (via gTTS) for all 4 languages |
| 🔴🟠🟢 **Urgency Detection** | Automatically flags deadlines, penalties, and required actions |
| ✉️ **Reply Drafting** | Generates a formal English reply letter with editable placeholders |
| 📥 **PDF Download** | Download the reply as a professional A4 PDF |
| 📷 **Camera & Sample Support** | Take photos directly or use pre-built sample notices for zero-friction testing |
| 🔒 **Privacy First** | Images are processed in-memory only — nothing is stored |

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[Google Gemma 4](https://ai.google.dev/)** — Multimodal AI model (via Google GenAI SDK)
- **[gTTS](https://github.com/pndurette/gTTS)** — Google Text-to-Speech for Bengali, Hindi, Tamil & Marathi audio
- **[fpdf2](https://github.com/py-pdf/fpdf2)** — PDF generation for reply letters
- **[Pillow](https://python-pillow.org/)** — Image preprocessing and sample document generation
- **[Pydantic](https://docs.pydantic.dev/)** — Structured output validation

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- A **[Google AI API key](https://aistudio.google.com/apikey)** (free tier works)

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

4. **Set your API key**

   **Option A — Environment variable:**
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY = "your-api-key-here"

   # macOS / Linux
   export GEMINI_API_KEY="your-api-key-here"
   ```

   **Option B — Streamlit secrets file:**
   Create `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

   The app will open at **http://localhost:8501**.

---

## 📸 How to Use

1. **Select your language** from the sidebar dropdown (Bengali, Hindi, Tamil, or Marathi).
2. Choose **Upload**, **Camera**, or **Try Sample Document**.
3. Click **🔍 Analyze Document**.
4. View the results:
   - **Summary tab** — Native language summary, urgency level, deadline, and audio playback.
   - **Reply tab** — Editable English reply draft with placeholder detector.
5. Edit any `[placeholders]` in the reply.
6. Click **⬇️ Download Reply as PDF**.

---

## 🌐 Supported Languages

- 🇧🇩 / 🇮🇳 **Bengali (বাংলা)** — `code: bn`
- 🇮🇳 **Hindi (हिन्दी)** — `code: hi`
- 🇮🇳 **Tamil (தமிழ்)** — `code: ta`
- 🇮🇳 **Marathi (मराठी)** — `code: mr`

---

## 🔒 Privacy & Security

- **No data storage** — Images are processed in-memory and discarded after the session.
- **No server-side logging of document content**.
- **API key protection** — Keys are loaded from environment variables or Streamlit secrets.

---

<p align="center">
  Built with ❤️ for Indian language speakers<br>
  <strong>🌉 LipiSetu AI — The Bridge of Letters</strong>
</p>
