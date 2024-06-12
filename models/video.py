from db import db

class VideoModel(db.Model):
    __tablename__ = 'video'

    video_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    video = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False) #name
    course_id = db.Column(db.ForeignKey('course.course_id'), nullable=False) #dn -video/course-
    #relations
    course = db.relationship('CourseModel', back_populates='video_course') #dn -video/course-