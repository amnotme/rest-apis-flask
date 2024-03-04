from flask import Flask
from flask_smorest import Api
from config.config import Config
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from db import db
import models


def create_app(db_url=None):
    app = Flask(__name__)
    app.config.from_object(Config(db_url=db_url))
    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
