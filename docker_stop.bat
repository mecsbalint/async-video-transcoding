@echo off
echo Stopping and removing containers...
docker-compose down -v --remove-orphans
pause
