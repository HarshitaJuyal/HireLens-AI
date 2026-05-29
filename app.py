import streamlit as st

from modules.parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from modules.nlp_analyzer import clean_text
from modules.ats_engine import calculate_ats_score
from modules.skills import TECHNICAL_SKILLS
from modules.ai_feedback import get_resume_feedback


# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="HireLens AI",
    page_icon="📄",
    layout="wide"
)


# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161A23;
}

/* Hero Section */
.hero-card {
    background: linear-gradient(135deg, #111827, #1E293B);
    padding: 35px;
    border-radius: 20px;
    border: 1px solid #334155;
    margin-bottom: 30px;
    text-align: center;
}

/* Main Title */
.hero-title {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00FFA3, #00C8FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.hero-subtitle {
    font-size: 1.2rem;
    color: #94A3B8;
}

/* Skill Badge */
.skill-badge {
    display: inline-block;
    background: #0F172A;
    color: #00FFA3;
    border: 1px solid #00FFA3;
    border-radius: 30px;
    padding: 8px 15px;
    margin: 5px;
    font-weight: bold;
}

/* ATS Score Card */
.score-card {
    background: linear-gradient(135deg, #00FFA3, #00C8FF);
    color: black;
    padding:5px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 10px;
}

.score-card h1 {
    color: black !important;
    font-size: 2.5rem;
}

/* Progress Bar */
div.stProgress > div > div > div > div {
    background-color: #00FFA3;
}

/* Metric */
div[data-testid="metric-container"] {
    background-color: #1E2530;
    border-radius: 15px;
    padding: 20px;
}

/* Text Area */
textarea {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================
# HERO SECTION
# ==================================

st.markdown("""
<div class="hero-card">
    <div class="hero-title">HireLens AI</div>
    <div class="hero-subtitle">
        AI-Powered ATS Resume Analyzer & Interview Assistant
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================
# SIDEBAR
# ==================================

st.sidebar.header("📄 Upload Resume")

uploaded_file = st.sidebar.file_uploader(
    "Upload Your Resume",
    type=["pdf", "docx"]
)


# ==================================
# JOB DESCRIPTION
# ==================================

job_description = st.text_area(
    "Paste Job Description",
    height=250
)


# ==================================
# MAIN ANALYSIS
# ==================================

if uploaded_file:

    st.success("Resume uploaded successfully!")

    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)

    elif file_type == "docx":
        resume_text = extract_text_from_docx(uploaded_file)

    else:
        st.error("Unsupported file type.")
        st.stop()

    # Clean Resume
    cleaned_resume = clean_text(resume_text)

    # Extract Skills
    filtered_skills = []

    for word in cleaned_resume:
        if word in TECHNICAL_SKILLS:
            filtered_skills.append(word)

    filtered_skills = list(set(filtered_skills))

    # ATS Analysis
    ats_result = calculate_ats_score(
        filtered_skills,
        job_description
    )

    # Gemini Feedback
    ai_feedback = get_resume_feedback(
        filtered_skills,
        ats_result["missing_keywords"]
    )

    # ==============================
    # SKILLS SECTION
    # ==============================

    st.subheader("🛠 Important Resume Skills")

    skills_html = ""

    for skill in filtered_skills:
        skills_html += f"""
        <span class="skill-badge">
            {skill.upper()}
        </span>
        """

    st.markdown(skills_html, unsafe_allow_html=True)

    # ==============================
    # ATS SCORE
    # ==============================

    score = ats_result["score"]

    st.subheader("📊 ATS Match Score")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
      st.metric("ATS Score", f"{score}%")

    with col2:
     st.metric(
        "Matched Skills",
        len(ats_result["matched_keywords"])
    )

    with col3:
     st.metric(
        "Missing Skills",
        len(ats_result["missing_keywords"])
    )

    with col4:
     if score >= 80:
        rank = "Excellent"
     elif score >= 60:
        rank = "Good"
     else:
        rank = "Needs Work"

    st.metric("Resume Status", rank)

    st.markdown(
        f"""
        <div class="score-card">
            <h2>ATS SCORE</h2>
            <h1>{score}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(int(score))

    # ==============================
    # MATCHED / MISSING
    # ==============================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Matched Skills")

        matched_html = ""

        for skill in ats_result["matched_keywords"]:
            matched_html += f"""
            <span class="skill-badge">
                ✅ {skill.upper()}
            </span>
            """

        st.markdown(
            matched_html,
            unsafe_allow_html=True
        )

    with col2:

        st.subheader("❌ Missing Skills")

        missing_html = ""

        for skill in ats_result["missing_keywords"][:20]:
            missing_html += f"""
            <span class="skill-badge">
                ❌ {skill.upper()}
            </span>
            """

        st.markdown(
            missing_html,
            unsafe_allow_html=True
        )

    # ==============================
    # AI FEEDBACK
    # ==============================

    st.subheader("🤖 AI Resume Feedback")

    st.markdown(ai_feedback)


# ==================================
# INFO MESSAGE
# ==================================

if job_description:
    st.info("Job description added!")