from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from db import db
from models import AdminModel
from schemas import AdminSchema


blp = Blueprint("Admins", "admins", description="Operations on Admins")


@blp.route("/register_admin")
class AdminRegister(MethodView):
    @blp.arguments(AdminSchema)
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

#delete
