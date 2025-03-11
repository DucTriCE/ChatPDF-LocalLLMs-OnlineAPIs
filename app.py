import os
import time
import streamlit as st
from rag import ChatPDF
from config import OLLAMA_MODELS, ONLINE_MODELS
from utils import clear_chat, read_and_save_file, chat, initialize_session

st.set_page_config(page_title="RAG with Local Ollama Models / Online API")


def page():
    """Main app page layout."""       
    st.header("RAG with Local Ollama Models / Online LLMs API")
    
    initialize_session()
    chat()

    with st.sidebar:

        option = st.selectbox(
            "Choosing host type",
            ("Local", "Online"),
            index=None,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

        if option == "Local":

            llm_option = st.selectbox(
                "Choosing model",
                (tuple(OLLAMA_MODELS.keys())),
                index=None,
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )

            if not llm_option:
                st.warning("Please select a model.")
                return
            
            st.session_state.llm_option = llm_option
            st.session_state.is_local = True
            st.session_state.llm_model = OLLAMA_MODELS[llm_option]["llm_model"]
            st.session_state.embedding_model = "all-minilm" if "Deepseek" not in llm_option else "mxbai-embed-large"
            st.session_state.dimensions = 1024
            st.write(f"LLM: '{st.session_state.llm_model}'")
            st.write(f"Embedding: '{st.session_state.embedding_model}'")
            st.write(f"Dimensions: {st.session_state.dimensions}")

            st.session_state.llm_model = OLLAMA_MODELS[llm_option]["llm_model"]
            st.session_state.embedding_model = "all-minilm" if "Deepseek" not in llm_option else "mxbai-embed-large"

        elif option == "Online":
            
            llm_option = st.selectbox(
                "Choosing model",
                (tuple(ONLINE_MODELS.keys())),
                index=None,
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )
            if not llm_option:
                st.warning("Please select a model.")
                return

            st.session_state.llm_option = llm_option
            st.session_state.is_local = False
            st.session_state.llm_model = ONLINE_MODELS[llm_option]["llm_model"]
            st.session_state.embedding_model = ONLINE_MODELS[llm_option]["embedding_model"]  
            st.session_state.dimensions = ONLINE_MODELS[llm_option]["dimensions"]     
            st.write(f"LLM: '{st.session_state.llm_model}'")
            st.write(f"Embedding: '{st.session_state.embedding_model}'")
            st.write(f"Dimensions: {st.session_state.dimensions}")

            if "GPT" in llm_option:
                if not st.session_state.openai_api_key:
                    api_key = st.text_input("Enter your OpenAI API Key", type="password", key="openai_key")
                    if st.button("Save API Key"):
                        st.session_state.is_local = False
                        st.session_state.openai_api_key = api_key
                        os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
                        clear_chat()
                    else:
                        return
                else:
                    if st.button("Show API Key"):
                        st.write(f'"{st.session_state.openai_api_key}"')
            else:
                if not st.session_state.gemini_api_key:
                    api_key = st.text_input("Enter your Gemini API Key", type="password", key="gemini_key")
                    if st.button("Save API Key"):
                        st.session_state.is_local = False
                        st.session_state.gemini_api_key = api_key
                        os.environ["GOOGLE_API_KEY"] = st.session_state.gemini_api_key
                        clear_chat()
                    else:
                        return
                else:
                    if st.button("Show API Key"):
                        st.write(f'"{st.session_state.gemini_api_key}"')
            
        else:
            st.warning("Please select LLM's type options.")
            return
        
        if "selected_model" not in st.session_state or st.session_state.selected_model != st.session_state.llm_option:
            st.session_state.selected_model = st.session_state.llm_option           # Store the new selection
            st.session_state.assistant = None                                       # Reset assistant to force reloading
            clear_chat()

        if st.session_state.assistant is None:
            st.session_state.assistant = ChatPDF(
                is_local=st.session_state.is_local,
                api_key=st.session_state.openai_api_key if "GPT" in st.session_state.llm_option else st.session_state.gemini_api_key,
                llm_model=st.session_state.llm_model,
                embedding_model=st.session_state.embedding_model,
                dimensions=st.session_state.dimensions
            )
            read_and_save_file()
        
        # Retrieval settings
        st.subheader("Settings")
        st.session_state["retrieval_k"] = st.slider(
            "Number of Retrieved Results (k)", min_value=1, max_value=10, value=5
        )
        st.session_state["retrieval_threshold"] = st.slider(
            "Similarity Score Threshold", min_value=0.0, max_value=1.0, value=0.2, step=0.05
        )
        if st.button("Clear conversation"):
            clear_chat()

        st.subheader("Upload Documents")
        st.file_uploader(
            "Upload a PDF document",
            type=["pdf"],
            key="file_uploader",
            on_change=read_and_save_file,
            label_visibility="collapsed",
            accept_multiple_files=True,
        )


if __name__ == "__main__":
    page()
