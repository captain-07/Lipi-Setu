# Contributing to LipiSetu AI

Thanks for helping make official documents easier to understand.

## Quick start

```bash
git clone https://github.com/captain-07/Lipi-Setu.git
cd Lipi-Setu
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements-dev.txt
streamlit run app.py
```

The sample flow works with no API keys and no network access. Add
`GEMINI_API_KEY` and `ELEVEN_LABS_API_KEY` only when you need to test real
uploads; see the README for the supported environment variables and secrets.

## Before opening a pull request

```bash
ruff check .
ruff format --check .
pytest
```

If you changed the interface, also:

- Walk through the sample flow in all five languages.
- Test the upload flow with an image and a PDF.
- Test at a phone width (about 390 px): the sidebar should start collapsed and
  the input card should be reachable without a wall of hero cards.
- Check that the reply PDF renders a Bengali, Devanagari, and Tamil name.
- Regenerate the README cover if the brand or hero copy changed:

  ```bash
  pip install playwright
  playwright install chromium
  python scripts/generate_cover.py
  ```

Never commit `.streamlit/secrets.toml`, real API keys, or user documents.

## Translations

All UI copy lives in `SUPPORTED_LANGUAGES` in `app.py`. Every language must
define exactly the same keys; `tests/test_i18n.py` enforces this.

- Prefer the native language for primary actions and labels. Keep product names
  and technical terms such as `PDF`, `API`, and `Google Gemma 4` as they are.
- Use only the documented format fields: `{mb}`, `{count}`, `{filled}`,
  `{total}`, `{lang}`, `{old}`, and `{new}`. A test catches unknown fields.
- Keep button labels short. The source English wording is not shown in the UI.
- If you add a sample document, add `document_type_local` and a bundled audio
  file for every language.

## Adding a language

1. Copy an existing block in `SUPPORTED_LANGUAGES` and translate every value.
2. Add the language code, native name, and font/text CSS classes.
3. Add the language to `samples/demo_analyses.json` for every sample.
4. Generate the demo audio with `python scripts/generate_demo_audio.py --force`.
5. Add a self-hosted WOFF2 UI font under `static/fonts/` and a TTF for PDFs
   under `assets/fonts/` if the script is not already covered.
6. Run the tests and add the language to the README table.

## Demo assets

The offline demo is deliberately self-contained:

- `samples/demo_analyses.json` — written analyses, localized document types
- `samples/audio/*.mp3` — speech files
- `static/fonts/*.woff2` — browser fonts
- `assets/fonts/*.ttf` — PDF fonts

Keep the demo working without network access. If you regenerate the audio,
listen to at least one file per language before committing it.

## Code style

- Python 3.10+, Ruff formatting, 120-character lines.
- Keep the single-file Streamlit orchestration unless a module has a clear,
  testable boundary.
- Add a test for parsing, validation, export, or translation changes.
- Do not silently drop user input. Unfilled placeholders must remain visible.
