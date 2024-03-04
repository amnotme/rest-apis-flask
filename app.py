from flask import Flask
from flask_smorest import Api
from config.config import Config

from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
