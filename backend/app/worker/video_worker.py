from celery import Celery
from werkzeug.datastructures import FileStorage
from app.worker.thumbnail_genreator import generate_thumbnail
from app.worker.video_metadata_processor import process_metadata
from app.worker.preview_generator import generate_preview


app = Celery("video_worker", broker="redis://localhost:6379/0")


@app.task
def process_video(id: int, video: FileStorage):

    duration, video_stream_list, audio_stream_list, subtitles_stream_list = process_metadata(video)

    generate_thumbnail(id, video, duration)

    generate_preview(id, video, video_stream_list, audio_stream_list)
