from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
import os

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

@tool
def score_resume(
    extracted_entities: str,
    company_check: str,
    timeline_report: str
) -> str:
    """
    Uses AI to score resume credibility based on extracted entities, company verification, and timeline validation.
    Returns an integrity score with justification.
    """
    prompt = f"""
    Analyze the following data from a candidate's resume analysis:
    
    1. Extracted Entities:
    {extracted_entities}

    2. Company Check Results:
    {company_check}

    3. Timeline Validation Report:
    {timeline_report}

    Based on the above, assign a final resume credibility score between 0–100.
    Also, explain your rationale for the score (e.g., timeline inconsistencies, fake companies, unrealistic job hops).

    Return the result in the following JSON format:
    {{
      "score": <number>,
      "verdict": "<summary of issues>",
      "ok": true or false
    }}
    """
    return llm.invoke(prompt).content
