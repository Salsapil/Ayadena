from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import VideoModel
from schemas import PlainVideoSchema, VideoSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


blp = Blueprint("Videoes", "videos", description="Operations on Admins")


@blp.route("/video")
class VideoList(MethodView):
    @blp.response(200, PlainVideoSchema(many=True))
    def get(self):
        return VideoModel.query.all()

    @blp.arguments(VideoSchema)
    @blp.response(201, VideoSchema)
    def post(self, video_data):
        video = VideoModel(**video_data)
        if VideoModel.query.filter(VideoModel.description == video_data["description"]).first():
            abort(409, message="A Video with that name already exists.")
        try:
            db.session.add(video)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Integrity Error",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the product.")

        return video


@blp.route("/video/<int:video_id>") #int to all
class Video(MethodView):
    @blp.response(200, PlainVideoSchema)
    def delete(self, video_id):
        video = VideoModel.query.get_or_404(video_id)
        db.session.delete(video)
        db.session.commit()
        return {"message": "deleted"}

    # @blp.arguments(VideoUpdateSchema)
    # @blp.response(200, PlainVideoSchema)
    # def put(self, video_data, video_id, update_column=None):
    #     video = VideoModel.query.get_or_404(video_id)

    #     if video:
    #         if update_column:
    #             for key, value in video_data.items():
    #                 if key == update_column:
    #                     setattr(video, key, value)
    #         else:
    #             video.name = video_data.get("name", video.name)
    #             video.description = video_data.get("description", video.description)
    #             video.duration = video_data.get("duration", video.duration)
    #         try:
    #             db.session.commit()
    #             return video
    #         except IntegrityError:
    #             db.session.rollback()
    #             abort(400, message="Update failed due to integrity constraint violation.")
    #     else:
    #         abort(404, message="Product not found.")