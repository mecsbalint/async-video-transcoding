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
    duration: float | None
    fps: int | None
    codec: str | None


class JobDoneDto(JobDto):
    state: JobState = Field(default=JobState.DONE)
    original_url: str | None
    preview_url: str | None
    thumbnail_url: str | None
    original_video_metadata: MetadataDto | None


class JobFailedDto(JobDto):
    state: JobState = Field(default=JobState.FAILED)
    error_message: str
