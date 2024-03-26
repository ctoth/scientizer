#!/bin/bash

# Start the Celery worker and beat scheduler
celery -A retrievers.tasks worker --loglevel=info --beat
