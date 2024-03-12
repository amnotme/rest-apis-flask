from flask import Flask, jsonify
from flask_smorest import Api
from config.config import Config
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from db import db
from blocklist import BLOCKLIST
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


def create_app(db_url=None):
    app = Flask(__name__)

    _configure_app(app=app, db_url=db_url)
    _create_databases(app=app)
    _configure_migration(app=app, db=db)
    _register_blueprints(app=app)
    _configure_jwt(app=app)

    return app


def _configure_app(app, db_url):
    app.config.from_object(Config(db_url=db_url))


def _register_blueprints(app):
    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)


def _create_databases(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()


def _configure_migration(app, db):
    migrate = Migrate(app, db=db)


def _configure_jwt(app):
    jwt = JWTManager(app)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_block_list(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error": "authorization required",
                }
            ),
            401,
        )
