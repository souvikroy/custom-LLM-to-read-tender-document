import streamlit as st
import tempfile
import os
import json
from main import analyze_pdf_with_llm, CRITERIA

import os

st.set_page_config(page_title="Tender Document Analyzer", layout="wide")

st.title("Tender Document Analyzer (Gemini LLM)")
st.write(
    "Upload one or more tender PDF files. The app will extract information based on technical, financial, and commercial criteria using the Gemini LLM (gemini-2.0-flash)."
)

api_key = st.text_input("Enter your Gemini API Key (will not be stored):", type="password")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

uploaded_files = st.file_uploader(
    "Upload PDF files", type=["pdf"], accept_multiple_files=True
)

if uploaded_files:
    if st.button("Analyze"):
        results = {}
        with st.spinner("Analyzing documents..."):
            for uploaded_file in uploaded_files:
                # Save uploaded file to a temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                try:
                    result = analyze_pdf_with_llm(tmp_path, CRITERIA)
                    results[uploaded_file.name] = result
                except Exception as e:
                    results[uploaded_file.name] = {"error": str(e)}
                finally:
                    os.remove(tmp_path)
        st.success("Analysis complete!")
        for fname, data in results.items():
            st.subheader(f"Results for {fname}")
            st.json(data)
else:
    st.info("Please upload one or more PDF files to begin.")
