# tools/web_search.py

import requests
import os

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_company_online(company_name: str) -> bool:
    """Search for a company online using Tavily or DuckDuckGo-style API"""
    if not TAVILY_API_KEY:
        return False  # Fallback if key not present

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {TAVILY_API_KEY}"},
            json={"query": company_name, "max_results": 3}
        )
        results = response.json()
        return len(results.get("results", [])) > 0
    except:
        return False
