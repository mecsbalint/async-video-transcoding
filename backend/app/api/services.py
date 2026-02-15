import os
from werkzeug.datastructures import FileStorage
from app.api.dtos import JobDoneDto, JobDto, JobFailedDto
from app.database.session import SessionLocal
from app.database.models import Job
from app.job_state import JobState
from app.worker.video_worker import process_video
from app.folders import UPLOAD_FOLDER_PATH


def upload_video(video: FileStorage) -> JobDto:
    session = SessionLocal()
    output_file_path = None

    try:
        new_job = Job(state=JobState.QUEUED)
        session.add(new_job)
        session.commit()
        session.refresh(new_job)

        local_output_file_path = f"{new_job.id}/{video.filename}"
        print("Save original video ")
        output_file_path = f"{UPLOAD_FOLDER_PATH}/{local_output_file_path}"
        os.makedirs(f"{UPLOAD_FOLDER_PATH}/{new_job.id}")
        video.save(output_file_path)
        print(f"Original video file saved to: {output_file_path}")

        process_video.delay(new_job.id, output_file_path, local_output_file_path)

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
