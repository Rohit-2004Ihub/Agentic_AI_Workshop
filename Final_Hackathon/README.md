AI-Powered Personalized Study Planner
This project is an AI-driven personalized study plan generator designed to help learners effectively plan and track their study goals using uploaded learning materials. It leverages LangChain, Google Gemini (via GenerativeAI API), and agentic task pipelines to create daily plans, generate micro-goals, provide feedback, and evaluate learning consistency.

Features
Upload a learning roadmap or log as PDF.


Extract topics, backlogs, and recent history from the document.


Generate a personalized daily study plan based on roadmap and backlog.


Map each study task to actionable micro-goals.


Analyze the quality of the study plan with AI-generated feedback.


Calculate consistency score based on recent activity.


Dynamic agent pipeline powered by LangChain and Gemini 1.5 Flash.



Tech Stack
Backend: Django + LangChain + Gemini API


Frontend: HTML5 (Django Templates)


AI Models: Google Gemini 1.5 Flash


Vector Store: FAISS (optional for RAG-based goal generation)


PDF Processing: PyPDF2


Environment Management: dotenv, os



Folder Structure
bash
CopyEdit
ai_study_planner/
├── backend/
│   ├── agents/
│   │   ├── topic_extractor.py
│   │   ├── task_scheduler.py
│   │   ├── micro_goal_mapper.py
│   │   ├── backlog_manager.py
│   │   ├── feedback_analyzer.py
│   │   └── consistency_scorer.py
│   ├── core/
│   │   └── agent_orchestrator.py
│   ├── utils/
│   │   └── pdf_reader.py
├── studyplanner/
│   ├── templates/studyplanner/index.html
│   ├── views.py
│   ├── forms.py
├── main.py (optional runner)
├── manage.py
├── .env
└── requirements.txt


Installation
1. Clone the Repository
git clone https://github.com/your-org/ai-study-planner.git
cd ai-study-planner

2. Create and Activate Virtual Environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment
GOOGLE_API_KEY=your_api_key_here

5. Run Django Server
python manage.py runserver

Then open http://localhost:8000 in your browser.

How It Works
Agent Pipeline
PDF Upload
User uploads a learning roadmap, logs, or profile PDF.


Text Extraction
Extract raw text using PyPDF2.


Topic Extraction Agent
Identifies topics and study goals from the uploaded document.


Task Scheduler Agent
Generates 3–5 actionable tasks for the day using LLM.


Micro Goal Mapper Agent
Enriches each task with small achievable subtasks (micro-goals).


Backlog Manager Agent
Selects important backlog tasks and merges with today's plan.


Feedback Analyzer Agent
Reviews priority mix, diversity, and relevance using LLM + rule-based logic.


Consistency Scorer Agent
Calculates consistency score based on recent history and current plan.



Example Output
json
CopyEdit
{
  "plan": [
    {
      "title": "Review Graph Traversal Algorithms",
      "priority": "High",
      "micro_goals": ["Watch BFS/DFS lecture", "Draw 3 graph problems", "Code 2 LeetCode questions"],
      "source": "Roadmap"
    },
    {
      "title": "Revise Heap Memory Management",
      "priority": "Medium",
      "micro_goals": ["Read OS notes", "Sketch heap allocation example"],
      "source": "Backlog"
    }
  ],
  "feedback": [
    "Try to include more roadmap topics.",
    "Only 1 high-priority task found. Increase task intensity.",
    "Missing micro-goals in 1 task."
  ],
  "consistency": {
    "score": 85,
    "streak": 2,
    "momentum": "Medium"
  }
}


┌──────────────────────┐
│    HTML Frontend     │
│  (Upload PDF Form)   │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│     Django View      │
│ index(request)       │
└────────┬─────────────┘
         │
         ▼
┌────────────────────────────┐
│  PDF Extractor (utils)     │
└────────┬───────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Agent Orchestrator         │
│ (run all agents sequentially│
└────────┬────────────────────┘
         │
         ▼
┌────────┴────────┬───────────┬────┬────────┬────┬─────────┬───────┬────────────────┬
│ Topic Extractor │ Task Scheduler │ Micro Goal  │ Backlog Manager │ Feedback &     │
│ Agent           │ Agent          │ Mapper Agent│ Agent           │ Scoring Agents │
└─────────────────┴────────────────┴─────────────┴─────────────────┴────────────────┴
         │
         ▼
┌─────────────────────────────┐
│ Django Template (index.html)│
│ Render tasks, feedback,     │
│ micro-goals, consistency    │
└─────────────────────────────┘




Future Improvements
Add user authentication and dashboards
Integrate spaced repetition for task scheduling
Save and visualize past plans using charts
Enable RAG using FAISS + custom PDF dataset

