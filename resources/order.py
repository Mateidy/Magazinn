from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt , get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import OrderModel , ItemModel
from schemas import OrderSchema , AddItemToOrderSchema

blp=Blueprint("Order",__name__, description="Operations on orders")
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
    def put(self,order_data):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort (401, message="Admin privilege required.")
        try:
            order=OrderModel.query.get_or_404(order_data.get("id"))
            order.status=order_data.get("status",order.status)
            db.session.commit()
            return order
        except Exception as e:
            print(f"Error occured:{e}")
            abort(500, message="An error occurred while updating the order")
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

@blp.route("/order/<int:order_id>/add_item")
class AddItemToOrder(MethodView):
    @jwt_required()
    @blp.arguments(AddItemToOrderSchema)
    @blp.response(200,OrderSchema)
    def post (self,order_data,order_id):
        user_id=get_jwt_identity()
        try:
            order=OrderModel.query.filter_by(id=order_id,user_id=user_id).first()
            if not order:
                abort (404,message=f"Order with ID {order_id} not found for this user.")

            item_id=order_data.get("item_id")
            quantity=order_data.get("quantity",1)

            item=ItemModel.query.get_or_404(item_id)
            if not item:
                abort (404,message=f"Item with ID {item_id} not found .")

            existing_order_item=OrderItemModel.query.filter_by(order_id=order_id,item_id=item_id).first()
            if existing_order_item:
                existing_order_item.quantity+=quantity
            else:
                order_item=OrderItemModel(
                    order_id=order_id,
                    item_id=item_id,
                    quantity=quantity,
                    price_per_unit=item.price,
                    store_id=item.store_id
                )
                db.session.add(order_item)

            order.total_price+=item.price*quantity
            db.session.commit()

            return order
        except SQLAlchemyError as e:
            print (f"Error occurred: {e}")
            abort(500,message="An error occurred while adding the item to the order.")





