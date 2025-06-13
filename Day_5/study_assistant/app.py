import streamlit as st
import PyPDF2
from quiz_utils import summarize_content, generate_quiz

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    return full_text

st.set_page_config(page_title="Study Assistant", layout="centered")
st.title("📘 AI Study Assistant using Gemini + LangChain")

uploaded_file = st.file_uploader("Upload a PDF file with study material", type="pdf")

if uploaded_file:
    st.info("📄 Extracting text from PDF...")
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    with st.expander("🔍 View Raw Text"):
        st.text_area("PDF Content", pdf_text, height=300)

    if st.button("Generate Summary and Quiz"):
        with st.spinner("Summarizing content..."):
            summary = summarize_content(pdf_text)
            st.success("✅ Summary Generated!")
            st.markdown(f"### Summary\n{summary}")

        with st.spinner("Generating quiz questions..."):
            quiz = generate_quiz(summary)
            st.success("✅ Quiz Generated!")
            st.markdown("### Quiz Questions")
            st.markdown(quiz)
