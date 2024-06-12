from db import db

class EventModel(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    #relations
    Product_event = db.relationship('ProductModel', back_populates='event', lazy='dynamic', cascade="all, delete") #dn -event/product-
    user = db.relationship('UserModel', back_populates='event', secondary='user_event') #dnn -event/user-