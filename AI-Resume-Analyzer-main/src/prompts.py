SYSTEM_PROMPT = """
You are an expert ATS (Applicant Tracking System) and professional career coach.

Analyze resumes carefully and provide professional, constructive, and concise feedback.

Always return your answers in Markdown format.
"""


SUMMARY_PROMPT = """
Analyze the following resume and write a professional summary in 5-6 bullet points.

Resume:
{resume}
"""


ATS_PROMPT = """
You are an expert ATS (Applicant Tracking System).

Analyze the resume against the given job description.

Resume:
{resume}

Job Description:
{job_description}

Return ONLY valid JSON.

{{
  "ats_score": 85,
  "matching_skills": [
    "Python",
    "Machine Learning"
  ],
  "missing_skills": [
    "Docker",
    "AWS"
  ],
  "strengths": [
    "Strong ML Projects",
    "Good Python Skills"
  ],
  "weaknesses": [
    "No Cloud Experience"
  ],
  "suggestions": [
    "Add Docker projects",
    "Mention measurable achievements"
  ]
}}

Do not include markdown.
Do not include explanation.
Return JSON only.
"""

INTERVIEW_PROMPT = """
Based on the following resume and job description, generate:

- 10 Technical Interview Questions
- 5 HR Interview Questions

Resume:
{resume}

Job Description:
{job_description}
"""