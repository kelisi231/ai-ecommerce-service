import io
import fitz
from docx import Document as DocxDocument

SUPPORT_DOCUMENTS_TYPE = {"pdf", "txt", "docx"}


def extract_text_by_type(filename: str, content: bytes):
    document_type = filename.rsplit(".", 1)[-1].lower()
    if document_type not in SUPPORT_DOCUMENTS_TYPE:
        raise ValueError(f"Document type {document_type} is not supported.")
    if document_type == "txt":
        return content.decode("utf-8", errors="ignore")
    if document_type == "pdf":
       doc = fitz.open(stream=content, filetype="pdf")
       return "\n".join(page.get_text() for page in doc)
    doc = DocxDocument(io.BytesIO(content))
    return "\n".join(paragraphs.text for paragraphs in doc.paragraphs)