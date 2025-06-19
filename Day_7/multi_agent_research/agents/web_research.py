# agents/web_research.py

import requests
import os
from langchain_google_genai import ChatGoogleGenerativeAI

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "demo")  # Replace with your key

def web_research_agent(query: str) -> str:
    try:
        tavily_url = "https://api.tavily.com/search"
        response = requests.post(tavily_url, json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 5
        })

        results = response.json().get("results", [])
        if not results:
            return "No relevant results found via web search."

        content = "\n".join([f"- {r['title']}: {r['content']}" for r in results])
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

        prompt = f"""Summarize the following web search results and answer the query.

Query: {query}

Search Results:
{content}
"""
        return model.invoke(prompt)

    except Exception as e:
        return f"Web research error: {e}"
