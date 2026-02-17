import os
from typing import List, cast
from sqlalchemy import select
from werkzeug.datastructures import FileStorage
from app.api.dtos import JobDoneDto, JobDto, JobFailedDto, JobListElementDto
from app.database.session import SessionLocal
from app.database.models import Job
from app.job_state import JobState
from app.worker.video_worker import process_video
from app.folders import UPLOAD_FOLDER_PATH
from app.env_variables import SMALL_FILE_MAX_SIZE


def upload_video(video: FileStorage, request_priority: str | None) -> JobDto:
    session = SessionLocal()
    output_file_path = None

    try:
        new_job = Job(state=JobState.QUEUED)
        session.add(new_job)
        session.commit()
        session.refresh(new_job)

        local_output_file_path = os.path.join(str(new_job.id), cast(str, video.filename))
        print("Save original video ")
        output_file_path = os.path.join(UPLOAD_FOLDER_PATH, local_output_file_path)
        job_folder = os.path.join(UPLOAD_FOLDER_PATH, str(new_job.id))
        os.makedirs(job_folder)
        video.save(output_file_path)
        print(f"Original video file saved to: {output_file_path}")
        priority = "high" if __get_job_priority(output_file_path, request_priority) else "low"

        process_video.apply_async(args=[new_job.id, output_file_path, local_output_file_path], queue=priority)

        return JobDto.model_validate(new_job)
    except Exception as e:
        session.rollback()
        if output_file_path and os.path.exists(output_file_path):
            os.remove(output_file_path)
        raise e
    finally:
        session.close()


def get_job(id: int) -> JobDto | None:
    session = SessionLocal()
    try:
        job = session.get(Job, id)
        if not job:
            return None
        match job.state:
            case JobState.DONE:
                return JobDoneDto.model_validate(job)
            case JobState.FAILED:
                return JobFailedDto(id=job.id, error_message="Job failed during execution")
            case _:
                return JobDto.model_validate(job)
    except Exception:
        # TODO: implement error handling
        return None
    finally:
        session.close()


def get_all_jobs() -> List[JobListElementDto] | None:
    session = SessionLocal()
    try:
        job_dicts = session.execute(select(Job.id, Job.state, Job.thumbnail_url)).mappings().all()
        return [JobListElementDto.model_validate(job_dict) for job_dict in job_dicts]
    except Exception:
        return None
    finally:
        session.close()


def __get_job_priority(saved_file_path: str, request_priority: str | None) -> bool:
    if request_priority == "high":
        return True
    return os.stat(saved_file_path).st_size < SMALL_FILE_MAX_SIZE
