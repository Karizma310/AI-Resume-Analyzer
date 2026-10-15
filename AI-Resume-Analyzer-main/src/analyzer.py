import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

from src.prompts import (
    SYSTEM_PROMPT,
    SUMMARY_PROMPT,
    ATS_PROMPT,
    INTERVIEW_PROMPT,
)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY missing. Check your .env file.")

client = genai.Client(api_key=api_key)


def generate_with_retry(prompt):
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            return response.text

        except ServerError:
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))


    return None


def generate_summary(resume_text):

    prompt = SYSTEM_PROMPT + "\n\n" + SUMMARY_PROMPT.format(
        resume=resume_text
    )

    return generate_with_retry(prompt)


def analyze_resume(resume_text, job_description):

    prompt = SYSTEM_PROMPT + "\n\n" + ATS_PROMPT.format(
        resume=resume_text,
        job_description=job_description,
    )

    text = generate_with_retry(prompt)

    if text is None:
        return {
            "ats_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "suggestions": [
                "Gemini server unavailable."
            ]
        }

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        return {
            "ats_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "suggestions": [
                "Gemini returned invalid JSON."
            ]
        }


def generate_interview_questions(resume_text, job_description):

    prompt = SYSTEM_PROMPT + "\n\n" + INTERVIEW_PROMPT.format(
        resume=resume_text,
        job_description=job_description,
    )

    return generate_with_retry(prompt)
