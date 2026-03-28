"""
Aesthetics Wiki Scraper
========================
Scrapes https://aesthetics.fandom.com/wiki/List_of_Aesthetics
and optionally each individual aesthetic page for descriptions + related aesthetics.

Requirements:
    pip install requests beautifulsoup4

Usage:
    python scrape_aesthetics.py                  # scrape list only → aesthetics_list.json
    python scrape_aesthetics.py --deep           # scrape list + each page → aesthetics_deep.json
    python scrape_aesthetics.py --deep --limit 50  # scrape first 50 pages only
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import argparse
import re
import sys

BASE_URL = "https://aesthetics.fandom.com"
LIST_URL = f"{BASE_URL}/wiki/List_of_Aesthetics"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_page(url: str, retries: int = 3) -> BeautifulSoup | None:
    """Fetch a page with retries and return parsed soup."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except requests.RequestException as e:
            print(f"  ⚠ Attempt {attempt+1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None


def scrape_aesthetic_list() -> list[dict]:
    """
    Scrape the main List of Aesthetics page.
    Returns a list of dicts: {name, url, category}
    """
    print("📥 Fetching main list page...")
    soup = fetch_page(LIST_URL)
    if not soup:
        print("❌ Failed to fetch the list page.")
        sys.exit(1)

    content = soup.find("div", class_="mw-parser-output")
    if not content:
        print("❌ Could not find page content.")
        sys.exit(1)

    aesthetics = []
    current_category = "Uncategorized"

    for element in content.children:
        if not hasattr(element, "name"):
            continue

        # Track category headers (h2, h3)
        if element.name in ("h2", "h3"):
            header_text = element.get_text(strip=True)
            # Remove [edit] spans
            header_text = re.sub(r"\[edit[^\]]*\]", "", header_text).strip()
            if header_text:
                current_category = header_text

        # Parse links from lists and paragraphs
        if element.name in ("ul", "ol", "div", "p"):
            links = element.find_all("a", href=True)
            for link in links:
                href = link["href"]
                name = link.get_text(strip=True)

                # Filter: only wiki article links, skip meta/category/file links
                if (
                    href.startswith("/wiki/")
                    and ":" not in href
                    and name
                    and len(name) > 1
                    and not href.startswith("/wiki/List_of")
                    and not href.startswith("/wiki/Category")
                ):
                    aesthetics.append({
                        "name": name,
                        "url": BASE_URL + href,
                        "category": current_category,
                    })

    # Deduplicate by URL
    seen = set()
    unique = []
    for a in aesthetics:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    print(f"✅ Found {len(unique)} unique aesthetics.")
    return unique


def scrape_aesthetic_page(url: str) -> dict:
    """
    Scrape an individual aesthetic page for:
    - description (first paragraph)
    - related aesthetics (from Related/See Also/Similar sections + sidebar)
    - key visuals / gallery image URLs
    """
    soup = fetch_page(url)
    if not soup:
        return {}

    content = soup.find("div", class_="mw-parser-output")
    if not content:
        return {}

    result = {}

    # --- Description: first non-empty paragraph ---
    for p in content.find_all("p", recursive=False):
        text = p.get_text(strip=True)
        if len(text) > 50:
            result["description"] = text
            break

    # --- Related aesthetics: links from Related/See Also sections ---
    related = []
    for header in content.find_all(["h2", "h3"]):
        header_text = header.get_text(strip=True).lower()
        if any(kw in header_text for kw in ["related", "see also", "similar", "influenced"]):
            # Grab links from next siblings until next header
            sibling = header.find_next_sibling()
            while sibling and sibling.name not in ("h2", "h3"):
                for link in sibling.find_all("a", href=True):
                    href = link["href"]
                    name = link.get_text(strip=True)
                    if href.startswith("/wiki/") and ":" not in href and name:
                        related.append(name)
                sibling = sibling.find_next_sibling() if sibling else None

    if related:
        result["related"] = list(dict.fromkeys(related))  # dedupe, preserve order

    # --- Gallery images ---
    images = []
    for img in content.find_all("img", src=True):
        src = img["src"]
        if "static" not in src and "data:image" not in src and src.startswith("http"):
            # Get higher-res version by removing /revision/... suffix
            clean_src = re.split(r"/revision/", src)[0]
            if clean_src not in images:
                images.append(clean_src)
    if images:
        result["images"] = images[:6]  # cap at 6

    return result


def main():
    parser = argparse.ArgumentParser(description="Scrape Aesthetics Wiki")
    parser.add_argument("--deep", action="store_true", help="Also scrape individual pages")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of pages to scrape (0 = all)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds")
    args = parser.parse_args()

    # Step 1: Get the list
    aesthetics = scrape_aesthetic_list()

    # Step 2: Optionally deep-scrape each page
    if args.deep:
        total = args.limit if args.limit > 0 else len(aesthetics)
        subset = aesthetics[:total]
        print(f"\n🔍 Deep scraping {len(subset)} aesthetic pages (delay: {args.delay}s)...\n")

        for i, aesthetic in enumerate(subset):
            print(f"  [{i+1}/{len(subset)}] {aesthetic['name']}...")
            details = scrape_aesthetic_page(aesthetic["url"])
            aesthetic.update(details)
            time.sleep(args.delay)

        output_file = "aesthetics_deep.json"
    else:
        output_file = "aesthetics_list.json"

    # Step 3: Save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(aesthetics, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved {len(aesthetics)} aesthetics to {output_file}")


if __name__ == "__main__":
    main()
