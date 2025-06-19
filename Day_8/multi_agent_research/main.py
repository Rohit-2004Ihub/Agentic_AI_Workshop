# 📁 multi_agent_research/main.py

from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from typing import TypedDict, Literal
from agents.router import router_agent
from agents.web_research import web_research_agent
from agents.rag import rag_agent
from agents.summarizer import summarization_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the state schema
class GraphState(TypedDict):
    query: str
    route: Literal["llm", "web_research", "rag"]
    result: str
    final_answer: str

# Define nodes
def router_node(state: GraphState) -> GraphState:
    if "route" in state and state["route"] in ["llm", "web_research", "rag"]:
        print(f"[Router] Manual override to: {state['route']}")
        return state
    route = router_agent(state["query"])
    print(f"[Router] Auto route to: {route}")
    return {**state, "route": route}

def llm_node(state: GraphState) -> GraphState:
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    result = model.invoke(state["query"]).content
    return {**state, "result": result}

def web_node(state: GraphState) -> GraphState:
    result = web_research_agent(state["query"])
    return {**state, "result": result}

def rag_node(state: GraphState) -> GraphState:
    from utils.pdf_loader import create_vector_store
    from langchain_community.vectorstores import FAISS
    from langchain.embeddings import HuggingFaceEmbeddings

    RAG_INDEX_FOLDER = "rag_index"
    query = state["query"]

    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        if not os.path.exists(os.path.join(RAG_INDEX_FOLDER, "index.faiss")):
            create_vector_store()

        vectorstore = FAISS.load_local(RAG_INDEX_FOLDER, embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(query)

        print(f"[RAG] Retrieved {len(docs)} documents")
        context = "\n\n".join([doc.page_content for doc in docs])
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

        prompt = f"""You are an expert researcher. Using the following documents, answer the query precisely.

Documents:
{context}

Query: {query}
"""
        result = model.invoke(prompt).content
        return {**state, "result": result}

    except Exception as e:
        return {**state, "result": f"RAG error: {e}"}

def summarize_node(state: GraphState) -> GraphState:
    final = summarization_agent(state["query"], state["result"])
    return {**state, "final_answer": final}

# Build the LangGraph
def build_graph() -> Runnable:
    builder = StateGraph(GraphState)

    # Add agents
    builder.add_node("router", router_node)
    builder.add_node("llm", llm_node)
    builder.add_node("web_research", web_node)
    builder.add_node("rag", rag_node)
    builder.add_node("summarization", summarize_node)

    # Add edges
    builder.set_entry_point("router")
    builder.add_conditional_edges("router", lambda x: x["route"], {
        "llm": "llm",
        "web_research": "web_research",
        "rag": "rag"
    })
    builder.add_edge("llm", "summarization")
    builder.add_edge("web_research", "summarization")
    builder.add_edge("rag", "summarization")
    builder.add_edge("summarization", END)

    return builder.compile()

# Optional: build FAISS index if running this script directly
if __name__ == "__main__":
    from utils.pdf_loader import create_vector_store
    create_vector_store()
    print("FAISS index created from rag_pdfs/")
