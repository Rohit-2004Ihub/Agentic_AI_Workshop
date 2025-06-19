from langchain_google_genai import ChatGoogleGenerativeAI

def router_agent(query: str) -> str:
    lower_query = query.lower()

    # Rule-based keyword matching
    if any(keyword in lower_query for keyword in ["latest", "current", "today", "news", "trending"]):
        return "web_research"
    elif any(keyword in lower_query for keyword in ["according to pdf", "based on document", "in the dataset", "from the pdf", "as per the document"]):
        return "rag"

    # LLM-based fallback routing
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
    prompt = f"""
You are a routing agent. Classify the following query into one of three categories:

Query: "{query}"

- web_research: for real-time or current information (e.g. news, events)
- rag: if it needs knowledge from internal documents (e.g. PDFs or uploaded files)
- llm: for general reasoning or creative responses

Respond with only one of: web_research, rag, or llm.
"""
    decision = llm.invoke(prompt).content.strip().lower()
    print(f"[RouterAgent] LLM decision: {decision}")

    if decision in ["web_research", "rag", "llm"]:
        return decision

    print("[RouterAgent] Invalid LLM output. Defaulting to 'llm'")
    return "llm"
