"""Rebuild wine_regions.geojson with larger polygons visible at world zoom level."""
import json, os

OUTPUT = os.path.join(os.path.dirname(__file__), "..", "geojson", "wine_regions.geojson")

def rect(cx, cy, w, h, name, region_key, country, wine_style, grapes):
    """Make a rectangular polygon centered at cx,cy with width w and height h (in degrees)."""
    x0, x1 = cx - w/2, cx + w/2
    y0, y1 = cy - h/2, cy + h/2
    return {
        "type": "Feature",
        "properties": {
            "region_key": region_key,
            "display_name": name,
            "country": country,
            "wine_style": wine_style,
            "primary_grapes": grapes,
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[x0,y0],[x1,y0],[x1,y1],[x0,y1],[x0,y0]]]
        }
    }

features = [
    # France
    rect(-0.5, 44.9,  3.0, 2.0,  "Bordeaux (Red)",    "bordeaux_red",     "France",       "red",       ["Cabernet Sauvignon","Merlot","Cabernet Franc"]),
    rect( 4.8, 47.0,  1.5, 3.5,  "Burgundy (Red)",    "burgundy_red",     "France",       "red",       ["Pinot Noir"]),
    rect( 4.8, 47.0,  1.5, 3.5,  "Burgundy (White)",  "burgundy_white",   "France",       "white",     ["Chardonnay"]),
    rect( 4.0, 49.2,  4.0, 2.0,  "Champagne",         "champagne",        "France",       "sparkling", ["Chardonnay","Pinot Noir","Pinot Meunier"]),
    rect( 4.8, 45.2,  1.2, 1.5,  "Northern Rhone",    "rhone_north",      "France",       "red",       ["Syrah"]),
    rect( 4.8, 44.0,  2.5, 1.5,  "Southern Rhone",    "rhone_south",      "France",       "red",       ["Grenache","Syrah","Mourvedre"]),
    # Italy
    rect( 8.0, 44.7,  2.5, 1.5,  "Piedmont",          "piedmont",         "Italy",        "red",       ["Nebbiolo"]),
    rect(11.2, 43.4,  3.0, 2.0,  "Tuscany",           "tuscany",          "Italy",        "red",       ["Sangiovese"]),
    rect(10.9, 45.5,  2.0, 1.5,  "Veneto",            "veneto",           "Italy",        "red",       ["Corvina","Rondinella"]),
    # Spain
    rect(-2.5, 42.5,  4.0, 1.5,  "Rioja",             "rioja",            "Spain",        "red",       ["Tempranillo","Garnacha"]),
    rect(-3.7, 41.6,  3.5, 1.5,  "Ribera del Duero",  "ribera_del_duero", "Spain",        "red",       ["Tempranillo"]),
    # USA
    rect(-122.4, 38.5, 1.5, 2.0, "Napa Valley",       "napa_valley",      "USA",          "red",       ["Cabernet Sauvignon"]),
    rect(-122.9, 38.4, 1.5, 2.0, "Sonoma",            "sonoma",           "USA",          "red",       ["Pinot Noir","Chardonnay"]),
    rect(-123.2, 45.0, 2.0, 3.0, "Willamette Valley", "willamette",       "USA",          "red",       ["Pinot Noir"]),
    # Southern Hemisphere / Other
    rect( 138.9,-34.5, 2.0, 1.5, "Barossa Valley",    "barossa",          "Australia",    "red",       ["Shiraz"]),
    rect(  7.0, 49.9,  2.5, 1.5, "Mosel",             "mosel",            "Germany",      "white",     ["Riesling"]),
    rect( -7.5, 41.2,  3.0, 2.0, "Douro",             "douro",            "Portugal",     "fortified", ["Touriga Nacional","Touriga Franca"]),
    rect(-68.5,-33.5,  3.0, 3.0, "Mendoza",           "mendoza",          "Argentina",    "red",       ["Malbec"]),
    rect( 18.8,-33.9,  2.0, 1.5, "Stellenbosch",      "stellenbosch",     "South Africa", "red",       ["Cabernet Sauvignon","Pinotage"]),
    rect(173.8,-41.5,  3.0, 2.0, "Marlborough",       "marlborough",      "New Zealand",  "white",     ["Sauvignon Blanc"]),
]

geojson = {"type": "FeatureCollection", "features": features}

with open(OUTPUT, "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Wrote {len(features)} features to {OUTPUT}")
for feat in features:
    p = feat["properties"]
    coords = feat["geometry"]["coordinates"][0]
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    print(f"  {p['region_key']:20s} | lng {min(xs):.1f}–{max(xs):.1f} | lat {min(ys):.1f}–{max(ys):.1f}")
