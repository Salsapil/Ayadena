from db import db
from models import UserModel

class SellerModel(UserModel):
    __tablename__ = "seller"

    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    national_id = db.Column(db.String(255), nullable=False)
    bank_acc = db.Column(db.String(80), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False) #added
    brand_name = db.Column(db.String(80), nullable=False)
    units_sold = db.Column(db.String(80))
    rate = db.Column(db.Integer)
    unpaid_balance = db.Column(db.Integer)
    paid_balance = db.Column(db.Integer)
    #relations
    Product_seller = db.relationship('ProductModel', back_populates='seller', lazy='dynamic', cascade="all, delete") #dn -seller/product-
    
