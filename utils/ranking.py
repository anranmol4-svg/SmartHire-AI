from typing import Dict, List

def assign_candidate_status(ats_score: float) -> str:
    """
    Categorizes candidate status based on total ATS score benchmarking.
    """
    if ats_score >= 65.0:
        return "Shortlist"
    elif ats_score >= 50.0:
        return "Strong Candidate"
    elif ats_score >= 35.0:
        return "Review"
    else:
        return "Reject"

def rank_candidates(candidate_list: List[Dict]) -> List[Dict]:
    """
    Sorts candidates descending by ATS score and assigns 1-based rank position.
    """
    # Sort by ATS score highest to lowest
    sorted_candidates = sorted(candidate_list, key=lambda x: x["ats_score"], reverse=True)
    
    # Assign rank numbers
    for index, candidate in enumerate(sorted_candidates, start=1):
        candidate["rank"] = index
        candidate["status"] = assign_candidate_status(candidate["ats_score"])
        
    return sorted_candidates