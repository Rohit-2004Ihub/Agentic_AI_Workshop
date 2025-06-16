import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from agent.resume_agent import run_resume_validation

st.set_page_config(page_title="Resume Fraud Detector", layout="centered")
st.title("🕵️ Resume Fraud Detector")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

if uploaded_file and st.button("Analyze Resume"):
    with st.spinner("Processing..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        extracted_data, validated_report = run_resume_validation(raw_text)

        st.subheader("📄 Extracted Entities")
        st.text_area("Extracted Entities (JSON)", value=extracted_data, height=250, max_chars=None)

        st.subheader("✅ Validation Results")
        st.text_area("Validation Summary", value=validated_report, height=250, max_chars=None)
