from retrievers.mendeley import MendeleyRetriever

def main():
    # Initialize the MendeleyRetriever
    retriever = MendeleyRetriever()

    # Define the query for paper retrieval
    query = 'machine learning'

    # Start the paper retrieval process
    retriever.retrieve_papers(query)

if __name__ == '__main__':
    main()
