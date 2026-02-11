from typing import Literal
from pydantic import BaseModel


class VideoUploadResponseDto(BaseModel):
    job_id: int
    status: Literal["queued", "running", "done", "failed"]
