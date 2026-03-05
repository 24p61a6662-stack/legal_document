from pypdf import PdfReader
from docx import Document

def load_document(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages])
    
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()