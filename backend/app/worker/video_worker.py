from celery import Celery
from werkzeug.datastructures import FileStorage

app = Celery("video_worker", broker="redis://localhost:6379/0")

@app.task
def process_video(id: int, video: FileStorage):
    pass
