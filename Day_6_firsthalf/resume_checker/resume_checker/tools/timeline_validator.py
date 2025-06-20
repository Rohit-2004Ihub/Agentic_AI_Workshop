from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

@tool
def validate_timeline(data_json: str) -> str:
    """
    Analyze timeline for date overlaps and unrealistic jumps. Return JSON summary.
    """
    prompt = f"""
You are a timeline analysis tool.
Data:
{data_json}
Check for overlapping durations, unexplained gaps, or unrealistic fast promotions.
Return JSON:
{{
 "overlaps": [...],
 "gaps_months": [...],
 "irregular_jumps": [...],
 "ok": true/false
}}
"""
    return llm.invoke(prompt).content.strip()
