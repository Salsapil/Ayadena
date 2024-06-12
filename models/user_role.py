from db import db

class UserRoleModel(db.Model):
    __tablename__ = "UserRole"
    
    role_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    #relations
    user = db.relationship('UserModel', back_populates='role') #dn att -user/role-