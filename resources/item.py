from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError
from db import db

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(schema=ItemUpdateSchema)
    @blp.response(status_code=200, schema=ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        NotImplementedError("Updating not implemented yet")

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        NotImplementedError("Deleting not implemented yet")


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(status_code=200, schema=ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @blp.arguments(schema=ItemSchema)
    @blp.response(status_code=201, schema=ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json() (not needed with a blp schema

        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500, message="An error has occurred while inserting "
            )
        return item
