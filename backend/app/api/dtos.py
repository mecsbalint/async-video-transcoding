from typing import List
from pydantic import BaseModel, Field
from app.job_state import JobState


class DtoBaseModel(BaseModel):
    model_config = {
        "from_attributes": True
    }


class VideoStreamMetadataDto(DtoBaseModel):
    fps: float | None
    codec: str | None
    width: int | None
    height: int | None


class AudioStreamMetadataDto(DtoBaseModel):
    codec: str | None
    language: str | None
    sample_rate: str | None


class SubtitlesStreamMetadataDto(DtoBaseModel):
    codec: str | None
    language: str | None


class JobDto(DtoBaseModel):
    id: int
    state: JobState


class JobDoneDto(JobDto):
    state: JobState = Field(default=JobState.DONE)
    original_url: str
    preview_url: str
    thumbnail_url: str
    duration: float | None
    video_streams_metadata: List[VideoStreamMetadataDto]
    audio_streams_metadata: List[AudioStreamMetadataDto]
    subtitles_streams_metadata: List[SubtitlesStreamMetadataDto]


class JobFailedDto(JobDto):
    state: JobState = Field(default=JobState.FAILED)
    error_message: str


class JobListElementDto(JobDto):
    thumbnail_url: str | None
