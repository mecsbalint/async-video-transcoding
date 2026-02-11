from flask import Flask, Response, request, jsonify
from app.api import ALLOWED_EXTENSIONS
from app.api.dtos import VideoUploadResponseDto


def is_allowed_file(filename: str | None) -> bool:
    if filename is None:
        return False
    for ext in ALLOWED_EXTENSIONS:
        if ext == filename.rsplit('.', 1)[1].lower():
            return True
    return False


def init_endpoints(app: Flask):

    @app.route("/api/uploads", methods=["POST"])
    def upload_video():
        if "file" not in request.files:
            # TODO: implement error handling
            return Response(status=400)

        file = request.files['file']

        if not file.filename:
            # TODO: implement error handling
            return Response(status=400)

        if file and is_allowed_file(file.filename):
            # TODO: call Celery worker with file
            response_dto = VideoUploadResponseDto(job_id=12, status="queued")
            return jsonify(response_dto.model_dump()), 201

        # TODO: implement error handling
        return Response(status=400)

    @app.route("/api/jobs/<job_id>", methods=["GET"])
    def get_job(job_id):
        return Response(status=201)
