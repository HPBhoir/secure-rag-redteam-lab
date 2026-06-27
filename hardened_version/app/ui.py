
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.main import ask_question

st.set_page_config(page_title="Vulnerable RAG Lab", layout="wide")
st.title("Vulnerable RAG Security Lab")

business_id = st.selectbox("Choose business/tenant", ["P", "C", "S"])
question = st.text_area("Ask a question")

if st.button("Submit"):
    if question.strip():
        result = ask_question(business_id, question)
        st.subheader("Answer")
        st.write(result["answer"])

        if result["tool_result"]:
            st.subheader("Tool Result")
            st.json(result["tool_result"])

        st.caption(f"Logged to: {result['log_file']}")
