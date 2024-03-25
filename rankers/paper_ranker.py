from datastore.database import Session, Paper, ErrorScore

def rank_papers():
    with Session() as db_session:
        # Retrieve all papers and their corresponding error scores
        papers = db_session.query(Paper).all()
        ranked_papers = []
        for paper in papers:
            error_score = db_session.query(ErrorScore).filter(ErrorScore.paper_id == paper.id).one_or_none()
            if error_score:
                combined_score = (paper.altmetric_score or 0) - error_score.score
            else:
                combined_score = (paper.altmetric_score or 0)
            ranked_papers.append((paper, combined_score))

        # Sort the papers by the combined score in descending order
        ranked_papers.sort(key=lambda x: x[1], reverse=True)

        # Return the ranked list of papers
        return [paper for paper, score in ranked_papers]
