import streamlit as st
from travel_agent import run_travel_assistant

st.set_page_config(page_title="Travel Assistant AI", layout="centered")

st.title("🧳 Travel Assistant AI")
st.markdown("Get **real-time weather** and **top attractions** for any destination.")

city = st.text_input("Enter your destination city:")

if st.button("Get Travel Info") and city:
    with st.spinner("Fetching details..."):
        result = run_travel_assistant(city)
        st.success("Here's what I found:")
        st.markdown(result)
