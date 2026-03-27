// ── Color palette by family ──
const FAMILIES = {
  "Vintage / Retro":      { color: "#fef0d5", stroke: "#e0c97a" },
  "Dark / Edgy":          { color: "#e8dff5", stroke: "#b8a5d4" },
  "Romantic / Soft":      { color: "#fce4ec", stroke: "#e0a0b0" },
  "Clean / Minimal":      { color: "#eceff1", stroke: "#b0bec5" },
  "Streetwear / Urban":   { color: "#daeef3", stroke: "#8cbdcc" },
  "Nature / Organic":     { color: "#dcedc8", stroke: "#a5c98a" },
  "Maximalist / Eclectic":{ color: "#ffe0b2", stroke: "#e0a050" },
  "Cultural / Regional":  { color: "#f5ddd0", stroke: "#cda58a" },
};

// ── Nodes ──
const aesthetics = [
  // ── Vintage / Retro ──
  {
    id: "70s-boho",
    name: "70s Boho",
    family: "Vintage / Retro",
    tagline: "Free-spirited, earthy, and sun-drenched",
    tags: ["1970s", "warm tones", "flowy"],
    elements: ["Flared jeans", "Crochet tops", "Suede fringe", "Platform shoes", "Round sunglasses", "Earth tones"],
    brands: ["Free People", "Spell & The Gypsy", "Doen", "Ulla Johnson", "Faithfull the Brand", "Anthropologie"],
    description: "Rooted in the counterculture movement of the 1970s, 70s Boho is all about freedom, self-expression, and a connection to nature. Think Stevie Nicks on a California afternoon.",
    references: ["Stevie Nicks", "Almost Famous (2000)", "Fleetwood Mac", "Laurel Canyon"],
    images: []
  },
  {
    id: "mod",
    name: "Mod",
    family: "Vintage / Retro",
    tagline: "Sharp, geometric, and London-cool",
    tags: ["1960s", "graphic", "structured"],
    elements: ["Shift dresses", "Go-go boots", "Bold geometric prints", "Mini skirts", "Color blocking", "Heavy eyeliner"],
    brands: ["Mary Quant", "Courreges", "Miu Miu", "Marimekko", "Ted Baker"],
    description: "Born in 1960s London, Mod was the look of youth rebellion — clean lines, bold patterns, and a confidence that said 'the future is now'. Twiggy is the patron saint.",
    references: ["Twiggy", "A Clockwork Orange", "The Who", "Mary Quant"],
    images: []
  },
  {
    id: "pin-up",
    name: "Pin-Up",
    family: "Vintage / Retro",
    tagline: "Glamorous, playful, and unapologetically feminine",
    tags: ["1940s-50s", "retro glam", "bold lip"],
    elements: ["High-waisted shorts", "Polka dots", "Victory rolls", "Red lipstick", "Winged eyeliner", "Bullet bras"],
    brands: ["Pinup Girl Clothing", "Collectif", "Bettie Page Clothing", "Besame Cosmetics", "What Katie Did"],
    description: "Pin-Up style draws from WWII-era Americana — Bettie Page, Vargas girls, and a celebration of curves. It's campy, confident, and always a little winking at you.",
    references: ["Bettie Page", "Dita Von Teese", "Grease (1978)", "Vargas illustrations"],
    images: []
  },
  {
    id: "rockabilly",
    name: "Rockabilly",
    family: "Vintage / Retro",
    tagline: "Greased-up rebellion meets vintage charm",
    tags: ["1950s", "rock n roll", "americana"],
    elements: ["Pompadours", "Leather jackets", "Bandanas", "Cuffed jeans", "Cherry prints", "Creeper shoes"],
    brands: ["Schott NYC", "Steady Clothing", "Sourpuss Clothing", "Lucky 13", "Levi's Vintage"],
    description: "A fusion of 1950s rock 'n' roll and hillbilly country. Rockabilly is Elvis meets hot rods — it's louder and more rebellious than Pin-Up, but shares the same vintage DNA.",
    references: ["Elvis Presley", "Cry-Baby (1990)", "The Stray Cats", "Psychobilly subculture"],
    images: []
  },

  // ── Dark / Edgy ──
  {
    id: "grunge",
    name: "Grunge",
    family: "Dark / Edgy",
    tagline: "I rolled out of bed and I don't care",
    tags: ["1990s", "Seattle", "anti-fashion"],
    elements: ["Flannel shirts", "Ripped jeans", "Doc Martens", "Band tees", "Messy hair", "Oversized everything"],
    brands: ["Doc Martens", "Converse", "Carhartt WIP", "Dickies", "Levi's", "Thrift stores (the real brand)"],
    description: "Born in early-90s Seattle alongside Nirvana and Pearl Jam, grunge was a rejection of the polished excess of the 80s. It's thrift-store chic elevated to a cultural movement.",
    references: ["Kurt Cobain", "Courtney Love", "Singles (1992)", "Pearl Jam"],
    images: []
  },
  {
    id: "goth",
    name: "Goth",
    family: "Dark / Edgy",
    tagline: "Romantic darkness, Victorian drama",
    tags: ["1980s-now", "black", "theatrical"],
    elements: ["All black", "Lace", "Corsets", "Silver jewelry", "Dark lipstick", "Velvet", "Platform boots"],
    brands: ["Killstar", "Dolls Kill", "Disturbia", "Rick Owens", "Ann Demeulemeester", "Demonia"],
    description: "Emerging from post-punk in the early 80s, goth is a celebration of the dark and beautiful. It borrows from Victorian mourning wear, horror cinema, and romantic poetry.",
    references: ["Siouxsie Sioux", "The Cure", "Beetlejuice (1988)", "Bauhaus"],
    images: []
  },
  {
    id: "punk",
    name: "Punk",
    family: "Dark / Edgy",
    tagline: "Destroy, create, repeat",
    tags: ["1970s-now", "DIY", "anti-establishment"],
    elements: ["Safety pins", "Leather jackets", "Mohawks", "Tartan", "Studs & spikes", "Combat boots", "Band patches"],
    brands: ["Vivienne Westwood", "Dr. Martens", "Underground England", "Tripp NYC", "Manic Panic"],
    description: "Punk isn't just a look — it's an ideology. Born in 70s London and NYC, punk fashion is deliberately confrontational, DIY, and opposed to mainstream everything.",
    references: ["Vivienne Westwood", "Sex Pistols", "Ramones", "SLC Punk! (1998)"],
    images: []
  },
  {
    id: "whimsigoth",
    name: "Whimsigoth",
    family: "Dark / Edgy",
    tagline: "If a witch went to a garden party",
    tags: ["2020s", "mystical", "dark feminine"],
    elements: ["Celestial prints", "Flowing black dresses", "Crystal jewelry", "Tarot motifs", "Dark florals", "Sheer layers"],
    brands: ["Free People", "Rat & Boa", "Spell & The Gypsy", "The Vampire's Wife", "Killstar"],
    description: "A softer, more mystical take on goth that emerged on TikTok. Think 90s Stevie Nicks meets The Craft — dark but dreamy, occult but approachable.",
    references: ["The Craft (1996)", "Practical Magic", "Stevie Nicks (again)", "Florence Welch"],
    images: []
  },
  {
    id: "emo",
    name: "Emo",
    family: "Dark / Edgy",
    tagline: "Feelings worn on black skinny jeans",
    tags: ["2000s", "emotional", "music-driven"],
    elements: ["Side-swept bangs", "Skinny jeans", "Studded belts", "Converse", "Band merch", "Eyeliner (all genders)"],
    brands: ["Hot Topic", "Converse", "Vans", "Tripp NYC", "BlackCraft Cult"],
    description: "Emo fashion grew out of the mid-2000s emo/post-hardcore music scene. It's deeply personal, a little theatrical, and always tied to the emotional intensity of the music.",
    references: ["My Chemical Romance", "Paramore", "Pete Wentz", "Hot Topic culture"],
    images: []
  },

  // ── Romantic / Soft ──
  {
    id: "coquette",
    name: "Coquette",
    family: "Romantic / Soft",
    tagline: "Bows, blush, and batting eyelashes",
    tags: ["2020s", "hyper-feminine", "flirty"],
    elements: ["Bows & ribbons", "Lace", "Baby pink", "Ballet flats", "Pearl jewelry", "Sheer fabrics"],
    brands: ["Sandy Liang", "LoveShackFancy", "For Love & Lemons", "Agent Provocateur", "Simone Rocha"],
    description: "Coquette is femininity turned up to eleven — inspired by Lolita aesthetics, French boudoirs, and a deliberate, knowing performance of girlhood.",
    references: ["Marie Antoinette (2006)", "Lana Del Rey", "Sofia Coppola", "Bridgerton"],
    images: []
  },
  {
    id: "balletcore",
    name: "Balletcore",
    family: "Romantic / Soft",
    tagline: "Grace, discipline, and a perfect bun",
    tags: ["2020s", "ethereal", "movement"],
    elements: ["Wrap tops", "Leg warmers", "Ballet flats", "Leotard silhouettes", "Soft pink", "Hair ribbons", "Tulle"],
    brands: ["Repetto", "Capezio", "Skims", "Miu Miu", "Simone Rocha"],
    description: "Inspired by professional ballet dancers — both on stage and in rehearsal. It's the effortless elegance of a dancer grabbing coffee after class.",
    references: ["Black Swan (2010)", "Center Stage (2000)", "Misty Copeland", "Degas paintings"],
    images: []
  },
  {
    id: "cottagecore",
    name: "Cottagecore",
    family: "Romantic / Soft",
    tagline: "Baking bread in a wildflower meadow",
    tags: ["2020s", "pastoral", "handmade"],
    elements: ["Prairie dresses", "Puff sleeves", "Florals", "Linen & cotton", "Straw hats", "Basket bags", "Peter Pan collars"],
    brands: ["Doen", "Christy Dawn", "Hill House Home", "Reformation", "& Other Stories"],
    description: "A romanticized vision of rural life — gardens, baking, candlelight, and simplicity. Cottagecore exploded during the pandemic as an antidote to modern anxieties.",
    references: ["Little Women (2019)", "Taylor Swift's folklore", "Studio Ghibli", "Beatrix Potter"],
    images: []
  },
  {
    id: "dark-academia",
    name: "Dark Academia",
    family: "Romantic / Soft",
    tagline: "Old libraries, espresso, and existential dread",
    tags: ["2020s", "intellectual", "autumnal"],
    elements: ["Tweed blazers", "Turtlenecks", "Oxford shoes", "Plaid trousers", "Satchels", "Earth tones", "Gold-rimmed glasses"],
    brands: ["Ralph Lauren", "Brooks Brothers", "Barbour", "Dr. Martens", "Cambridge Satchel Co."],
    description: "An obsession with classical education, literature, and the aesthetics of old European universities. It's romantic but moody — think studying Keats in a Gothic library at midnight.",
    references: ["Dead Poets Society (1989)", "The Secret History", "Donna Tartt", "Oxford University"],
    images: []
  },
  {
    id: "light-academia",
    name: "Light Academia",
    family: "Romantic / Soft",
    tagline: "Same library, but it's golden hour",
    tags: ["2020s", "warm", "optimistic"],
    elements: ["Cream knits", "Linen trousers", "Loafers", "Tote bags", "Soft gold tones", "White button-downs"],
    brands: ["Sezane", "Arket", "Toast", "Margaret Howell", "Massimo Dutti"],
    description: "The sunnier twin of Dark Academia. Same love of literature and learning, but with a Mediterranean warmth — afternoons in Italian gardens rather than midnight libraries.",
    references: ["Call Me by Your Name (2017)", "Normal People", "Greek poetry", "Florence"],
    images: []
  },

  // ── Clean / Minimal ──
  {
    id: "minimalist",
    name: "Minimalist",
    family: "Clean / Minimal",
    tagline: "Less is literally everything",
    tags: ["timeless", "neutral", "intentional"],
    elements: ["Monochrome palette", "Clean silhouettes", "Quality basics", "No logos", "Structured bags", "Simple jewelry"],
    brands: ["COS", "The Row", "Jil Sander", "Everlane", "Uniqlo", "Aritzia"],
    description: "The art of reduction. Minimalist fashion strips away decoration to focus on cut, fabric, and proportion. Every piece earns its place.",
    references: ["Jil Sander", "The Row", "COS", "Japanese minimalism"],
    images: []
  },
  {
    id: "quiet-luxury",
    name: "Quiet Luxury",
    family: "Clean / Minimal",
    tagline: "If you know, you know",
    tags: ["2020s", "stealth wealth", "understated"],
    elements: ["Cashmere everything", "No visible logos", "Neutral palette", "Perfect tailoring", "Loro Piana", "Subtle textures"],
    brands: ["Loro Piana", "The Row", "Brunello Cucinelli", "Khaite", "Toteme", "Max Mara"],
    description: "Also called 'stealth wealth' — the idea that true luxury doesn't need a logo. It's about fabric quality, perfect fit, and the confidence of understatement. Succession made this mainstream.",
    references: ["Succession (HBO)", "Gwyneth Paltrow", "Loro Piana", "The Row"],
    images: []
  },
  {
    id: "old-money",
    name: "Old Money",
    family: "Clean / Minimal",
    tagline: "Generational wealth in a cable-knit sweater",
    tags: ["timeless", "prep-adjacent", "coastal elite"],
    elements: ["Cable knits", "Navy blazers", "Loafers", "Tennis whites", "Pearls", "Boat shoes", "Monogrammed anything"],
    brands: ["Ralph Lauren", "J.Crew", "Sperry", "Barbour", "L.L. Bean", "Lacoste"],
    description: "The aesthetic of inherited wealth and Ivy League traditions. Old Money is preppy's more refined, less try-hard older sibling. Think the Kennedys at Hyannis Port.",
    references: ["The Talented Mr. Ripley (1999)", "Ralph Lauren", "Slim Aarons photography", "JFK & Jackie O"],
    images: []
  },
  {
    id: "clean-girl",
    name: "Clean Girl",
    family: "Clean / Minimal",
    tagline: "Dewy skin and a slicked-back bun",
    tags: ["2020s", "effortless", "glowy"],
    elements: ["Slicked-back hair", "Gold hoops", "Minimal makeup", "Neutral athleisure", "Lip gloss", "Clean skincare"],
    brands: ["Glossier", "Mejuri", "Skims", "Alo Yoga", "Summer Fridays", "Rhode"],
    description: "An aesthetic centered on looking polished with minimal visible effort. Dewy skin, simple gold jewelry, and that just-left-pilates glow.",
    references: ["Hailey Bieber", "Matilda Djerf", "Glossier", "Pilates culture"],
    images: []
  },

  // ── Streetwear / Urban ──
  {
    id: "y2k",
    name: "Y2K",
    family: "Streetwear / Urban",
    tagline: "The future as imagined in 2001",
    tags: ["early 2000s", "shiny", "pop culture"],
    elements: ["Low-rise everything", "Butterfly clips", "Bedazzled", "Tiny sunglasses", "Metallic fabrics", "Platform flip-flops"],
    brands: ["Juicy Couture", "Ed Hardy", "Von Dutch", "Baby Phat", "BCBG", "Steve Madden"],
    description: "Y2K is the early-2000s tech-optimism aesthetic — Paris Hilton's Sidekick, silver everything, and the belief that the future would be fun and sparkly.",
    references: ["Paris Hilton", "Destiny's Child", "Zenon: Girl of the 21st Century", "Bratz dolls"],
    images: []
  },
  {
    id: "techwear",
    name: "Techwear",
    family: "Streetwear / Urban",
    tagline: "Dressed for a cyberpunk apocalypse",
    tags: ["futuristic", "functional", "dark"],
    elements: ["Gore-Tex shells", "Cargo pants", "Utility straps", "All black", "Waterproof everything", "Acronym bags"],
    brands: ["ACRONYM", "Nike ACG", "Arc'teryx Veilance", "Stone Island Shadow Project", "Salomon"],
    description: "Fashion optimized for function in urban environments. Techwear treats clothing like gear — waterproof, modular, and ready for anything. It looks like a video game protagonist.",
    references: ["ACRONYM", "Nike ACG", "Blade Runner", "Ghost in the Shell"],
    images: []
  },
  {
    id: "hypebeast",
    name: "Hypebeast",
    family: "Streetwear / Urban",
    tagline: "Limited edition or nothing",
    tags: ["2010s-now", "hype", "logos"],
    elements: ["Supreme box logo", "Yeezys", "Off-White", "Streetwear collabs", "Sneaker rotation", "Oversized hoodies"],
    brands: ["Supreme", "Off-White", "Nike/Jordan", "Stussy", "Palace", "A Bathing Ape"],
    description: "Built on the culture of limited drops, resale markets, and brand worship. Hypebeast style is about having the thing nobody else can get — and making sure people see it.",
    references: ["Virgil Abloh", "ComplexCon", "StockX", "Kanye West"],
    images: []
  },
  {
    id: "skater",
    name: "Skater",
    family: "Streetwear / Urban",
    tagline: "Thrashed Vans and a board under your arm",
    tags: ["1990s-now", "casual", "SoCal"],
    elements: ["Vans", "Baggy pants", "Graphic tees", "Beanies", "Thrasher magazine", "Worn-in everything"],
    brands: ["Vans", "Dickies", "Santa Cruz", "Thrasher", "Nike SB", "HUF"],
    description: "Born from actual skateboarding culture — functional, comfortable, and deliberately unconcerned with fashion. The authenticity is the point.",
    references: ["Tony Hawk", "Thrasher Magazine", "Supreme (origins)", "Mid90s (2018)"],
    images: []
  },

  // ── Nature / Organic ──
  {
    id: "gorpcore",
    name: "Gorpcore",
    family: "Nature / Organic",
    tagline: "Trail mix as a personality trait",
    tags: ["2020s", "outdoor", "functional"],
    elements: ["Fleece jackets", "Hiking boots", "Nalgene bottles", "Arc'teryx", "Cargo shorts", "Carabiners on everything"],
    brands: ["Arc'teryx", "Salomon", "The North Face", "Patagonia", "Hoka", "Gramicci"],
    description: "Outdoor gear worn as everyday fashion. Gorpcore (GORP = Good Ol' Raisins and Peanuts) is the intersection of REI and runway — practicality made cool.",
    references: ["Salomon shoes", "Arc'teryx", "Patagonia", "The North Face collabs"],
    images: []
  },
  {
    id: "granola",
    name: "Granola",
    family: "Nature / Organic",
    tagline: "Sunrise yoga and reusable everything",
    tags: ["earthy", "sustainable", "wellness"],
    elements: ["Birkenstocks", "Tie-dye", "Linen", "No makeup", "Crystals", "Tote bags", "Earth tones"],
    brands: ["Birkenstock", "Patagonia", "Outdoor Voices", "Girlfriend Collective", "Tevas", "Baggu"],
    description: "The outdoorsy, wellness-oriented, eco-conscious aesthetic. Granola is less about gear and more about lifestyle — farmers markets, van life, and sustainable living.",
    references: ["Patagonia (the ethos)", "Van life culture", "Erewhon", "Outdoor Voices"],
    images: []
  },
  {
    id: "coastal-grandmother",
    name: "Coastal Grandmother",
    family: "Nature / Organic",
    tagline: "Linen pants and a beach house in Maine",
    tags: ["2020s", "relaxed", "refined"],
    elements: ["Linen everything", "Bucket hats", "Striped shirts", "Wicker baskets", "Reading glasses on a chain", "White pants"],
    brands: ["Eileen Fisher", "L.L. Bean", "J.Crew", "Faherty", "Alex Mill", "Le Creuset (the lifestyle)"],
    description: "Coined by TikTok creator Lex Nicoleta — it's the lifestyle aesthetic of a woman who has a beach house, reads Ina Garten cookbooks, and wears linen year-round.",
    references: ["Diane Keaton in Something's Gotta Give", "Ina Garten", "Nancy Meyers films", "Martha's Vineyard"],
    images: []
  },

  // ── Maximalist / Eclectic ──
  {
    id: "indie-sleaze",
    name: "Indie Sleaze",
    family: "Maximalist / Eclectic",
    tagline: "2007 called and wants you at the afterparty",
    tags: ["late 2000s", "messy", "party"],
    elements: ["American Apparel", "Messy eyeliner", "Leather jackets", "Wayfarers", "Flash photography", "Neon accents"],
    brands: ["American Apparel", "Ray-Ban", "Urban Outfitters", "AllSaints", "Cheap Monday"],
    description: "The aesthetic of late-2000s Brooklyn/Shoreditch party culture. Indie Sleaze is deliberately messy, hedonistic, and photographed at 3am with a disposable camera.",
    references: ["The Cobrasnake", "Alexa Chung", "The Strokes", "Skins (UK)"],
    images: []
  },
  {
    id: "camp",
    name: "Camp",
    family: "Maximalist / Eclectic",
    tagline: "It's so bad it's good — no, it's ART",
    tags: ["timeless", "theatrical", "ironic"],
    elements: ["Over-the-top everything", "Irony", "Bold prints", "Feathers", "Sequins", "Dramatic silhouettes"],
    brands: ["Moschino", "Versace", "Gucci (Alessandro Michele era)", "Jean Paul Gaultier", "Jeremy Scott"],
    description: "As Susan Sontag wrote: 'the essence of Camp is its love of the unnatural: of artifice and exaggeration.' Camp is fashion that knows it's being ridiculous and revels in it.",
    references: ["Met Gala 2019", "Susan Sontag's Notes on Camp", "RuPaul", "Moschino"],
    images: []
  },
  {
    id: "barbiecore",
    name: "Barbiecore",
    family: "Maximalist / Eclectic",
    tagline: "Hot pink is a neutral",
    tags: ["2022-23", "pink", "bold"],
    elements: ["Hot pink everything", "Platform heels", "Matching sets", "Plastic accessories", "Bubblegum glam"],
    brands: ["Valentino", "Zara", "ASOS", "Steve Madden", "Skims"],
    description: "Triggered by the Barbie movie marketing machine, Barbiecore is a full commitment to pink — not as a subtle accent, but as an entire worldview.",
    references: ["Barbie (2023)", "Valentino Pink PP", "Margot Robbie press tour", "Zara Barbie collab"],
    images: []
  },
  {
    id: "kitsch",
    name: "Kitsch",
    family: "Maximalist / Eclectic",
    tagline: "Taste is overrated",
    tags: ["timeless", "playful", "lowbrow"],
    elements: ["Novelty prints", "Clashing patterns", "Souvenir aesthetics", "Plastic jewelry", "Ironic graphic tees", "Flamingos"],
    brands: ["Moschino", "Lazy Oaf", "Irregular Choice", "Betsey Johnson", "Lisa Frank (the energy)"],
    description: "Kitsch deliberately embraces what 'good taste' rejects. It's the aesthetic of motel signs, lawn flamingos, and Hawaiian shirts — populist, joyful, and aggressively unhip.",
    references: ["John Waters", "Jeff Koons", "Moschino", "Ugly Christmas sweaters"],
    images: []
  },

  // ── Cultural / Regional ──
  {
    id: "parisian",
    name: "Parisian Chic",
    family: "Cultural / Regional",
    tagline: "Effortless (with enormous effort)",
    tags: ["French", "timeless", "understated"],
    elements: ["Breton stripes", "Red lipstick", "Trench coats", "Ballet flats", "Messy hair", "Little black dresses", "Basket bags"],
    brands: ["Rouje", "Sezane", "Isabel Marant", "A.P.C.", "Celine", "Saint Laurent"],
    description: "The mythologized French girl look — supposedly effortless, always chic. In reality, it's a carefully curated set of classics that project nonchalance.",
    references: ["Jane Birkin", "Jeanne Damas", "Emily in Paris (satirically)", "Rouje"],
    images: []
  },
  {
    id: "japanese-street",
    name: "Japanese Street",
    family: "Cultural / Regional",
    tagline: "Harajuku rules, anything goes",
    tags: ["Tokyo", "eclectic", "subcultural"],
    elements: ["Layering", "Platform shoes", "Mixed prints", "Kawaii accessories", "Decora", "Oversized silhouettes"],
    brands: ["Comme des Garcons", "BAPE", "Undercover", "Sacai", "Issey Miyake", "Kapital"],
    description: "An umbrella for the wildly diverse street fashion of Harajuku and beyond — from Lolita to decora to avant-garde. The unifying principle is fearless self-expression.",
    references: ["FRUiTS magazine", "BAPE", "Comme des Garcons", "Harajuku culture"],
    images: []
  },
  {
    id: "scandi",
    name: "Scandinavian",
    family: "Cultural / Regional",
    tagline: "Hygge but make it fashion",
    tags: ["Nordic", "functional", "cozy-minimal"],
    elements: ["Neutral palette", "Functional outerwear", "Clean lines", "Chunky knits", "White sneakers", "Wool everything"],
    brands: ["COS", "Acne Studios", "Ganni", "& Other Stories", "Arket", "Filippa K"],
    description: "Scandinavian fashion merges minimalism with warmth — designed for dark winters and a culture that values function, quality, and understated beauty.",
    references: ["COS", "Acne Studios", "& Other Stories", "Copenhagen Fashion Week"],
    images: []
  },
  {
    id: "latina-glam",
    name: "Latina Glam",
    family: "Cultural / Regional",
    tagline: "Bold, proud, and turning heads",
    tags: ["cultural", "bold", "celebratory"],
    elements: ["Hoops", "Bold lips", "Body-con silhouettes", "Slicked-back buns", "Nameplate necklaces", "Statement nails"],
    brands: ["Fashion Nova", "Fenty Beauty", "Naked Wolfe", "Oh Polly", "NYX Cosmetics", "BuddyLove"],
    description: "Rooted in Latina culture and identity — it's glamorous, confident, and unapologetic. A celebration of body positivity, bold beauty, and cultural pride.",
    references: ["JLo", "Selena Quintanilla", "Cardi B", "Chola subculture influence"],
    images: []
  },
];

// ── Connections ──
const connections = [
  // Vintage / Retro internal
  { source: "70s-boho", target: "mod", label: "era neighbors" },
  { source: "pin-up", target: "rockabilly", label: "shared roots" },
  { source: "70s-boho", target: "rockabilly", label: "americana thread" },

  // Dark / Edgy internal
  { source: "grunge", target: "punk", label: "DIY rebellion" },
  { source: "goth", target: "punk", label: "post-punk origins" },
  { source: "goth", target: "whimsigoth", label: "softened into" },
  { source: "grunge", target: "emo", label: "evolved into" },
  { source: "punk", target: "emo", label: "emotional branch" },

  // Romantic / Soft internal
  { source: "coquette", target: "balletcore", label: "hyper-feminine" },
  { source: "cottagecore", target: "light-academia", label: "pastoral warmth" },
  { source: "dark-academia", target: "light-academia", label: "lighter twin" },

  // Clean / Minimal internal
  { source: "minimalist", target: "quiet-luxury", label: "elevated basics" },
  { source: "quiet-luxury", target: "old-money", label: "stealth wealth" },
  { source: "clean-girl", target: "minimalist", label: "beauty crossover" },

  // Streetwear / Urban internal
  { source: "y2k", target: "hypebeast", label: "brand obsession" },
  { source: "skater", target: "hypebeast", label: "streetwear roots" },
  { source: "techwear", target: "hypebeast", label: "urban overlap" },

  // Nature / Organic internal
  { source: "gorpcore", target: "granola", label: "outdoor lifestyle" },
  { source: "granola", target: "coastal-grandmother", label: "natural ease" },

  // Maximalist / Eclectic internal
  { source: "camp", target: "kitsch", label: "taste rebellion" },
  { source: "barbiecore", target: "camp", label: "pink maximalism" },
  { source: "indie-sleaze", target: "kitsch", label: "ironic fashion" },

  // Cultural / Regional internal
  { source: "parisian", target: "scandi", label: "European minimal" },

  // ── Cross-family bridges ──
  { source: "dark-academia", target: "goth", label: "dark romanticism" },
  { source: "dark-academia", target: "old-money", label: "prep roots" },
  { source: "cottagecore", target: "granola", label: "back to nature" },
  { source: "cottagecore", target: "70s-boho", label: "earthy feminine" },
  { source: "whimsigoth", target: "coquette", label: "dark vs. light feminine" },
  { source: "grunge", target: "indie-sleaze", label: "messy chic" },
  { source: "grunge", target: "skater", label: "90s casual" },
  { source: "y2k", target: "barbiecore", label: "pop excess" },
  { source: "clean-girl", target: "parisian", label: "effortless polish" },
  { source: "techwear", target: "goth", label: "dark futurism" },
  { source: "old-money", target: "parisian", label: "quiet elegance" },
  { source: "balletcore", target: "light-academia", label: "soft discipline" },
  { source: "punk", target: "japanese-street", label: "subcultural exchange" },
  { source: "mod", target: "parisian", label: "60s cool" },
  { source: "latina-glam", target: "y2k", label: "bold & glossy" },
  { source: "latina-glam", target: "pin-up", label: "glam femininity" },
  { source: "scandi", target: "minimalist", label: "less is more" },
  { source: "scandi", target: "gorpcore", label: "functional dressing" },
  { source: "coastal-grandmother", target: "quiet-luxury", label: "refined ease" },
  { source: "indie-sleaze", target: "y2k", label: "era overlap" },
  { source: "japanese-street", target: "camp", label: "maximalist expression" },
  { source: "70s-boho", target: "granola", label: "hippie lineage" },
  { source: "emo", target: "indie-sleaze", label: "2000s subcultures" },
];
