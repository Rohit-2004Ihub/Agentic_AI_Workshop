Resume Fraud Detector
This project is a simple yet powerful AI-driven tool built with Streamlit, LangChain, and Gemini API that detects fraudulent information in resumes. It uses multiple AI agents to:

Extract entities like job titles, companies, and employment dates

Check for fake or unverifiable companies

Detect timeline overlaps or unrealistic career jumps

Assign credibility scores to resumes

🚀 Features
📄 PDF resume upload

🧠 AI-powered entity extraction

🔍 Timeline validation with logic for overlaps & jumps

🌐 Company credibility check (simulated)

✅ Final credibility score with validation summary


    resume_checker/
│
├── app.py                            # Streamlit frontend
├── agent/
│   └── resume_agent.py              # Main agent orchestrator using LangChain
│
├── tools/
│   ├── extractor.py                 # Extracts job experience info using LLM
│   └── validator.py                 # Validates timeline and companies
│
├── utils/
│   └── pdf_reader.py                # Extracts text from uploaded PDF
│
├── .env                             # Contains your Google API key
└── README.md                        # You're here!


pip install -r requirements.txt


streamlit
langchain
langchain-google-genai
python-dotenv
PyPDF2



GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY==your_google_gemini_api_key

streamlit run app.py
Then open http://localhost:8501 in your browser.