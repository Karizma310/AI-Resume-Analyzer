import os
import tempfile
from pathlib import Path

import streamlit as st

from src.extractor import extract_text_from_pdf
from src.analyzer import (
    analyze_resume,
    generate_summary,
    generate_interview_questions,
)
from src.report_generator import create_pdf
from src.ui import display_dashboard


# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
)


# -----------------------------------
# Load External CSS
# -----------------------------------

css_file = Path("assets/styles.css")

if css_file.exists():
    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


# -----------------------------------
# Session State
# -----------------------------------

defaults = {
    "analysis_complete": False,
    "summary": None,
    "ats": None,
    "questions": None,
    "resume": None,
    "jd": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------------
# Cache AI Responses
# -----------------------------------

@st.cache_data(show_spinner=False)
def cached_analysis(resume_text, job_description):

    summary = generate_summary(resume_text)

    ats = analyze_resume(
        resume_text,
        job_description,
    )

    questions = generate_interview_questions(
        resume_text,
        job_description,
    )

    return summary, ats, questions


# -----------------------------------
# Hero Section
# -----------------------------------

st.markdown(
    """
<div class="hero">

<h1>🤖 AI Resume Analyzer</h1>

<p>
Analyze your resume using Google's Gemini AI.
Receive an ATS score, resume summary,
missing skills, improvement suggestions,
interview questions, and a professional PDF report.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:

    st.title("📌 AI Resume Analyzer")

    st.caption("Professional Resume Review Tool")

    st.markdown("---")

    st.markdown(
        """
### ✨ Features

- ATS Score
- Resume Summary
- Skill Matching
- Missing Skills
- Resume Analytics
- Interview Questions
- PDF Report
- Interactive Dashboard
"""
    )

    st.markdown("---")

    st.success("Powered by Google Gemini 2.5 Flash")


# -----------------------------------
# Input Section
# -----------------------------------

left, right = st.columns(2)

with left:

    uploaded_resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"],
    )

with right:

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=260,
        placeholder="Paste the complete job description here...",
    )


# -----------------------------------
# Analyze Button
# -----------------------------------

analyze = st.button(
    "🚀 Analyze Resume",
    width="stretch",
)

if analyze:

    if uploaded_resume is None:

        st.warning("Please upload your resume.")

        st.stop()

    if not job_description.strip():

        st.warning("Please paste the job description.")

        st.stop()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    ) as tmp:

        tmp.write(uploaded_resume.read())

        pdf_path = tmp.name

    with st.spinner("Extracting Resume..."):

        resume_text = extract_text_from_pdf(
            pdf_path
        )

    os.remove(pdf_path)

    status = st.status(
        "Analyzing Resume...",
        expanded=True,
    )

    status.write("📄 Resume extracted successfully")

    status.write("🧠 Generating AI summary...")

    try:

        summary, ats_analysis, interview_questions = cached_analysis(
            resume_text,
            job_description,
        )

    except Exception as e:

        status.update(
            label="Analysis Failed",
            state="error",
        )

        st.error(str(e))

        st.stop()

    status.write("🎯 ATS analysis completed")

    status.write("🎤 Interview questions generated")

    status.update(
        label="Analysis Complete",
        state="complete",
    )

    st.session_state.analysis_complete = True

    st.session_state.summary = summary

    st.session_state.ats = ats_analysis

    st.session_state.questions = interview_questions

    st.session_state.resume = resume_text

    st.session_state.jd = job_description

# -----------------------------------
# Display Dashboard
# -----------------------------------

if st.session_state.analysis_complete:

    st.markdown("## 📊 Analysis Results")

    score = st.session_state.ats["ats_score"]

    if score >= 85:
        st.success(f"🌟 Excellent Resume! ATS Score: {score}%")

    elif score >= 70:
        st.info(f"✅ Good Resume! ATS Score: {score}%")

    elif score >= 50:
        st.warning(f"⚠ Your Resume Needs Improvement. ATS Score: {score}%")

    else:
        st.error(f"❌ Low ATS Score: {score}%")

    st.markdown("")

    col1, col2 = st.columns([5, 1])

    with col2:

        if st.button(
            "🗑 Clear Analysis",
            width="stretch",
        ):

            for key in [
                "analysis_complete",
                "summary",
                "ats",
                "questions",
                "resume",
                "jd",
            ]:

                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

    display_dashboard(
        st.session_state.summary,
        st.session_state.ats,
        st.session_state.questions,
        st.session_state.resume,
        st.session_state.jd,
    )

    st.markdown("---")

    report_path = create_pdf(
        st.session_state.summary,
        st.session_state.ats,
        st.session_state.questions,
    )

    with open(report_path, "rb") as pdf:

        st.download_button(
            label="📥 Download Professional PDF Report",
            data=pdf,
            file_name="Resume_Report.pdf",
            mime="application/pdf",
            width="stretch",
        )

# -----------------------------------
# Footer
# -----------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
<div class="footer">

<h4>🤖 AI Resume Analyzer</h4>

<p>
Built using <b>Python</b> • <b>Streamlit</b> •
<b>Google Gemini</b> • <b>Plotly</b>
</p>

<p>
Designed to help job seekers improve resumes with AI-powered insights.
</p>

</div>
""",
    unsafe_allow_html=True,
)
