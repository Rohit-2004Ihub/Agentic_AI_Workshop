import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
    google_api_key=GOOGLE_API_KEY
)

# 🧠 Prompt to filter backlog intelligently
prompt = PromptTemplate(
    input_variables=["today_tasks", "backlog"],
    template="""
You are an intelligent study planner.

📌 Your task: From the BACKLOG, select 2–3 tasks that:
- are **not already in** TODAY'S PLAN,
- and are **most urgent or relevant** for today.

📋 For each selected task, assign a priority: "High" or "Medium".

✏️ Format:
[
  {{"title": "Task Title", "priority": "High"}},
  ...
]

TODAY'S PLAN:
{today_tasks}

BACKLOG:
{backlog}
"""
)

# LLM Chain
llm_chain = LLMChain(llm=llm, prompt=prompt)

# 🚀 Final Backlog Agent
def merge_backlog_into_tasks(today_tasks, backlog):
    """
    Merges intelligent backlog suggestions into today's study plan using Gemini LLM.
    Falls back to simple deduplication if LLM fails.
    """
    existing_titles = {task["title"].lower() for task in today_tasks}
    today_summary = "\n".join(f"- {task['title']}" for task in today_tasks)
    backlog_summary = "\n".join(f"- {item['title']}" for item in backlog)

    try:
        response = llm_chain.run({
            "today_tasks": today_summary,
            "backlog": backlog_summary
        })

        selected = json.loads(response.strip().strip("`").replace("json", "").strip())

        # Merge selected backlog tasks
        for task in selected:
            title = task.get("title", "").strip()
            priority = task.get("priority", "High")
            if title and title.lower() not in existing_titles:
                today_tasks.append({
                    "title": title,
                    "priority": priority,
                    "source": "Backlog"
                })

        print("🧾 LLM-Selected Backlog Added:", [t["title"] for t in selected])
        return today_tasks

    except Exception as e:
        print("⚠️ LLM Backlog Agent failed:", e)

        # ✅ Fallback logic
        fallback_added = []
        merged = today_tasks.copy()
        for item in backlog:
            title = item.get("title", "").strip()
            if title and title.lower() not in existing_titles:
                merged.append({"title": title, "priority": "High", "source": "Backlog"})
                fallback_added.append(title)
        print("🧾 Fallback Backlog Added:", fallback_added)
        return merged
