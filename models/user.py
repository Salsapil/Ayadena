from db import db


class UserModel(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    # user_type = db.Column(db.String(255), nullable=True)
    #subscripe
    #payment att for subscription plan --> always true
    #relations
    role = db.relationship('UserRoleModel', back_populates='user', lazy='dynamic', cascade="all, delete") #dn att -user/role-
    order_buyer = db.relationship('OrderModel', back_populates='buyer', lazy='dynamic', cascade="all, delete") #dn -buyer/order-
    plan = db.relationship('SubscriptionPlanModel', back_populates='learner', secondary='learner_plan') #dnn -learner/plan-
    event = db.relationship('EventModel', back_populates='user', secondary='user_event') #dnn -event/user-
    course = db.relationship('CourseModel', back_populates='learner', secondary='learner_course') #dnn -learner/course-
