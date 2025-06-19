# 📁 utils/pdf_loader.py

import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings

PDF_FOLDER = "rag_pdfs"
INDEX_FOLDER = "rag_index"

def create_vector_store():
    documents = []

    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            path = os.path.join(PDF_FOLDER, filename)
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            if text.strip():
                documents.append(Document(page_content=text, metadata={"source": filename}))
            else:
                print(f"⚠️ No extractable text in: {filename}")

    if not documents:
        print("⚠️ No text extracted from PDFs.")
        return

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(documents)

    # Use HuggingFace for local embedding (offline, no API needed)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local(INDEX_FOLDER)

    print("✅ FAISS index created and saved to rag_index/")
