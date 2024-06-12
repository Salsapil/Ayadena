from db import db

class PaymentModel(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    # method = db.Column(db.String(255), nullable=False) #delete
    card_name = db.Column(db.String(255), nullable=False)
    card_number = db.Column(db.Integer, nullable=False)
    exp_month = db.Column(db.String(255), nullable=False)
    exp_year = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    #FKs
    order_id = db.Column(db.ForeignKey('order.order_id'), nullable=False) #dn -payment/order-
    #relations
    order = db.relationship('OrderModel', back_populates='payment') #dn -payment/order-