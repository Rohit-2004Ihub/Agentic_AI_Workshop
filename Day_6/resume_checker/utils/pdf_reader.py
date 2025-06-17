import PyPDF2

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    return text
