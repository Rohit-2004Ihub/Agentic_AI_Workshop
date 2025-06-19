import requests
import os

def verify_companies(companies):
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    verified = {}
    for company in companies:
        response = requests.post(
            "https://api.tavily.com/search",
            json={"query": company, "api_key": tavily_api_key}
        )
        data = response.json()
        verified[company] = "Exists" if data.get("results") else "Not Found"
    return verified
