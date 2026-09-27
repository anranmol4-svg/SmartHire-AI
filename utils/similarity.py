from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
import numpy as np

def compute_similarity_scores(jd_cleaned: str, resumes_cleaned: List[str]) -> List[float]:
    """
    Computes Cosine Similarity between a cleaned Job Description 
    and a list of cleaned candidate resumes using TF-IDF.
    
    Args:
        jd_cleaned (str): Cleaned Job Description text.
        resumes_cleaned (List[str]): List of cleaned Resume texts.
        
    Returns:
        List[float]: Similarity score ratios between 0.0 and 1.0 for each resume.
    """
    if not jd_cleaned or not resumes_cleaned:
        return [0.0] * len(resumes_cleaned)
    
    # Combine JD and Resumes into a single corpus for vocabulary fitting
    corpus = [jd_cleaned] + resumes_cleaned
    
    # Configure Vectorizer
    # ngram_range=(1,2) allows catching uni-grams ('python') and bi-grams ('machine learning')
    vectorizer = TfidfVectorizer(ngram_range=(1, 1), sublinear_tf=True, min_df=1)
    
    # Fit and transform corpus into TF-IDF sparse matrix
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # JD vector is at index 0, candidate resume vectors start at index 1
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]
    
    # Compute pair-wise cosine similarity between JD vector and all Resume vectors
    similarity_matrix = cosine_similarity(jd_vector, resume_vectors)
    
    # Flatten 2D array to 1D list of scores
    scores = similarity_matrix.flatten().tolist()
    
    # Ensure scores stay bounded between 0.0 and 1.0
    return [max(0.0, min(1.0, float(score))) for score in scores]