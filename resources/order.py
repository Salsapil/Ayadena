from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import OrderModel, OrderProductModel, ProductModel
from flask import render_template, request, json
import datetime
from schemas import ProductSchema, OrderProductSchema
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
