import re
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal, Union
from chatbot_agent import get_llm_response
from math_tools import plus, subtract, multiply, divide

# Define state
class GraphState(TypedDict):
    query: str
    response: str

# Determine if it's a math query
def detect_math_query(state: GraphState) -> Literal["math", "chat"]:
    query = state["query"].lower()
    if re.search(r"\b(plus|add|minus|subtract|times|multiply|divided by|divide)\b", query):
        return "math"
    return "chat"

# Math resolver
def math_tool_node(state: GraphState) -> GraphState:
    query = state["query"].lower()
    nums = list(map(float, re.findall(r"\d+(?:\.\d+)?", query)))
    if "plus" in query or "add" in query:
        result = plus(*nums)
    elif "minus" in query or "subtract" in query:
        result = subtract(*nums)
    elif "times" in query or "multiply" in query:
        result = multiply(*nums)
    elif "divided" in query or "divide" in query:
        result = divide(*nums)
    else:
        result = "Sorry, I couldn't understand the math operation."
    return {"query": state["query"], "response": str(result)}

# Chat LLM node
def chatbot_node(state: GraphState) -> GraphState:
    return {"query": state["query"], "response": get_llm_response(state["query"])}

# Build LangGraph
def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("chatbot", chatbot_node)
    builder.add_node("math", math_tool_node)
    builder.set_entry_point("chatbot")
    builder.add_conditional_edges("chatbot", detect_math_query, {
        "math": "math",
        "chat": END
    })
    builder.add_edge("math", END)
    return builder.compile()
