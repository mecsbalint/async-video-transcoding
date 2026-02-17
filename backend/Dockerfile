FROM mwader/static-ffmpeg:8.0 AS ffmpeg
FROM python:3.13.7-slim
RUN apt-get update && \
    apt-get install -y libpq-dev gcc
COPY --from=ffmpeg /ffmpeg /usr/local/bin/ffmpeg
COPY --from=ffmpeg /ffprobe /usr/local/bin/ffprobe
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
