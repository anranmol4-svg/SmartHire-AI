import streamlit as st
import pandas as pd
from utils.database import fetch_all_candidates

st.set_page_config(page_title="SmartHire AI - Candidate Audit", layout="wide")

# Custom Typography and Footer
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .author-footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: transparent; color: #94A3B8;
        text-align: center; padding: 8px 0; font-size: 13px; font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Candidate Evaluation Report")
st.caption("SmartHire AI Audit System")
st.markdown("Detailed ATS score breakdown, identified skill coverage, and extracted resume content.")

st.divider()

candidates = fetch_all_candidates()

if not candidates:
    st.info("No candidate data found. Please run an evaluation on the main page first.")
else:
    candidate_options = {f"Rank #{c['rank']} - {c['filename']} (Score: {c['ats_score']})": c for c in candidates}
    selected_label = st.selectbox("Select Candidate:", list(candidate_options.keys()))
    candidate = candidate_options[selected_label]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ATS Score", f"{candidate['ats_score']} / 100")
    col2.metric("TF-IDF Similarity", f"{candidate['similarity_pct']}%")
    col3.metric("Rank", f"#{candidate['rank']}")
    col4.metric("Status", candidate['status'])

    st.divider()

    st.subheader("Score Decomposition")
    bd = candidate["breakdown"]
    
    bd_df = pd.DataFrame([
        {"Component": "Skill Match (40%)", "Awarded Score": bd["skill_score"], "Maximum": 40.0},
        {"Component": "Text Similarity (30%)", "Awarded Score": bd["similarity_score"], "Maximum": 30.0},
        {"Component": "Work Experience (15%)", "Awarded Score": bd["experience_score"], "Maximum": 15.0},
        {"Component": "Education Match (10%)", "Awarded Score": bd["education_score"], "Maximum": 10.0},
        {"Component": "Projects & Section Quality (5%)", "Awarded Score": bd["projects_score"], "Maximum": 5.0}
    ])
    
    st.dataframe(bd_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Skill Alignment")
    
    skill_col1, skill_col2 = st.columns(2)
    
    with skill_col1:
        st.markdown(f"**Matched Skills ({len(candidate['matched_skills'])})**")
        if candidate['matched_skills']:
            st.write(", ".join([f"`{s}`" for s in candidate['matched_skills']]))
        else:
            st.write("No explicit skill matches detected.")
            
    with skill_col2:
        st.markdown(f"**Missing Skills ({len(candidate['missing_skills'])})**")
        if candidate['missing_skills']:
            st.write(", ".join([f"`{s}`" for s in candidate['missing_skills']]))
        else:
            st.write("All required skills satisfied.")

    st.divider()
    with st.expander("View Raw Extracted Resume Content"):
        st.text_area("Parsed Text:", candidate["raw_text"], height=300)

st.markdown('<div class="author-footer">By Anmol Singh</div>', unsafe_allow_html=True)