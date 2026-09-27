import streamlit as st
import pandas as pd
from collections import Counter
from utils.database import fetch_all_candidates

st.set_page_config(page_title="SmartHire AI - Recruiter Insights", layout="wide")

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

st.title("Talent Pool Analytics")
st.caption("SmartHire AI Aggregated Metrics")
st.markdown("Macro-level analysis across candidate distributions and common missing skills.")

st.divider()

candidates = fetch_all_candidates()

if not candidates:
    st.info("No candidates evaluated yet. Run screening on the main application to populate analytics.")
else:
    st.subheader("Candidate Status Categorization")
    
    df = pd.DataFrame(candidates)
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(status_counts, use_container_width=True, hide_index=True)
        
    with col2:
        st.bar_chart(data=status_counts, x="Status", y="Count")

    st.divider()

    st.subheader("Skill Gap Frequency Analysis")
    st.markdown("Most frequently missing skills across the applicant pool:")

    all_missing_skills = []
    for c in candidates:
        all_missing_skills.extend(c["missing_skills"])

    if all_missing_skills:
        skill_counts = Counter(all_missing_skills).most_common(10)
        missing_df = pd.DataFrame(skill_counts, columns=["Skill", "Count Missing"])
        
        st.bar_chart(data=missing_df, x="Skill", y="Count Missing")
    else:
        st.success("No recurring skill gaps found across candidates.")

st.markdown('<div class="author-footer">By Anmol Singh</div>', unsafe_allow_html=True)