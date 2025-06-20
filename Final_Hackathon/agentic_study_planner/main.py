# streamlit_app.py

import streamlit as st
import os

from backend.utils.pdf_reader import extract_text_from_pdf
from backend.core.agent_orchestrator import generate_study_plan

# Set up directories
UPLOAD_DIR = "backend/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Streamlit UI
st.set_page_config(page_title="📘 AI Study Plan Generator", layout="centered")
st.title("📄 Upload Learning PDF to Generate Smart Study Plan")

uploaded_file = st.file_uploader("📤 Upload your learning roadmap / backlog PDF", type="pdf")

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, "learner_upload.pdf")

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ PDF uploaded and saved.")

    # 1. Extract text from PDF
    try:
        text = extract_text_from_pdf(file_path)
    except Exception as e:
        st.error(f"❌ Error reading PDF: {str(e)}")
        st.stop()

    # Simulated history and backlog (replace with real data if available)
    history = []
    backlog = []

    st.info("🔄 Running Agent Pipeline...")

    # 2. Run all agents via orchestrator
    result = generate_study_plan(text, history=history, backlog=backlog)

    # Sequential Output from each Agent
    st.write("### ✅ Task Scheduler Agent Output")
    for task in result["plan"]:
        st.markdown(f"🔹 **{task['title']}** – Priority: `{task['priority']}`")

    st.divider()

    st.write("### 🎯 Micro Goal Mapper Output")
    for task in result["plan"]:
        st.subheader(f"📘 {task['title']}")
        micro_goals = task.get("micro_goals", [])
        if micro_goals:
            for goal in micro_goals:
                st.markdown(f"- {goal}")
        else:
            st.warning("⚠️ No micro-goals generated.")

    st.divider()

    st.write("### 📥 Backlog Manager Output")
    st.markdown("✅ Backlogs have been merged into today's task list where necessary.")

    st.divider()

    st.write("### 🔎 Study Plan Feedback (Feedback Analyzer Agent)")
    if result["feedback"]:
        for insight in result["feedback"]:
            st.markdown(f"- 💡 {insight}")
    else:
        st.markdown("✅ No feedback needed. Your study plan looks great!")
    st.divider()

    st.write("### 📊 Consistency Score (Consistency Scorer Agent)")
    st.metric("📈 Today's Consistency Score", f"{result['consistency']['score']} / 100")
    st.caption(f"📍 Streak: {result['consistency']['streak']} days")
