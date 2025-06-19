import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from agents.entity_extractor import extract_entities
from agents.company_verifier import verify_companies
from agents.timeline_validator import validate_timeline
from agents.credibility_scorer import score_resume

st.set_page_config(page_title="Resume Checker", layout="centered")
st.title("🔎 Resume Authenticity Checker (AI + RAG + Agents)")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.success("✅ Resume uploaded and processed.")

    with st.spinner("🔍 Extracting entities..."):
        entities = extract_entities(text)
    st.json(entities)

    with st.spinner("🌐 Verifying companies..."):
        company_check = verify_companies([exp["company"] for exp in entities["work_experience"]])
    st.json(company_check)

    with st.spinner("🕒 Validating timeline..."):
        timeline_check = validate_timeline(entities["work_experience"])
    st.json(timeline_check)

    with st.spinner("📊 Scoring credibility..."):
        final_score = score_resume(entities, company_check, timeline_check)
    st.write(f"🔐 **Resume Credibility Score:** {final_score['score']} / 100")
    st.write(f"⚠️ **Flagged Issues:** {final_score['flags']}")
