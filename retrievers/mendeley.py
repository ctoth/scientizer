import requests
from mendeley import Mendeley
from datastore.database import Session, Paper
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .task_queue import process_paper


import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from detectors.ai_scorer import OpenAIScorer, AnthropicScorer
from datastore.database import ErrorScore

class MendeleyRetriever:
    def __init__(self):
        self.mendeley = Mendeley(
            config('MENDELEY_CLIENT_ID'), config('MENDELEY_CLIENT_SECRET'))
        self.session = self.mendeley.start_client_credentials_flow().authenticate()
    def score_abstract(self, abstract):
        # Initialize the AI scorer (replace with actual implementation)
        scorer = OpenAIScorer(api_key='your_api_key', prompt='your_prompt')
        score, explanation = scorer.score_paper(abstract)
        return score, explanation

    def retrieve_papers(self, query):
        logging.info(f"Starting retrieval of papers for query: {query}")
        papers = self.session.catalog.search(query, view='bib')
        try:
            with Session() as db_session:
                for paper in papers.iter():
                    logging.info(f"Processing paper: {paper.title}")
                    # Extract relevant metadata
                    title = paper.title
                    if not paper.authors:
                        logging.info(f"Skipping paper without authors: {title}")
                        continue
                    authors = ', '.join([f"{author.first_name} {author.last_name}" for author in paper.authors])
                    abstract = paper.abstract
                    ...

                    # Save the paper to the database
                    if abstract:  # Only process papers with an abstract
                        score, explanation = self.score_abstract(abstract)

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

                        # Store the score in the ErrorScore table
                        error_score = ErrorScore(
                            paper_id=new_paper.id,
                            score=score,
                            explanation=explanation,
                            created_at=datetime.now()
                        )
                        db_session.add(error_score)

                        # Push the paper ID to the task queue for further processing
                        process_paper.delay(new_paper.id)

                logging.info("Successfully saved all retrieved papers to the database.")
                db_session.commit()
        except SQLAlchemyError as e:
            logging.error(f"An error occurred while saving papers: {e}")

# Example usage:
# retriever = MendeleyRetriever()
# retriever.retrieve_papers('machine learning')
