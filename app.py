from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from db import db
from flask import render_template
import urllib.parse
from resources.user import blp as UserBlueprint
from resources.admin import blp as AdminBlueprint
from resources.product import blp as ProductBlueprint
from resources.seller import blp as SellerBlueprint
from resources.product_category import blp as CategoryBlueprint
from resources.course import blp as CourseBlueprint
from resources.course_category import blp as CCategoryBlueprint
from resources.video import blp as VideoBlueprint
from resources.order import blp as OrderBlueprint
import os


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    password = urllib.parse.quote_plus("AyadenaBella2024")
    url = "postgresql+psycopg2://postgres.envjesdrvtvnztfajcjr:{}@aws-0-us-west-1.pooler.supabase.com:6543/postgres".format(password)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate=Migrate(app,db)
    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AdminBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(SellerBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(CCategoryBlueprint)
    api.register_blueprint(CourseBlueprint)
    api.register_blueprint(VideoBlueprint)
    api.register_blueprint(OrderBlueprint)
    app.config["JWT_SECRET_KEY"] = "Salsabil"
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    jwt = JWTManager(app)

    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/about_us')
    def about():
        return render_template('about us.html')

    # with app.app_context():
    #     import models

    #     db.create_all()
    #     category = models.ProductCategoryModel()
    #     category.name = "crochet"
    #     category.description = "hand grafts"
    #     db.session.add(category)
    #     db.session.commit()

    return app