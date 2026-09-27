import sqlite3
import json
from typing import List, Dict, Optional

DB_PATH = "resume_matcher.db"

def init_db():
    """
    Initializes SQLite table structure if it does not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            raw_text TEXT,
            ats_score REAL,
            similarity_score REAL,
            status TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            breakdown_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_candidate_result(data: Dict):
    """
    Inserts or updates candidate assessment record in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO candidates 
        (filename, raw_text, ats_score, similarity_score, status, matched_skills, missing_skills, breakdown_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['filename'],
        data['raw_text'],
        data['ats_score'],
        data['similarity_pct'],
        data['status'],
        json.dumps(data['matched_skills']),
        json.dumps(data['missing_skills']),
        json.dumps(data['breakdown'])
    ))
    conn.commit()
    conn.close()

def fetch_all_candidates() -> List[Dict]:
    """
    Retrieves all ranked candidates ordered by ATS score descending.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, filename, ats_score, similarity_score, status, 
               matched_skills, missing_skills, breakdown_json, raw_text 
        FROM candidates 
        ORDER BY ats_score DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for rank, r in enumerate(rows, start=1):
        results.append({
            "rank": rank,
            "id": r[0],
            "filename": r[1],
            "ats_score": r[2],
            "similarity_pct": r[3],
            "status": r[4],
            "matched_skills": json.loads(r[5]),
            "missing_skills": json.loads(r[6]),
            "breakdown": json.loads(r[7]),
            "raw_text": r[8]
        })
    return results

def clear_all_candidates():
    """
    Resets database records for new screening batches.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates")
    conn.commit()
    conn.close()