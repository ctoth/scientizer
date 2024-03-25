import requests
from mendeley import Mendeley
from datastore.database import Session, Paper
import os
from datetime import datetime

class MendeleyRetriever:
    def __init__(self, client_id, client_secret):
        self.mendeley = Mendeley(os.environ.get('MENDELEY_CLIENT_ID'), os.environ.get('MENDELEY_CLIENT_SECRET'))
        self.session = self.mendeley.start_client_credentials_flow().authenticate()

    def retrieve_papers(self, query):
        papers = self.session.catalog.search(query, view='bib')
        db_session = Session()
        for paper in papers.iter():
            # Extract relevant metadata
            title = paper.title
            authors = ', '.join([author['name'] for author in paper.authors])
            abstract = paper.abstract
            altmetric_score = paper.scores.get('altmetric_score')

            # Save the paper to the database
            new_paper = Paper(
                title=title,
                authors=authors,
                abstract=abstract,
                altmetric_score=altmetric_score,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db_session.add(new_paper)

            # Push the paper ID to the task queue for further processing
            # This part is left as a placeholder for integration with a task queue system
            # task_queue.enqueue('process_paper', new_paper.id)

        db_session.commit()
        db_session.close()

# Example usage:
# retriever = MendeleyRetriever()
# retriever.retrieve_papers('machine learning')
