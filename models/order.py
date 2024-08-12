from datetime import datetime
from db import db


class OrderItemModel(db.Model):
    __tablename="order_items"

    order_id=db.Column(db.Integer,db.ForeignKey("orders.id"),primary_key=True)
    item_id=db.Column(db.Integer,db.ForeignKey("items.id"),primary_key=True)
    quantity=db.Column(db.Integer,nullable=False)
    price_per_unit=db.Column(db.Float,nullable=False)
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),nullable=False)

    order=db.relationship("OrderModel",back_populates="order_items")
    item=db.relationship("ItemModel")
    store=db.relationship("StoreModel")

class OrderModel(db.Model):
    __tablename__="orders"

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    total_price=db.Column(db.Float,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow,nullable=False)

    user=db.relationship("UserModel", backref="orders", lazy="select")
    order_items=db.relationship("OrderItemModel", back_populates="order",lazy="select")

    @property
    def quantity(self):
        return sum(item.quantity for item in self.order_items)
