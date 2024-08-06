from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import OrderModel , ItemModel
from schemas import OrderSchema , AddItemToOrderSchema

blp=Blueprint("Order",__name__, description="Operations on orders")


@blp.route("/order/<int:order_id>")
class Order(MethodView):
    @jwt_required()
    @blp.response(200,OrderSchema)

    def get(self,order_id):
        order=OrderModel.query.get_or_404(order_id)
        return order

    @jwt_required()
    def delete(self,order_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        try:
            order=OrderModel.query.get_or_404(order_id)
            db.session.delete(order)
            db.session.commit()
            return {"message":"Order deleted."}
        except Exception as e:
            print(f"Error occured:{e}")
            abort(500, message="An error occurred while deleting the order")

@blp.route("/order")
class OrderList(MethodView):
    @jwt_required()
    @blp.response(200,OrderSchema(many=True))

    def get(self):
        orders=OrderModel.query.all()
        return orders

    @jwt_required()
    @blp.arguments(OrderSchema)
    @blp.response(200,OrderSchema)
    def put(self,order_data,order_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort (401, message="Admin privilege required.")
        try:
            order=OrderModel.query.get_or_404(order_id)
            order.status=order_data.get("status",order.status)
            db.session.commit()
            return order
        except Exception as e:
            print(f"Error occured:{e}")
            abort(500, message="An error occurred while updating the order")

@blp.route("/order/<int:order_id>/add_item")
class OrderItemAdd(MethodView):

    @blp.arguments(AddItemToOrderSchema, location='json')
    @blp.response(200,OrderSchema)
    def post(self,order_data,order_id):
        try:
            order=OrderModel.query.get(order_id)
            if not order:
                order=OrderModel(id=order_id)
                db.session.add(order)
                db.session.commit()

            item_id=order_data.get("item_id")
            quantity=order_data.get("quantity",1)

            item=ItemModel.query.get_or_404(item_id)
            if not item:
                abort(404, message=f"Item with id {item_id} not found")

            existing_order_item=next((oi for oi in order.items if oi.id==item_id), None)
            if existing_order_item:
                existing_order_item.quantity+=quantity
            else:
                order.items.append(item)

            total_price=sum(item.price*oi.quantity for oi in order.items)
            order.total_price=total_price

            db.session.commit()

            return order
        except SQLAlchemyError as e:
            print (f"Error occured:{e}")
            abort(500,message="An error occurred while adding the item in order")
