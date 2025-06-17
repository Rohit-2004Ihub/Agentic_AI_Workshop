from langchain_core.tools import tool
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
TAVILY_KEY = os.getenv("TAVILY_API_KEY")


def clean_json_string(text: str) -> str:
    """
    Cleans a JSON string that may have markdown formatting like ```json ... ```
    and returns a valid JSON string.
    """
    text = text.strip()

    # If markdown-style block exists
    if text.startswith("```"):
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("[") or part.startswith("{"):
                return part
        return ""  # Nothing usable found
    return text  # No markdown, return as-is


@tool
def verify_companies(companies_json: str) -> str:
    """
    Takes a JSON list of companies and verifies their existence via Tavily API.
    Returns a JSON object like: {"Company A": true, "Company B": false}
    """
    try:
        cleaned = clean_json_string(companies_json)

        if not cleaned:
            return json.dumps({"error": "Empty JSON string after cleaning."})

        companies = json.loads(cleaned)

        if not isinstance(companies, list):
            return json.dumps({"error": "Expected a list of company objects."})

    except Exception as e:
        return json.dumps({"error": f"Failed to parse input: {str(e)}"})

    results = {}
    for entry in companies:
        name = entry.get("company")
        verified = False

        if name:
            if TAVILY_KEY:
                try:
                    response = requests.post(
                        "https://api.tavily.com/search",
                        headers={"Authorization": f"Bearer {TAVILY_KEY}"},
                        json={"query": name, "max_results": 1}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        verified = bool(data.get("results"))
                except Exception as e:
                    print(f"Error verifying {name}: {e}")
                    verified = False
        results[name] = verified

    return json.dumps(results, indent=2)
    