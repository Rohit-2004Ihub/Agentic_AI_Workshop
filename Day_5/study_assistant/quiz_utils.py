import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_content(content: str) -> str:
    prompt = f"Summarize the following study material into concise bullet points:\n\n{content}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_quiz(summary: str) -> str:
    prompt =  f"""
You are an expert quiz generator. Based on the following summary, generate exactly 3 multiple-choice questions in the specified format.

Each question must:
- Be based strictly on the summary
- Have 4 answer choices (a, b, c, d)
- Be numbered like this: 1. a), 2. b), 3. c), 4. d)
- Show the answer in this format: Answer: b) <correct answer text>
- Be clearly separated by a blank line

Summary:
{summary}

Format:
1. <question>
1. a) <option A>
2. b) <option B>
3. c) <option C>
4. d) <option D>

Answer: <correct letter and option>
"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

