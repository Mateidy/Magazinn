from marshmallow import Schema , fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)

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

class PlainProductSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)

class PlainOrderSchema(Schema):
    id=fields.Int(dump_only=True)
    user_id=fields.Int(required=True)
    item_id=fields.Int(required=True)
    date=fields.DateTime(dump_only=True)
    quantity=fields.Int(required=True)

class OrderSchema(PlainOrderSchema):
    user=fields.Nested(lambda:UserSchema(),dump_only=True)
    item=fields.Nested(ItemSchema(), dump_only=True)

class OrderUpdateSchema(Schema):
    user_id=fields.Int()
    item_id=fields.Int()
    quantity=fields.Int()


class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True)
    orders=fields.List(fields.Nested(PlainOrderSchema(),dump_only=True))


