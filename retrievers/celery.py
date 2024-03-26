from celery import Celery
from decouple import config

# Initialize Celery


app = Celery('tasks', broker=config('CELERY_BROKER_URL',
             default='sqla+sqlite:///celerydb.sqlite'))
