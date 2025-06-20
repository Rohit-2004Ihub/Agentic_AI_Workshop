# backend/agents/topic_extractor.py

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import json

# topic_extractor.py
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


def extract_study_topics(pdf_text):
    prompt = PromptTemplate.from_template("""
You are a study assistant.

From the following roadmap or study notes, extract 2-7 important CS topics that the learner should focus on **today**.

If there are topics with deadlines or topics that have not been reviewed recently, include them.

If the content is unclear or unstructured, try to extract any repeated or technical terms.

Respond only with a JSON list:
["Stacks", "Graphs", "Virtual Memory"]

Text:
{pdf_text}
""")

    try:
        result = (prompt | llm).invoke({"pdf_text": pdf_text})
        raw = result.content.strip()

        if raw.startswith("```"):
            raw = raw.strip("`").replace("json", "").strip()

        topics = json.loads(raw)

        if not isinstance(topics, list) or not topics:
            raise ValueError("Empty topic list")

        print("✅ Extracted Topics:", topics)
        return topics

    except Exception as e:
        print("⚠️ Failed to extract topics:", e)
        print("⚠️ Raw output:", result.content if 'result' in locals() else "No result")
        # 👇 Add fallback so Task Scheduler works
        return ["Graphs", "Threads", "Virtual Memory"]
