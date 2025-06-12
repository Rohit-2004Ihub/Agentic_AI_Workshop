import os
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# ========== 1. Setup ==========
genai.configure(api_key="AIzaSyDFdXTNcjx1bezvBC4-jCE89VUThmF0xhQ")  # Replace with your API key

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ========== 2. Load and Chunk Text File ==========
def load_txt_chunks(filepath, chunk_size=200):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ========== 3. Load and Chunk CSV File ==========
def load_csv_chunks(filepath):
    df = pd.read_csv(filepath)
    chunks = []
    for _, row in df.iterrows():
        row_text = f"Student {row['name']} with register number {row['register_number']} scored {row['staff_mark']} marks."
        chunks.append(row_text)
    return chunks

# ========== 4. Combine All Chunks ==========
chunks_txt = load_txt_chunks(r"C:\Users\HP\Downloads\my_doc.txt")
chunks_csv = load_csv_chunks(r"C:\Users\HP\Downloads\bulk_staff.csv")
all_chunks = chunks_txt + chunks_csv

# ========== 5. Embedding and FAISS Index ==========
embeddings = model.encode(all_chunks)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# ========== 6. Retrieval ==========
def retrieve_context(query, k=3):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)
    return [all_chunks[i] for i in indices[0]]

# ========== 7. Generation ==========
def generate_answer(query, context):
    prompt = (
        "Answer the question based only on the following context:\n\n"
        f"{context}\n\n"
        f"Question: {query}\nAnswer:"
    )
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text

# ========== 8. Full RAG ==========
def rag_ask(query):
    context_chunks = retrieve_context(query)
    combined_context = "\n".join(context_chunks)
    return generate_answer(query, combined_context)

# ========== 9. Try It ==========
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (or type 'exit'): ")
        if user_query.lower() == "exit":
            break
        answer = rag_ask(user_query)
        print("\nAnswer:\n", answer)
