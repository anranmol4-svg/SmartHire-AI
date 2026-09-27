import re
from typing import Dict, List
from utils.skill_extractor import analyze_skill_overlap

def extract_experience_years(text: str) -> int:
    """
    Extracts maximum work experience years using regex heuristics.
    e.g. '5+ years experience', '3 yrs', '4 years in software engineering'
    """
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)?',
        r'(?:experience|exp)\s*:\s*(\d+)\+?\s*(?:years?|yrs?)'
    ]
    
    found_years = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            val = int(match)
            if val < 45:  # Sanity check: exclude numbers like year 2024 or 50+
                found_years.append(val)
                
    return max(found_years) if found_years else 0

def calculate_ats_score(
    similarity_score: float, 
    raw_resume_text: str, 
    raw_jd_text: str,
    skill_db_path: str = "data/skills.csv"
) -> Dict:
    """
    Calculates a balanced ATS Score out of 100 with non-linear scaling.
    """
    # 1. Skill Match Analysis (40%)
    skill_analysis = analyze_skill_overlap(raw_resume_text, raw_jd_text, skill_db_path)
    jd_skills = skill_analysis["jd_skills"]
    matched_skills = skill_analysis["matched_skills"]
    
    if jd_skills:
        # Instead of strict linear ratio, cap denominator at top 8 essential skills
        # or use a soft curve so candidates aren't penalized for massive JDs
        coverage = len(matched_skills) / min(len(jd_skills), 8)
        skill_ratio = min(1.0, coverage)
    else:
        skill_ratio = 0.5
        
    skill_score = skill_ratio * 40.0

    # 2. Scaled TF-IDF Similarity Weight (30%)
    # Cosine values between 0.10 and 0.35 are strong for multi-page documents.
    # We apply non-linear scaling: min(1.0, similarity * 2.5)
    scaled_sim = min(1.0, similarity_score * 2.5)
    sim_score = scaled_sim * 30.0

    # 3. Experience Match Heuristic (15%)
    exp_years = extract_experience_years(raw_resume_text)
    exp_score = min((exp_years / 3.0) * 15.0, 15.0) if exp_years > 0 else 7.5 # Default fallback

    # 4. Education Heuristic (10%)
    edu_keywords = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'b.s.', 'm.s.', 'degree', 'computer', 'engineering']
    has_edu = any(k in raw_resume_text.lower() for k in edu_keywords)
    edu_score = 10.0 if has_edu else 5.0

    # 5. Projects & Certifications (5%)
    proj_keywords = ['project', 'certification', 'certified', 'portfolio', 'publication', 'github', 'experience']
    has_proj = any(k in raw_resume_text.lower() for k in proj_keywords)
    proj_score = 5.0 if has_proj else 2.5

    # Total ATS Score
    total_ats = round(skill_score + sim_score + exp_score + edu_score + proj_score, 2)
    total_ats = max(0.0, min(100.0, total_ats))

    return {
        "ats_score": total_ats,
        "similarity_pct": round(similarity_score * 100, 2),
        "matched_skills": matched_skills,
        "missing_skills": skill_analysis["missing_skills"],
        "extra_skills": skill_analysis["extra_skills"],
        "extracted_exp_years": exp_years,
        "breakdown": {
            "skill_score": round(skill_score, 2),
            "similarity_score": round(sim_score, 2),
            "experience_score": round(exp_score, 2),
            "education_score": round(edu_score, 2),
            "projects_score": round(proj_score, 2)
        }
    }