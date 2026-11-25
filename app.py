
import streamlit as st
import asyncio

from autogen_agent import ask_movie_agent
from database import create_database


# Create Database
create_database()


# Page Configuration
st.set_page_config(
    page_title="Movie Automation System",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Automation System")

st.write(
    "Ask anything about Movies, Multiplex and Halls."
)


# Store Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display Previous Messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat Input
user_prompt = st.chat_input(
    "Ask about movies..."
)


if user_prompt:

    # Display User Message
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.write(user_prompt)


    # Get AI Response
    with st.chat_message("assistant"):

        with st.spinner("AI Agent is working..."):

            try:

                response = asyncio.run(
                    ask_movie_agent(user_prompt)
                )

                st.write(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                st.error(f"Error: {e}")
