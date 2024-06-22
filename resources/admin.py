from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import render_template
from passlib.hash import pbkdf2_sha256
from db import db
from models import AdminModel
from schemas import AdminSchema


blp = Blueprint("Admins", "admins", description="Operations on Admins")


@blp.route("/register_admin")
class AdminRegister(MethodView):
    def get(self):
        return render_template('admin.html')
    # @blp.arguments(AdminSchema)
    def post(self, admin_data):
        if AdminModel.query.filter(AdminModel.email == admin_data["email"]).first():
            abort(409, message="An admin with that email already exists.")

        admin = AdminModel(
            email=admin_data["email"],
            password=pbkdf2_sha256.hash(admin_data["password"]),
        )
        db.session.add(admin)
        db.session.commit()

        return {"message": "Admin created successfully."}, 201

@blp.route("/admin")
class AdminList(MethodView):
    """GET"""

    @blp.response(200, AdminSchema(many=True))
    def get(self):
        return AdminModel.query.all()

@blp.route("/admin_user", methods=["GET"])
def checkout():
    return render_template("admin_user.html")

@blp.route("/admin_courses", methods=["GET"])
def checkout():
    return render_template("admin_courses.html")

@blp.route("/admin_product", methods=["GET"])
def checkout():
    return render_template("admin_product.html")

@blp.route("/admin_order", methods=["GET"])
def checkout():
    return render_template("admin_order.html")

@blp.route("/admin_seller", methods=["GET"])
def checkout():
    return render_template("admin_seller.html")