# chat_ui.py

import streamlit as st
from chatbot.rag_pipeline import generate_answer

st.set_page_config(page_title="Changi Airport Chatbot", layout="centered")
st.title("🛫 Changi Airport Assistant")

st.markdown("""
Ask anything about Changi Airport — facilities, shopping, attractions, terminals and more!
""")

# Input
user_input = st.text_input("Enter your question:")

# When submitted
if user_input:
    with st.spinner("Searching for answer..."):
        response = generate_answer(user_input)
    st.success("Answer:")
    st.write(response)
