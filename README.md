# Async Video Transcoding App

## About the Project

The Async Video Transcoding App is a Homework project for [NAVA](https://nava.hu/).


### Core Features

* **Python API:** A Flask-based API for video uploading and state querying.
* **Video Processing Pipeline:** A pipeline for video processing built with Celery library and using ffmpeg and ffprobe for video processing and metadata extraction.
* **Priority Queue:** There are tow queues the workers are subscribed to and the jobs are allocated based on the request's priority state and the to be processed file's size
* **Frontend:** One way to interact with the API is through a minimal yet tasteful React frontend which list the jobs and show the processed videos' thumbnail images and previews
* **CLI client:** A Python client to interact with the API
* **Powershell Demo Script:** A demo script to show the app starts up
* **Dockerization:** The application can be run with Docker Compose


### Built with

* [![Python][Python-ico]][Python-url]
* [![Flask][Flask-ico]][Flask-url]
* [![ffmpeg][ffmpeg-ico]][ffmpeg-url]
* [![Celery][celery-ico]][celery-url]
* [![Docker][Docker-ico]][Docker-url]
* [![PostgreSQL][PostgreSQL-ico]][PostgreSQL-url]
* [![SQLAlchemy][SQLAlchemy-ico]][SQLAlchemy-url]
* [![Redis][Redis-ico]][Redis-url]
* [![TypeScript][TS-ico]][TS-url]
* [![React][React-ico]][React-url]




## Getting Started

### Prerequisites

* **Docker Desktop:** You can download from here: [Docker Desktop][Docker-Desktop]. You have to sign up to use the Docker Desktop app.
* **For the CLI client**
    * Python 3.9 or higher: [Python download][Python-download]
    * pip (Python package manager): [pip installation][pip-installation]

### Download app

* You can download the application here: [BMG GitHub page](https://github.com/mecsbalint/boci-minesweeper-game). Click on the Code button and choose the Download ZIP option. After downloading unzip it.
* Or alternatively clone the repository: ```git clone https://github.com/mecsbalint/boci-minesweeper-game```

### Set Up and Run

1. **Install and Run Docker Desktop:** Download and run the installation file and follow the steps. After installation run the Docker Desktop application.
2. **Set up .env file:** Rename the `.env.example` file to `.env` in the app's root folder and optionally set up the env variables (but they all have default values).
3. **Build the Docker Images:** Run the `docker_build.bat` batch file from the application's root folder.
4. **Start the Application:** Run the `docker_start.bat` batch file from the application's root folder.

### Access the Application
1. **With Frontend:** Open a web browser and go to `http://localhost:` + `FRONTEND_PORT_NUMBER` to access the frontend (by default it's `http://localhost:5173`). The port number can be changed in the `.env` file.
2. **With CLI client:**
    1. Install dependencies: from the root folder run the `cd cli` and the `pip install -r requirements.txt` commands
    2. Start the CLI client: run the `python client.py` command with the neccessary arguments (see below)

### Stop the Application

* Run the `docker_stop.bat` batch file from the application's root folder.

## How to use CLI client
**Usage**
* `python client.py <mode> [path] [options]`

**Modes** 
* `batch_upload` (upload all files from a folder) 
* `single_upload` (upload a single file)

**Options**
* `--priority {high,low}` (set upload priority)
* `--wait` (wait for the upload(s) to be completed)

**Example**
* `python client.py single_upload example.mp4 --priority high --wait` (Upload single file with high priority request and wait until the upload is finished with either done or failed state)


## Contact

mecsbalint@gmail.com - https://github.com/mecsbalint


<!-- Links -->

[Docker-Desktop]: https://www.docker.com/products/docker-desktop/
[pip-installation]: https://pip.pypa.io/en/latest/installation/
[Python-download]: https://www.python.org/downloads/


[ffmpeg-ico]: https://img.shields.io/badge/ffmpeg-35422E?style=for-the-badge&logo=ffmpeg
[ffmpeg-url]: https://www.ffmpeg.org/

[TS-ico]: https://img.shields.io/badge/TypeScript-687959?style=for-the-badge&logo=typescript
[TS-url]: https://www.typescriptlang.org/

[React-ico]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react
[React-url]: https://reactjs.org/

[SQLAlchemy-ico]: https://img.shields.io/badge/SQLAlchemy-35495E?style=for-the-badge&logo=sqlalchemy
[SQLAlchemy-url]: https://www.sqlalchemy.org/

[Docker-ico]: https://img.shields.io/badge/Docker-DD0031?style=for-the-badge&logo=docker
[Docker-url]: https://www.docker.com/

[PostgreSQL-ico]: https://img.shields.io/badge/PostgreSQL-4A4A55?style=for-the-badge&logo=postgresql
[PostgreSQL-url]: https://www.postgresql.org/

[Python-ico]: https://img.shields.io/badge/Python-ADD8E6?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/

[Pytest-ico]: https://img.shields.io/badge/Pytest-c7d302?style=for-the-badge&logo=pytest
[Pytest-url]: https://flask.palletsprojects.com/en/stable/

[Flask-ico]: https://img.shields.io/badge/Flask-0d7560?style=for-the-badge&logo=flask
[Flask-url]: https://docs.pytest.org/en/stable/

[Redis-ico]: https://img.shields.io/badge/Redis-4A4A55?style=for-the-badge&logo=redis
[Redis-url]: https://redis.io/

[Celery-ico]: https://img.shields.io/badge/Celery-25c2a0?style=for-the-badge&logo=celery
[Celery-url]: https://docs.celeryq.dev/en/stable/#
