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
