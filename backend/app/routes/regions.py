from flask import Blueprint, jsonify

from app.services.vintage_service import get_regions_geojson_with_vintage, get_year_range, DataUnavailableError

regions_bp = Blueprint("regions", __name__)


@regions_bp.route("/regions/<int:year>")
def regions_with_vintage(year):
    try:
        yr = get_year_range()
        if year < yr["min_year"] or year > yr["max_year"]:
            return jsonify({
                "error": f"Year must be between {yr['min_year']} and {yr['max_year']}."
            }), 400
        return jsonify(get_regions_geojson_with_vintage(year))
    except DataUnavailableError as e:
        return jsonify({"error": str(e)}), 503
