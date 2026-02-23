from app.services.vintage_service import _load_vintage_data

SIGNIFICANCE_PREFERENCES = {
    "birthday": {
        "style_preference": ["sparkling", "red", "white"],
        "prefer_regions": ["champagne", "bordeaux_red", "burgundy_red", "napa_valley"],
        "template": "For a birthday celebration, {wine_style} from {region} is a wonderful choice \u2014 and {year} was {quality_adj} for this region. {detail}",
    },
    "anniversary": {
        "style_preference": ["red", "sparkling", "white"],
        "prefer_regions": ["burgundy_red", "bordeaux_red", "champagne", "tuscany", "piedmont"],
        "template": "To mark this anniversary, {wine_style} from {region} captures depth and elegance \u2014 {year} was {quality_adj} here. {detail}",
    },
    "wedding": {
        "style_preference": ["sparkling", "white", "red"],
        "prefer_regions": ["champagne", "burgundy_white", "napa_valley", "marlborough"],
        "template": "A wedding calls for something joyous \u2014 {wine_style} from {region} in {year} brings {quality_adj} character to the toast. {detail}",
    },
    "graduation": {
        "style_preference": ["sparkling", "white", "red"],
        "prefer_regions": ["champagne", "marlborough", "willamette", "mosel"],
        "template": "Celebrate this achievement with {wine_style} from {region} \u2014 {year} was {quality_adj}, much like the promise ahead. {detail}",
    },
    "retirement": {
        "style_preference": ["red", "fortified", "white"],
        "prefer_regions": ["bordeaux_red", "burgundy_red", "douro", "piedmont", "rhone_north"],
        "template": "A well-aged {wine_style} from {region}'s {quality_adj} {year} vintage \u2014 refined, complex, and worth the wait. {detail}",
    },
    "memorial": {
        "style_preference": ["red", "white", "fortified"],
        "prefer_regions": ["burgundy_red", "bordeaux_red", "rhone_north", "douro"],
        "template": "In remembrance, {wine_style} from {region} \u2014 {year} produced {quality_adj} wines, a fitting tribute. {detail}",
    },
    "other": {
        "style_preference": ["red", "white", "sparkling"],
        "prefer_regions": ["bordeaux_red", "burgundy_red", "champagne", "napa_valley"],
        "template": "For this special occasion, {wine_style} from {region} is an excellent choice \u2014 {year} was {quality_adj} for the region. {detail}",
    },
}

QUALITY_ADJECTIVES = {
    "outstanding": "an exceptional year",
    "excellent": "an excellent year",
    "good": "a good year",
    "average": "a modest but respectable year",
    "poor": "a challenging year, though skilled producers still shone",
    "no_data": "a year we have limited data on",
}

WINE_STYLE_LABELS = {
    "red": "a bold red",
    "white": "an elegant white",
    "sparkling": "a sparkling wine",
    "fortified": "a fortified wine",
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
        "primary": _format(primary, prefs, year),
        "alternatives": [_format(a, prefs, year) for a in alternatives],
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


def _format(candidate, prefs, year):
    quality_adj = QUALITY_ADJECTIVES.get(candidate["quality_tier"], "a notable year")
    wine_style_label = WINE_STYLE_LABELS.get(candidate["wine_style"], "wine")

    text = prefs["template"].format(
        wine_style=wine_style_label,
        region=candidate["region_name"],
        year=year,
        quality_adj=quality_adj,
        detail=candidate["description"],
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
