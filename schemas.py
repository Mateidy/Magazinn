from marshmallow import Schema , fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)

class AddItemToOrderSchema(Schema):
    user_id=fields.Int(required=True)
    item_id = fields.Int(required=True)
    quantity = fields.Int(missing=1)

class PlainStoreSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)

class PlainTagSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()

class ItemUpdateSchema(Schema):
    name=fields.Str()
    price=fields.Float()
    store_id=fields.Int()

class ItemSchema(PlainItemSchema):
    store_id=fields.Int(required=True,load_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()) , dump_only=True)
class StoreSchema(PlainStoreSchema):
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id=fields.Int(load_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)

class TagAndItemSchema(Schema):
    message=fields.Str()
    item=fields.Nested(ItemSchema)
    tag=fields.Nested(TagSchema)

class OrderSchema(Schema):
    id=fields.Int(dump_only=True)
    user_id=fields.Int(dump_only=True)
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    total_price=fields.Float(dump_only=True)
    quantity=fields.Int(dump_only=True)
    created_at=fields.Date(dump_only=True)

class RoleSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True)
    roles=fields.List(fields.Nested(RoleSchema))






