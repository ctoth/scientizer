from celery import Celery
from decouple import config
from datastore.database import Session, Paper, ErrorScore
from detectors.ai_scorer import AIScorer, OpenAIScorer, AnthropicScorer
from datetime import datetime

# Initialize Celery
app = Celery('task_queue', broker='sqla+sqlite:///celerydb.sqlite', backend='db+sqlite:///celery_results.sqlite')

@app.task
def process_paper(paper_id):
    with Session() as db_session:
        paper = db_session.query(Paper).get(paper_id)
        if paper:
            # Determine which AI scorer to use
            scorer_name = config('AI_SCORER', default='OpenAI')
            if scorer_name == 'OpenAI':
                scorer = OpenAIScorer(config('OPENAI_API_KEY'), config('OPENAI_PROMPT'))
            elif scorer_name == 'Anthropic':
                scorer = AnthropicScorer(config('ANTHROPIC_API_KEY'), config('ANTHROPIC_PROMPT'))
            else:
                raise ValueError(f"Unsupported AI scorer: {scorer_name}")

            # Score the paper and save the score to the database
            score, explanation = scorer.score_paper(paper.abstract)
            error_score = ErrorScore(paper_id=paper.id, score=score, explanation=explanation, created_at=datetime.now())
            db_session.add(error_score)
            db_session.commit()
