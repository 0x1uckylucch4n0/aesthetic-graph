"""
Reads images.json and updates js/data.js with the image URLs.
Run: ~/.pyenv/versions/3.11.9/bin/python scraper/update_images.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMAGES_FILE = ROOT / "js" / "images.json"
DATA_FILE = ROOT / "js" / "data.js"


def main():
    with open(IMAGES_FILE) as f:
        images = json.load(f)

    with open(DATA_FILE) as f:
        data_js = f.read()

    updated = 0
    for aesthetic_id, urls in images.items():
        if not urls:
            continue

        # Build the JS array string
        urls_js = json.dumps(urls)

        # Replace the images: [] for this aesthetic
        # Match: id: "aesthetic-id" ... images: [...]
        # We look for the images array that follows this specific id
        pattern = (
            r'(id:\s*"' + re.escape(aesthetic_id) + r'".*?)'
            r'images:\s*\[.*?\]'
        )
        replacement = r'\1images: ' + urls_js

        new_data_js, count = re.subn(pattern, replacement, data_js, flags=re.DOTALL)
        if count > 0:
            data_js = new_data_js
            updated += 1
            print(f"[OK] {aesthetic_id}: {len(urls)} images")
        else:
            print(f"[SKIP] {aesthetic_id}: pattern not found in data.js")

    with open(DATA_FILE, "w") as f:
        f.write(data_js)

    print(f"\nUpdated {updated} aesthetics in data.js")


if __name__ == "__main__":
    main()
