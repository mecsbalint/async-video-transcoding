from typing import List
from werkzeug.datastructures import FileStorage
import subprocess
from app.folders import UPLOAD_FOLDER_PATH
from app.database.models import VideoStreamMetaData, AudioStreamMetaData


def generate_preview(id: int, video: FileStorage, video_streams: List[VideoStreamMetaData], audio_streams: List[AudioStreamMetaData]):

    video_stream_index = next((i for i, stream in enumerate(video_streams) if stream.codec == "libx264"), None)
    audio_stream_index = next((i for i, stream in enumerate(audio_streams) if stream.codec == "aac"), None)

    if video_stream_index:
        video_stream_subcommand = [f"0:v:{video_stream_index}"]
    else:
        video_stream_subcommand = ["0:v:0", "-c:v", "libx264"]

    if audio_stream_index:
        audio_stream_subcommand = [f"0:a:{audio_stream_index}"]
    else:
        audio_stream_subcommand = ["0:a:0?", "-c:a", "aac"]

    subprocess.run(
        ["ffmpeg", "-y", "-i", "pipe:0", "-map", *video_stream_subcommand, "-map", *audio_stream_subcommand, "-vf", "scale=-2:480", f"{UPLOAD_FOLDER_PATH}/{id}/thumbnail.jpg"],
        input=video.stream.read(),
        check=True
    )
