from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from agents import fetch_nearby_stores
from typing import TypedDict

# 1. Define the state schema
class GraphState(TypedDict):
    input: str
    tool_output: str
    insight: str

# 2. Setup Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyA8Mgdp2_gjGPESD_C_QKlfDbreUKQTDd4")

# 3. Tool execution node
def run_tool_node(state: GraphState) -> GraphState:
    user_input = state["input"]
    tool_output = fetch_nearby_stores.invoke(user_input)
    return {**state, "tool_output": tool_output}

# 4. Gemini analysis node
def generate_insight_node(state: GraphState) -> GraphState:
    prompt = f"""
    Based on the following list of clothing stores and locations:
    {state['tool_output']}

    Simulate their footfall trends and busiest hours using realistic assumptions.
    Provide the insight as a business-friendly report.
    """
    response = llm.invoke(prompt)
    return {**state, "insight": response.content}

# 5. Build the graph
def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("fetch_stores", run_tool_node)
    builder.add_node("generate_report", generate_insight_node)

    builder.set_entry_point("fetch_stores")
    builder.add_edge("fetch_stores", "generate_report")
    builder.set_finish_point("generate_report")
    return builder.compile()
