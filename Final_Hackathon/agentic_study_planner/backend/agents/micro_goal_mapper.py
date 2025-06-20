# backend/agents/micro_goal_mapper.py

import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.vector_store import load_vector_store

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY missing in .env")
os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.4)

def enrich_tasks_with_micro_goals(task_list):
    retriever = load_vector_store("faiss_index/micro_goal_index").as_retriever()
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

    for task in task_list:
        topic = task["title"]
        query = f"""
Suggest 2 actionable micro-goals for the topic "{topic}".
Use the internal knowledge base. Be specific and task-oriented.
If no data found, still suggest general subtasks based on common learning steps.
"""
        try:
            response = qa.run(query)
            task["micro_goals"] = response.strip().split("\n")
        except Exception as e:
            task["micro_goals"] = ["Micro-goal generation failed."]
            print(f"⚠️ Error for task '{topic}':", e)

    return task_list
