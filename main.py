from retrievers.mendeley import MendeleyRetriever
from retrievers.tasks import app as celery_app
import logging

def main():
    # Configure logging to show info level messages
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Check if Celery workers are running
    try:
        inspector = celery_app.control.inspect()
        workers = inspector.ping()
        if not workers:
            logging.error("No Celery workers are running. Please start the workers to process tasks.")
            return
    except IOError as e:
        logging.error(f"Unable to connect to the Celery broker: {e}")
        return

    # Initialize the MendeleyRetriever
    retriever = MendeleyRetriever()

    # Define the query for paper retrieval
    query = 'machine learning'

    # Start the paper retrieval process
    retriever.retrieve_papers(query)

if __name__ == '__main__':
    main()
