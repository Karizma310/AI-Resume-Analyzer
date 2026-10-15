from src.extractor import extract_text_from_pdf
from src.analyzer import (
    generate_summary,
    analyze_resume,
    generate_interview_questions,
)

resume = extract_text_from_pdf("sample_resume.pdf")

job_description = """
We are looking for a Python Developer with experience in
Machine Learning, SQL, Git, and REST APIs.
"""

print("=" * 80)
print("SUMMARY")
print("=" * 80)

print(generate_summary(resume))

print("=" * 80)
print("ATS ANALYSIS")
print("=" * 80)

print(analyze_resume(resume, job_description))

print("=" * 80)
print("INTERVIEW QUESTIONS")
print("=" * 80)

print(generate_interview_questions(resume, job_description))
