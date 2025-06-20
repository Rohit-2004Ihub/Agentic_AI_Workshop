import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from agent.resume_agent import run_resume_validation

st.set_page_config(page_title="Resume Fraud Detector", layout="wide")
st.title("🕵️ Resume Fraud Detector")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

if uploaded_file and st.button("Analyze Resume"):
    with st.spinner("Processing resume..."):
        raw_text = extract_text_from_pdf(uploaded_file)

        extracted_entities, company_check, timeline_report, final_score = run_resume_validation(raw_text)

        st.subheader("📌 Extracted Entities")
        st.text_area("Entities", extracted_entities, height=300)

        st.subheader("🔍 Company Verification")
        st.text_area("Verified Companies", company_check, height=300)

        st.subheader("⏳ Timeline Analysis")
        st.text_area("Timeline Validation", timeline_report, height=300)

        st.subheader("✅ Final Credibility Score & Flags")
        st.text_area("Score Report", final_score, height=350)
