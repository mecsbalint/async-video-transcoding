import os

STATIC_FOLDER_URL = "/api/uploads"

UPLOAD_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
