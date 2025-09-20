import os
from PyPDF2 import PdfReader

PDF_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pdf')

def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def ingest_pdfs():
    pdf_texts = {}
    for filename in os.listdir(PDF_FOLDER):
        if filename.lower().endswith('.pdf'):
            path = os.path.join(PDF_FOLDER, filename)
            pdf_texts[filename] = extract_text_from_pdf(path)
    return pdf_texts
