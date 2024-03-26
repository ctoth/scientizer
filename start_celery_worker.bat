@echo off

REM Start the Celery worker and beat scheduler
celery -A retrievers.tasks worker --loglevel=info --beat
pause
@echo off

REM Start the Celery worker and beat scheduler
celery -A retrievers.tasks worker --loglevel=info --beat
pause
