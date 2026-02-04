import streamlit as st
import requests
import time

st.title("Personal AI Assistant")

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send request to backend
    try:
        response = requests.post(f"{BACKEND_URL}/chat", json={"message": prompt})
        if response.status_code == 200:
            assistant_response = response.json()["response"]
        else:
            assistant_response = "Sorry, I couldn't process your request."
    except:
        assistant_response = "Error connecting to backend. Make sure it's running."

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Sidebar for adding knowledge
with st.sidebar:
    st.header("Add Knowledge")
    knowledge_text = st.text_area("Enter knowledge text:")
    if st.button("Add Knowledge"):
        if knowledge_text:
            try:
                response = requests.post(f"{BACKEND_URL}/add_knowledge", json={"text": knowledge_text})
                if response.status_code == 200:
                    st.success("Knowledge added successfully!")
                else:
                    st.error("Failed to add knowledge.")
            except:
                st.error("Error connecting to backend.")
        else:
            st.warning("Please enter some text.")