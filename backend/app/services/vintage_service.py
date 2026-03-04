import json
import logging
import os

log = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
_vintage_data = None
_geojson_data = None


class DataUnavailableError(Exception):
    pass


def _load_vintage_data():
    global _vintage_data
    if _vintage_data is None:
        path = os.path.join(_DATA_DIR, "vintage", "vintage_data.json")
        try:
            with open(path) as f:
                _vintage_data = json.load(f)
        except FileNotFoundError:
            log.error(f"Vintage data file not found: {path}")
            raise DataUnavailableError("Vintage data file not found.")
        except json.JSONDecodeError as e:
            log.error(f"Vintage data file is malformed: {e}")
            raise DataUnavailableError("Vintage data file is malformed.")
    return _vintage_data


def _load_geojson():
    global _geojson_data
    if _geojson_data is None:
        path = os.path.join(_DATA_DIR, "geojson", "wine_regions.geojson")
        try:
            with open(path) as f:
                _geojson_data = json.load(f)
        except FileNotFoundError:
            log.error(f"GeoJSON file not found: {path}")
            raise DataUnavailableError("GeoJSON regions file not found.")
        except json.JSONDecodeError as e:
            log.error(f"GeoJSON file is malformed: {e}")
            raise DataUnavailableError("GeoJSON regions file is malformed.")
    return _geojson_data


def get_year_range():
    data = _load_vintage_data()
    return {
        "min_year": data["metadata"]["year_range"][0],
        "max_year": data["metadata"]["year_range"][1],
    }


def get_year_report(year: int) -> dict:
    """Return a harvest report: winners, strugglers, best pick, and a summary narrative."""
    data = _load_vintage_data()
    year_str = str(year)

    regions = []
    for region_key, region in data["regions"].items():
        vintage = region["vintages"].get(year_str)
        if vintage:
            regions.append({
                "region_key": region_key,
                "display_name": region["display_name"],
                "country": region["country"],
                "wine_style": region["wine_style"],
                "primary_grapes": region["primary_grapes"],
                **vintage,
            })

    if not regions:
        return {"year": year, "winners": [], "strugglers": [], "best_pick": None, "summary": "No vintage data available for this year."}

    # Sort by score
    regions.sort(key=lambda r: r.get("score", 0), reverse=True)

    # Winners: score >= 90 — return ALL qualifying regions, sorted best first
    all_winners = [r for r in regions if r.get("score", 0) >= 90]

    # Strugglers: score < 75 — return ALL qualifying regions, sorted worst first
    all_strugglers = sorted(
        [r for r in regions if 0 < r.get("score", 0) < 75],
        key=lambda r: r.get("score", 0)
    )

    # Best pick: highest scoring region
    best_pick = regions[0] if regions else None

    # Build a short narrative summary
    avg_score = sum(r.get("score", 0) for r in regions if r.get("score", 0) > 0)
    scored = [r for r in regions if r.get("score", 0) > 0]
    avg = avg_score / len(scored) if scored else 0

    if avg >= 90:
        market_tone = f"{year} was an exceptional year across the board — rare conditions aligned in multiple regions simultaneously."
    elif avg >= 85:
        market_tone = f"{year} was a strong vintage overall, with standout performances concentrated in Europe's classic regions."
    elif avg >= 78:
        market_tone = f"{year} was a mixed vintage. Some regions thrived; others faced difficult growing conditions."
    else:
        market_tone = f"{year} was a challenging vintage. Quality was inconsistent and few regions produced exceptional wines."

    top_names = ", ".join(r["display_name"] for r in all_winners[:3]) if all_winners else "none standouts"
    struggler_names = ", ".join(r["display_name"] for r in all_strugglers[:2]) if all_strugglers else "none"

    summary = (
        f"{market_tone} "
        + (f"Best results came from {top_names}" + (f" and {len(all_winners) - 3} more regions" if len(all_winners) > 3 else "") + ". "
           if all_winners else "")
        + (f"Regions that struggled included {struggler_names}" + (f" and {len(all_strugglers) - 2} others" if len(all_strugglers) > 2 else "") + ". "
           if all_strugglers else "")
        + (f"Top recommendation: {best_pick['display_name']} ({best_pick['score']}/100)." if best_pick else "")
    )

    return {
        "year": year,
        "summary": summary,
        "average_score": round(avg, 1),
        "winners": all_winners,
        "total_winners": len(all_winners),
        "strugglers": all_strugglers,
        "total_strugglers": len(all_strugglers),
        "best_pick": best_pick,
        "total_regions": len(scored),
    }


def get_vintage_by_year(year):
    data = _load_vintage_data()
    year_str = str(year)
    results = []

    for region_key, region in data["regions"].items():
        vintage = region["vintages"].get(year_str)
        if vintage:
            results.append({
                "region_key": region_key,
                "display_name": region["display_name"],
                "country": region["country"],
                "wine_style": region["wine_style"],
                "primary_grapes": region["primary_grapes"],
                **vintage,
            })

    return {"year": year, "regions": results}


def get_regions_geojson_with_vintage(year):
    geojson = _load_geojson()
    data = _load_vintage_data()
    year_str = str(year)

    features = []
    for feature in geojson["features"]:
        region_key = feature["properties"]["region_key"]
        new_feature = {
            "type": "Feature",
            "geometry": feature["geometry"],
            "properties": {**feature["properties"]},
        }

        region = data["regions"].get(region_key)
        if region:
            vintage = region["vintages"].get(year_str)
            if vintage:
                new_feature["properties"].update(vintage)
            else:
                new_feature["properties"]["score"] = 0
                new_feature["properties"]["quality_tier"] = "no_data"
                new_feature["properties"]["description"] = "No vintage data available for this year."
        else:
            new_feature["properties"]["score"] = 0
            new_feature["properties"]["quality_tier"] = "no_data"

        features.append(new_feature)

    return {"type": "FeatureCollection", "features": features}
