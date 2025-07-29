# streamlit_app.py

import streamlit as st
from chatbot.rag_pipeline import generate_answer

st.set_page_config(page_title="Changi Airport Chatbot", layout="centered")

st.title("✈️ Changi Airport Chatbot")
st.markdown("Ask me anything about **Changi Airport** or **Jewel Changi Airport**!")

query = st.text_input("Enter your question:", "")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = generate_answer(query)
        st.success(answer)
