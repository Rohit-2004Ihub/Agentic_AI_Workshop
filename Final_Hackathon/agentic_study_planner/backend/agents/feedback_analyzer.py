import os
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY missing from .env")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.4
)

# Feedback Prompt Template
feedback_prompt = PromptTemplate.from_template("""
You are a helpful and constructive academic assistant.

Analyze the following study tasks and provide feedback on:
- Whether the priorities are well-balanced.
- If there are too many tasks (overload).
- Whether micro-goals are clear or missing.
- Tips specific to task content (e.g., recursion, graphs, OS).
- How the learner can improve tomorrow.

Format your answer as a JSON list of strings.

Example Output:
[
  "Try to reduce the number of low-priority tasks.",
  "Micro-goals are missing for some tasks. Add more clarity."
]

Tasks:
{tasks}
""")

# Chain: Prompt → LLM → JSON parse
llm_chain = feedback_prompt | llm | RunnableLambda(
    lambda x: json.loads(x.content.strip().strip("`").replace("json", "").strip())
)

# Final Feedback Analyzer Agent
def analyze_plan_feedback(tasks):
    if not tasks:
        return ["No tasks found to analyze."]

    # --- RULE BASED ---
    rule_feedback = []
    priorities = [t.get("priority", "").lower() for t in tasks]
    high, medium, low = priorities.count("high"), priorities.count("medium"), priorities.count("low")

    if high == 0:
        rule_feedback.append("📌 Try to include at least one high-priority task to drive progress.")
    if low > high:
        rule_feedback.append("⚠️ Too many low-priority tasks can slow momentum. Rebalance priorities.")
    if len(tasks) > 5:
        rule_feedback.append("⏳ You have many tasks today. Consider limiting to 3–5 for deeper focus.")

    from_backlog = [t for t in tasks if t.get("source") == "Backlog"]
    if len(from_backlog) == len(tasks):
        rule_feedback.append("🗂️ All tasks are from backlog. Mix in roadmap topics for long-term growth.")
    elif len(from_backlog) > 2:
        rule_feedback.append("📉 You’re addressing backlog — great! Try to complete one daily to stay on track.")

    no_micro_goals = [t for t in tasks if not t.get("micro_goals")]
    if no_micro_goals:
        rule_feedback.append(f"🔍 {len(no_micro_goals)} task(s) are missing micro-goals. Add subtasks for better clarity.")

    for task in tasks:
        title = task.get("title", "").lower()
        if "recursion" in title:
            rule_feedback.append("💡 Recursion is tricky — use trace tables or recursive stack traces.")
        if "graph" in title:
            rule_feedback.append("🧠 Graphs need structure — divide into BFS, DFS, shortest path, etc.")
        if "os" in title or "operating" in title:
            rule_feedback.append("📘 OS topics are best learned through simulations and visual explanations.")

    # --- LLM FEEDBACK ---
    try:
        task_json = json.dumps(tasks, indent=2)
        llm_feedback = llm_chain.invoke({"tasks": task_json})
    except Exception as e:
        print("⚠️ LLM Feedback generation failed:", e)
        llm_feedback = []

    return rule_feedback + llm_feedback
