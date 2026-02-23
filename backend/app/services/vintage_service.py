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
