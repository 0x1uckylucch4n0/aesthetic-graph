"""
Extract inline links from all aesthetic wiki pages.
Reads aesthetics_deep.json, visits each page, extracts all internal wiki links,
and saves them as the 'related' field.
"""

import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
INPUT_FILE = ROOT / "aesthetics_deep.json"

EXTRACT_JS = """() => {
    const content = document.querySelector('.mw-parser-output');
    if (!content) return [];

    const related = [];
    const allLinks = content.querySelectorAll('a[href^="/wiki/"]');
    for (const link of allLinks) {
        const href = link.getAttribute('href');
        const name = link.textContent.trim();
        if (href && !href.includes(':') && name && name.length > 1
            && !href.startsWith('/wiki/List_of')
            && !href.startsWith('/wiki/Category')
            && !href.startsWith('/wiki/Main_Page')) {
            related.push(name);
        }
    }
    return [...new Set(related)];
}"""


def main():
    with open(INPUT_FILE) as f:
        data = json.load(f)

    print(f"Loaded {len(data)} aesthetics")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = ctx.new_page()

        for i, aesthetic in enumerate(data):
            url = aesthetic.get("url", "")
            if not url:
                continue

            try:
                page.goto(url, wait_until="load", timeout=25000)
                time.sleep(2)

                related = page.evaluate(EXTRACT_JS)
                aesthetic["related"] = related

                if len(related) > 0:
                    print(f"  [{i+1}/{len(data)}] {aesthetic['name']} → {len(related)} links")
                else:
                    print(f"  [{i+1}/{len(data)}] {aesthetic['name']} → 0")

            except Exception as e:
                print(f"  [{i+1}/{len(data)}] {aesthetic['name']} ERROR: {e}")
                aesthetic["related"] = aesthetic.get("related", [])

            # Save every 50 pages
            if (i + 1) % 50 == 0 or (i + 1) == len(data):
                with open(INPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"  [SAVED] {i+1}/{len(data)}")

            time.sleep(0.3)

        browser.close()

    # Final save
    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    has_related = sum(1 for a in data if a.get("related") and len(a["related"]) > 0)
    total_links = sum(len(a.get("related", [])) for a in data)
    print(f"\nDone! {has_related}/{len(data)} aesthetics have related links")
    print(f"Total related links: {total_links}")


if __name__ == "__main__":
    main()
