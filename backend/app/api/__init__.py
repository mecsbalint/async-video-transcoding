from flask import Flask
from app.api.endpoints import init_endpoints
from app.folders import UPLOAD_FOLDER_PATH, STATIC_FOLDER_URL
from app.api.error_handlers import init_error_handlers


def init_api():

    app = Flask(__name__, static_folder=UPLOAD_FOLDER_PATH, static_url_path=STATIC_FOLDER_URL)

    init_endpoints(app)

    init_error_handlers(app)

    return app
