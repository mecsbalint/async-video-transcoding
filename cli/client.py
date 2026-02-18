import sys
import os
from typing import cast
import requests


def run():
    arg_l = sys.argv
    file_paths = __get_valid_file_paths(arg_l[1], arg_l[2])

    processed_jobs = __send_requests(file_paths)

    print(processed_jobs)


def __get_valid_file_paths(run_type: str, rel_path: str) -> list[str]:
    if run_type not in ["single_upload", "batch_upload"]:
        raise Exception("Illegal argument. The first argument of the command must be either 'single_upload' or 'batch_upload'")

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


def __send_requests(file_paths: list[str]) -> list[tuple[str, str, str]]:
    jobs: list[tuple[str, str, str]] = []

    for path in file_paths:
        print(f"Start process file {path}")
        with open(path, "rb") as file:
            response = requests.post("http://api:8000/api/uploads", files={"video": file})
            if response.status_code == 201:
                response_body = cast(dict[str, str], response.json())
                jobs.append((response_body["id"], response_body["state"], path))
        print("Finished process file {path}")

    return jobs


if __name__ == "__main__":
    run()
