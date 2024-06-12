from db import db

class AdminModel(db.Model):
    __tablename__ = "admin"
    
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
