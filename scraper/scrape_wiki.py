"""
Aesthetics Wiki Scraper (Playwright version)
=============================================
Uses Playwright to bypass Fandom's bot protection.
Scrapes https://aesthetics.fandom.com/wiki/List_of_Aesthetics

Usage:
    python scrape_wiki.py                    # list only → aesthetics_list.json
    python scrape_wiki.py --deep             # list + each page → aesthetics_deep.json
    python scrape_wiki.py --deep --limit 50  # first 50 pages only
"""

import json
import re
import time
import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "https://aesthetics.fandom.com"
LIST_URL = f"{BASE_URL}/wiki/List_of_Aesthetics"
OUTPUT_DIR = Path(__file__).parent.parent


def scrape_list(page) -> list[dict]:
    """Scrape the main List of Aesthetics page."""
    print("Fetching main list page...")
    page.goto(LIST_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    aesthetics = page.evaluate("""
        () => {
            const content = document.querySelector('.mw-parser-output');
            if (!content) return [];

            const results = [];
            let currentCategory = 'Uncategorized';

            for (const el of content.children) {
                if (el.tagName === 'H2' || el.tagName === 'H3') {
                    let text = el.textContent.trim().replace(/\\[edit.*?\\]/g, '').trim();
                    if (text) currentCategory = text;
                }

                if (['UL', 'OL', 'DIV', 'P'].includes(el.tagName)) {
                    const links = el.querySelectorAll('a[href]');
                    for (const link of links) {
                        const href = link.getAttribute('href');
                        const name = link.textContent.trim();
                        if (
                            href && href.startsWith('/wiki/') &&
                            !href.includes(':') &&
                            name && name.length > 1 &&
                            !href.startsWith('/wiki/List_of') &&
                            !href.startsWith('/wiki/Category')
                        ) {
                            results.push({ name, url: href, category: currentCategory });
                        }
                    }
                }
            }

            // Deduplicate by URL
            const seen = new Set();
            return results.filter(a => {
                if (seen.has(a.url)) return false;
                seen.add(a.url);
                return true;
            });
        }
    """)

    # Add full URLs
    for a in aesthetics:
        a["url"] = BASE_URL + a["url"]

    print(f"Found {len(aesthetics)} unique aesthetics.")
    return aesthetics


def scrape_page(page, url: str) -> dict:
    """Scrape an individual aesthetic page for description, related, and images."""
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(1.5)
    except Exception as e:
        print(f"    Error loading {url}: {e}")
        return {}

    return page.evaluate("""
        () => {
            const content = document.querySelector('.mw-parser-output');
            if (!content) return {};

            const result = {};

            // Description: first non-empty paragraph
            const paras = content.querySelectorAll(':scope > p');
            for (const p of paras) {
                const text = p.textContent.trim();
                if (text.length > 50) {
                    result.description = text;
                    break;
                }
            }

            // Related aesthetics — from dedicated sections
            const related = [];
            const headers = content.querySelectorAll('h2, h3');
            for (const h of headers) {
                const ht = h.textContent.trim().toLowerCase();
                if (['related', 'see also', 'similar', 'influenced'].some(kw => ht.includes(kw))) {
                    let sib = h.nextElementSibling;
                    while (sib && sib.tagName !== 'H2' && sib.tagName !== 'H3') {
                        const links = sib.querySelectorAll('a[href^="/wiki/"]');
                        for (const link of links) {
                            const href = link.getAttribute('href');
                            const name = link.textContent.trim();
                            if (!href.includes(':') && name) related.push(name);
                        }
                        sib = sib.nextElementSibling;
                    }
                }
            }

            // Also extract inline links from ALL paragraphs and list items
            // These are references to other aesthetics within the text
            const allLinks = content.querySelectorAll('p a[href^="/wiki/"], li a[href^="/wiki/"]');
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

            if (related.length) result.related = [...new Set(related)];

            // Gallery images
            const images = [];
            const imgs = content.querySelectorAll('img[src^="http"]');
            for (const img of imgs) {
                let src = img.src;
                if (src.includes('static') || src.includes('data:image')) continue;
                src = src.split('/revision/')[0];
                if (!images.includes(src)) images.push(src);
                if (images.length >= 8) break;
            }
            if (images.length) result.images = images;

            return result;
        }
    """)


def main():
    parser = argparse.ArgumentParser(description="Scrape Aesthetics Wiki (Playwright)")
    parser.add_argument("--deep", action="store_true", help="Also scrape individual pages")
    parser.add_argument("--limit", type=int, default=0, help="Limit pages to scrape (0 = all)")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Step 1: Get the list
        aesthetics = scrape_list(page)

        # Step 2: Optionally deep-scrape
        if args.deep:
            total = args.limit if args.limit > 0 else len(aesthetics)
            subset = aesthetics[:total]
            print(f"\nDeep scraping {len(subset)} aesthetic pages...\n")

            for i, aesthetic in enumerate(subset):
                print(f"  [{i+1}/{len(subset)}] {aesthetic['name']}...")
                details = scrape_page(page, aesthetic["url"])
                aesthetic.update(details)
                time.sleep(0.5)

            output_file = OUTPUT_DIR / "aesthetics_deep.json"

            # Save progress after every 25 pages
            if (i + 1) % 25 == 0 or (i + 1) == len(subset):
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(aesthetics, f, indent=2, ensure_ascii=False)
                print(f"  [SAVED] {i+1}/{len(subset)} to {output_file}")

        else:
            output_file = OUTPUT_DIR / "aesthetics_list.json"

        browser.close()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(aesthetics, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(aesthetics)} aesthetics to {output_file}")


if __name__ == "__main__":
    main()
