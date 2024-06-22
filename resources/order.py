from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import OrderModel, OrderProductModel, ProductModel, PaymentModel, UserModel
from flask import render_template, request, json, jsonify
import datetime
from schemas import ProductSchema, OrderSchema, PlainPaymentSchema, OrderProductSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Orders", __name__, description="Operations on categories")

@blp.route("/add_to_cart")
class OrderList(MethodView):
    # @blp.response(200, PlainCatSchema(many=True))
    def get(self):
        buyer_id = 7
        order = OrderModel.query.filter_by(buyer_id=buyer_id, order_compelete=False).first()

        if not order:
            return render_template('cart.html', order=[])

        order_products = OrderProductModel.query.filter_by(order_id=order.order_id).all()

        product_ids = [op.product_id for op in order_products]
        products = ProductModel.query.filter(ProductModel.product_id.in_(product_ids)).all()
        
        products_data = ProductSchema(many=True).dump(products)

        return render_template('cart.html', order=products_data)

    # @blp.arguments(OrderSchema) #dn make name unique 
    # @blp.response(201, OrderSchema)
    def post(self):
        order_data = request.get_json()
        buyer_id = 7
        product_id = order_data.get("product_id")

        product = ProductModel.query.get(product_id)

        if not product:
            return {"error": "Product not found"}, 404

        order = OrderModel.query.filter_by(buyer_id=buyer_id, order_compelete=False).first()

        if not order:
            order = OrderModel(
                buyer_id=buyer_id,
                order_compelete=False,
                date=datetime.datetime.now(),
                amount=0,
                block_no=0,
                street="",
                city="",
                country="",
                postal_code=0,
            )
            db.session.add(order)
            db.session.commit()

        order_product = OrderProductModel(order_id=order.order_id, product_id=product_id)
        db.session.add(order_product)
        db.session.commit()

        response_data = {
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }

        return json.dumps(response_data), 200, {'ContentType': 'application/json'}

@blp.route("/remove_from_cart", methods=["DELETE"])
class RemoveFromCart(MethodView):
    def delete(self):
        order_data = request.get_json()
        product_id = order_data.get("product_id")
        buyer_id = 7

        # Find the current incomplete order
        order = OrderModel.query.filter_by(buyer_id=buyer_id, order_compelete=False).first()
        if not order:
            return {"error": "Order not found"}, 404

        # Find the order product record to delete
        order_product = OrderProductModel.query.filter_by(order_id=order.order_id, product_id=product_id).first()
        if not order_product:
            return {"error": "Product not found in order"}, 404

        # Delete the order product record
        db.session.delete(order_product)
        db.session.commit()

        return {"message": "Product removed from order"}, 200

@blp.route("/update_order", methods=["PUT"])
class UpdateOrder(MethodView):
    def put(self):
        order_data = request.get_json()
        buyer_id = 7
        order = OrderModel.query.filter_by(buyer_id=buyer_id, order_compelete=False).first()
        order_id = order.order_id

        order = OrderModel.query.get(order_id)
        if not order:
            return {"error": "Order not found"}, 404

        try:
            order.block_no = order_data.get("block_no", order.block_no)
            order.street = order_data.get("street", order.street)
            order.city = order_data.get("city", order.city)
            order.country = order_data.get("country", order.country)
            order.postal_code = order_data.get("postal_code", order.postal_code)
            order.amount = order_data.get("amount", order.amount)

            db.session.commit()

            response_data = OrderSchema().dump(order)
            return json.dumps(response_data), 200, {'ContentType': 'application/json'}
        except (SQLAlchemyError, IntegrityError) as e:
            db.session.rollback()
            return {"error": str(e)}, 400

@blp.route("/insert_payment", methods=["POST"])
class InsertPayment(MethodView):
    def post(self):
        payment_data = request.get_json()
        buyer_id = 7
        order = OrderModel.query.filter_by(buyer_id=buyer_id, order_compelete=False).first()
        order_id = order.order_id
        try:
            new_payment = PaymentModel(
                date=datetime.datetime.now(),
                amount=0,
                card_name=payment_data.get("card_name"),
                card_number=payment_data.get("card_number"),
                exp_month=payment_data.get("exp_month"),
                exp_year=payment_data.get("exp_year"),
                cvv=payment_data.get("cvv"),
                order_id=order_id
            )
            print(new_payment)
            
            db.session.add(new_payment)
            db.session.commit()
            
            if new_payment.order_id == order_id:
                order.order_compelete = True
                db.session.commit()

            response_data = PlainPaymentSchema().dump(new_payment)
            return json.dumps(response_data), 201, {'ContentType': 'application/json'}
        except (SQLAlchemyError, IntegrityError) as e:
            db.session.rollback()
            return {"error": str(e)}, 400

@blp.route("/checkout", methods=["GET"])
def checkout():
    buyer_id = 7
    order = OrderModel.query.filter_by(buyer_id=buyer_id, order_compelete=False).first()
    order_id = order.order_id
    return render_template("checkout.html", order_id=order_id)

# final
@blp.route('/admin_orders', methods=['GET'])
def get_orders():
    orders = db.session.query(OrderModel, UserModel).join(UserModel, OrderModel.buyer_id == UserModel.user_id).all()
    orders_list = [
        {
            'order_id': order.OrderModel.order_id,
            'date': order.OrderModel.date.strftime("%Y-%m-%d"),
            'username': order.UserModel.username
        } for order in orders
    ]
    return jsonify(orders_list)

@blp.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = OrderModel.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'}), 200
    return jsonify({'message': 'Order not found'}), 404
