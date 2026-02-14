from typing import List, Literal
from celery import Celery
from werkzeug.datastructures import FileStorage
import json
import subprocess
from random import randrange
from math import ceil
from app.folders import UPLOAD_FOLDER_PATH
from app.database.models import VideoStreamMetaData, AudioStreamMetaData, SubtitlesStreamMetaData


app = Celery("video_worker", broker="redis://localhost:6379/0")


@app.task
def process_video(id: int, video: FileStorage):

    duration, video_stream_list, audio_stream_list, subtitles_stream_list = __process_metadata(video)

    __generate_thumbnail(id, video, duration)

    __generate_preview(id, video, video_stream_list, audio_stream_list)

    __save_video(id, video)


def __process_metadata(video: FileStorage) -> tuple[float, List[VideoStreamMetaData], List[AudioStreamMetaData], List[SubtitlesStreamMetaData]]:
    metadata = __get_metadata(video)

    duration = float(metadata["format"]["duration"])

    streams = metadata["streams"]

    video_stream_list: List[VideoStreamMetaData] = []
    audio_stream_list: List[AudioStreamMetaData] = []
    subtitles_stream_list: List[SubtitlesStreamMetaData] = []

    for stream in streams:
        type: Literal["video", "audio", "subtitles"] = stream["codec_type"]
        match type:
            case "video":
                video_stream_list.append(VideoStreamMetaData(
                    fps=__calc_fps(stream["avg_frame_rate"]),
                    codec=stream["codec_name"],
                    width=stream["width"],
                    height=stream["height"]
                ))
            case "audio":
                audio_stream_list.append(AudioStreamMetaData(
                    fps=__calc_fps(stream["avg_frame_rate"]),
                    codec=stream["codec_name"]
                ))
            case "subtitles":
                subtitles_stream_list.append(SubtitlesStreamMetaData(
                    fps=__calc_fps(stream["avg_frame_rate"]),
                    codec=stream["codec_name"]
                ))

    return duration, video_stream_list, audio_stream_list, subtitles_stream_list


def __get_metadata(video: FileStorage):

    process = subprocess.run(
        ["ffprobe", "-print_format", "json", "-show_format", "-show_streams", "pipe:0"],
        capture_output=True,
        input=video.stream.read()
    )

    metadata = json.loads(process.stdout)

    return metadata


def __calc_fps(fps_raw: str) -> float:
    dividend, divisor = fps_raw.split("/")
    return int(dividend) / int(divisor)


def __generate_thumbnail(id: int, video: FileStorage, duration: float):
    random_second = randrange(1, ceil(duration) if duration < 59 else 60)

    subprocess.run(
        ["ffmpeg", "-i", "pipe:0", "-ss", f"00:00:{random_second:02d}.000", "-vframes", "1", "-vf", "scale=-2:360", f"{UPLOAD_FOLDER_PATH}/{id}/thumbnail.jpg"],
        input=video.stream.read(),
        check=True
    )


def __generate_preview(id: int, video: FileStorage, video_streams: List[VideoStreamMetaData], audio_streams: List[AudioStreamMetaData]):

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


def __save_video(id: int, video: FileStorage):
    video.save(f"{UPLOAD_FOLDER_PATH}/{id}/{video.filename}")
