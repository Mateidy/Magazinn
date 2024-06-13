from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import OrderModel , ItemModel
from schemas import OrderSchema , OrderUpdateSchema , ItemSchema

blp=Blueprint("Orders", __name__ , description="Operations on orders")

@blp.route("/order/<int:order_id>")
class Order(MethodView):
    jwt_required()
    @blp.response(200,OrderSchema)
    def get(self,order_id):
        order=OrderModel.query.get_or_404(order_id)
        return order

    jwt_required()
    def delete(self,order_id):
        order=OrderModel.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return {"message":"Order deleted."}

    @jwt_required()
    @blp.arguments(OrderUpdateSchema)
    @blp.response(200,OrderSchema)
    def put(self,order_data,order_id):
        order=OrderModel.query.get_or_404(order_id)
        if order:
            if "user_id" in order_data:
                order.user_id = order_data["user_id"]
            if "item_id" in order_data:
                order.item_id=order_data["item_id"]
            if "quantity" in order_data:
                order.quantity=order_data["quantity"]
        else:
            order=OrderModel(id=order_id,**order_data)
            db.session.add(order)
        db.session.commit()
        return order

@blp.route("/order/<int:order_id>/items")
class OrderItems(MethodView):
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post (self,order_id,item_data):
        order=OrderModel.query.get_or_404(order_id)
        new_item=ItemModel(**item_data)
        order.items.append(new_item)

        try:
            db.session.add(order)
            db.session.commit()
        except SQLAlchemyError:
            abort (500,message="An error occured while adding the item to the order.")

        return order




@blp.route("/order")
class OrderList(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200,OrderSchema(many=True))
    def get(self):
        return OrderModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(OrderSchema)
    @blp.response(201,OrderSchema)
    def post(self,order_data):
        order=OrderModel(**order_data)

        try:
            db.session.add(order)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occured while placing the order ")
        return order






