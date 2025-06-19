import streamlit as st
from graph_builder import build_graph

st.title("🤖 LangGraph Math & Chat Agent")

query = st.text_input("Ask a question or math problem:", "")

if query:
    graph = build_graph()
    result = graph.invoke({"query": query})
    st.success(result["response"])
