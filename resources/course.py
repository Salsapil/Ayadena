from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import CourseModel
from schemas import PlainCourseSchema, CourseSchema, CourseUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("Courses", "courses", description="Operations on Admins")


@blp.route("/course")
class CourseList(MethodView):
    @blp.response(200, PlainCourseSchema(many=True))
    def get(self):
        return CourseModel.query.all()

    @blp.arguments(CourseSchema)
    @blp.response(201, CourseSchema)
    def post(self, course_data):
        course = CourseModel(**course_data)
        if CourseModel.query.filter(CourseModel.name == course_data["name"]).first():
            abort(409, message="A Course with that name already exists.")
        try:
            db.session.add(course)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Integrity Error",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the product.")

        return course


@blp.route("/course/<int:course_id>") #int to all
class Course(MethodView):
    @blp.response(200, PlainCourseSchema)
    def delete(self, course_id):
        course = CourseModel.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {"message": "deleted"}

    @blp.arguments(CourseUpdateSchema)
    @blp.response(200, PlainCourseSchema)
    def put(self, course_data, course_id, update_column=None):
        course = CourseModel.query.get_or_404(course_id)

        if course:
            if update_column:
                for key, value in course_data.items():
                    if key == update_column:
                        setattr(course, key, value)
            else:
                course.name = course_data.get("name", course.name)
                course.description = course_data.get("description", course.description)
                course.duration = course_data.get("duration", course.duration)
            try:
                db.session.commit()
                return course
            except IntegrityError:
                db.session.rollback()
                abort(400, message="Update failed due to integrity constraint violation.")
        else:
            abort(404, message="Product not found.")