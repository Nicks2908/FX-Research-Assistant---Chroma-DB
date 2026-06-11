import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv

from services.pdf_loader import extract_pages
from services.chunker import create_chunks
from services.embedding_service import generate_embedding
from services.vector_store import (
    create_faiss_index,
    search_faiss_index
)
from services.chroma_store import (
    store_chunks,search_chunks
)

from services.llm_service import (
    generate_response
)

from services.prompts import (
    qa_prompt,
    analyst_prompt,
    executive_summary_prompt,
    risk_prompt,
    trade_prompt,
    compare_prompt,
    outlook_prompt
)

# ====================================
# ENVIRONMENT
# ====================================

load_dotenv()

API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=os.getenv("API_KEY"))

# ====================================
# PAGE
# ====================================

st.set_page_config(page_title="Forex Research Assistant",layout="wide")

st.title("📈 Forex Research Assistant")

# ====================================
# SESSION STATE
# ====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# ====================================
# SIDEBAR
# ====================================

st.sidebar.header("Research Settings")

mode = st.sidebar.selectbox("Mode",["Q&A","Analyst"])

tool = st.sidebar.selectbox("Research Tool",["Chat","Executive Summary","Risk Analysis","Trade Extraction","Compare Reports","Weekly Outlook"])

# ====================================
# HISTORY FUNCTION
# ====================================

def build_history():

    history = ""

    for message in st.session_state.messages[-10:]:

        history += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    return history

    # First option : Return records in list format, which can be used for various purposes, such as displaying the chat history in the UI or passing it to the LLM in a structured way. Each message is represented as a dictionary with "role" and "content" keys, making it easy to identify who said what in the conversation.
    # One liner: return list(st.session_state.messages[-10:])
    # This is a more complex structure that concatenates the last 10 messages into a single string, which can be used as part of the prompt for the LLM. The format is "role: content\n" for each message, which helps the model understand the conversation flow and context.
    
    # Second option : Return a formatted string of the last 10 messages, which can be directly included in the prompt for the LLM. This format provides a clear and concise representation of the conversation history, making it easier for the model to understand the context and generate relevant responses.
    # for message in st.session_state.messages[-10:]:
    #     with st.chat_message(message["role"]):
    #         st.write(message["content"])
# ====================================
# FILE UPLOAD
# ====================================

uploaded_files = st.file_uploader("Upload Forex Reports", type=["pdf"], accept_multiple_files=True)

# ====================================
# PROCESS DOCUMENTS
# ====================================

if uploaded_files:

    if st.button("Process Documents"):

        with st.spinner("Processing reports..."):

            all_chunks = []

            # --------------------------
            # Extract + Chunk
            # --------------------------

            for uploaded_file in uploaded_files:

                pages = extract_pages(uploaded_file)

                chunks = create_chunks(pages)

                for chunk in chunks:

                    chunk["document"] = (uploaded_file.name)

                    all_chunks.append(chunk)

            # --------------------------
            # Embeddings
            # --------------------------

            embeddings = []

            for chunk in all_chunks:

                embeddings.append(
                    generate_embedding(chunk["text"])
                )

            # --------------------------
            # FAISS
            # --------------------------

            # index = create_faiss_index(embeddings) # Create FAISS index and store embeddings in memory
            index = store_chunks(all_chunks, embeddings) # Store chunks and embeddings in ChromaDB

            st.session_state.index = index
            st.session_state.chunks = all_chunks

            st.success(
                "Documents processed successfully."
            )

# ====================================
# DISPLAY CHAT HISTORY
# ====================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# ====================================
# CHAT SECTION
# ====================================

if "index" in st.session_state:

    question = st.chat_input("Ask a question...")

    if question:

        # --------------------------
        # Save User Message
        # --------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        st.chat_message("user").write(question)

        # --------------------------
        # Retrieval
        # --------------------------

        query_embedding = generate_embedding(question)

        # results = search_faiss_index(st.session_state.index, query_embedding) # Search FAISS index for relevant chunks
        results = search_chunks(query_embedding) # Search ChromaDB for relevant chunks

        # retrieved_chunks = [
        #     st.session_state.chunks[int(i)]
        #     for i in results
        # ]

        # context = "\n\n".join(
        #     [
        #         chunk["text"]
        #         for chunk in retrieved_chunks
        #     ]
        # )

        context = "\n\n".join(results["documents"][0]) # Extract relevant chunks from ChromaDB results and concatenate into context string

        history = build_history()

        # ==================================
        # PROMPT SELECTION
        # ==================================

        if tool == "Executive Summary":

            prompt = executive_summary_prompt(
                context
            )

        elif tool == "Risk Analysis":

            prompt = risk_prompt(
                context
            )

        elif tool == "Trade Extraction":

            prompt = trade_prompt(
                context
            )

        elif tool == "Compare Reports":

            prompt = compare_prompt(
                context
            )

        elif tool == "Weekly Outlook":

            prompt = outlook_prompt(
                context
            )

        else:

            if mode == "Q&A":

                prompt = qa_prompt(
                    question,
                    context,
                    history
                )

            else:

                prompt = analyst_prompt(
                    question,
                    context,
                    history
                )

        # ==================================
        # LLM CALL
        # ==================================

        answer = generate_response(prompt)

        # ==================================
        # SAVE RESPONSE
        # ==================================

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # ==================================
        # DISPLAY RESPONSE
        # ==================================

        with st.chat_message("assistant"):

            st.write(answer)

            st.markdown(
                "### Sources"
            )

            sources = set()

            # for chunk in retrieved_chunks:

            #     sources.add(
            #         f"{chunk['document']} - "
            #         f"(Page {chunk['page_no']})"
            #     )

            for chunk in results["metadatas"][0]: # Extract metadata from ChromaDB results to display sources

                sources.add(
                    f"{chunk['document']} - "
                    f"(Page {chunk['page']})"
                )

            for source in sources:

                st.write(f"• {source}")