from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, ItemTagSchema
from models import TagModel, StoreModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db

blp = Blueprint("tags", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required(fresh=True)
    @blp.arguments(schema=TagSchema)
    @blp.response(status_code=201, schema=TagSchema)
    def post(self, tag_data, store_id):

        # if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
        # 	abort(http_status_code=422, message="There is already a tag associated to this store")
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(http_status_code=500, message="A tag with that name already exists")
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message="An error occurred while saving your new tag",
            )

        return tag, 201


@blp.route("/tag")
class TagList(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        return tags


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required(fresh=True)
    @blp.arguments(schema=TagSchema)
    @blp.response(status_code=200, schema=TagSchema)
    def put(self, tag_data, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag:
            tag.name = tag_data["name"]
            tag.store_id = tag_data["store_id"]
        else:
            tag = TagModel(id=tag_id, **tag_data)

        db.session.add(tag)
        db.session.commit()

        return tag

    @jwt_required(fresh=True)
    @blp.response(
        status_code=202,
        description="Deletes a tag if no item is tagged with it",
        example={"message": "Tag has been deleted"},
    )
    @blp.response(
        status_code=404,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):

        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()

            return {"message": "Tag has been deleted"}
        abort(
            http_status_code=400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):

    @jwt_required(fresh=True)
    @blp.response(status_code=201, schema=TagSchema)
    def post(self, tag_id, item_id):

        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message=f"An error occurred while linking tag_id {tag_id} to item_id {item_id}",
            )
        return tag

    @jwt_required(fresh=True)
    @blp.response(status_code=200, schema=ItemTagSchema)
    def delete(self, tag_id, item_id):

        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)

        item.tags.remove(tag)

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message=f"Something occurred while attempting to delete tag_id: {tag_id} from item_id: {item_id}",
            )

        return {"message": f"Tag {tag_id} has been deleted from Item {item_id}"}
