from typing import List, Literal
from werkzeug.datastructures import FileStorage
import json
import subprocess
from app.database.models import VideoStreamMetaData, AudioStreamMetaData, SubtitlesStreamMetaData


def process_metadata(video: FileStorage) -> tuple[float, List[VideoStreamMetaData], List[AudioStreamMetaData], List[SubtitlesStreamMetaData]]:
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
