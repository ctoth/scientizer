from celery import Celery
from decouple import config

# Initialize Celery
app = Celery('task_queue', broker=config('CELERY_BROKER_URL', default='redis://localhost:6379/0'))

@app.task
def process_paper(paper_id):
    # Placeholder for the paper processing logic
    # This should be replaced with the actual processing code
    print(f"Processing paper with ID: {paper_id}")
