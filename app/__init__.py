import os

from flask import Flask
from flask_smorest import Api

from app.resources.items import blp_items
from app.resources.stores import blp_store
from app.db import db
import app.models


def create_app(db_url=None):
    app = Flask(__name__)

    from app import views


    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "STORE REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()
    api.register_blueprint(blp_items)
    api.register_blueprint(blp_store)

    return app
