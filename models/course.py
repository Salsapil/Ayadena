from db import db
class CourseModel(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255), nullable=True)
    route = db.Column(db.String(255), nullable=True)
    cat_id = db.Column(db.ForeignKey('course_category.cat_id'), nullable=False) #dn -category/course-
    #relations
    cat = db.relationship('CourseCategoryModel', back_populates='CourseCat') #dn -category/course-
    video_course = db.relationship('VideoModel', back_populates='course', lazy='dynamic', cascade="all, delete") #dn -video/course-
    learner = db.relationship('UserModel', back_populates='course', secondary='learner_course') #dnn -learner/course-
