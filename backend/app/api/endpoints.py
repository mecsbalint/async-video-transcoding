from flask import Flask, Response, request, jsonify
from app.api.services import upload_video as upload_video_service, get_job as get_job_service, get_all_jobs as get_all_jobs_service


def init_endpoints(app: Flask):

    @app.route("/api/uploads", methods=["POST"])
    def upload_video():
        if "video" not in request.files:
            # TODO: implement error handling
            return Response(status=400)

        priority = request.args.get("priority", None)

        video = request.files["video"]

        if not video.filename:
            # TODO: implement error handling
            return Response(status=400)

        if not video or not __is_allowed_file(video.filename):
            # TODO: implement error handling
            return Response(status=400)

        response_dto = upload_video_service(video, priority)
        return jsonify(response_dto.model_dump()), 201

    @app.route("/api/jobs/<job_id>", methods=["GET"])
    def get_job(job_id: str):
        id = int(job_id)
        jobDto = get_job_service(id)
        if not jobDto:
            # TODO: implement error handling
            return Response(status=400)
        return jobDto.model_dump()

    @app.route("/api/jobs", methods=["GET"])
    def get_all_jobs():
        job_dtos = get_all_jobs_service()
        if job_dtos is None:
            # TODO: implement error handling
            return Response(status=400)
        return [dto.model_dump() for dto in job_dtos]


def __is_allowed_file(filename: str | None) -> bool:
    from app.api import ALLOWED_EXTENSIONS
    if filename is None:
        return False
    for ext in ALLOWED_EXTENSIONS:
        if ext == filename.rsplit('.', 1)[1].lower():
            return True
    return False
