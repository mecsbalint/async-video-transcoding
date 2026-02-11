from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True)
    state = Column(String)
    original_url = Column(String)
    preview_url = Column(String)
    thumbnail_url = Column(String)
    original_video_metadata = relationship("MetaData", uselist=False, back_populates="job")


class MetaData(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True)
    duration = Column(Integer)
    fps = Column(Integer)
    codec = Column(String)
    job = relationship("Job", uselist=False, back_populates="original_video_metadata")
