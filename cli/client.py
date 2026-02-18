import sys
import os
from typing import Literal, cast
import requests
from dotenv import load_dotenv
import time

load_dotenv("..\\.env")

API_PORT_NUMBER = os.getenv("API_PORT_NUMBER")


def run():
    arg_l = sys.argv

    if arg_l[1] not in ["single_upload", "batch_upload"]:
        if len(arg_l) < 3:
            raise Exception("Illegal arguments. The first option has to have an argument.")

        file_paths = __get_valid_file_paths(arg_l[1], arg_l[2])

        is_wait, priority = __get_upload_options(arg_l[4:])

        processed_jobs = __send_uploads_requests(file_paths, priority)

        if len(processed_jobs) == 0:
            print(f"There were no valid files set as file or folder in the arg [{arg_l[2]}]")
        elif is_wait:
            while next(iter([job[0] for job in processed_jobs if job[1] in ["queued", "running"]]), None):
                time.sleep(10)
                __send_check_requests(processed_jobs)
                __print_jobs(processed_jobs)
        else:
            __print_jobs(processed_jobs)

        print("Processing finished")

    else:
        raise Exception("Illegal arguments. The first option of the command must be 'single_upload', 'batch_upload' or 'check_job")


def __get_valid_file_paths(run_type: str, rel_path: str) -> list[str]:

    file_paths: list[str] = []

    abs_path = os.path.abspath(rel_path)
    if not os.path.exists(abs_path):
        raise Exception("Illegal argument. The file or folder set as upload argument must exist.")

    if run_type == "single_upload":
        if os.path.isfile(abs_path):
            file_paths.append(abs_path)
        else:
            raise Exception("Illegal argument. The 'single_upload' command must set a file as argument and not a folder")
    else:
        if not os.path.isfile(abs_path):
            for file in os.listdir(abs_path):
                if os.path.isfile(file):
                    file_paths.append(file)
        else:
            raise Exception("Illegal argument. The 'batch_upload' command must set a folder as argument and not a file")

    return file_paths


def __get_upload_options(sub_arg: list[str]) -> tuple[bool, Literal["high", "low"]]:
    priority = "low"
    is_wait = False
    for arg in sub_arg:
        if arg == "--wait":
            is_wait = True
        if arg == "--priority":
            value = sub_arg.pop()
            if value not in ["high", "low"]:
                raise Exception("Illegal argument. The --priority option must be either high or low")
            else:
                priority = cast(Literal["high", "low"], value)
    return is_wait, priority


def __send_uploads_requests(file_paths: list[str], priority: Literal["high", "low"]) -> list[list[str]]:
    jobs: list[list[str]] = []

    for path in file_paths:
        print(f"Start process file {path}")
        with open(path, "rb") as file:
            response = requests.post(f"http://localhost:{API_PORT_NUMBER}/api/uploads?priority={priority}", files={"video": file})
            if response.status_code == 201:
                response_body = cast(dict[str, str], response.json())
                jobs.append([response_body["id"], response_body["state"], path])
        print("Finished process file {path}")

    return jobs


def __send_check_requests(processed_jobs: list[list[str]]):
    for job in processed_jobs:
        if job[1] in ["queued", "rubbing"]:
            response = requests.get(f"http://localhost:{API_PORT_NUMBER}/api/jobs/{job[0]}")
            if response.status_code == 200:
                response_body = cast(dict[str, str], response.json())
                job[1] = response_body["state"]


def __print_jobs(processed_jobs: list[list[str]]):
    print("Processed jobs:")
    for job in processed_jobs:
        print(f"Id: {job[0]} | State: {job[1]} | OG File: {job[2]}")


if __name__ == "__main__":
    run()
