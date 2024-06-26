from datastore.database import ErrorScore
from detectors.ai_scorer import OpenAIScorer, AnthropicScorer
import requests
from mendeley import Mendeley
from datastore.database import Session, Paper
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .tasks import score_paper
from concurrent.futures import ThreadPoolExecutor
import os


import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class MendeleyRetriever:
    def __init__(self):
        self.mendeley = Mendeley(
            config('MENDELEY_CLIENT_ID'), config('MENDELEY_CLIENT_SECRET'))
        self.session = self.mendeley.start_client_credentials_flow().authenticate()

    def retrieve_papers(self, topic):
        num_workers = os.cpu_count()  # Default to the number of CPUs
        max_workers = config('THREAD_POOL_MAX_WORKERS',
                             default=num_workers, cast=int)
        logging.info(f"Starting retrieval of papers for topic: {topic}")
        papers = self.session.catalog.search(topic, view='bib')
        executor = ThreadPoolExecutor(max_workers=max_workers)
        try:
            with Session() as db_session:
                for paper in papers.iter():
                    logging.info(f"Processing paper: {paper.title}")
                    # Extract relevant metadata
                    title = paper.title
                    if not paper.authors:
                        logging.info(
                            f"Skipping paper without authors: {title}")
                        continue
                    authors = ', '.join(
                        [f"{author.first_name} {author.last_name}" for author in paper.authors])
                    abstract = paper.abstract
                    ...

                    # Save the paper to the database
                    if abstract:  # Only process papers with an abstract

                        new_paper = Paper(
                            title=title,
                            authors=authors,
                            abstract=abstract,
                            altmetric_score=None,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        db_session.add(new_paper)
                        db_session.flush()  # Flush to assign an ID to new_paper

                        # Asynchronously enqueue the scoring task using Celery
                        score_paper.delay(new_paper.id)

                logging.info(
                    "Successfully saved all retrieved papers to the database.")
                db_session.commit()
        except SQLAlchemyError as e:
            logging.error(f"An error occurred while saving papers: {e}")
        finally:
            executor.shutdown(wait=False)

# Example usage:
# retriever = MendeleyRetriever()
# retriever.retrieve_papers('machine learning')
