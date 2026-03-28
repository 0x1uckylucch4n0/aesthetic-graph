"""
Pinterest image scraper for Universes.
Uses Playwright to search Pinterest for each aesthetic and grab image URLs.
Run: ~/.pyenv/versions/3.11.9/bin/python scraper/pinterest_scraper.py
"""

import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Each aesthetic and the Pinterest search query for it
AESTHETICS = {
    "70s-boho": "70s boho aesthetic fashion",
    "mod": "1960s mod fashion aesthetic",
    "pin-up": "pin up girl vintage aesthetic",
    "rockabilly": "rockabilly fashion aesthetic",
    "grunge": "grunge aesthetic fashion 90s",
    "goth": "goth fashion aesthetic",
    "punk": "punk fashion aesthetic",
    "whimsigoth": "whimsigoth aesthetic",
    "emo": "emo aesthetic fashion 2000s",
    "coquette": "coquette aesthetic fashion",
    "balletcore": "balletcore aesthetic",
    "cottagecore": "cottagecore aesthetic fashion",
    "dark-academia": "dark academia aesthetic",
    "light-academia": "light academia aesthetic",
    "minimalist": "minimalist fashion aesthetic",
    "quiet-luxury": "quiet luxury fashion aesthetic",
    "old-money": "old money aesthetic fashion",
    "clean-girl": "clean girl aesthetic",
    "y2k": "y2k fashion aesthetic",
    "techwear": "techwear fashion aesthetic",
    "hypebeast": "hypebeast fashion aesthetic",
    "skater": "skater fashion aesthetic",
    "gorpcore": "gorpcore aesthetic fashion",
    "granola": "granola girl aesthetic",
    "coastal-grandmother": "coastal grandmother aesthetic",
    "indie-sleaze": "indie sleaze aesthetic fashion",
    "camp": "camp fashion aesthetic met gala",
    "barbiecore": "barbiecore aesthetic fashion",
    "kitsch": "kitsch fashion aesthetic",
    "parisian": "parisian chic fashion aesthetic",
    "japanese-street": "harajuku japanese street fashion",
    "scandi": "scandinavian fashion aesthetic",
    "latina-glam": "latina glam fashion aesthetic",
}

IMAGES_PER_AESTHETIC = 6
OUTPUT_FILE = Path(__file__).parent.parent / "js" / "images.json"


def scrape_pinterest_images(page, query, count=6):
    """Search Pinterest and extract image URLs from results."""
    search_url = f"https://pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
    print(f"  Fetching: {search_url}")

    page.goto(search_url, wait_until="networkidle", timeout=30000)
    time.sleep(3)  # let images lazy-load

    # Scroll down a bit to load more images
    for _ in range(3):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1)

    # Grab image URLs from pin results
    # Pinterest renders images in <img> tags within pin containers
    images = page.evaluate("""
        () => {
            const imgs = document.querySelectorAll('img[src*="pinimg.com"]');
            const urls = [];
            for (const img of imgs) {
                let src = img.src;
                // Upgrade to higher resolution: swap /236x/ for /564x/
                src = src.replace('/75x/', '/564x/')
                         .replace('/236x/', '/564x/')
                         .replace('/474x/', '/564x/');
                if (src.includes('/564x/') && !urls.includes(src)) {
                    urls.push(src);
                }
                if (urls.length >= """ + str(count) + """) break;
            }
            return urls;
        }
    """)

    return images


def main():
    results = {}

    # Load existing results if any (for resuming)
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE) as f:
            results = json.load(f)
        print(f"Loaded {len(results)} existing entries from {OUTPUT_FILE}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headed so Pinterest doesn't block
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for aesthetic_id, query in AESTHETICS.items():
            # Skip if already scraped
            if aesthetic_id in results and len(results[aesthetic_id]) >= IMAGES_PER_AESTHETIC:
                print(f"[SKIP] {aesthetic_id} — already have {len(results[aesthetic_id])} images")
                continue

            print(f"\n[SCRAPING] {aesthetic_id}: '{query}'")
            try:
                images = scrape_pinterest_images(page, query, IMAGES_PER_AESTHETIC)
                results[aesthetic_id] = images
                print(f"  Got {len(images)} images")
            except Exception as e:
                print(f"  ERROR: {e}")
                results[aesthetic_id] = []

            # Save after each aesthetic (so we can resume)
            with open(OUTPUT_FILE, "w") as f:
                json.dump(results, f, indent=2)

            # Small delay between searches
            time.sleep(2)

        browser.close()

    print(f"\nDone! Saved to {OUTPUT_FILE}")
    print(f"Total aesthetics scraped: {len(results)}")
    total_images = sum(len(v) for v in results.values())
    print(f"Total images: {total_images}")


if __name__ == "__main__":
    main()
