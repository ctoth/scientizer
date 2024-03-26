from datastore.database import Session, Paper, ErrorScore

def rank_papers_by_error_score():
    with Session() as db_session:
        # Retrieve all papers and their corresponding error scores
        # Join the papers with their error scores and order by the error score
        ranked_papers_query = db_session.query(Paper, ErrorScore.score).\
            outerjoin(ErrorScore, Paper.id == ErrorScore.paper_id).\
            order_by(ErrorScore.score.asc())

        # Execute the query and return the results
        ranked_papers = ranked_papers_query.all()
        return ranked_papers
