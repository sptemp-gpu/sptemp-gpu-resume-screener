import fitz  # PyMuPDF
from docx import Document

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    text = file.read().decode("utf-8")  # Decode to text
    return text
