import pandas as pd
import re
from typing import Set, Dict, List

def load_master_skills(skill_db_path: str = "data/skills.csv") -> Set[str]:
    """
    Loads master skill list from CSV.
    """
    try:
        skills_df = pd.read_csv(skill_db_path)
        return set(skills_df['skill'].str.lower().tolist())
    except Exception:
        # Fallback default set if file is missing/unreadable
        return {
            "python", "java", "c++", "sql", "machine learning", 
            "deep learning", "tensorflow", "pytorch", "scikit-learn", 
            "fastapi", "flask", "docker", "kubernetes", "aws", "azure", 
            "git", "github", "linux", "react", "node.js", "mongodb", 
            "mysql", "postgresql", "pandas", "numpy", "power bi", "excel"
        }

def extract_skills_from_text(text: str, master_skills: Set[str]) -> Set[str]:
    """
    Detects known skills in text using exact regex word boundary matching.
    """
    text_lower = text.lower()
    detected_skills = set()
    
    for skill in master_skills:
        # Escape special symbols (e.g. c++, node.js) and enforce word boundaries
        escaped_skill = re.escape(skill)
        pattern = r'(?<!\w)' + escaped_skill + r'(?!\w)'
        
        if re.search(pattern, text_lower):
            detected_skills.add(skill)
            
    return detected_skills

def analyze_skill_overlap(resume_text: str, jd_text: str, skill_db_path: str = "data/skills.csv") -> Dict[str, List[str]]:
    """
    Compares candidate skills against job description requirements.
    """
    master_skills = load_master_skills(skill_db_path)
    
    jd_skills = extract_skills_from_text(jd_text, master_skills)
    resume_skills = extract_skills_from_text(resume_text, master_skills)
    
    matched = jd_skills.intersection(resume_skills)
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills
    
    return {
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "extra_skills": sorted(list(extra)),
        "jd_skills": sorted(list(jd_skills)),
        "resume_skills": sorted(list(resume_skills))
    }