import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """Extract all text from the uploaded PDF file."""
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"❌ Error extracting text: {e}"
