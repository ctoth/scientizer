from retrievers.mendeley import MendeleyRetriever
import logging

def main():
    # Configure logging to show info level messages
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the MendeleyRetriever
    retriever = MendeleyRetriever()

    # Define the query for paper retrieval
    query = 'machine learning'

    # Start the paper retrieval process
    retriever.retrieve_papers(query)

if __name__ == '__main__':
    main()
