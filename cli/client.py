import sys
import os


def run():
    arg_l = sys.argv
    file_paths = __get_valid_file_paths(arg_l[1], arg_l[2])


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


if __name__ == "__main__":
    run()
