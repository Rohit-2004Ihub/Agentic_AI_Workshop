import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load API key
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 📜 Prompt for LLM-based consistency scoring
prompt = PromptTemplate(
    input_variables=["history_summary", "today_plan_summary"],
    template="""
You are a productivity assistant that evaluates a learner's study consistency.

Using the HISTORY and TODAY'S PLAN below, return:
1. A score between 0 and 100 (based on streaks, task completion, plan volume)
2. A 1–2 word momentum label ("High", "Medium", "Low")
3. A streak count: how many recent days were consistent

Respond in this JSON format:
{{
  "score": <int>,
  "streak": <int>,
  "momentum": "<string>"
}}

HISTORY:
{history_summary}

TODAY'S PLAN:
{today_plan_summary}
"""
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

# Helper: Format tasks into readable checklist
def summarize_tasks(tasks):
    return "\n".join(
        f"- {t.get('title')} ({'✅' if t.get('completed') else '❌'})"
        for t in tasks
    )

# 🧠 Final Consistency Agent
def calculate_consistency_score(history, today_plan):
    history_summary = summarize_tasks(history)
    today_summary = summarize_tasks(today_plan)

    try:
        response = llm_chain.run({
            "history_summary": history_summary,
            "today_plan_summary": today_summary
        })

        parsed = json.loads(response.strip().strip("`").replace("json", "").strip())

        return {
            "score": parsed.get("score", 0),
            "streak": parsed.get("streak", 0),
            "momentum": parsed.get("momentum", "Unknown")
        }

    except Exception as e:
        print("⚠️ LLM Consistency Scorer failed:", e)

        # 🛠️ Safe Fallback Logic
        completed = sum(1 for h in history if h.get("completed"))
        streak = history[-3:]
        streak_count = sum(1 for d in streak if d.get("completed"))
        score = (completed * 10 + streak_count * 20 + len(today_plan) * 5)

        return {
            "score": score,
            "streak": streak_count,
            "momentum": (
                "🔥 High" if score > 100 else
                "⚡ Medium" if score > 60 else
                "🔸 Low"
            )
        }
