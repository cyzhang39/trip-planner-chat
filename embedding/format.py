import re
import unicodedata
import json
from pathlib import Path
from tqdm import tqdm

_TRANSLATION_RE = re.compile(r'\s*\([^()]*"[^\"]*"\)')

def clean_text(text: str):
    """
    - Normalize, drop () translations, white space to single space
    """
    text = unicodedata.normalize("NFKC", text)
    text = _TRANSLATION_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_json(input_path: Path, output_path: Path):
    """
    Read raw data, format and clean raw data, and write out formatted data
    """
    with input_path.open("r") as f:
        total = sum(1 for _ in f)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    kept = 0

    with input_path.open("r") as fin, \
         output_path.open("w") as fout:
        for line in tqdm(fin, total=total, desc="Formating JSON"):
            try:
                obj = json.loads(line)
                title = obj.get("title", "").strip()
                text = obj.get("text", "").strip()
                if not text:
                    continue
                cleaned = clean_text(text)
                if not cleaned:
                    continue
                kept += 1
                out = {"title": title or "<no title>", "text": cleaned}
                fout.write(json.dumps(out) + "\n")
            except json.JSONDecodeError:
                continue

    print(f"✅ Cleaned {kept} lines, saved to {output_path}")
