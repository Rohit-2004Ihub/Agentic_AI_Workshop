from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from tools.web_search import search_company_online  # 👈 This will be a custom search tool

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

@tool
def validate_resume_timeline(text: str) -> str:
    """Validates resume timeline, detects overlaps, and checks company existence online. Returns short paragraph summary."""

    # Step 1: Extract company names (basic approach via LLM)
    extract_prompt = f"""
Extract only the company names from the resume below as a Python list. Do not include any extra text.

Resume:
{text}
"""
    try:
        company_names_str = llm.invoke(extract_prompt).content.strip()
        company_list = eval(company_names_str) if company_names_str.startswith("[") else []
    except:
        company_list = []

    # Step 2: Check online presence of each company
    non_verified_companies = []
    for company in company_list:
        result = search_company_online(company)  # custom web search tool
        if not result:  # if search returns empty or no good match
            non_verified_companies.append(company)

    # Step 3: Resume analysis + credibility report
    validate_prompt = f"""
You are an AI resume checker.

1. The following companies could not be verified online: {non_verified_companies}
2. Analyze the following resume text for:
   - Timeline overlaps
   - Unrealistic gaps or jumps
3. Then assign a credibility score (0–100) based on your findings.
4. Write a short paragraph report combining all observations.

Resume:
{text}

Return only the final paragraph summary.
"""

    try:
        summary = llm.invoke(validate_prompt).content.strip()
        return summary
    except Exception as e:
        return f"❌ Error generating report: {e}"
