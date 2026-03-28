"""
Scrape Aesthetics Wiki using the MediaWiki API.
No Cloudflare issues, gets links + descriptions + images reliably.

Usage:
    python scraper/api_scrape.py
"""

import json
import re
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
LIST_FILE = ROOT / "aesthetics_list.json"
OUTPUT_FILE = ROOT / "aesthetics_deep.json"

API_URL = "https://aesthetics.fandom.com/api.php"
HEADERS = {
    "User-Agent": "UniversesBot/1.0 (aesthetic graph project)"
}


def api_parse(page_title: str) -> dict | None:
    """Use MediaWiki parse API to get links, text, and images for a page."""
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text|links|images",
        "format": "json",
    }
    try:
        resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if "parse" in data:
            return data["parse"]
    except Exception as e:
        print(f"    API error: {e}")
    return None


def extract_description(html: str) -> str:
    """Extract first meaningful paragraph from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 50:
            return text
    return ""


def extract_images(html: str) -> list[str]:
    """Extract image URLs from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if "static" in src or "data:image" in src:
            continue
        if not src.startswith("http"):
            continue
        # Clean up Fandom image URLs
        clean = re.split(r"/revision/", src)[0]
        # Skip tiny icons
        width = img.get("width", "")
        if width and width.isdigit() and int(width) < 50:
            continue
        if clean not in images:
            images.append(clean)
        if len(images) >= 8:
            break
    return images


def main():
    # Load the list of aesthetics
    with open(LIST_FILE) as f:
        aesthetics = json.load(f)

    print(f"Loaded {len(aesthetics)} aesthetics from list")

    # Build set of valid names for connection matching
    all_names = set(a["name"] for a in aesthetics)

    results = []

    for i, aesthetic in enumerate(aesthetics):
        name = aesthetic["name"]
        # Extract page title from URL
        page_title = aesthetic["url"].split("/wiki/")[-1]

        print(f"  [{i+1}/{len(aesthetics)}] {name}...")

        parsed = api_parse(page_title)
        if not parsed:
            results.append(aesthetic)
            continue

        # Extract internal links (namespace 0 = main articles)
        links = parsed.get("links", [])
        related = []
        for link in links:
            if link.get("ns") == 0 and "exists" in link:
                link_name = link["*"]
                if link_name in all_names and link_name != name:
                    related.append(link_name)

        # Extract description and images from HTML
        html = parsed.get("text", {}).get("*", "")
        description = extract_description(html)
        images = extract_images(html)

        aesthetic["related"] = related
        aesthetic["description"] = description
        aesthetic["images"] = images

        if related:
            print(f"    → {len(related)} connections, {len(images)} images")

        results.append(aesthetic)

        # Save every 50
        if (i + 1) % 50 == 0 or (i + 1) == len(aesthetics):
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"  [SAVED] {i+1}/{len(aesthetics)}")

        time.sleep(0.5)  # Be nice to the API

    # Final save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    has_related = sum(1 for a in results if a.get("related"))
    has_desc = sum(1 for a in results if a.get("description"))
    total_links = sum(len(a.get("related", [])) for a in results)
    print(f"\nDone!")
    print(f"  {has_desc}/{len(results)} have descriptions")
    print(f"  {has_related}/{len(results)} have connections")
    print(f"  Total connection links: {total_links}")


if __name__ == "__main__":
    main()
