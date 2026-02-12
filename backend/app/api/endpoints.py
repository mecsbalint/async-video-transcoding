from flask import Flask, Response, request, jsonify
from app.api.services import upload_video as upload_video_service, get_job as get_job_service


def is_allowed_file(filename: str | None) -> bool:
    from app.api import ALLOWED_EXTENSIONS
    if filename is None:
        return False
    for ext in ALLOWED_EXTENSIONS:
        if ext == filename.rsplit('.', 1)[1].lower():
            return True
    return False


def init_endpoints(app: Flask):

    @app.route("/api/uploads", methods=["POST"])
    def upload_video():
        if "video" not in request.files:
            # TODO: implement error handling
            return Response(status=400)

        video = request.files["video"]

        if not video.filename:
            # TODO: implement error handling
            return Response(status=400)

        if not video or not is_allowed_file(video.filename):
            # TODO: implement error handling
            return Response(status=400)

        response_dto = upload_video_service(video)
        return jsonify(response_dto.model_dump()), 201

    @app.route("/api/jobs/<job_id>", methods=["GET"])
    def get_job(job_id: str):
        id = int(job_id)
        jobDto = get_job_service(id)
        if not jobDto:
            return Response(status=400)
        return jobDto.model_dump()
