import streamlit as st
import requests
import os
import subprocess
import tempfile

def initialize_session():
    
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    if "assistant" not in st.session_state:
        st.session_state.assistant = None
    
    if "file_uploader" not in st.session_state:
        st.session_state.file_uploader = []

    if "llm_model" not in st.session_state:
        st.session_state.llm_model = "deepseek-r1:latest"

    if "embedding_model" not in st.session_state:
        st.session_state.embedding_model = "mxbai-embed-large"

    if "dimensions" not in st.session_state:
        st.session_state.dimensions = 1024

    if "is_local" not in st.session_state:
        st.session_state.is_local = True
        
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""

    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = ""
        
    if "ingestion_spinner" not in st.session_state:
        st.session_state.ingestion_spinner = st.empty()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "llm_option" not in st.session_state:
        st.session_state.llm_option = ""
        
def clear_chat():
    st.session_state.chat_history = []
    st.rerun()

def read_and_save_file():
    """Handle file upload and ingestion."""

    st.session_state.chat_history = []
    st.session_state.assistant.clear()

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}..."):
            st.session_state.assistant.ingest(file_path)

        os.remove(file_path)

def chat():
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(key="chat", placeholder="What is up?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        if st.session_state.assistant is None:
            st.write("Please select a model.")
            return
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            response_placeholder = st.empty()
            streamed_content = ""

            try:
                response_stream = st.session_state.assistant.ask(
                    prompt.strip(),
                    k=st.session_state["retrieval_k"],
                    score_threshold=st.session_state["retrieval_threshold"],
                )

                for chunk in response_stream:
                    streamed_content += chunk
                    response_placeholder.markdown(streamed_content)

                st.session_state.chat_history.append({"role": "assistant", "content": streamed_content})

            except ValueError as e:
                response_placeholder.markdown(f"**Error:** {str(e)}")