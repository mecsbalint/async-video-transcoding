from werkzeug.datastructures import FileStorage
import subprocess
from random import randrange
from math import ceil
from app.folders import UPLOAD_FOLDER_PATH


def generate_thumbnail(id: int, video: FileStorage, duration: float):
    random_second = randrange(1, ceil(duration) if duration < 59 else 60)

    subprocess.run(
        ["ffmpeg", "-i", "pipe:0", "-ss", f"00:00:{random_second:02d}.000", "-vframes", "1", "-vf", "scale=-2:360", f"{UPLOAD_FOLDER_PATH}/{id}/thumbnail.jpg"],
        input=video.stream.read(),
        check=True
    )
