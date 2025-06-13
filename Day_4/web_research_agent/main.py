from agent import WebResearchAgent

# Replace with your actual API keys
GEMINI_API_KEY = "AIzaSyBVsVjmgBPpiYWyV0S77ju8mRcPbOyoKrw"
TAVILY_API_KEY = "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"

def main():
    topic = input("Enter your research topic: ")
    agent = WebResearchAgent(topic, GEMINI_API_KEY, TAVILY_API_KEY)

    print("\n[1] Generating research questions...")
    questions = agent.generate_questions()
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")

    print("\n[2] Gathering web results...")
    agent.collect_answers()

    print("\n[3] Generating report...")
    report = agent.generate_report()

    with open("report_output.md", "w", encoding="utf-8") as file:
        file.write(report)

    print("\n✅ Report saved as 'report_output.md'")

if __name__ == "__main__":
    main()
