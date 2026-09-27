# SmartHire AI 💼
> An enterprise-grade, automated resume screening and candidate ranking system built with Python, NLP, and Streamlit.
---

## 📌 Overview
**SmartHire AI** simplifies talent acquisition by automatically parsing candidate resumes, matching key technical skills against job descriptions, and generating objective ATS scores. The system features multi-page navigation, database persistence, and interactive recruiter analytics.

---

## ✨ Key Features
* **📄 Multi-Format Resume Parsing:** Supports PDF document parsing using `PyMuPDF`.
* **🧠 Hybrid ATS Scoring Engine:** Combines TF-IDF vector similarity (30%), explicit skill overlap (40%), work experience heuristics (15%), education alignment (10%), and project/section validation (5%).
* **📊 Interactive Leaderboard:** Ranks candidates with dynamic filtering by status (*Shortlist*, *Strong Candidate*, *Review*, *Reject*) and live search.
* **🔎 Candidate Evaluation Audit:** Detailed sub-page decomposing candidate scores, matched skills, missing skills, and extracted text.
* **📈 Recruiter Analytics:** High-level dashboard displaying candidate distribution and common skill gaps across applicant pools.
* **💾 Data Persistence:** Powered by SQLite to preserve evaluated batch candidate data across sessions.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **NLP & Scoring:** Scikit-learn (TF-IDF Vectorizer), PyMuPDF, NLTK
* **Database:** SQLite3
* **Data Processing:** Pandas, NumPy

---