from flask import Flask, request, jsonify
from app.api.services import upload_video as upload_video_service, get_job as get_job_service, get_all_jobs as get_all_jobs_service, get_jobs as get_jobs_service
from app.env_variables import ALLOWED_EXTENSIONS


def init_endpoints(app: Flask):

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    @app.route("/api/uploads", methods=["POST"])
    def upload_video():
        if "video" not in request.files:
            return jsonify({"error": "No video file part in the request"}), 400

        priority = request.args.get("priority", None)

        video = request.files["video"]

        if not video.filename:
            return jsonify({"error": "No selected file"}), 400

        if not video or not __is_allowed_file(video.filename):
            return jsonify({"error": "Invalid file type"}), 400

        response_dto = upload_video_service(video, priority)
        return jsonify(response_dto.model_dump()), 201

    @app.route("/api/jobs/<job_id>", methods=["GET"])
    def get_job(job_id: str):
        id = int(job_id)
        jobDto = get_job_service(id)
        if not jobDto:
            return jsonify({"error": "Jobs not found"}), 404
        return jobDto.model_dump()

    @app.route("/api/jobs", methods=["GET"])
    def get_jobs():
        ids = request.args.get("ids", None)
        if ids is None:
            job_dtos = get_all_jobs_service()
        else:
            try:
                job_dtos = get_jobs_service([int(id) for id in ids.split(",")])
            except Exception:
                return jsonify({"error": "The ids query param isn't in the correct format"}), 400
        if job_dtos is None:
            return jsonify({"error": "Jobs not found"}), 404
        return [dto.model_dump() for dto in job_dtos]


def __is_allowed_file(filename: str | None) -> bool:
    if filename is None:
        return False
    for ext in ALLOWED_EXTENSIONS:
        if ext == filename.rsplit('.', 1)[1].lower():
            return True
    return False
