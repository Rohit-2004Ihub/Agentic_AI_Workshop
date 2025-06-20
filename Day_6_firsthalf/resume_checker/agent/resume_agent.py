from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

from tools.extractor import extract_resume_entities
from tools.validator import validate_resume_timeline

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

tools = [extract_resume_entities, validate_resume_timeline]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_resume_validation(text: str):
    extracted = agent.run(f"Extract job experience from this resume: {text}")
    validated = agent.run(f"Validate this resume for fraud and score it: {text}")
    return extracted, validated
