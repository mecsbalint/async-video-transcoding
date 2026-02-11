from flask import Flask
from app.api.endpoints import init_endpoints


def init_api():
    app = Flask(__name__)

    init_endpoints(app)

    return app
