from celery import Celery
from detectors.ai_scorer import OpenAIScorer, AnthropicScorer
from datastore.database import Session, Paper, ErrorScore
from datetime import datetime
import logging

# Initialize Celery
app = Celery('tasks', broker='your_broker_url')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.task
def score_paper(paper_id):
    with Session() as db_session:
        paper = db_session.query(Paper).get(paper_id)
        if not paper:
            logging.error(f"Paper with ID {paper_id} not found.")
        logging.info(f"Scoring paper with ID {paper_id}: {paper.title}")
        # Initialize the AI scorer (replace with actual implementation)
        scorer = OpenAIScorer(api_key='your_api_key', prompt='your_prompt')
        score, explanation = scorer.score_paper(paper.abstract)
        try:
            score, explanation = scorer.score_paper(paper.abstract)
            logging.info(f"Scored paper with ID {paper_id}: Score - {score}, Explanation - {explanation}")
        except Exception as e:
            logging.error(f"Error scoring paper with ID {paper_id}: {e}")
            return

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
