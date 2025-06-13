import os
from tavily import TavilyClient
import google.generativeai as genai


class WebResearchAgent:
    def __init__(self, topic, gemini_api_key, tavily_api_key):
        self.topic = topic
        self.questions = []
        self.answers = {}

        # Configure APIs
        self.client = TavilyClient(api_key=tavily_api_key)
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    def generate_questions(self):
        """Generate 5–6 well-structured research questions using Gemini LLM."""
        prompt = f"""Generate 5–6 diverse and detailed research questions on the topic: "{self.topic}".
                   Each question should cover a different aspect and be phrased clearly."""
        response = self.model.generate_content(prompt)
        self.questions = [line.strip("-• ").strip() for line in response.text.split('\n') if "?" in line]
        return self.questions

    def shorten_query(self, long_question):
        """Use Gemini to shorten any question over 400 characters."""
        prompt = f"""Please shorten the following question to be under 400 characters without losing its core meaning:\n\n{long_question}"""
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def search_web(self, question):
        """Perform web search using Tavily with smart query shortening."""
        print(f"[+] Original Question: {question}")

        # Handle long queries
        if len(question) > 400:
            question = self.shorten_query(question)
            print(f"[✓] Shortened Query for Tavily: {question}")

        results = self.client.search(query=question, search_depth="advanced", max_results=5)
        return [(item['title'], item['content']) for item in results['results']]

    def collect_answers(self):
        """Search web for each question and collect answers."""
        for question in self.questions:
            self.answers[question] = self.search_web(question)

    def generate_report(self):
        """Generate a markdown report with title, introduction, Q&A sections, and conclusion."""
        report = f"# Web Research Report on **{self.topic.title()}**\n\n"

        report += "## Introduction\n"
        report += f"This report presents a comprehensive exploration of the topic **{self.topic}**. "\
                  "It is structured around key research questions generated using a large language model, "\
                  "and each section includes relevant findings obtained from current and reliable web sources.\n\n"

        for idx, question in enumerate(self.questions, 1):
            report += f"## {idx}. {question}\n"
            search_results = self.answers.get(question, [])
            if not search_results:
                report += "_No relevant web results found._\n\n"
                continue

            for title, content in search_results:
                report += f"### {title.strip()}\n{content.strip()}\n\n"

        report += "## Conclusion\n"
        report += "This report compiled insights from various online sources to answer multiple aspects of the topic. "\
                  "Through systematic question-based investigation, it helps readers gain a deeper understanding "\
                  f"of **{self.topic}** from multiple perspectives.\n"

        return report
