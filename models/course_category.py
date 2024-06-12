from db import db

class CourseCategoryModel(db.Model):
    __tablename__ = 'course_category'

    cat_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    #relations
    CourseCat = db.relationship('CourseModel', back_populates='cat', lazy='dynamic', cascade="all, delete") #dn -category/course-