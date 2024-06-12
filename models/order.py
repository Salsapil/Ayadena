from db import db

class OrderModel(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    block_no = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False) #added
    order_compelete = db.Column(db.Boolean, nullable=False, default=False) #added
    #FKs
    buyer_id = db.Column(db.ForeignKey('user.user_id'), nullable=False) #dn -buyer/order-
    #relations
    buyer = db.relationship('UserModel', back_populates='order_buyer') #dn -buyer/order-
    payment = db.relationship('PaymentModel', back_populates='order', lazy='dynamic', cascade="all, delete") #dn -payment/order-
    product = db.relationship('ProductModel', back_populates='order', secondary='order_product') #dnn -order/product-
    