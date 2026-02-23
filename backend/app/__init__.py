from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.vintage import vintage_bp
    from app.routes.regions import regions_bp
    from app.routes.recommend import recommend_bp

    app.register_blueprint(vintage_bp, url_prefix="/api")
    app.register_blueprint(regions_bp, url_prefix="/api")
    app.register_blueprint(recommend_bp, url_prefix="/api")

    return app
