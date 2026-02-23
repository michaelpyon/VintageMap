from flask import Blueprint, jsonify

from app.services.vintage_service import get_vintage_by_year, get_year_range, DataUnavailableError

vintage_bp = Blueprint("vintage", __name__)


@vintage_bp.route("/vintage/<int:year>")
def vintage(year):
    try:
        yr = get_year_range()
        if year < yr["min_year"] or year > yr["max_year"]:
            return jsonify({
                "error": f"Year must be between {yr['min_year']} and {yr['max_year']}."
            }), 400
        return jsonify(get_vintage_by_year(year))
    except DataUnavailableError as e:
        return jsonify({"error": str(e)}), 503


@vintage_bp.route("/year-range")
def year_range():
    try:
        return jsonify(get_year_range())
    except DataUnavailableError as e:
        return jsonify({"error": str(e)}), 503
