from modules.nlp_analyzer import clean_text
from modules.skills import TECHNICAL_SKILLS


def calculate_ats_score(resume_keywords, job_description):

    # Clean job description
    cleaned_job_description = clean_text(job_description)

    # Keep only technical skills from JD
    filtered_job_skills = []

    for word in cleaned_job_description:

        if word in TECHNICAL_SKILLS:
            filtered_job_skills.append(word)

    # Remove duplicates
    filtered_job_skills = list(set(filtered_job_skills))

    # Convert into sets
    resume_set = set(resume_keywords)

    job_set = set(filtered_job_skills)

    # Find matched skills
    matched_keywords = resume_set.intersection(job_set)

    # Find missing skills
    missing_keywords = job_set.difference(resume_set)

    # Calculate ATS score
    if len(job_set) > 0:
        score = (len(matched_keywords) / len(job_set)) * 100
    else:
        score = 0

    return {
        "score": round(score, 2),
        "matched_keywords": list(matched_keywords),
        "missing_keywords": list(missing_keywords)
    }