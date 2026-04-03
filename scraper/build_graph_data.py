"""
Build graph data.js from the Aesthetics Wiki deep scrape.
============================================================
Reads aesthetics_deep.json and generates js/data.js with:
- All aesthetics as nodes with descriptions, elements, brands, references, images
- Connections derived from the wiki's "Related Aesthetics" sections
- Star sizes based on popularity (number of connections)

Usage:
    python scraper/build_graph_data.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUT_FILE = ROOT / "aesthetics_deep.json"
OUTPUT_FILE = ROOT / "js" / "data.js"

# ── Category → Family mapping ──
# The wiki has its own categories; we map them to our color families
CATEGORY_TO_FAMILY = {
    # Direct matches
    "Vintage": "Vintage / Retro",
    "Retro": "Vintage / Retro",
    "Nostalgia": "Vintage / Retro",
    "1950s": "Vintage / Retro",
    "1960s": "Vintage / Retro",
    "1970s": "Vintage / Retro",
    "1980s": "Vintage / Retro",
    "1990s": "Vintage / Retro",
    "2000s": "Vintage / Retro",

    "Dark": "Dark / Edgy",
    "Goth": "Dark / Edgy",
    "Gothic": "Dark / Edgy",
    "Punk": "Dark / Edgy",
    "Grunge": "Dark / Edgy",
    "Emo": "Dark / Edgy",
    "Horror": "Dark / Edgy",
    "Metal": "Dark / Edgy",

    "Romantic": "Romantic / Soft",
    "Soft": "Romantic / Soft",
    "Cottagecore": "Romantic / Soft",
    "Fairycore": "Romantic / Soft",
    "Feminine": "Romantic / Soft",
    "Academia": "Romantic / Soft",
    "Lolita": "Romantic / Soft",
    "Kawaii": "Romantic / Soft",
    "Cute": "Romantic / Soft",
    "Pastel": "Romantic / Soft",
    "Whimsical": "Romantic / Soft",
    "Angelic": "Romantic / Soft",
    "Fairy": "Romantic / Soft",
    "Princesscore": "Romantic / Soft",

    "Minimalism": "Clean / Minimal",
    "Minimal": "Clean / Minimal",
    "Clean": "Clean / Minimal",
    "Modern": "Clean / Minimal",
    "Corporate": "Clean / Minimal",
    "Professional": "Clean / Minimal",
    "Luxury": "Clean / Minimal",

    "Streetwear": "Streetwear / Urban",
    "Urban": "Streetwear / Urban",
    "Hip-Hop": "Streetwear / Urban",
    "Y2K": "Streetwear / Urban",
    "Hypebeast": "Streetwear / Urban",
    "Skater": "Streetwear / Urban",
    "Techwear": "Streetwear / Urban",
    "Cyberpunk": "Streetwear / Urban",
    "Futuristic": "Streetwear / Urban",
    "Sci-Fi": "Streetwear / Urban",

    "Nature": "Nature / Organic",
    "Outdoors": "Nature / Organic",
    "Cottagecore": "Nature / Organic",
    "Goblincore": "Nature / Organic",
    "Forestcore": "Nature / Organic",
    "Organic": "Nature / Organic",
    "Earthy": "Nature / Organic",
    "Coastal": "Nature / Organic",
    "Nautical": "Nature / Organic",
    "Garden": "Nature / Organic",
    "Botanical": "Nature / Organic",

    "Maximalism": "Maximalist / Eclectic",
    "Eclectic": "Maximalist / Eclectic",
    "Colorful": "Maximalist / Eclectic",
    "Camp": "Maximalist / Eclectic",
    "Kitsch": "Maximalist / Eclectic",
    "Indie": "Maximalist / Eclectic",
    "Art": "Maximalist / Eclectic",
    "Artistic": "Maximalist / Eclectic",
    "Surreal": "Maximalist / Eclectic",
    "Psychedelic": "Maximalist / Eclectic",
    "Clowncore": "Maximalist / Eclectic",
    "Kidcore": "Maximalist / Eclectic",

    "Cultural": "Cultural / Regional",
    "Regional": "Cultural / Regional",
    "Japanese": "Cultural / Regional",
    "Korean": "Cultural / Regional",
    "African": "Cultural / Regional",
    "Latin": "Cultural / Regional",
    "European": "Cultural / Regional",
    "British": "Cultural / Regional",
    "French": "Cultural / Regional",
    "Scandinavian": "Cultural / Regional",
    "Italian": "Cultural / Regional",
    "American": "Cultural / Regional",
}

FAMILIES = {
    "Vintage / Retro":       {"color": "#fef0d5", "stroke": "#e0c97a"},
    "Dark / Edgy":           {"color": "#e8dff5", "stroke": "#b8a5d4"},
    "Romantic / Soft":       {"color": "#fce4ec", "stroke": "#e0a0b0"},
    "Clean / Minimal":       {"color": "#eceff1", "stroke": "#b0bec5"},
    "Streetwear / Urban":    {"color": "#daeef3", "stroke": "#8cbdcc"},
    "Nature / Organic":      {"color": "#dcedc8", "stroke": "#a5c98a"},
    "Maximalist / Eclectic": {"color": "#ffe0b2", "stroke": "#e0a050"},
    "Cultural / Regional":   {"color": "#f5ddd0", "stroke": "#cda58a"},
}

DEFAULT_FAMILY = "Maximalist / Eclectic"


WIKI_SECTION_HEADERS = [
    'Origins', 'Other names', 'Decade of origin', 'Location of origin',
    'Visuals & Themes', 'Key motifs', 'Key colours', 'Key colors',
    'Key values', 'Connections', 'Relatedaesthetics', 'ConnectionsRelated',
    'Related aesthetics', 'Creator(s)', 'Subcategories', 'Sub-genres',
    'Notable figures', 'See also', 'External links', 'References',
    'Gallery', 'Music', 'Films', 'Literature', 'Activities',
    'Behavior', 'Lifestyle', 'Fashion', 'Key figures', 'Notable people',
    'Types of', 'Media',
]
HEADER_PATTERN = '|'.join(re.escape(h) for h in WIKI_SECTION_HEADERS)


def extract_wiki_field(text, field_name):
    """Extract value after a wiki section header."""
    pattern = re.escape(field_name) + r'(.*?)(?=' + HEADER_PATTERN + r'|$)'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return ""


def clean_wiki_description(name, raw_desc):
    """Parse raw wiki dump into a clean description and tagline."""
    if not raw_desc or len(raw_desc) < 5:
        return f"{name} is a distinct aesthetic movement.", f"The {name} aesthetic"

    decade = extract_wiki_field(raw_desc, 'Decade of origin')
    location = extract_wiki_field(raw_desc, 'Location of origin')
    motifs = extract_wiki_field(raw_desc, 'Key motifs')
    values = extract_wiki_field(raw_desc, 'Key values')
    other_names = extract_wiki_field(raw_desc, 'Other names')

    # Get intro text (before first wiki header)
    intro_parts = re.split(HEADER_PATTERN, raw_desc)
    intro = intro_parts[0].strip() if intro_parts else ""

    # Strip wiki disambiguation notices
    intro = re.sub(r'This (?:article|page) (?:is about|describes)[^.]*\.\s*', '', intro)
    intro = re.sub(r'For (?:other|the)[^.]*(?:see|See)[^.]*\.\s*', '', intro)
    intro = intro.strip()

    if intro.startswith(name):
        intro = intro[len(name):].strip()

    # Remove image captions
    intro = re.sub(
        r'^[^.]*(?:photo|image|example|artwork|cover art|depicting|illustration|'
        r'typical|wearing|showing|featuring|pictured|seen in|characterized|'
        r'screenshot|archetype|still from|poster|album|painting|'
        r'commonly|standard|originally|distributed)[^.]*\.?\s*',
        '', intro, flags=re.IGNORECASE
    )
    intro = intro.strip()

    parts = []
    if intro and len(intro) > 20:
        parts.append(intro.rstrip('.') + '.')

    if decade or location:
        origin_bits = []
        if decade:
            origin_bits.append(f"emerging in the {decade}")
        if location:
            origin_bits.append(f"from {location}")
        parts.append(f"{name} is an aesthetic {' '.join(origin_bits)}.")
    elif not parts:
        parts.append(f"{name} is a distinct aesthetic movement.")

    if motifs:
        motif_list = [m.strip() for m in re.split(r',\s*', motifs) if m.strip() and len(m.strip()) > 1][:6]
        if motif_list:
            parts.append(f"Key visual elements include {', '.join(motif_list).lower()}.")

    if values:
        val_list = [v.strip() for v in re.split(r',\s*', values) if v.strip() and len(v.strip()) > 1][:5]
        if val_list:
            parts.append(f"It embodies {', '.join(val_list).lower()}.")

    if other_names:
        aka_list = [n.strip() for n in re.split(r',\s*', other_names) if n.strip() and len(n.strip()) > 1][:4]
        if aka_list:
            parts.append(f"Also known as {', '.join(aka_list)}.")

    desc = ' '.join(parts)
    tagline = parts[0] if parts else f"The {name} aesthetic"
    if len(tagline) > 80:
        tagline = tagline[:77] + "..."

    return desc, tagline


def slugify(name: str) -> str:
    """Convert aesthetic name to a URL-friendly slug."""
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def guess_family(aesthetic: dict) -> str:
    """Guess the family based on the wiki category and name."""
    category = aesthetic.get("category", "")
    name = aesthetic.get("name", "")
    desc = aesthetic.get("description", "")

    combined = f"{category} {name} {desc}".lower()

    # Check category keywords
    for keyword, family in CATEGORY_TO_FAMILY.items():
        if keyword.lower() in combined:
            return family

    return DEFAULT_FAMILY


def build_graph_data():
    with open(INPUT_FILE) as f:
        raw = json.load(f)

    print(f"Loaded {len(raw)} aesthetics from wiki")

    # Filter out meta pages and very thin entries
    aesthetics = []
    for a in raw:
        name = a.get("name", "").strip()
        if not name or len(name) < 2:
            continue
        # Skip meta pages
        if any(skip in name.lower() for skip in [
            "list of", "category", "by decade", "by category",
            "wanted pages", "help", "wiki", "admin", "blog",
            "template", "navigation", "main page"
        ]):
            continue
        aesthetics.append(a)

    print(f"After filtering meta pages: {len(aesthetics)}")

    # Build name → slug lookup
    name_to_slug = {}
    slug_set = set()
    for a in aesthetics:
        slug = slugify(a["name"])
        # Handle duplicates
        if slug in slug_set:
            slug = slug + "-2"
        slug_set.add(slug)
        name_to_slug[a["name"]] = slug

    # Build connections from "related" fields
    # Only keep MUTUAL connections (A links to B AND B links to A)
    # This filters out noise from index-like pages that link everything
    connection_set = set()
    connection_count = {}

    # First pass: build directional link map
    links_from = {}  # slug → set of slugs it links to
    for a in aesthetics:
        slug = name_to_slug.get(a["name"])
        if not slug:
            continue
        connection_count.setdefault(slug, 0)
        links_from[slug] = set()

        related = a.get("related", [])
        for rel_name in related:
            rel_slug = name_to_slug.get(rel_name)
            if rel_slug and rel_slug != slug:
                links_from[slug].add(rel_slug)

    # Second pass: only keep mutual connections (bidirectional)
    connections = []
    for slug, targets in links_from.items():
        for target in targets:
            if target in links_from and slug in links_from[target]:
                pair = tuple(sorted([slug, target]))
                if pair not in connection_set:
                    connection_set.add(pair)
                    connections.append({
                        "source": pair[0],
                        "target": pair[1],
                    })
                    connection_count[slug] = connection_count.get(slug, 0) + 1
                    connection_count[target] = connection_count.get(target, 0) + 1

    print(f"Mutual connections: {len(connections)}")

    # Store raw connection counts for sizing BEFORE capping
    raw_connection_count = dict(connection_count)

    # If still too many, cap per node
    MAX_CONNECTIONS_PER_NODE = 8
    if len(connections) > 5000:
        # Score each connection: prefer connections between nodes with fewer total links
        # (this keeps meaningful niche connections, drops spam from mega-connected nodes)
        scored = []
        for c in connections:
            s_count = connection_count.get(c["source"], 0)
            t_count = connection_count.get(c["target"], 0)
            # Lower combined count = more specific relationship
            score = s_count + t_count
            scored.append((score, c))
        scored.sort(key=lambda x: x[0])

        # Keep connections, limiting each node to MAX_CONNECTIONS_PER_NODE
        kept = []
        node_conn_count = {}
        for score, c in scored:
            s, t = c["source"], c["target"]
            s_n = node_conn_count.get(s, 0)
            t_n = node_conn_count.get(t, 0)
            if s_n < MAX_CONNECTIONS_PER_NODE and t_n < MAX_CONNECTIONS_PER_NODE:
                kept.append(c)
                node_conn_count[s] = s_n + 1
                node_conn_count[t] = t_n + 1

        connections = kept
        # Recalculate connection counts
        connection_count = {}
        for c in connections:
            connection_count[c["source"]] = connection_count.get(c["source"], 0) + 1
            connection_count[c["target"]] = connection_count.get(c["target"], 0) + 1

        print(f"After capping per-node: {len(connections)}")

    # Calculate star sizes based on connection count
    # More connections = bigger star = more "mainstream"
    max_connections = max(connection_count.values()) if connection_count else 1

    # Size tiers based on RAW (uncapped) connection count
    raw_counts = sorted(raw_connection_count.values(), reverse=True)
    p90 = raw_counts[int(len(raw_counts) * 0.03)] if raw_counts else 1
    p75 = raw_counts[int(len(raw_counts) * 0.10)] if raw_counts else 1
    p50 = raw_counts[int(len(raw_counts) * 0.30)] if raw_counts else 1
    p25 = raw_counts[int(len(raw_counts) * 0.60)] if raw_counts else 1
    print(f"Raw connection percentiles: p3={p90}, p10={p75}, p30={p50}, p60={p25}")

    def get_size_tier(slug):
        count = raw_connection_count.get(slug, 0)
        if count >= p90:
            return 5   # huge — top 3% viral mainstream
        elif count >= p75:
            return 4   # large — top 10%
        elif count >= p50:
            return 3   # medium — top 30%
        elif count >= p25:
            return 2   # small — top 60%
        else:
            return 1   # tiny — bottom 40%, emerging

    # Build the JS data
    nodes = []
    for a in aesthetics:
        slug = name_to_slug.get(a["name"])
        if not slug:
            continue

        family = guess_family(a)
        raw_desc = a.get("description", "")
        images = a.get("images", [])
        related = a.get("related", [])
        category = a.get("category", "Uncategorized")
        size_tier = get_size_tier(slug)
        conn_count = connection_count.get(slug, 0)

        # Clean description and generate tagline
        desc, tagline = clean_wiki_description(a["name"], raw_desc)

        nodes.append({
            "id": slug,
            "name": a["name"],
            "family": family,
            "tagline": tagline,
            "tags": [category],
            "elements": [],
            "brands": [],
            "description": desc,
            "references": [],
            "images": images[:8],
            "size": size_tier,
            "connectionCount": conn_count,
        })

    # Sort nodes: biggest stars first, then alphabetical
    nodes.sort(key=lambda n: (-n["size"], n["name"]))

    print(f"Nodes: {len(nodes)}")
    print(f"Size distribution: " + str({
        f"tier_{i}": sum(1 for n in nodes if n["size"] == i) for i in range(1, 6)
    }))

    # ── Generate JS ──
    js = """// ── Auto-generated from Aesthetics Wiki ──
// Generated by scraper/build_graph_data.py

// ── Color palette by family ──
const FAMILIES = """ + json.dumps(FAMILIES, indent=2) + """;

// ── Star size config ──
// size 1 = tiny (emerging), 5 = huge (viral mainstream)
const STAR_SIZES = {
  1: { outer: 30, inner: 18, round: 6 },   // tiny
  2: { outer: 42, inner: 26, round: 8 },   // small
  3: { outer: 55, inner: 34, round: 11 },  // medium
  4: { outer: 68, inner: 42, round: 13 },  // large
  5: { outer: 82, inner: 50, round: 15 },  // huge
};

// ── Nodes ──
const aesthetics = """ + json.dumps(nodes, indent=2, ensure_ascii=False) + """;

// ── Connections ──
const connections = """ + json.dumps(connections, indent=2, ensure_ascii=False) + """;
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js)

    print(f"\nWritten to {OUTPUT_FILE}")
    print(f"  {len(nodes)} nodes, {len(connections)} connections")


if __name__ == "__main__":
    build_graph_data()
