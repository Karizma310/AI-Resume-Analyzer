from src.extractor import extract_text_from_pdf

resume_path = "Sample_resume.pdf"

text = extract_text_from_pdf(resume_path)

print(text[:1000])