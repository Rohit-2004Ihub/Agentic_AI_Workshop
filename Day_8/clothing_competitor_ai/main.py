import streamlit as st
from graph import build_graph

# Streamlit App Title
st.title("🛍️ Clothing Competitor Analyzer")

# Input fields for latitude and longitude
lat = st.text_input("Enter Latitude (e.g., 12.9716)")
lon = st.text_input("Enter Longitude (e.g., 77.5946)")

# Run the analysis on button click
if st.button("Analyze Competitors"):
    if lat and lon:
        location = f"{lat},{lon}"
        
        # Run the LangGraph workflow
        st.info("Running competitor analysis...")
        workflow = build_graph()
        result = workflow.invoke({"input": location})
        
        # Display results
        st.subheader("🧾 Nearby Clothing Stores:")
        st.text(result["tool_output"])

        st.subheader("📊 Business Insight:")
        st.markdown(result["insight"])
    else:
        st.warning("Please enter both latitude and longitude.")
