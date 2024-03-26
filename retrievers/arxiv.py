import logging
import requests
from datetime import datetime
from datastore.database import Session, Paper
from .tasks import score_paper

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ArxivRetriever:
    ARXIV_API_URL = 'http://export.arxiv.org/api/query'

    def retrieve_papers(self, topic, max_results=100):
        params = {
            'search_query': f'all:{topic}',
            'start': 0,
            'max_results': max_results
        }
        response = requests.get(self.ARXIV_API_URL, params=params)
        if response.status_code == 200:
            self._process_response(response.text)
        else:
            logging.error(f"Arxiv API request failed with status code: {response.status_code}")

    def _process_response(self, response_xml):
        # This method should parse the XML response from the Arxiv API
        # and store the retrieved papers in the database.
        # XML parsing and database storage logic goes here.
        pass

# Example usage:
# retriever = ArxivRetriever()
# retriever.retrieve_papers('quantum physics')
