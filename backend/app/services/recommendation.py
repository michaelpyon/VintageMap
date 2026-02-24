from app.services.vintage_service import _load_vintage_data

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


def _format(candidate, prefs, year, is_primary=False):
    quality_phrase = QUALITY_PHRASES.get(candidate["quality_tier"], "a notable year")
    wine_style_label = WINE_STYLE_LABELS.get(candidate["wine_style"], "wine")
    detail = candidate["description"]

    if is_primary:
        text = prefs["primary_template"].format(
            wine_style_label=wine_style_label,
            region=candidate["region_name"],
            year=year,
            quality_phrase=quality_phrase,
            detail=detail,
        )
    else:
        # Alternatives: purely about the wine — no occasion framing, no repeated intro
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
