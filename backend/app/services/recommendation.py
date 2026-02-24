from app.services.vintage_service import _load_vintage_data

# ── Rich Vintage Notes for key region+year combos ────────────────
VINTAGE_NOTES = {
    ("bordeaux_red", 1982): "A transformative year that put Bordeaux on the modern map. Deep, concentrated, opulent fruit with 40+ years of aging potential. Most bottles are now at glorious peak, showing truffle, tobacco, and dried roses over a backbone of sweet cassis.",
    ("bordeaux_red", 1990): "Generous, sun-kissed, and immediately charming from release. The Right Bank excelled with plush Merlot. Now mature, showing leather, cedar, and fig compote. Drink soon for maximum pleasure.",
    ("bordeaux_red", 2000): "The Millennium vintage. A perfect growing season produced wines of extraordinary structure and depth. Still drinking beautifully, especially Saint-Emilion and Pomerol, with decades of life ahead.",
    ("bordeaux_red", 2005): "Powerful, tannic, and built for the long haul. A hot summer concentrated everything. The best Cabernet-dominant Left Bank wines are just entering their prime, with blackcurrant, graphite, and violets.",
    ("bordeaux_red", 2009): "Hedonistic and generous. Warm conditions produced rich, low-acid wines that seduced early but are aging gracefully. Expect dark chocolate, ripe plum, and warm spice.",
    ("bordeaux_red", 2010): "The intellectual counterpart to 2009. Cooler finish brought acid and structure. Extraordinary aging potential. Still youthful, with intense cassis, iron, and fresh herbs.",
    ("bordeaux_red", 2015): "A return-to-form vintage after a tricky decade. Balanced, elegant, and approachable young. Silky tannins, red and black fruit in harmony, with floral lift.",
    ("bordeaux_red", 2016): "Widely hailed as the vintage of the decade. A dry, warm summer followed by perfectly timed September rain. Classic structure with modern polish. Cabernet Sauvignon excelled.",
    ("burgundy_red", 1990): "A hot, early harvest produced deeply colored Pinot Noir of unusual richness. The best are now at peak, showing wild strawberry, forest floor, and a haunting smoky finish.",
    ("burgundy_red", 2005): "A great year across all appellations. Balanced acidity and ripe fruit. The Cote de Nuits produced wines of crystalline purity. Now entering their prime drinking window.",
    ("burgundy_red", 2010): "Widely considered one of Burgundy's greatest modern vintages. Pinot Noir of rare elegance, with pure red fruit, mineral tension, and laser-focused acidity wrapped in silky tannins.",
    ("burgundy_red", 2015): "A warm vintage that produced generous, fruit-forward Burgundy. More accessible than 2010 but with real depth. Drink now through 2035 for the top crus.",
    ("napa_valley", 2013): "The year Napa delivered near-perfect conditions. A long, even growing season produced concentrated but balanced Cabernet Sauvignon. Drinking perfectly now, with blackberry, mocha, and sage.",
    ("napa_valley", 2016): "Another benchmark Napa vintage. Moderate temperatures preserved freshness while building intensity. Look for cassis, graphite, and dried herb notes.",
    ("napa_valley", 2019): "A cooler vintage by Napa standards that produced wines of remarkable finesse. Lower alcohol, bright acidity, and complex aromatics. One for the cellar.",
    ("tuscany", 1997): "Tuscany's sun-drenched masterpiece. Brunello di Montalcino from this year remains one of Italy's greatest modern wines, with dried cherry, leather, and balsamic depth.",
    ("tuscany", 2010): "A classic cool-vintage Sangiovese. Bright acidity, fine tannins, and aromatic complexity. Brunello and Chianti Classico Riserva are drinking superbly now.",
    ("champagne", 2008): "A champagne vintage that changed the conversation. Razor-sharp acidity, extraordinary minerality, and tiny, persistent bubbles. The wine world still talks about it.",
    ("champagne", 2002): "One of the great Champagne vintages. Rich and toasty, with brioche, hazelnut, and citrus zest. Prestige cuvees from this year are legendary.",
    ("piedmont", 1990): "A legendary Barolo vintage. Hot, dry conditions produced powerful, concentrated Nebbiolo with exceptional aging potential. Now showing tar, roses, dried herbs, and sweet spice.",
    ("piedmont", 2010): "One of the finest modern Barolo vintages. A cool growing season produced wines of remarkable elegance and transparency. Pure red cherry, rose petal, and mineral intensity.",
    ("rhone_north", 2010): "A stunning year for Syrah. Cool conditions preserved acidity while delivering deep color and intense aromatics. Hermitage and Cote-Rotie produced wines for the ages.",
    ("rhone_south", 2007): "A benchmark year for Chateauneuf-du-Pape. Warm but not excessive, producing rich Grenache-based blends with garrigue, dark fruit, and spice.",
    ("rioja", 2001): "One of the great modern Rioja vintages. Traditional producers made wines of exceptional balance. Now showing dried cherry, vanilla, tobacco, and coconut from American oak aging.",
    ("mosel", 2019): "An outstanding Riesling vintage. Perfect balance of ripeness and acidity. Both dry and sweet styles excelled, with peach, slate, and petrol-tinged minerality.",
}

SIGNIFICANCE_PREFERENCES = {
    "birthday": {
        "style_preference": ["sparkling", "red", "white"],
        "prefer_regions": ["champagne", "bordeaux_red", "burgundy_red", "napa_valley"],
        # {wine_style_label}, {region}, {year}, {quality_phrase}, {detail}
        "primary_template": "For a birthday celebration, {wine_style_label} from {region} is a wonderful choice. {year} was {quality_phrase}. {detail}",
    },
    "anniversary": {
        "style_preference": ["red", "sparkling", "white"],
        "prefer_regions": ["burgundy_red", "bordeaux_red", "champagne", "tuscany", "piedmont"],
        "primary_template": "To mark this anniversary, {wine_style_label} from {region} captures depth and elegance. {year} was {quality_phrase} here. {detail}",
    },
    "wedding": {
        "style_preference": ["sparkling", "white", "red"],
        "prefer_regions": ["champagne", "burgundy_white", "napa_valley", "marlborough"],
        "primary_template": "A wedding calls for something joyous — {wine_style_label} from {region} is a natural choice. {year} was {quality_phrase}. {detail}",
    },
    "graduation": {
        "style_preference": ["sparkling", "white", "red"],
        "prefer_regions": ["champagne", "marlborough", "willamette", "mosel"],
        "primary_template": "Celebrate this achievement with {wine_style_label} from {region}. {year} was {quality_phrase}, much like the promise ahead. {detail}",
    },
    "retirement": {
        "style_preference": ["red", "fortified", "white"],
        "prefer_regions": ["bordeaux_red", "burgundy_red", "douro", "piedmont", "rhone_north"],
        "primary_template": "A well-aged {wine_style_label} from {region} — the {year} is {quality_phrase}, refined and worth every year of cellaring. {detail}",
    },
    "memorial": {
        "style_preference": ["red", "white", "fortified"],
        "prefer_regions": ["burgundy_red", "bordeaux_red", "rhone_north", "douro"],
        "primary_template": "In remembrance, {wine_style_label} from {region}. {year} produced {quality_phrase} wines — a fitting tribute. {detail}",
    },
    "other": {
        "style_preference": ["red", "white", "sparkling"],
        "prefer_regions": ["bordeaux_red", "burgundy_red", "champagne", "napa_valley"],
        "primary_template": "For this special occasion, {wine_style_label} from {region} is an excellent choice. {year} was {quality_phrase} for the region. {detail}",
    },
}

QUALITY_PHRASES = {
    "outstanding": "exceptional",
    "excellent": "excellent",
    "good": "a good year",
    "average": "a modest but respectable year",
    "poor": "a challenging year — though skilled producers still shone",
    "no_data": "a year with limited records",
}

# For alternatives — region-centric, no occasion framing
# {region}, {year}, {quality_phrase}, {detail}, {wine_style_label}
ALTERNATIVE_TEMPLATE = "{detail} {year} was {quality_phrase} for {region}."

WINE_STYLE_LABELS = {
    "red": "red wine",
    "white": "white wine",
    "sparkling": "sparkling wine",
    "fortified": "fortified wine",
    "rosé": "rosé",
}


def recommend(year, significance):
    data = _load_vintage_data()
    prefs = SIGNIFICANCE_PREFERENCES.get(significance, SIGNIFICANCE_PREFERENCES["other"])
    year_str = str(year)

    candidates = []
    for region_key, region in data["regions"].items():
        vintage = region["vintages"].get(year_str)
        if not vintage:
            continue
        candidates.append({
            "region_key": region_key,
            "region_name": region["display_name"],
            "country": region["country"],
            "wine_style": region["wine_style"],
            "grapes": region["primary_grapes"],
            "score": vintage["score"],
            "quality_tier": vintage["quality_tier"],
            "description": vintage["description"],
            "drinking_window": vintage.get("drinking_window", "unknown"),
            "notable_wines": vintage.get("notable_wines", []),
        })

    for c in candidates:
        c["rec_score"] = _compute_score(c, prefs)

    candidates.sort(key=lambda c: c["rec_score"], reverse=True)

    primary = candidates[0] if candidates else None
    alternatives = candidates[1:4] if len(candidates) > 1 else []

    if not primary:
        return {
            "year": year,
            "significance": significance,
            "primary": None,
            "alternatives": [],
            "message": f"We don't have vintage data for {year}. Try a year between {data['metadata']['year_range'][0]} and {data['metadata']['year_range'][1]}.",
        }

    return {
        "year": year,
        "significance": significance,
        "primary": _format(primary, prefs, year, is_primary=True),
        "alternatives": [_format(a, prefs, year, is_primary=False) for a in alternatives],
    }


def _compute_score(candidate, prefs):
    score = 0.0
    score += candidate["score"] * 0.5

    style = candidate["wine_style"]
    if style in prefs["style_preference"]:
        rank = prefs["style_preference"].index(style)
        score += (30 - rank * 10)

    if candidate["region_key"] in prefs["prefer_regions"]:
        rank = prefs["prefer_regions"].index(candidate["region_key"])
        score += max(20 - rank * 5, 5)

    return score


def _build_detail(candidate, year):
    """Build a rich, specific detail string. Prefer curated VINTAGE_NOTES, fall back to score-based text."""
    region_key = candidate["region_key"]
    note_key = (region_key, year)

    if note_key in VINTAGE_NOTES:
        return VINTAGE_NOTES[note_key]

    # Score-based fallback with specificity
    score = candidate["score"]
    region = candidate["region_name"]
    dw = candidate.get("drinking_window", "unknown")

    # Drinking window context
    dw_text = {
        "young": "Still youthful with primary fruit character.",
        "at_peak": "Now at its peak drinking window.",
        "mature": "Fully mature, showing developed secondary aromas.",
        "past_peak": "Past its prime, though well-stored bottles may still show character.",
        "cellaring": "Still needs time in the cellar to reach its potential.",
    }.get(dw, "")

    if score >= 95:
        return f"An exceptional year for {region}. The conditions aligned to produce wines of rare concentration and complexity. {dw_text}"
    elif score >= 90:
        return f"A standout vintage for {region}, with wines showing depth, balance, and aging potential. {dw_text}"
    elif score >= 85:
        return f"A very good year in {region}. Well-made wines with character and regional typicity. {dw_text}"
    elif score >= 80:
        return f"A solid vintage for {region}. The wines show clean fruit and honest expression, if not the intensity of the best years. {dw_text}"
    elif score >= 75:
        return f"A mixed vintage in {region}. Careful producers still made appealing wines, though selection matters. {dw_text}"
    else:
        return f"A challenging year in {region}. Difficult growing conditions tested even the best producers, though some managed to craft wines of surprising quality. {dw_text}"


def _format(candidate, prefs, year, is_primary=False):
    quality_phrase = QUALITY_PHRASES.get(candidate["quality_tier"], "a notable year")
    wine_style_label = WINE_STYLE_LABELS.get(candidate["wine_style"], "wine")
    detail = _build_detail(candidate, year)

    if is_primary:
        text = prefs["primary_template"].format(
            wine_style_label=wine_style_label,
            region=candidate["region_name"],
            year=year,
            quality_phrase=quality_phrase,
            detail=detail,
        )
    else:
        text = ALTERNATIVE_TEMPLATE.format(
            region=candidate["region_name"],
            year=year,
            quality_phrase=quality_phrase,
            detail=detail,
        )

    suggestion = ""
    if candidate["notable_wines"]:
        names = ", ".join(candidate["notable_wines"][:3])
        suggestion = f"Look for: {names}."

    return {
        "region_key": candidate["region_key"],
        "region_name": candidate["region_name"],
        "country": candidate["country"],
        "wine_style": candidate["wine_style"],
        "score": candidate["score"],
        "quality_tier": candidate["quality_tier"],
        "grapes": candidate["grapes"],
        "notable_wines": candidate["notable_wines"],
        "drinking_window": candidate["drinking_window"],
        "recommendation_text": text,
        "suggestion": suggestion,
    }
