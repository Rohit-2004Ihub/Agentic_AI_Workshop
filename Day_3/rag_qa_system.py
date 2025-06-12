import os
import faiss
import json
import time
import numpy as np
import pdfplumber
import streamlit as st
from google.api_core.exceptions import ResourceExhausted
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


# ========== Document Preprocessing ==========
def extract_chunks_from_pdf(pdf_path):
    """Extract and chunk PDF into paragraph-level chunks."""
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                for para in text.split("\n\n"):
                    if len(para.strip().split()) > 10:
                        chunks.append({
                            "text": para.strip(),
                            "metadata": {
                                "paper_title": os.path.basename(pdf_path),
                                "page_number": page_num
                            }
                        })
    return chunks


def preprocess_papers(data_dir="data"):
    """Process and vectorize all PDFs in the data folder."""
    all_chunks = []
    paper_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.pdf')]
    for path in paper_paths:
        all_chunks.extend(extract_chunks_from_pdf(path))

    # Embed chunks
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = [model.encode(chunk['text']) for chunk in all_chunks]
    embeddings = np.array(embeddings)

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save data
    faiss.write_index(index, "faiss_index.bin")
    with open("chunks.json", "w") as f:
        json.dump(all_chunks, f)


# ========== Load Data ==========
@st.cache_resource
def load_index_and_chunks():
    index = faiss.read_index("faiss_index.bin")
    with open("chunks.json", "r") as f:
        chunks = json.load(f)
    return index, chunks


# ========== Retrieval ==========
def retrieve_relevant_chunks(query, model, index, chunks, k=3):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)
    return [chunks[i] for i in indices[0]]


# ========== Answer Generation ==========
def generate_answer(query, retrieved_chunks, llm, retries=3, wait_sec=10):
    context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a helpful AI assistant. Answer the user's question based only on the context provided.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )
    )
    chain = LLMChain(prompt=prompt, llm=llm)

    for attempt in range(retries):
        try:
            return chain.run(context=context, question=query)
        except ResourceExhausted as e:
            st.warning(f"Gemini quota exhausted (attempt {attempt+1}/{retries}). Retrying in {wait_sec} seconds...")
            time.sleep(wait_sec)
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            break

    return "❌ Failed to generate answer due to quota limits. Try again later."

# ========== Streamlit UI ==========
def main():
    st.title("📚 AI Research Paper Q&A (RAG System)")
    st.write("Ask any question based on the uploaded AI research papers.")

    # Load index and model
    index, chunks = load_index_and_chunks()
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    query = st.text_input("🔍 Enter your question:")
    if st.button("Submit") and query:
        with st.spinner("Searching and generating answer..."):
            results = retrieve_relevant_chunks(query, embedding_model, index, chunks, k=3)
            answer = generate_answer(query, results, langchain_model)
            st.markdown("### ✅ Answer:")
            st.write(answer)
            st.markdown("### 📎 Source References:")
            for chunk in results:
                meta = chunk["metadata"]
                st.write(f"- **{meta['paper_title']}**, Page {meta['page_number']}")


# ========== LangChain Gemini Init ==========
if __name__ == "__main__":
    # Gemini API Key (can also use genai.configure(api_key=...) globally if needed)
    langchain_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.5,
        max_tokens=1024,
        google_api_key="AIzaSyDO6k-A9D_nFyizi9wwieKix2LE4hnzhiE"
    )

    # First-time preprocessing
    if not os.path.exists("faiss_index.bin") or not os.path.exists("chunks.json"):
        preprocess_papers(data_dir="data")

    # Start Streamlit app
    main()
