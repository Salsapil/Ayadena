from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from db import db
from models import SellerModel
from models import UserModel, AdminModel
from schemas import PlainUserSchema, UserSchema
from flask_jwt_extended import create_access_token
from flask import render_template, request, jsonify, session


blp = Blueprint("Users", "users", description="Operations on users")

# @blp.route("/register_page", methods=["GET"])
# def registration():
#     return render_template("register.html")

@blp.route("/register")
class UserRegister(MethodView):
    def get(self):
        return render_template('registerr.html')

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
        return render_template('loginn.html')

    # @blp.arguments(PlainUserSchema) #load incoming data to user schema --> object
    def post(self):
        user_data = request.get_json()
        
        # Check if the user is an admin
        admin = AdminModel.query.filter(
            AdminModel.email == user_data["email"]
        ).first()
        if admin and pbkdf2_sha256.verify(user_data["password"], admin.password):
            session['identity_id'] = admin.admin_id
            session['user_type'] = 'admin'
            return {"email": admin.email, "user_type": "admin"}, 200

        # Check if the user is a regular user
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            session['identity_id'] = user.user_id
            if SellerModel.query.filter_by(user_id=user.user_id).first():
                session['user_type'] = 'seller'
                return {"username": user.username, "user_type": "seller"}, 200
            session['user_type'] = 'user'
            return {"username": user.username, "user_type": "user"}, 200

        # If no valid credentials are found, abort with 401
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
