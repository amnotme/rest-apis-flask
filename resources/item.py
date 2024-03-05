from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from db import db

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @blp.arguments(schema=ItemUpdateSchema)
    @blp.response(status_code=200, schema=ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:

            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()

        return {"message": "Item has been deleted"}, 200


@blp.route("/item")
class ItemList(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @jwt_required(fresh=True)
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
