from db import db

class ProductModel(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(asdecimal=True), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    #FKs
    cat_id = db.Column(db.ForeignKey('product_category.cat_id'), nullable=False) #dn -category/product-
    seller_id = db.Column(db.ForeignKey('seller.seller_id'), nullable=False) #dn -seller/product-
    event_id = db.Column(db.ForeignKey('event.event_id'), nullable=True) #dn -event/product-
    #relations
    seller = db.relationship('SellerModel', back_populates='Product_seller') #dn -seller/product-
    cat = db.relationship('ProductCategoryModel', back_populates='Product_cat') #dn -category/product-
    event = db.relationship('EventModel', back_populates='Product_event') #dn -event/product-
    order = db.relationship('OrderModel', back_populates='product', secondary='order_product') #dnn -order/product-
