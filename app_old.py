from dotenv import load_dotenv
import streamlit as st
from services.pdf_loader import extract_text
from services.chunker import create_chunks
from services.embedding_service import generate_embedding
from services.vector_store import create_faiss_index, search_faiss_index
from services.llm_service import ask_gemini

load_dotenv()

st.set_page_config(page_title="FX Research Assistant", layout="wide")

st.title("FX Research Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant for Forex research."
        }
    ]


st.session_state.messages[0]= {
        "role": "system", 
        "content": "You are a helpful assistant for Forex research."
}



uploaded_file = st.file_uploader("Upload a PDF document", type="pdf", accept_multiple_files = True)

if uploaded_file:
    if st.button("Process Document"):
        st.spinner("Processing...")

        text = extract_text(uploaded_file)
        chunks = create_chunks(text)
        embeddings = [generate_embedding(chunk) for chunk in chunks]
        index = create_faiss_index(embeddings)
        st.session_state.index = index
        st.session_state.chunks = chunks

        st.success("Document processed and indexed successfully!")

        if index in st.session_state:

            history = ""

            for message in st.session_state.messages:
                history += f"{message['role']}: {message['content']}\n"

            query = st.chat_input("Enter your query:")

            if query:
                # Store user message
                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": query
                    }
                )

                # Display user message
                st.chat_message("user", avatar="user").write(query)

                query_embedding = generate_embedding(query)
                results_indices = search_faiss_index(st.session_state.index, query_embedding)
        
                context = "\n\n".join([st.session_state.chunks[idx] for idx in results_indices])  # Get surrounding chunks for context
                sources = set()

                
                for chunk in context:
                    sources.add(
                        {
                            "document": uploaded_file.name,
                            "page": chunk['page'],
                            "text": chunk['text']
                        }
                    )
                
                st.markdown(
                    "### Sources"
                )

                for source in sources:
                    st.write(source)

                answer = ask_gemini(query, context, history)  # Pass the query and context to Gemini for a more informed answer

                st.chat_message("assistant", avatar="assistant").write(answer)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
