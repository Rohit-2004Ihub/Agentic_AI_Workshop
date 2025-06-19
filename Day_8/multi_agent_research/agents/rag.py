# agents/rag.py

from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

RAG_INDEX_FOLDER = "rag_index"

def rag_agent(query: str) -> str:
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = FAISS.load_local(RAG_INDEX_FOLDER, embeddings, allow_dangerous_deserialization=True)

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(query)

        context = "\n\n".join([doc.page_content for doc in docs])
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

        prompt = f"""You are an expert researcher. Using the following documents, answer the query precisely.

Documents:
{context}

Query: {query}
"""
        return model.invoke(prompt)
    except Exception as e:
        return f"RAG error: {e}"
