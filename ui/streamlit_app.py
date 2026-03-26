import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from app.main import CustomerSupportSystem


st.set_page_config(page_title="AI Customer Support Assistant")

st.title("AI Customer Support Assistant")
st.write("Ask questions based on company documents.")

if "system" not in st.session_state:
    st.session_state.system = CustomerSupportSystem()

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.write(content)

user_input = st.chat_input("Write your question")

if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    response = st.session_state.system.ask(user_input)

    st.session_state.messages.append(("assistant", response))
    with st.chat_message("assistant"):
        st.write(response)