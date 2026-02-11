from flask import Flask, Response


def init_endpoints(app: Flask):

    @app.route("/api/uploads", methods=["GET"])
    def upload_video():
        return Response(status=201)

    @app.route("/api/jobs/<job_id>", methods=["GET"])
    def get_job(job_id):
        return Response(status=201)
