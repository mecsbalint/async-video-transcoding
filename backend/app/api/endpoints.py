from flask import Flask, Response, request, jsonify
from app.api.dtos import JobDoneDto, JobDto, JobFailedDto
from app.database.session import SessionLocal
from app.database.models import Job
from app.job_state import JobState


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
        if "file" not in request.files:
            # TODO: implement error handling
            return Response(status=400)

        file = request.files['file']

        if not file.filename:
            # TODO: implement error handling
            return Response(status=400)

        if file and is_allowed_file(file.filename):
            # TODO: call Celery worker with file
            response_dto = JobDto(id=12, state=JobState.QUEUED)
            return jsonify(response_dto.model_dump()), 201

        # TODO: implement error handling
        return Response(status=400)

    @app.route("/api/jobs/<job_id>", methods=["GET"])
    def get_job(job_id: str):
        session = SessionLocal()

        try:
            job = session.query(Job).get(int(job_id))
            if not job:
                # TODO: implement error handling
                return Response(status=400)
            match job.state:
                case JobState.DONE:
                    dto = JobDoneDto.model_validate(job)
                    return jsonify(dto.model_dump()), 200
                case JobState.FAILED:
                    dto = JobFailedDto(id=job.id, error_message="Job failed during execution")
                    return jsonify(dto.model_dump()), 200
                case _:
                    dto = JobDto.model_validate(job)
                    return jsonify(dto.model_dump()), 200
        except Exception:
            # TODO: implement error handling
            return Response(status=500)
        finally:
            session.close()
