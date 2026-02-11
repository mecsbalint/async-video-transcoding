from sqlalchemy import Enum
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
    original_video_metadata: Mapped["MetaData"] = relationship(back_populates="job")


class MetaData(Base):
    __tablename__ = "metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    duration: Mapped[int] = mapped_column()
    fps: Mapped[int] = mapped_column()
    codec: Mapped[str] = mapped_column()
    job: Mapped["Job"] = relationship(back_populates="original_video_metadata")
