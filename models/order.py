from db import db
from datetime import datetime

class OrderModel(db.Model):
    __tablename__="order"

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    item_id=db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)

    user=db.relationship("UserModel", back_populates="orders")
    item=db.relationship("ItemModel",back_populates="orders")