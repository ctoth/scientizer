from datastore.database import Session, Paper, ErrorScore

def rank_papers():
    with Session() as db_session:
        # Retrieve all papers and their corresponding error scores
        papers = db_session.query(Paper).all()
        ranked_papers = []
        for paper in papers:
            error_score = db_session.query(ErrorScore).filter(ErrorScore.paper_id == paper.id).one_or_none()
            # Normalize scores to a 0 to 1 scale
            normalized_altmetric = (paper.altmetric_score or 0) / 1000
            normalized_error = (error_score.score if error_score else 0) / 100

            # Apply weights to each score
            # Assuming altmetric score is twice as important as error score
            weighted_altmetric = normalized_altmetric * 0.67
            weighted_error = normalized_error * 0.33

            # Calculate the final combined score
            combined_score = weighted_altmetric - weighted_error

            # Add the paper and its combined score to the list
            ranked_papers.append((paper, combined_score))

        # Sort the papers by the combined score in descending order
        ranked_papers.sort(key=lambda x: x[1], reverse=True)

        # Return the ranked list of papers
        return [paper for paper, score in ranked_papers]
