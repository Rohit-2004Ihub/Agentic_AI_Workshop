# Agentic_AI_Workshop

----------------------------------------------------Day3----------------------------------------------------
# 📚 AI Research Paper QA - RAG using Gemini + LangChain

A simple Retrieval-Augmented Generation (RAG) system that allows you to **ask questions over multiple research papers** and get answers generated using **Gemini AI**, with source references. It uses **LangChain**, **FAISS**, and **Google Generative AI**.

---

## 🚀 Features

- 📂 Upload and read multiple PDF research papers.
- ✂️ Automatic chunking of text using LangChain's text splitter.
- 📚 Vector embeddings using HuggingFace models or Gemini embeddings.
- 🔎 Similarity search using FAISS.
- 🧠 Answer generation using Gemini Pro (or HuggingFace fallback).
- 🌐 Streamlit-based web UI.

---

## 🛠️ Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Gemini AI API](https://ai.google.dev/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ai-research-qa.git
cd ai-research-qa/Day_3

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt


.env 
GOOGLE_API_KEY=your-gemini-api-key-here

----------------------------------------------------Day4----------------------------------------------------

# 🌐 Web Research Agent using ReAct Pattern

This project implements a **Web Research Agent** that uses the **ReAct pattern (Reasoning + Acting)** to perform topic-based research using LLMs and web search tools.

The agent:
1. Generates research questions using a Large Language Model (Google Gemini).
2. Searches the web using the Tavily API.
3. Compiles a structured report with a title, introduction, question-wise findings, and a conclusion.

---

## 🚀 Features

✅ Uses **Gemini (Google Generative AI)** for intelligent question planning  
✅ Uses **Tavily API** for web search (latest and real-time data)  
✅ Smart **query shortening** for long research questions (>400 characters)  
✅ Fully **structured markdown report** with:
- Title
- Introduction
- Per-question sections
- Web result subsections
- Conclusion

---

## 🧠 Architecture (ReAct Pattern)

[Start]
↓
[LLM (Gemini) Generates Questions] ← Planning Phase (Reasoning)
↓
[Search Each Question with Tavily] ← Acting Phase (Tool Use)
↓
[Extract Answers]
↓
[Generate Final Report]
↓
[End]


---

## 📦 Installation

### ✅ Prerequisites
- Python 3.8+
- Gemini API Key (from https://ai.google.dev)
- Tavily API Key (from https://tavily.com)

### 🔧 Setup

```bash
git clone <repo-url>
cd web_research_agent

# Install dependencies
pip install -r requirements.txt

api keys

GEMINI_API_KEY = "your_gemini_api_key"
TAVILY_API_KEY = "your_tavily_api_key"

Run the agent
python main.py

---------------------------------------------------Day5----------------------------------------------------



# 📘 AI Study Assistant

A lightweight, standalone Study Assistant that helps students summarize study material and automatically generate multiple-choice quiz questions — all without needing external vector databases or retrieval systems.

Built with:
- 🌐 [Streamlit](https://streamlit.io) for interactive UI
- 🧠 [Gemini AI (Google Generative AI)](https://ai.google.dev/)
- 🧱 [LangChain](https://www.langchain.com) for prompt orchestration
- 📄 PyPDF2 for extracting content from PDFs

---

## 🚀 Features

- ✅ Upload course documents in PDF format
- ✨ Automatically summarize educational content into bullet points
- 📝 Generate multiple-choice quiz questions with correct answers
- 💡 Format output cleanly (no HTML tags like `<br>`)
- ⚙️ Fully local, no external vector databases required

---

## 📁 Project Structure


study_assistant/
│
├── app.py # Streamlit app (main UI)
├── quiz_utils.py # Gemini-based summarization & quiz logic
├── .env # Gemini API key (not checked into version control)

api keys

GEMINI_API_KEY = "your_gemini_api_key"

Run the agent
python app.py


🌍 Intelligent Travel Assistant AI
An AI-powered travel assistant built using LangChain, Gemini, and Streamlit that helps users find:

🌦️ Current weather at their destination

🧭 Top tourist attractions in the city

This app uses a multi-tool LangChain agent, combining a custom weather API tool and search agent to give a comprehensive response.

🚀 Features
Get real-time weather using WeatherAPI.

Fetch top-rated attractions using web search (DuckDuckGo or Tavily).

Built using LangChain’s create_tool_calling_agent() architecture.

Uses Gemini AI for summarization and reasoning.

Clean, interactive Streamlit UI.

User Input (city) ─────────────┐
                              ▼
                       [ LangChain Agent ]
                            /     \
                 [Weather Tool]  [Search Tool]
                            \     /
                              ▼
                Combined Final Answer (LLM)
                              ▼
                    Display via Streamlit UI

structure


travel_assistant_ai/
│
├── main.py                # Streamlit entry point
├── travel_agent.py        # LangChain agent logic
├── tools/
│   ├── weather_tool.py    # Custom weather tool using WeatherAPI
│   └── search_tool.py     # DuckDuckGo or Tavily-based web search tool
├── .env                   # API keys
├── README.md              # This file
└── requirements.txt



---------------------------------------------------Day6----------------------------------------------------


🛍️ Clothing Competitor Analyzer
This project is an intelligent business insight tool built with Streamlit, LangGraph, and Gemini AI. It helps clothing store owners analyze nearby competitors, simulate footfall trends, and receive business-friendly reports based on location.

🚀 Features
Enter latitude and longitude of your store location

Get a list of nearby clothing competitors using Overpass API (OpenStreetMap)

Simulate competitor footfall trends and peak hours

Get a realistic business insight report using Gemini 1.5 Flash

Built with a LangGraph agent workflow

📁 Project Structure
graphql
Copy
Edit
clothing_competitor_ai/
│
├── app.py                  # Streamlit frontend
├── graph.py                # LangGraph workflow and nodes
├── agents.py               # Tools and agent functions
├── tools/
│   └── overpass_search.py  # Clothing store fetch logic using Overpass API
└── README.md               # Project documentation
🔧 Requirements
Install dependencies with:

pip install -r requirements.txt
Typical contents of requirements.txt:

streamlit
langgraph
langchain
langchain-google-genai
requests
🔑 API Keys
Make sure to set your Gemini API key in graph.py:


ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key="YOUR_API_KEY"
)
▶️ How to Run
Run the app with:


streamlit run app.py

---------------------------------------------------Day7----------------------------------------------------



# 📘 Documentation – Multi-Agent Research and Summarization System

## 📌 Overview

This project is an intelligent agentic system built using **LangGraph**, **Gemini 1.5 Flash**, and **FAISS**, designed to handle user queries by routing them through specialized agents:
- **LLM Agent** – Handles general reasoning tasks
- **Web Research Agent** – Fetches current, real-time info from the web
- **RAG Agent** – Answers queries using embedded local PDFs
- **Summarization Agent** – Synthesizes results into a final structured response

---

## 🧠 System Architecture

                       +-----------------+
                       |     User Query   |
                       +--------+--------+
                                |
                                v
                         +-------------+
                         | Router Agent| <--- Determines route
                         +--+----------+
                            |   |   |
    +-----------------------+   |   +-------------------------+
    |                           |                             |
    v                           v                             v
+---------------+ +--------------------+ +----------------+
| LLM Agent | | Web Research Agent | | RAG Agent |
| (Gemini LLM) | | (live search API) | | (FAISS + PDFs) |
+-------+-------+ +---------+----------+ +--------+-------+
\ | /
_____________________|______________________/
|
v
+-----------------------------+
| Summarization Agent (LLM) |
+--------------+--------------+
|
v
+------------+
| Final Answer|
+-------------+


---

## 🧩 Agent Behavior

### 🔹 Router Agent
- Checks for keywords like `"latest"`, `"today"`, `"according to PDF"` to decide route
- Fallbacks to Gemini 1.5 Flash if unsure

### 🔹 LLM Agent
- Uses Gemini 1.5 Flash to respond to general queries
- No PDF or external data involved

### 🔹 Web Research Agent
- Performs a web search (can integrate Tavily, SerpAPI, or DuckDuckGo)
- Extracts top few snippets and sends them for summarization

### 🔹 RAG Agent
- Uses **HuggingFace embeddings** (`all-MiniLM-L6-v2`)
- Stores vectors via FAISS
- Extracts top-`k` relevant chunks from PDFs
- Gemini summarizes answers based on those documents

### 🔹 Summarization Agent
- Uses Gemini to synthesize and clean up the response

---

## ⚙️ LangGraph Workflow

```python
def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("router", router_node)
    builder.add_node("llm", llm_node)
    builder.add_node("web_research", web_node)
    builder.add_node("rag", rag_node)
    builder.add_node("summarization", summarize_node)

    builder.set_entry_point("router")
    builder.add_conditional_edges("router", lambda x: x["route"], {
        "llm": "llm",
        "web_research": "web_research",
        "rag": "rag"
    })
    builder.add_edge("llm", "summarization")
    builder.add_edge("web_research", "summarization")
    builder.add_edge("rag", "summarization")
    builder.add_edge("summarization", END)


PDF Processing (RAG Agent)
All PDFs are placed in rag_pdfs/

On running main.py, they are:

Parsed using PyPDF2

Split into ~1000 token chunks with 200-token overlap

Embedded using HuggingFace embeddings

Stored into FAISS at rag_index/

from langchain.embeddings import HuggingFaceEmbeddings
vectorstore = FAISS.from_documents(split_docs, embeddings)
vectorstore.save_local("rag_index")


General Query

"Explain the benefits of AI in education."
→ Routed to: LLM Agent


Real-Time Query
"What is the latest news in climate change?"
→ Routed to: Web Research Agent


PDF-Based Query
provide intoduction for the The Evolution and Impact of Digital Transformation on Global Economies form your data set
→ Routed to: Web Research Agent