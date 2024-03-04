import uuid
from validations.item_validations import (
    valid_create_item,
    valid_update_item,
    valid_item_for_store,
)
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(http_status_code=404, message="item_id not found in items")

    def put(self, item_id):
        item_data = request.get_json()
        if not valid_update_item(item_data):
            abort(
                http_status_code=422,
                message="price, or name not found in item request",
            )
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(http_status_code=404, message="item id not found in item request")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"Item {item_id} deleted"}, 201
        except KeyError:
            abort(http_status_code=404, message="Item id was not found")


@blp.route("/item")
class ItemList(MethodView):

    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()

        if not valid_create_item(item_data):
            abort(
                http_status_code=422,
                message="store_id, price, or name not found in item request",
            )
        if item_data["store_id"] not in stores:
            abort(http_status_code=404, message="store_id not found in item request")
        if not valid_item_for_store(item_data):
            abort(
                http_status_code=409,
                message="this item already exists in this store",
            )
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
