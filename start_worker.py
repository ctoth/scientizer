import argparse
import os
from decouple import config
from retrievers.tasks import setup_periodic_tasks
from retrievers.celery import app as celery_app

def start_worker(role):
    # Set environment variables for the Celery worker
    os.environ['CELERY_WORKER_ROLE'] = role
    os.environ['DATABASE_URL'] = config('DATABASE_URL')
    os.environ['BROKER_URL'] = config('CELERY_BROKER_URL')
    os.environ['RESULT_BACKEND'] = config('CELERY_RESULT_BACKEND')

    # Register the worker with the system (if needed)
    # This can be done by sending a message to a central service or updating a database
    # For example:
    # register_worker(role)

    # Start the Celery worker
    if role == 'retriever':
        setup_periodic_tasks()
        celery_app.worker_main(['worker', '--loglevel=info', '--beat'])
    elif role == 'scorer':
        celery_app.worker_main(['worker', '--loglevel=info'])
    else:
        raise ValueError(f"Unknown worker role: {role}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a Celery worker with a specified role.')
    parser.add_argument('role', choices=['retriever', 'scorer'], help='The role of the worker to start')
    args = parser.parse_args()
    start_worker(args.role)
