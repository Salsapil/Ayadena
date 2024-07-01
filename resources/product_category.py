from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import ProductCategoryModel
from flask import render_template
from schemas import PlainCatSchema, CategoryUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/category")
class CategoryList(MethodView):
    # @blp.response(200, PlainCatSchema(many=True))
    def get(self):
        category = ProductCategoryModel.query.all()
        category = PlainCatSchema().dump(category, many=True)
        print(category)
        return render_template('categories.html', category=category)

    @blp.arguments(PlainCatSchema) #dn make name unique 
    @blp.response(201, PlainCatSchema)
    def post(self, category_data):
        category = ProductCategoryModel(**category_data)
        if ProductCategoryModel.query.filter(ProductCategoryModel.name == category_data["name"]).first():
            abort(409, message="A category with that name already exists.")
        try:
            db.session.add(category)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred creating the product.")

        return category


@blp.route("/category/<string:category_id>")
class Category(MethodView):
    @blp.response(200, PlainCatSchema)
    def delete(self, category_id):
        category = ProductCategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()

    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200, PlainCatSchema)
    def put(self, category_data, category_id, update_column=None):
        category = ProductCategoryModel.query.get_or_404(category_id)

        if category:
            if update_column:
                for key, value in category_data.items():
                    if key == update_column:
                        setattr(category, key, value)
            else:
                category.name = category_data.get("name", category.name)
                category.description = category_data.get("description", category.description)

            try:
                db.session.commit()
                return category
            except IntegrityError:
                db.session.rollback()
                abort(400, message="Update failed due to integrity constraint violation.")
        else:
            abort(404, message="Product not found.")