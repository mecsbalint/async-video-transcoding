from pydantic import BaseModel, Field
from app.job_state import JobState


class DtoBaseModel(BaseModel):
    model_config = {
        "from_attributes": True
    }


class JobDto(DtoBaseModel):
    id: int
    state: JobState


class MetadataDto(DtoBaseModel):
    duration: float
    fps: int
    codec: str


class JobDoneDto(JobDto):
    state: JobState = Field(default=JobState.DONE)
    original_url: str
    preview_url: str
    thumbnail_url: str
    original_video_metadata: MetadataDto


class JobFailedDto(JobDto):
    state: JobState = Field(default=JobState.FAILED)
    error_message: str
