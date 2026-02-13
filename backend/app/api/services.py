from werkzeug.datastructures import FileStorage
from app.api.dtos import JobDoneDto, JobDto, JobFailedDto
from app.database.session import SessionLocal
from app.database.models import Job
from app.job_state import JobState
from app.worker.video_worker import process_video


def upload_video(file: FileStorage) -> JobDto:
    session = SessionLocal()

    try:
        new_job = Job(state=JobState.QUEUED)
        session.add(new_job)
        session.commit()
        session.refresh(new_job)
        process_video.delay(new_job.id, file)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    return JobDto.model_validate(new_job)


def get_job(id: int) -> JobDto | None:
    session = SessionLocal()
    try:
        job = session.query(Job).get(id)
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
