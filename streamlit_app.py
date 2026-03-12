import streamlit as st
import requests

st.title("Enterprise Multi-Source RAG + Agentic Analytics Demo")
question = st.text_input("Ask a business question", "Why are Texas snack sales down?")
role = st.selectbox("Role", ["analyst", "manager", "admin"])
regions = st.multiselect("Allowed regions", ["US-SOUTH", "US-WEST"], default=["US-SOUTH"])

if st.button("Run"):
    payload = {
        "question": question,
        "role": role,
        "allowed_regions": regions,
        "business_units": ["snacks"],
        "include_evidence": True,
    }
    resp = requests.post("http://localhost:8000/ask", json=payload, timeout=60)
    data = resp.json()
    st.subheader("Route")
    st.write(data.get("route"))
    st.subheader("Final Answer")
    st.write(data.get("answer"))
    st.subheader("Validation Notes")
    st.write(data.get("validation_notes"))
    st.subheader("Structured Evidence")
    st.json(data.get("structured_evidence"))
    st.subheader("Document Evidence")
    st.json(data.get("document_evidence"))
