from db import db

class SubscriptionPlanModel(db.Model):
    __tablename__ = 'subscription_plan'

    plan_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    #price--
    #relations
    learner = db.relationship("UserModel", back_populates="plan", secondary="learner_plan") #dnn -learner/plan-