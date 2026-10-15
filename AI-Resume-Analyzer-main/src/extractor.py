import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF resume.

    Args:
        pdf_path (str): Path to the uploaded PDF.

    Returns:
        str: Extracted text.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()
