from marshmallow import Schema, fields


class BaseItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class BaseStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(BaseItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(BaseStoreSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(BaseStoreSchema):
    items = fields.List(fields.Nested(BaseItemSchema()), dump_only=True)
