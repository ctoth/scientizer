from celery import Celery
from detectors.ai_scorer import OpenAIScorer, AnthropicScorer
from datastore.database import Session, Paper, ErrorScore
from datetime import datetime

# Initialize Celery
app = Celery('tasks', broker='your_broker_url')

@app.task
def score_paper(paper_id):
    with Session() as db_session:
        paper = db_session.query(Paper).get(paper_id)
        if paper:
            # Initialize the AI scorer (replace with actual implementation)
            scorer = OpenAIScorer(api_key='your_api_key', prompt='your_prompt')
            score, explanation = scorer.score_paper(paper.abstract)

            # Store the score in the ErrorScore table
            error_score = ErrorScore(
                paper_id=paper.id,
                score=score,
                explanation=explanation,
                created_at=datetime.now()
            )
            db_session.add(error_score)
            db_session.commit()
