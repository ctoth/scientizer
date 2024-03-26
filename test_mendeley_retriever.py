import pytest
from retrievers.mendeley import MendeleyRetriever


class TestMendeleyRetriever:
    def test_retrieve_papers(self, mocker):
        # Initialize the MendeleyRetriever
        retriever = MendeleyRetriever()

        # Define the query for paper retrieval
        query = 'test query'
