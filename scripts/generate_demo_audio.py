"""Pre-generate the offline demo audio for every sample x language pair.

Run once (needs network + ELEVEN_LABS_API_KEY), then commit the output:

    python scripts/generate_demo_audio.py            # only missing files
    python scripts/generate_demo_audio.py --force    # regenerate everything

Output: samples/audio/<sample>_<lang>.mp3, which app.py loads at runtime so the
"Try Sample Document" mode works with no internet and no API calls.
"""

from __future__ import annotations

import argparse
import io
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import MAX_TTS_CHARS, _clean_for_speech, get_elevenlabs_client  # noqa: E402

DEMO_JSON = ROOT / "samples" / "demo_analyses.json"
AUDIO_DIR = ROOT / "samples" / "audio"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="regenerate MP3s that already exist")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    data = json.loads(DEMO_JSON.read_text(encoding="utf-8"))
    samples = {k: v for k, v in data.items() if not k.startswith("_")}

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    client, voice_id = get_elevenlabs_client()

    written = skipped = failed = 0
    for sample_key, per_lang in samples.items():
        for lang_code, entry in sorted(per_lang.items()):
            out = AUDIO_DIR / f"{sample_key}_{lang_code}.mp3"
            if out.exists() and not args.force:
                print(f"skip  {out.name} (exists)")
                skipped += 1
                continue

            text = _clean_for_speech(entry["local_summary"])[:MAX_TTS_CHARS]
            try:
                stream = client.text_to_speech.convert(
                    voice_id=voice_id,
                    text=text,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )
                buf = io.BytesIO()
                for chunk in stream:
                    if isinstance(chunk, bytes):
                        buf.write(chunk)
                audio = buf.getvalue()
                if not audio:
                    raise RuntimeError("empty audio stream")
                out.write_bytes(audio)
                print(f"ok    {out.name}  {len(audio) / 1024:6.1f} KB")
                written += 1
            except Exception as exc:  # noqa: BLE001 - report and continue
                print(f"FAIL  {out.name}: {exc}", file=sys.stderr)
                failed += 1

    print(f"\nwritten={written} skipped={skipped} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())