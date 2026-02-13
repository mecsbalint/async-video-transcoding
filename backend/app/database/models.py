from typing import List
from sqlalchemy import Enum
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.job_state import JobState


class Job(Base):
    __tablename__ = "job"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[JobState] = mapped_column(Enum(JobState), nullable=False)
    original_url: Mapped[str] = mapped_column()
    preview_url: Mapped[str] = mapped_column()
    thumbnail_url: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()
    video_stream_metadata: Mapped[List["VideoStreamMetaData"]] = relationship(back_populates="job")
    audio_stream_metadata: Mapped[List["AudioStreamMetaData"]] = relationship(back_populates="job")
    subtitles_stream_metadata: Mapped[List["SubtitlesStreamMetaData"]] = relationship(back_populates="job")


class VideoStreamMetaData(Base):
    __tablename__ = "video_stream_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    fps: Mapped[float] = mapped_column()
    codec: Mapped[str] = mapped_column()
    width: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped["Job"] = relationship(back_populates="video_stream_metadata")


class AudioStreamMetaData(Base):
    __tablename__ = "audio_stream_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    fps: Mapped[float] = mapped_column()
    codec: Mapped[str] = mapped_column()
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped["Job"] = relationship(back_populates="audio_stream_metadata")


class SubtitlesStreamMetaData(Base):
    __tablename__ = "subtitles_stream_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    fps: Mapped[float] = mapped_column()
    codec: Mapped[str] = mapped_column()
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    job: Mapped["Job"] = relationship(back_populates="subtitles_stream_metadata")
