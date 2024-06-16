from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import OrderModel, OrderProductModel
from flask import render_template, request
import datetime
from schemas import OrderSchema, OrderProductSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Orders", __name__, description="Operations on categories")

@blp.route("/add_to_cart")
class OrderList(MethodView):
    # @blp.response(200, PlainCatSchema(many=True))
    def get(self):
        order = OrderProductModel.query.all()
        order = OrderProductSchema().dump(order, many=True)
        print(order)
        return render_template('cart.html', order=order)

    # @blp.arguments(OrderSchema) #dn make name unique 
    # @blp.response(201, OrderSchema)
    def post(self):
        order_data = request.get_json()
        print(order_data)
        order = OrderModel(buyer_id=7, order_compelete=False, date=datetime.datetime.now(), amount= 0, block_no= 0, street="", city="", country="", postal_code= 0,)
        db.session.add(order)
        db.session.commit()
        print(order.order_id)
        order_product = OrderProductModel(order_id=order.order_id, product_id=order_data["product_id"])
        db.session.add(order_product)
        db.session.commit()
        return{"result": "added"}
