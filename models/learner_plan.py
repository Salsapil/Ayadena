from db import db

class LearnerPlanModel(db.Model):
    __tablename__ = 'learner_plan'
    pk_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plan.plan_id'), nullable=False)
    # add start date/ end date columns 
