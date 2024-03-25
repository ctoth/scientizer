from celery import Celery
from decouple import config
from datastore.database import Session, Paper, ErrorScore
from detectors.ai_scorer import OpenAIScorer, AnthropicScorer

# Initialize Celery
app = Celery('task_queue', broker=config('CELERY_BROKER_URL', default='redis://localhost:6379/0'))

@app.task
def process_paper(paper_id):
    with Session() as db_session:
        paper = db_session.query(Paper).get(paper_id)
        if paper:
            # Initialize AI scorers
            openai_scorer = OpenAIScorer(config('OPENAI_API_KEY'), config('OPENAI_PROMPT'))
            anthropic_scorer = AnthropicScorer(config('ANTHROPIC_API_KEY'), config('ANTHROPIC_PROMPT'))

            # Score the paper
            openai_score, openai_explanation = openai_scorer.score_paper(paper.abstract)
            anthropic_score, anthropic_explanation = anthropic_scorer.score_paper(paper.abstract)

            # Save the scores to the database
            openai_error_score = ErrorScore(paper_id=paper.id, score=openai_score, explanation=openai_explanation, created_at=datetime.now())
            anthropic_error_score = ErrorScore(paper_id=paper.id, score=anthropic_score, explanation=anthropic_explanation, created_at=datetime.now())

            db_session.add(openai_error_score)
            db_session.add(anthropic_error_score)
            db_session.commit()
