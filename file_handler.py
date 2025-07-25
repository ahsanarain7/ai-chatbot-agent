
from PyPDF2 import PdfReader

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        return uploaded_file.read().decode("utf-8")
