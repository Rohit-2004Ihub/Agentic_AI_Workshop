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
def extract_resume_entities(text: str) -> str:
    """
    Extract job titles, companies, durations, and locations from resume text.
    Returns JSON string.
    """
    prompt = f"""
Extract job data in JSON list format:
[
  {{
    "company": "...",
    "title": "...",
    "duration": "MMM YYYY - MMM YYYY",
    "location": "City, Country"
  }},
  ...
]

Resume:
{text}
"""
    return llm.invoke(prompt).content.strip()
