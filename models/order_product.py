from db import db

class OrderProductModel(db.Model):
    __tablename__ = 'order_product'
    pk_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    count = db.Column(db.Integer, nullable=True) #added