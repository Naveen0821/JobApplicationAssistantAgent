import os
import streamlit as st
from dotenv import load_dotenv
from langgraph.graph import END

from src.state.application_state import ApplicationState
from src.graph.application_graph import build_graph
from src.nodes.resume_parser import parse_resume
from src.nodes.jd_parser import parse_jd

# Load environment
load_dotenv()

st.set_page_config(page_title="💼 Job Application Assistant", layout="wide")
st.title("💼 Intelligent Job Application Assistant")

if "graph_app" not in st.session_state:
    st.session_state.graph_app = None
if "state" not in st.session_state:
    st.session_state.state = {}

# Upload section
st.subheader("1. Upload Resume (.pdf or .docx)")
resume_file = st.file_uploader("Choose your resume file", type=["pdf", "docx"])

st.subheader("2. Paste Job Description")
job_description = st.text_area("Paste the full job description here")

if st.button("🚀 Run Agent"):
    if not resume_file or not job_description.strip():
        st.warning("⚠️ Please upload a resume and paste a job description.")
    else:
        with st.spinner("🔍 Parsing resume and job description..."):
            # Save and parse resume
            file_path = f"/tmp/{resume_file.name}"
            with open(file_path, "wb") as f:
                f.write(resume_file.read())

            resume_text = parse_resume(file_path)
            jd_text = parse_jd(job_description)

            # Build graph and run
            st.session_state.graph_app = build_graph()
            state: ApplicationState = {
                "resume_text": resume_text,
                "job_description": jd_text,
                "extracted_skills": [],
                "missing_skills": [],
                "recommended_edits": [],
                "revised_resume": None,
                "cover_letter": None,
                "user_feedback": None,
                "final_approved": False,
            }

            result = st.session_state.graph_app.invoke(state)
            st.session_state.state = result

        st.success("✅ Analysis complete.")

# Output section
if st.session_state.state:
    st.subheader("🧠 Resume Analysis")
    st.write("**Skill Gaps:**", st.session_state.state["missing_skills"])
    st.write("**Recommended Edits:**", st.session_state.state["recommended_edits"])

    st.subheader("📄 Revised Resume (Draft)")
    st.text_area("Updated Resume", st.session_state.state["revised_resume"], height=300)

    st.subheader("📝 Cover Letter")
    st.text_area("Cover Letter Draft", st.session_state.state["cover_letter"], height=300)

    if st.button("✅ Finalize"):
        st.session_state.state["final_approved"] = True
        st.success("📁 Final resume and cover letter saved for submission.")
