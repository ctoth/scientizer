from retrievers.mendeley import MendeleyRetriever
from retrievers.tasks import app as celery_app
import logging
import sys

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

    # Get the topic from command-line arguments
    if len(sys.argv) < 2:
        logging.error("No topic specified. Usage: python main.py <topic>")
        return
    topic = sys.argv[1]

    # Start the paper retrieval process
    retriever.retrieve_papers(topic)

if __name__ == '__main__':
    main()
