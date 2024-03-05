from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel
from db import db

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(status_code=200, schema=StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        db.session.delete(store)
        db.session.commit()

        return {"message": "store has been deleted"}, 200


@blp.route("/store")
class StoreList(MethodView):

    @blp.response(status_code=200, schema=StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores

    @blp.arguments(schema=StoreSchema)
    @blp.response(status_code=201, schema=StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(http_status_code=500, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(
                http_status_code=500, message="Something went wrong inserting a store"
            )
        return store
