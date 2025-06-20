from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

@tool
def extract_resume_entities(text: str) -> str:
    """Extract company names, job titles, and durations from the resume."""
    prompt = f"""
    Extract job experiences from the resume in JSON format:
    [
      {{
        "company": "Company Name",
        "title": "Job Title",
        "duration": "Jan 2020 - Mar 2023"
      }}
    ]

    Resume:
    {text}
    """
    return llm.invoke(prompt).content
