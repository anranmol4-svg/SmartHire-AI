import streamlit as st
import pandas as pd
from utils.pdf_parser import extract_text_from_pdf
from utils.preprocessing import clean_text
from utils.similarity import compute_similarity_scores
from utils.ats_score import calculate_ats_score
from utils.ranking import rank_candidates
from utils.database import init_db, save_candidate_result, fetch_all_candidates, clear_all_candidates

# 1. Page Configuration
st.set_page_config(
    page_title="SmartHire AI - Resume Screening & Ranking",
    page_icon="💼",
    layout="wide"
)

# 2. Custom Styling for Professional Look
st.markdown("""
    <style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Subdued professional headers */
    h1, h2, h3, h4 {
        color: #1E293B;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    /* Subtle footer signature styling */
    .author-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #94A3B8;
        text-align: center;
        padding: 8px 0;
        font-size: 13px;
        font-weight: 500;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Database on Startup
init_db()

# 4. Main Header Section
st.title("SmartHire AI")
st.caption("Automated Resume Screening & Candidate Ranking System")
st.markdown("""
An enterprise candidate evaluation engine. Upload a Job Description and candidate resumes to compute objective similarity scores, skill coverage, and transparent ATS rankings.
""")

st.divider()

# 5. Sidebar Controls & Ingestion
st.sidebar.title("Input Configuration")

st.sidebar.subheader("1. Job Description")
jd_file = st.sidebar.file_uploader("Upload JD (.txt)", type=["txt"], key="jd_file")
jd_text_input = st.sidebar.text_area("Or paste Job Description text:", height=150, placeholder="Paste job requirements here...")

jd_content = ""
if jd_file:
    jd_content = jd_file.read().decode("utf-8")
elif jd_text_input:
    jd_content = jd_text_input

st.sidebar.subheader("2. Candidate Resumes")
uploaded_resumes = st.sidebar.file_uploader(
    "Upload Resumes (.pdf)", 
    type=["pdf"], 
    accept_multiple_files=True,
    key="resumes"
)

st.sidebar.markdown("---")
process_btn = st.sidebar.button("Rank Candidates", type="primary", use_container_width=True)

# Updated single word RESET button
if st.sidebar.button("RESET", use_container_width=True):
    clear_all_candidates()
    st.sidebar.success("Database cleared.")
    st.rerun()

# 6. Execution Pipeline
if process_btn:
    if not jd_content.strip():
        st.error("Please upload or paste a Job Description before proceeding.")
    elif not uploaded_resumes:
        st.error("Please upload at least one candidate resume.")
    else:
        with st.spinner("Processing documents, running vectorization, and calculating ATS scores..."):
            cleaned_jd = clean_text(jd_content)
            
            parsed_resumes = []
            cleaned_resumes = []
            filenames = []
            
            for pdf in uploaded_resumes:
                raw_text, success, err_msg = extract_text_from_pdf(pdf.getvalue())
                
                if success:
                    cleaned_txt = clean_text(raw_text)
                    parsed_resumes.append(raw_text)
                    cleaned_resumes.append(cleaned_txt)
                    filenames.append(pdf.name)
                else:
                    st.warning(f"Skipped file {pdf.name}: {err_msg}")
            
            if cleaned_resumes:
                similarity_scores = compute_similarity_scores(cleaned_jd, cleaned_resumes)
                
                unranked_results = []
                for i in range(len(filenames)):
                    raw_text = parsed_resumes[i]
                    sim_score = similarity_scores[i]
                    filename = filenames[i]
                    
                    ats_result = calculate_ats_score(sim_score, raw_text, jd_content)
                    
                    candidate_payload = {
                        "filename": filename,
                        "raw_text": raw_text,
                        **ats_result
                    }
                    unranked_results.append(candidate_payload)
                
                ranked_batch = rank_candidates(unranked_results)
                
                for candidate in ranked_batch:
                    save_candidate_result(candidate)
                    
                st.success(f"Successfully evaluated and ranked {len(ranked_batch)} candidates.")

# 7. Leaderboard & Summary Display
candidates = fetch_all_candidates()

if candidates:
    col1, col2, col3, col4 = st.columns(4)
    avg_score = sum(c["ats_score"] for c in candidates) / len(candidates)
    shortlisted_count = len([c for c in candidates if c["status"] == "Shortlist"])
    top_score = max(c["ats_score"] for c in candidates)
    
    col1.metric("Total Applicants", len(candidates))
    col2.metric("Average ATS Score", f"{avg_score:.1f} / 100")
    col3.metric("Top ATS Score", f"{top_score:.1f}")
    col4.metric("Shortlisted", shortlisted_count)
    
    st.divider()
    
    st.subheader("Candidate Leaderboard")
    
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        search_query = st.text_input("Search Candidate:")
    with filter_col2:
        status_filter = st.selectbox("Filter Status:", ["All", "Shortlist", "Strong Candidate", "Review", "Reject"])
    
    df = pd.DataFrame(candidates)
    
    if search_query:
        df = df[df["filename"].str.contains(search_query, case=False, na=False)]
    if status_filter != "All":
        df = df[df["status"] == status_filter]
        
    if not df.empty:
        display_df = df[["rank", "filename", "ats_score", "similarity_pct", "status"]].copy()
        display_df.columns = ["Rank", "Candidate File", "ATS Score (/100)", "TF-IDF Match (%)", "Status"]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No candidates match the specified filter criteria.")
        
else:
    st.info("Upload a Job Description and candidate resumes using the sidebar to generate rankings.")

# 8. Signature Footer
st.markdown('<div class="author-footer">By Anmol Singh</div>', unsafe_allow_html=True)