from flask import Flask
from app.api.endpoints import init_endpoints

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = {"mp4", "mkv"}


def init_api():
    app = Flask(__name__)

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    init_endpoints(app)

    return app
