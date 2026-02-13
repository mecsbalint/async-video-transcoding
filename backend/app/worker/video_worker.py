from celery import Celery
from werkzeug.datastructures import FileStorage
from app.worker.process_video_metadata import process_metadata


app = Celery("video_worker", broker="redis://localhost:6379/0")


@app.task
def process_video(id: int, video: FileStorage):
    duration, video_stream_list, audio_stream_list, subtitles_stream_list = process_metadata(video)
