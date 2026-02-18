import os


SMALL_FILE_MAX_SIZE = int(os.getenv("SMALL_FILE_MAX_SIZE", 0))

ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "").split(",")

SUBPROCESS_TIMEOUT = int(os.getenv("SUBPROCESS_TIMEOUT", 0))

NUM_OF_TRIES = int(os.getenv("NUM_OF_TRIES", 0))

RETRY_DELAY = int(os.getenv("RETRY_DELAY", 0))
