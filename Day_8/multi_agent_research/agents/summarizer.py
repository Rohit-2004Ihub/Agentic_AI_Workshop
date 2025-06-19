# agents/summarizer.py

from langchain_google_genai import ChatGoogleGenerativeAI

def summarization_agent(query: str, content: str) -> str:
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    prompt = f"""
You are an expert summarizer.

Based on the following extracted information, create a well-structured, concise, and insightful answer to the user's query.

User Query: {query}

Extracted Information:
{content}

Final Answer:
"""
    try:
        return model.invoke(prompt)
    except Exception as e:
        return f"Summarization error: {e}"
