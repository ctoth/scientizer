import logging.config
from datetime import datetime

from decouple import config

from datastore.database import ErrorScore, Paper, Session
from detectors.ai_scorer import AnthropicScorer, OpenAIScorer

from .celery import app

logging_config = {
    'version': 1,
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
}
logging.config.dictConfig(logging_config)

logging.info(f"Celery is configured with broker: {app.conf.broker_url}")
logging.info(f"Registered tasks: {app.tasks.keys()}")


@app.task
def score_paper(paper_id):
    with Session() as db_session:
        paper = db_session.query(Paper).get(paper_id)
        if not paper:
            logging.error(f"Paper with ID {paper_id} not found.")
            return
        logging.info(
            f"Retrieved paper with ID {paper_id} for scoring: {paper.title}")
        score, explanation, scorer_type = score_abstract(paper.abstract)

        # If the score is successfully generated, store it in the ErrorScore table
        # Store the score in the ErrorScore table
        error_score = ErrorScore(
            paper_id=paper.id,
            score=score,
            explanation=explanation,
            scorer=scorer_type,  # Store the type of scorer used
            created_at=datetime.now()
        )
        db_session.add(error_score)
        db_session.commit()
    logging.info(f"Successfully stored score for paper with ID {paper_id}")


def score_abstract(abstract):
    # Initialize the AI scorer with the correct API key from environment variables
    # The scorer used can be configured via an environment variable
    scorer_type = config('SCORER_TYPE', default='OpenAI')
    api_key = config('SCORER_API_KEY')
    if scorer_type == 'OpenAI':
        scorer = OpenAIScorer(api_key=api_key)
    elif scorer_type == 'Anthropic':
        scorer = AnthropicScorer(api_key=api_key)
    else:
        logging.error(f"Invalid scorer type: {scorer_type}")
        raise ValueError(f"Invalid scorer type: {scorer_type}")
    try:
        score, explanation = scorer.score_paper(abstract)
        # Log the beginning of the abstract
        logging.info(f"Scoring abstract: {abstract[:30]}...")
        logging.info(
            f"Scored abstract: Score - {score}, Explanation - {explanation}")
        return score, explanation, scorer_type
    except Exception as e:
        # If an error occurs during scoring, log the error and exit the function
        logging.error(f"Error scoring abstract: {e}")
        return None, None, scorer_type  # Return None values to indicate failure
