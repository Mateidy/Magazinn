from datetime import datetime
from db import db


order_items=db.Table("order_items",
                      db.Column("user_id",db.Integer(),db.ForeignKey("orders.id")),
                      db.Column("order_id",db.Integer(),db.ForeignKey("items.id")))

class OrderModel(db.Model):
    __tablename__="orders"

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    total_price=db.Column(db.Float,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow,nullable=False)

    user=db.relationship("UserModel", backref="orders", lazy="select")
    items=db.relationship("ItemModel",secondary=order_items,backref="orders",lazy="select")
