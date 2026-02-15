from flask import Flask
from app.api.endpoints import init_endpoints
from app.folders import UPLOAD_FOLDER_PATH, STATIC_FOLDER_URL

ALLOWED_EXTENSIONS = {"mp4", "mkv"}


def init_api():

    app = Flask(__name__, static_folder=UPLOAD_FOLDER_PATH, static_url_path=STATIC_FOLDER_URL)

    init_endpoints(app)

    return app
