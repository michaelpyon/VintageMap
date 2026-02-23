from flask import Blueprint, jsonify, request

from app.services.recommendation import recommend
from app.services.vintage_service import get_year_range, DataUnavailableError

recommend_bp = Blueprint("recommend", __name__)

VALID_SIGNIFICANCES = [
    "birthday", "anniversary", "wedding",
    "graduation", "retirement", "memorial", "other",
]


@recommend_bp.route("/recommend")
def get_recommendation():
    year = request.args.get("year", type=int)
    significance = request.args.get("significance", "other")

    if not year:
        return jsonify({"error": "year parameter is required."}), 400

    yr = get_year_range()
    if year < yr["min_year"] or year > yr["max_year"]:
        return jsonify({
            "error": f"Year must be between {yr['min_year']} and {yr['max_year']}."
        }), 400

    if significance not in VALID_SIGNIFICANCES:
        significance = "other"

    try:
        return jsonify(recommend(year, significance))
    except DataUnavailableError as e:
        return jsonify({"error": str(e)}), 503
