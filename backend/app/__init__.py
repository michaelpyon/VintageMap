import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


def _read_cors_origins():
    raw = os.environ.get("CORS_ORIGINS", "*")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins if origins else ["*"]


def _compute_data_version():
    data_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    paths = [
        os.path.join(data_root, "vintage", "vintage_data.json"),
        os.path.join(data_root, "geojson", "wine_regions.geojson"),
    ]
    mtimes = [os.path.getmtime(path) for path in paths if os.path.exists(path)]
    latest = max(mtimes, default=0)
    return str(int(latest))


def create_app():
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    app = Flask(__name__, static_folder=static_dir)
    cors_origins = _read_cors_origins()
    CORS(app, resources={r"/api/*": {"origins": cors_origins if cors_origins != ["*"] else "*"}})
    data_version = _compute_data_version()

    from app.routes.vintage import vintage_bp
    from app.routes.regions import regions_bp
    from app.routes.recommend import recommend_bp

    app.register_blueprint(vintage_bp, url_prefix="/api")
    app.register_blueprint(regions_bp, url_prefix="/api")
    app.register_blueprint(recommend_bp, url_prefix="/api")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.before_request
    def maybe_return_not_modified():
        if request.method != "GET":
            return None
        if not request.path.startswith("/api/") or request.path == "/api/health":
            return None
        if request.if_none_match.contains(data_version):
            response = app.response_class(status=304)
            response.set_etag(data_version)
            response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=3600"
            return response
        return None

    @app.after_request
    def add_api_cache_headers(response):
        if request.path == "/api/health":
            response.headers["Cache-Control"] = "no-store"
            return response
        if request.path.startswith("/api/") and request.method == "GET":
            response.set_etag(data_version)
            response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=3600"
            response.headers["X-Data-Version"] = data_version
        return response

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        # Don't catch unmatched /api/* routes — return JSON 404 instead of the SPA.
        if path.startswith("api/"):
            return jsonify({"error": f"Not found: /{path}"}), 404
        if path and os.path.exists(os.path.join(static_dir, path)):
            return send_from_directory(static_dir, path)
        return send_from_directory(static_dir, "index.html")

    return app
