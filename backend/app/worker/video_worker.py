from io import BufferedReader
from typing import List, Literal, cast
from celery import Celery
import json
import subprocess
from random import randrange
from math import ceil
import os
import stat
import shutil
from app.folders import UPLOAD_FOLDER_PATH, STATIC_FOLDER_URL
from app.database.models import Job, VideoStreamMetaData, AudioStreamMetaData, SubtitlesStreamMetaData
from app.database.session import SessionLocal
from app.job_state import JobState


TIMEOUT = 60


app = Celery("video_worker", broker="redis://localhost:6379/0")


@app.task
def process_video(id: int, video_abs_path: str, video_local_path: str):

    # TODO: retry mechanism with maximum number of retries and a backoff mechanism (delaying retries)
    video = open(video_abs_path, "rb")
    try:
        # TODO: delete after dockerization (Windows-specific code)
        os.chmod(f"{UPLOAD_FOLDER_PATH}\\{id}", stat.S_IRWXU)

        __update_job_state_in_db(id, JobState.RUNNING)

        duration, video_stream_list, audio_stream_list, subtitles_stream_list = __process_metadata(video)

        thumbnail_local_path = __generate_thumbnail(id, video, duration)

        preview_local_path = __generate_preview(id, video)

        __update_job_in_db(id, duration, thumbnail_local_path, preview_local_path, video_local_path, video_stream_list, audio_stream_list, subtitles_stream_list)
    except Exception as e:
        try:
            video.close()
            folder_path = os.path.join(UPLOAD_FOLDER_PATH, str(id))
            shutil.rmtree(folder_path)
        except FileNotFoundError:
            pass
        except Exception:
            print("Error cleaning up the folder")
        finally:
            print(f"The process stopped with error: {e}")
            __update_job_state_in_db(id, JobState.FAILED)
    else:
        video.close()


def __update_job_state_in_db(id: int, state: JobState):
    print(f"Update job [id:{id}] state to {state.value}")

    session = SessionLocal()
    try:
        job = session.get(Job, id)
        if not job:
            raise Exception()
        job.state = state
        session.commit()
    except Exception as e:
        session.rollback()
        print("Database process failed")
        print(f"An error occured during database process while updating job [id:{id}]")
        raise e
    else:
        print(f"Update job [id:{id}] state to {state.value} is finished")
    finally:
        session.close()


def __process_metadata(video: BufferedReader) -> tuple[float, List[VideoStreamMetaData], List[AudioStreamMetaData], List[SubtitlesStreamMetaData]]:
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


def __get_metadata(video: BufferedReader):

    command = ["ffprobe", "-print_format", "json", "-show_format", "-show_streams", "pipe:0"]

    print(f"Video metadata extraction [{" ".join(command)}] has started")

    process = cast(subprocess.CompletedProcess[bytes], __run_process(command, video, capture_output=True))

    metadata = json.loads(process.stdout)

    print(f"Video metadata extraction [{" ".join(command)}] has finished")

    return metadata


def __run_process(command: List[str], video: BufferedReader, *, capture_output: bool = False, saved_files_path: List[str] = []) -> subprocess.CompletedProcess[bytes] | None:
    if saved_files_path and next((file_path for file_path in saved_files_path if not os.path.exists(file_path)), None) is None:
        return None

    try:
        video.seek(0)
        process = subprocess.run(
            command,
            capture_output=capture_output,
            input=video.read(),
            check=True,
            timeout=TIMEOUT
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        for saved_file_path in saved_files_path:
            if os.path.exists(saved_file_path):
                os.remove(saved_file_path)
        print("Process failed")
        print(e.stderr)
        raise RuntimeError(f"Process excecution failed with command [{" ".join(command)}]")
    else:
        return process


def __calc_fps(fps_raw: str) -> float:
    dividend, divisor = fps_raw.split("/")
    return int(dividend) / int(divisor)


def __generate_thumbnail(id: int, video: BufferedReader, duration: float) -> str:
    random_second = randrange(1, ceil(duration) if duration < 59 else 60)

    local_output_file_path = f"{id}\\thumbnail.jpg"

    output_file_path = f"{UPLOAD_FOLDER_PATH}\\{local_output_file_path}"

    command = ["ffmpeg", "-y", "-i", "pipe:0", "-ss", f"00:00:{random_second:02d}.000", "-vframes", "1", "-vf", "scale=-2:360", output_file_path]

    print(f"Generate thumbnail file: {" ".join(command)}")

    print(os.access(os.path.dirname(output_file_path), os.W_OK))

    __run_process(command, video, saved_files_path=[f"{UPLOAD_FOLDER_PATH}/{local_output_file_path}"])

    print(f"Thumbnail file saved to: {output_file_path}")

    return local_output_file_path


def __generate_preview(id: int, video: BufferedReader) -> str:

    local_output_file_path = f"{id}\\preview.mp4"

    output_file_path = f"{UPLOAD_FOLDER_PATH}\\{local_output_file_path}"

    command = ["ffmpeg", "-y", "-i", "pipe:0", "-map", "0:v:0", "-c:v", "h264", "-map", "0:a:0?", "-c:a", "aac", "-vf", "scale=-2:480", output_file_path]

    print(f"Generate preview file: {" ".join(command)}")

    __run_process(command, video, saved_files_path=[output_file_path])

    print(f"Preview file saved to: {output_file_path}")

    return local_output_file_path


def __update_job_in_db(id: int, duration: float, thumbnail_local_path: str, preview_local_path: str, video_local_path: str, video_stream_list: List[VideoStreamMetaData], audio_stream_list: List[AudioStreamMetaData], subtitles_stream_list: List[SubtitlesStreamMetaData]):

    print(f"Update job [id:{id}] data")

    session = SessionLocal()

    thumbnail_url = f"{STATIC_FOLDER_URL}/{thumbnail_local_path}"
    preview_url = f"{STATIC_FOLDER_URL}/{preview_local_path}"
    original_url = f"{STATIC_FOLDER_URL}/{video_local_path}"

    try:

        job = session.get(Job, id)

        if not job:
            raise Exception()

        job.state = JobState.DONE
        job.original_url = original_url
        job.preview_url = preview_url
        job.thumbnail_url = thumbnail_url
        job.duration = duration
        job.video_streams_metadata = video_stream_list
        job.audio_streams_metadata = audio_stream_list
        job.subtitles_streams_metadata = subtitles_stream_list

        session.commit()
    except Exception as e:
        session.rollback()
        print("Database process failed")
        print(f"An error occured during database process while updating job [id:{id}]")
        raise e
    else:
        print(f"Update job [id:{id}] data is finished")
    finally:
        session.close()
