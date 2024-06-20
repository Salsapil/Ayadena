from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import render_template, request
from db import db
from models import SellerModel, UserModel
from schemas import PlainSellerSchema
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token



blp = Blueprint("Sellers", "sellers", description="Operations on sellers")


@blp.route("/register_seller")
class SellerRegister(MethodView):
    def get(self):
        return render_template('seller_register.html')
    
    # @blp.arguments(PlainSellerSchema)
    def post(self):
        seller_data = request.get_json()
        seller = SellerModel(
            first_name=seller_data["first_name"],
            last_name=seller_data["last_name"],
            username=seller_data["username"],
            email=seller_data["email"],
            password=pbkdf2_sha256.hash(seller_data["password"]),
            phone=seller_data["phone"],
            birthday=seller_data["birthday"],
            city = seller_data["city"],
            country = seller_data["country"],
            postal_code = seller_data["postal_code"],
            national_id=seller_data["national_id"],
            brand_name=seller_data["brand_name"],
            bank_acc = seller_data["bank_acc"],
        )
        db.session.add(seller)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/seller")
class SellerList(MethodView):
    @blp.response(200, PlainSellerSchema(many=True))
    def get(self):
        return SellerModel.query.all()

@blp.route("/seller/<string:seller_id>")
class Seller(MethodView):
    @blp.response(200, PlainSellerSchema)
    def delete(self, seller_id):
        seller = SellerModel.query.get_or_404(seller_id)
        db.session.delete(seller)
        db.session.commit()
