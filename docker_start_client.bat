@echo off
echo Starting app with Docker Compose in detached mode...
docker-compose up -d

@REM In cmd run this command to use CLI: docker-compose run --rm cli client.py [args]

start cmd /k
