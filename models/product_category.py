from db import db

class ProductCategoryModel(db.Model):
    __tablename__ = 'product_category'

    cat_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    #relations
    Product_cat = db.relationship('ProductModel', back_populates='cat', lazy='dynamic', cascade="all, delete") #dn -category/product-