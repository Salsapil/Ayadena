from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from db import db
from models import SellerModel
from models import UserModel, AdminModel
from schemas import PlainUserSchema, UserSchema
from flask_jwt_extended import create_access_token
from flask import render_template, request, jsonify


blp = Blueprint("Users", "users", description="Operations on users")

# @blp.route("/register_page", methods=["GET"])
# def registration():
#     return render_template("register.html")

@blp.route("/register")
class UserRegister(MethodView):
    def get(self):
        return render_template('register.html')

    # @blp.arguments(PlainUserSchema)
    def post(self):
        user_data = request.get_json()
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")

        user = UserModel(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            phone=user_data["phone"],
            birthday=user_data["birthday"],
            city = user_data["city"],
            country = user_data["country"]
        )
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    def get(self):
        return render_template('login.html')

    # @blp.arguments(PlainUserSchema) #load incoming data to user schema --> object
    def post(self):
        user_data = request.get_json()
        admin = AdminModel.query.filter(
            AdminModel.email == user_data["email"]
        ).first()
        if admin and pbkdf2_sha256.verify(user_data["password"], admin.password):
            access_token = create_access_token(identity=admin.admin_id)
            return {"access_token": access_token, "email": admin.email}, 200

        user = UserModel.query.filter(
            UserModel.email == user_data["email"] #use .get
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.user_id)
            if (SellerModel.query.filter_by(user_id=user.user_id).first()) is not None:
                return {"access_token": access_token, "username": user.username, "seller": "{} is a seller".format(user.username)}, 200 #user
            return {"access_token": access_token, "username": user.username}, 200

        abort(401, message="Invalid credentials.")

# @blp.route("/user")
# class UserList(MethodView):
#     """GET"""

#     @blp.response(200, PlainUserSchema(many=True))
#     def get(self):
#         return UserModel.query.all()


@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "deleted"}

# final
@blp.route('/admin_users', methods=['GET'])
def get_users():
    users = UserModel.query.all()
    sellers = SellerModel.query.all()
    seller_ids = {seller.user_id for seller in sellers}
    users_list = [
        {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'is_seller': user.user_id in seller_ids
        } for user in users
    ]
    return jsonify(users_list)

@blp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404
