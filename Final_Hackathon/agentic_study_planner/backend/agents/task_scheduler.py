from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
from dotenv import load_dotenv

# Load the Gemini API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")
os.environ["GOOGLE_API_KEY"] = api_key

# Initialize Gemini 1.5 Flash model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# Dynamic prompt template (no exam, placement, or fixed tags)
prompt = PromptTemplate.from_template("""
You are an intelligent AI agent helping a learner create their **daily study tasks**.

Use the learner's **custom roadmap**, **recent study history**, and **learning preferences** to generate **3 to 5 concise, actionable tasks**.

📌 Format each task with:
- A short title describing what to do
- A priority (High / Medium / Low)
- A reason (why this task is important or timely)

📌 Guidelines:
- Only use topics provided by the learner.
- Prioritize tasks that were skipped, backlogged, or marked weak.
- Output a clean JSON array of task dictionaries.



Learner Profile:
{learner_profile}

Study Roadmap:
{roadmap}

Recent Learning History:
{history}
""")

def generate_daily_tasks(learner_profile: str, roadmap: str, history: str):
    """
    Generate 3–5 personalized study tasks from dynamic learner input.

    Arguments:
    - learner_profile: a sentence or paragraph written by the learner
    - roadmap: topics the learner plans to study
    - history: topics already studied, skipped, or marked difficult

    Returns:
    - List of dictionaries with 'title', 'priority', and 'reason'
    """
    chain = prompt | llm

    print("🧾 [DEBUG] Final Inputs to LLM:")
    print("🧍 Profile:", learner_profile)
    print("🗺️ Roadmap:", roadmap)
    print("📅 History:", history)

    response = chain.invoke({
        "learner_profile": learner_profile,
        "roadmap": roadmap,
        "history": history
    })

    print("🧠 LLM Output:")
    print(response.content)

    try:
        raw = response.content.strip()

        # Remove markdown wrapping if present
        if raw.startswith("```"):
            raw = raw.strip("`").replace("json", "").strip()

        return json.loads(raw)

    except Exception as e:
        print("⚠️ Failed to parse LLM output:", e)
        print("❌ Raw Output:", response.content)
        return []
