import uuid
from validations.store_validations import valid_create_store, valid_store
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(http_status_code=404, message="store_id not found in stores")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": f"Store {store_id} deleted"}, 201
        except KeyError:
            abort(http_status_code=404, message="Item id was not found")


@blp.route("/store")
class StoreList(MethodView):

    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        if not valid_create_store(store_data):
            abort(http_status_code=422, message="name not found in store request")
        if not valid_store(store_data):
            abort(http_status_code=409, message="this store already exists.")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201
