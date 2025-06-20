# backend/core/vector_store.py
import os
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


DATA_FOLDER = "backend/data/micro_goals/"
INDEX_FOLDER = "faiss_index/micro_goal_index"


def build_vector_store(data_folder: str, index_folder: str):
    if not os.path.exists(data_folder):
        print(f"📂 Input folder '{data_folder}' not found. Creating it.")
        os.makedirs(data_folder)
        print("⚠️ No documents found yet. Please add PDFs or TXT files and rerun.")
        return

    all_docs = []

    for filename in os.listdir(data_folder):
        path = os.path.join(data_folder, filename)
        if path.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif path.endswith(".txt"):
            loader = TextLoader(path)
        else:
            continue
        docs = loader.load()
        all_docs.extend(docs)

    if not all_docs:
        print("⚠️ No documents loaded. Add content and retry.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(all_docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    faiss_index = FAISS.from_documents(split_docs, embeddings)
    faiss_index.save_local(index_folder)

    print(f"✅ Vector store built and saved at: {index_folder}")

def load_vector_store(save_path: str):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)

