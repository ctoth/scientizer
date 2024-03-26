from celery import Celery
from decouple import config
from detectors.ai_scorer import OpenAIScorer, AnthropicScorer
from datastore.database import Session, Paper, ErrorScore
from datetime import datetime
import logging.config

# Initialize Celery
app = Celery('tasks', broker=config('CELERY_BROKER_URL', default='sqla+sqlite:///celerydb.sqlite'))

logging.config.dictConfig({
    'version': 1,
    ...
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
})

logging.info(f"Celery is configured with broker: {app.conf.broker_url}")
logging.info(f"Registered tasks: {app.tasks.keys()}")

@app.task
def score_paper(paper_id):
    # Task implementation remains the same
    with Session() as db_session:
        paper = db_session.query(Paper).get(paper_id)
        if not paper:
            logging.error(f"Paper with ID {paper_id} not found.")
            return
        logging.info(f"Retrieved paper with ID {paper_id} for scoring: {paper.title}")
        # Initialize the AI scorer (replace with actual implementation)
        scorer = OpenAIScorer(api_key='your_api_key', prompt='your_prompt')
        try:
            score, explanation = scorer.score_paper(paper.abstract)
            logging.info(f"Scoring paper with ID {paper_id}: {paper.title}")
            logging.info(f"Scored paper with ID {paper_id}: Score - {score}, Explanation - {explanation}")
        except Exception as e:
            # If an error occurs during scoring, log the error and exit the function
            logging.error(f"Error scoring paper with ID {paper_id}: {e}")
            raise  # Re-raise the exception to ensure it's captured by the Celery worker
            return

        # If the score is successfully generated, store it in the ErrorScore table
        # Store the score in the ErrorScore table
        error_score = ErrorScore(
            paper_id=paper.id,
            score=score,
            explanation=explanation,
            created_at=datetime.now()
        )
        db_session.add(error_score)
        db_session.commit()
        logging.info(f"Successfully stored score for paper with ID {paper_id}")
        logging.info(f"Successfully stored score for paper with ID {paper_id}")
