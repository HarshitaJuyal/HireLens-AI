import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_resume_feedback(resume_skills, missing_skills):

    prompt = f"""
    You are an expert ATS Resume Reviewer.

    Resume Skills:
    {resume_skills}

    Missing Skills:
    {missing_skills}

    Give:

    1. Resume improvement suggestions
    2. ATS optimization tips
    3. Skills to learn
    4. Career advice

    Keep the response concise and professional.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content