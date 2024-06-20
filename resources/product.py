from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from flask import render_template
from models import ProductModel, SellerModel
from schemas import ProductSchema, PlainProductSchema, ProductUpdateSchema, PlainSellerSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Products", __name__, description="Operations on users")

@blp.route("/product")
class ProductList(MethodView):
    # @blp.response(200, PlainProductSchema(many=True))
    def get(self):
        seller_id = 3
        seller_data = SellerModel.query.get_or_404(seller_id)
        seller_data = PlainSellerSchema().dump(seller_data)
        product = ProductModel.query.filter_by(seller_id=seller_id).all()
        product = ProductSchema().dump(product, many=True)
        return render_template('seller_page.html', product=product, seller_data=seller_data)

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        product = ProductModel(**product_data)
        try:
            db.session.add(product)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred creating the product.")

        return product


@blp.route("/product/<int:product_id>") #int to all
class Product(MethodView):
    @blp.response(200, PlainProductSchema)
    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "deleted"}

    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, PlainProductSchema)
    def put(self, product_data, product_id, update_column=None):
        product = ProductModel.query.get_or_404(product_id)

        if product:
            if update_column:
                for key, value in product_data.items():
                    if key == update_column:
                        setattr(product, key, value)
            else:
                product.name = product_data.get("name", product.name)
                product.description = product_data.get("description", product.description)
                product.price = product_data.get("price", product.price)
                product.amount = product_data.get("amount", product.amount)
                product.image = product_data.get("image", product.image)
                # add product.seller_id

            try:
                db.session.commit()
                return product
            except IntegrityError:
                db.session.rollback()
                abort(400, message="Update failed due to integrity constraint violation.")
        else:
            abort(404, message="Product not found.")
