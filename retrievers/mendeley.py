import requests
from mendeley import Mendeley
from datastore.database import Session, Paper
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .task_queue import process_paper

class MendeleyRetriever:
    def __init__(self):
        self.mendeley = Mendeley(config('MENDELEY_CLIENT_ID'), config('MENDELEY_CLIENT_SECRET'))
        self.session = self.mendeley.start_client_credentials_flow().authenticate()

    def retrieve_papers(self, query):
        papers = self.session.catalog.search(query, view='bib')
        try:
            with Session() as db_session:
                for paper in papers.iter():
                    # Extract relevant metadata
                    title = paper.title
                    authors = ', '.join([f"{author.first_name} {author.last_name}" for author in paper.authors])
                    abstract = paper.abstract
                    ...

                    # Save the paper to the database
                    if abstract:  # Only process papers with an abstract
                        new_paper = Paper(
                        title=title,
                        authors=authors,
                        abstract=abstract,
                        altmetric_score=None,
                        altmetric_score=None,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                        db_session.add(new_paper)
                        db_session.flush()  # Flush to assign an ID to new_paper

                        # Push the paper ID to the task queue for further processing
                        process_paper.delay(new_paper.id)

                db_session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred while saving papers: {e}")

# Example usage:
# retriever = MendeleyRetriever()
# retriever.retrieve_papers('machine learning')
