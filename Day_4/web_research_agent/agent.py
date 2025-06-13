import os
from tavily import TavilyClient
import google.generativeai as genai


class WebResearchAgent:
    def __init__(self, topic, gemini_api_key, tavily_api_key):
        self.topic = topic
        self.questions = []
        self.answers = {}
        self.client = TavilyClient(api_key=tavily_api_key)
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    def generate_questions(self):
        prompt = f"""Generate 5–6 diverse and detailed research questions on the topic: "{self.topic}".
Each question should cover a different aspect and be phrased clearly."""
        response = self.model.generate_content(prompt)
        self.questions = [line.strip("-• ").strip() for line in response.text.split('\n') if "?" in line]
        return self.questions

    def search_web(self, question):
        print(f"[+] Searching for: {question}")
        query = question[:400]
        results = self.client.search(query=query, search_depth="advanced", max_results=5)
        return [(item['title'], item['content']) for item in results['results']]

    def collect_answers(self):
        for question in self.questions:
            self.answers[question] = self.search_web(question)

    def generate_report(self):
        # Title
        report = f"# Web Research Report on **{self.topic.title()}**\n\n"

        # Introduction
        report += "## Introduction\n"
        report += f"This report presents a comprehensive exploration of the topic **{self.topic}**. "\
                  "It is structured around key research questions generated using a large language model, "\
                  "and each section includes relevant findings obtained from current and reliable web sources.\n\n"

        # Sections per question
        for idx, question in enumerate(self.questions, 1):
            report += f"## {idx}. {question}\n"
            search_results = self.answers.get(question, [])
            if not search_results:
                report += "_No relevant web results found._\n\n"
                continue

            for title, content in search_results:
                report += f"### {title.strip()}\n"
                report += f"{content.strip()}\n\n"

        # Conclusion
        report += "## Conclusion\n"
        report += "This report compiled insights from various online sources to answer multiple aspects of the topic. "\
                  "Through systematic question-based investigation, it helps readers gain a deeper understanding "\
                  f"of **{self.topic}** from multiple perspectives.\n"

        return report
