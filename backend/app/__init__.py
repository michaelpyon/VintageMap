import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS


def create_app():
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    app = Flask(__name__, static_folder=static_dir)
    CORS(app)

    from app.routes.vintage import vintage_bp
    from app.routes.regions import regions_bp
    from app.routes.recommend import recommend_bp

    app.register_blueprint(vintage_bp, url_prefix="/api")
    app.register_blueprint(regions_bp, url_prefix="/api")
    app.register_blueprint(recommend_bp, url_prefix="/api")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(static_dir, path)):
            return send_from_directory(static_dir, path)
        return send_from_directory(static_dir, "index.html")

    return app
