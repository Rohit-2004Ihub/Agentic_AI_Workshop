# streamlit_app.py

import streamlit as st
from main import build_graph

st.set_page_config(page_title="Multi-Agent Research with LangGraph", layout="wide")
st.title("🤖 LangGraph-Powered Research & Summarization")

query = st.text_input("🔍 Ask a question...")

if st.button("Run Agents"):
    with st.spinner("Processing..."):
        graph = build_graph()
        result = graph.invoke({"query": query})
        st.markdown("### ✅ Final Answer")
        st.success(result["final_answer"])

        st.markdown("### 🔀 Routing Path")
        st.info(f"Agent route taken: `{result['route']}`")

        st.markdown("### 🧾 Intermediate Output")
        st.code(result["result"])
