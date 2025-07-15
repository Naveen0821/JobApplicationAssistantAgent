import pdfplumber
import docx

def parse_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return parse_pdf_resume(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx_resume(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

def parse_pdf_resume(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def parse_docx_resume(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
