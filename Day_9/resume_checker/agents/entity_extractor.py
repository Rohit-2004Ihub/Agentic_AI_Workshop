import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

def clean_llm_response(text):
    # Remove markdown code fences like ```json or ```
    if text.startswith("```json"):
        text = text.lstrip("```json").strip()
    if text.endswith("```"):
        text = text.rstrip("```").strip()
    return text

def extract_entities(text):
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("❌ GOOGLE_API_KEY not found.")

    prompt = ChatPromptTemplate.from_template("""
    Extract structured data from the resume:
    - Job Titles
    - Companies
    - Start and End Dates
    - Locations

    Return the output as well-formatted JSON.
    
    Resume Text:
    {resume_text}
    """)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key
    )

    chain = prompt | llm
    result = chain.invoke({"resume_text": text})
    raw_output = result.content

    try:
        cleaned_output = clean_llm_response(raw_output)
        return json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Failed to parse JSON from Gemini response: {e}\nRaw output:\n{raw_output}")
