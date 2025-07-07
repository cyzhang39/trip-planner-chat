import re
import unicodedata
import json
from pathlib import Path
from tqdm import tqdm

REGEX = re.compile(r'\s*\([^()]*"[^\"]*"\)')

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = REGEX.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_json(input_path, output_path):
    with input_path.open("r") as f:
        total = sum(1 for _ in f)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    kept = 0

    with input_path.open("r") as fin, output_path.open("w") as fout:
        for line in tqdm(fin, total=total):
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

    print(f"Cleaned {kept} lines, saved to {output_path}")
