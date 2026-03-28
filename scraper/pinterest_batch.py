"""
Pinterest batch image scraper for Universes.
Scrapes images for aesthetics that don't have them yet, in batches.

Usage:
    python scraper/pinterest_batch.py              # next 50
    python scraper/pinterest_batch.py --batch 75   # next 75
    python scraper/pinterest_batch.py --status      # show progress
"""

import json
import re
import time
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "js" / "data.js"
IMAGES_CACHE = ROOT / "js" / "images.json"
IMAGES_PER_AESTHETIC = 6


def load_images_cache():
    if IMAGES_CACHE.exists():
        with open(IMAGES_CACHE) as f:
            return json.load(f)
    return {}


def save_images_cache(cache):
    with open(IMAGES_CACHE, "w") as f:
        json.dump(cache, f, indent=2)


def get_all_aesthetic_ids():
    """Parse data.js to get all aesthetic ids and names."""
    with open(DATA_FILE) as f:
        content = f.read()
    # Extract id and name pairs
    pairs = re.findall(r'"id":\s*"([^"]+)".*?"name":\s*"([^"]+)"', content, re.DOTALL)
    return pairs


def get_needs_images(cache):
    """Get aesthetics that don't have images yet."""
    all_aesthetics = get_all_aesthetic_ids()
    needs = []
    for aid, name in all_aesthetics:
        if aid not in cache or len(cache[aid]) < IMAGES_PER_AESTHETIC:
            needs.append((aid, name))
    return needs


def scrape_pinterest(page, query, count=6):
    """Search Pinterest and grab image URLs."""
    search_url = f"https://pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
    try:
        page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(0.8)

        images = page.evaluate("""
            () => {
                const imgs = document.querySelectorAll('img[src*="pinimg.com"]');
                const urls = [];
                for (const img of imgs) {
                    let src = img.src;
                    src = src.replace('/75x/', '/564x/')
                             .replace('/236x/', '/564x/')
                             .replace('/474x/', '/564x/');
                    if (src.includes('/564x/') && !urls.includes(src)) {
                        urls.push(src);
                    }
                    if (urls.length >= %d) break;
                }
                return urls;
            }
        """ % count)
        return images
    except Exception as e:
        print(f"    ERROR: {e}")
        return []


def inject_images_to_data(cache):
    """Update data.js with images from cache."""
    with open(DATA_FILE) as f:
        content = f.read()

    updated = 0
    for aid, urls in cache.items():
        if not urls:
            continue
        pattern = r'("id":\s*"' + re.escape(aid) + r'".*?"images":\s*)\[.*?\]'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            replacement = match.group(1) + json.dumps(urls)
            content = content[:match.start()] + replacement + content[match.end():]
            updated += 1

    with open(DATA_FILE, "w") as f:
        f.write(content)
    return updated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=50)
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    cache = load_images_cache()
    needs = get_needs_images(cache)
    total = len(get_all_aesthetic_ids())
    done = total - len(needs)

    if args.status:
        print(f"Progress: {done}/{total} aesthetics have images ({len(needs)} remaining)")
        print(f"Batches left: {(len(needs) + args.batch - 1) // args.batch}")
        return

    if not needs:
        print("All aesthetics have images!")
        return

    batch = needs[:args.batch]
    print(f"Batch: {len(batch)} aesthetics ({done}/{total} done, {len(needs)} remaining)")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for i, (aid, name) in enumerate(batch):
            query = f"{name} aesthetic fashion"
            print(f"  [{i+1}/{len(batch)}] {name}...")
            images = scrape_pinterest(page, query, IMAGES_PER_AESTHETIC)
            cache[aid] = images
            print(f"    → {len(images)} images")

            # Save cache after each (resume-safe)
            save_images_cache(cache)
            time.sleep(1.5)

        browser.close()

    # Inject into data.js
    updated = inject_images_to_data(cache)
    remaining = len(get_needs_images(cache))
    print(f"\nDone! Updated {updated} aesthetics in data.js")
    print(f"Progress: {total - remaining}/{total} ({remaining} remaining)")


if __name__ == "__main__":
    main()
