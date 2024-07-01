from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify
from db import db
from flask import render_template, session
from models import ProductModel, SellerModel, ProductCategoryModel
from schemas import ProductSchema, PlainProductSchema, ProductUpdateSchema, PlainSellerSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Products", __name__, description="Operations on users")

@blp.route("/product")
class ProductList(MethodView):
    # @blp.response(200, PlainProductSchema(many=True))
    def get(self):
        # seller_id = 3
        seller_id = session.get('identity_id')
        seller_data = SellerModel.query.get_or_404(seller_id)
        seller_data = PlainSellerSchema().dump(seller_data)
        product = ProductModel.query.filter_by(seller_id=seller_id).all()
        product = ProductSchema().dump(product, many=True)
        return render_template('seller_page.html', product=product, seller_data=seller_data)

    # @blp.arguments(ProductSchema)
    # @blp.response(201, ProductSchema)
    def post(self):
        product_data = request.get_json()
        print(product_data)
        product = ProductModel(
            seller_id = session.get('identity_id'),
            cat_id = product_data.get("cat_id"),
            name = product_data.get("name"),
            description = product_data.get("description"),
            price = product_data.get("price"),
            amount = 0,
            image = product_data.get("image")
        )
        try:
            db.session.add(product)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred creating the product.")

        return jsonify(product_data)


@blp.route("/delete_product", methods=["DELETE"])
class Product(MethodView):
    # @blp.response(200, PlainProductSchema)
    def delete(self):
        product_id = request.get_json()
        print(product_id)
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {"message": "deleted"}

    # @blp.arguments(ProductUpdateSchema)
    # @blp.response(200, PlainProductSchema)
@blp.route("/update_product", methods=["PUT"])
class ProductUpdate(MethodView):
    def put(self, update_column=None):
        product_data = request.get_json()
        print(product_data)
        product_id = product_data.get("product_id")
        print(product_id)
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

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                abort(400, message="Update failed due to integrity constraint violation.")

            # Convert the updated product instance to a dictionary using the schema
            product_schema = ProductSchema()
            updated_product_data = product_schema.dump(product)

            return jsonify(updated_product_data), 200  # Return the updated product data with a 200 OK status
        else:
            abort(404, message="Product not found.")

#final
@blp.route('/admin_products', methods=['GET'])
def get_products():
    products = ProductModel.query.all()
    products_list = [
        {
            'product_id': product.product_id,
            'name': product.name,
            'cat_id': product.cat_id,
            'seller_id': product.seller_id
        } for product in products
    ]
    return jsonify(products_list)

@blp.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductModel.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'product deleted successfully'}), 200
    return jsonify({'message': 'product not found'}), 404


@blp.route("/pottery_event")
class ProductList(MethodView):
    # @blp.response(200, PlainProductSchema(many=True))
    def get(self):
        cat_id = 3
        event_id = 1
        product = ProductModel.query.filter_by(cat_id=cat_id, event_id=event_id).all()
        product = ProductSchema().dump(product, many=True)
        return render_template('pottery_event.html', product=product)

@blp.route("/macrame_event")
class ProductList(MethodView):
    # @blp.response(200, PlainProductSchema(many=True))
    def get(self):
        cat_id = 4
        event_id = 2
        product = ProductModel.query.filter_by(cat_id=cat_id, event_id=event_id).all()
        product = ProductSchema().dump(product, many=True)
        return render_template('macrame_event.html', product=product)
