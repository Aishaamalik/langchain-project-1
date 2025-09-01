import streamlit as st
from utils import load_and_process_documents
from embeddings import embed_and_store_documents, retrieve_relevant_chunks
from query_handler import generate_answer
from index_monitor import monitor_index_changes

st.set_page_config(page_title="Private PDF/Docs Q&A (RAG)", layout="wide")

st.title("Private PDF/Docs Question Answering System")

# File uploader with drag and drop
uploaded_files = st.file_uploader(
    "Upload PDF or supported documents", 
    type=["pdf", "txt", "docx"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Process and index documents
    docs = load_and_process_documents(uploaded_files)
    embed_and_store_documents(docs)
    st.success("Documents indexed successfully!")

# Query input
query = st.text_input("Enter your question:")

if query:
    # Monitor index for changes and re-embed if needed
    monitor_index_changes()
    
    # Retrieve relevant chunks from vector store
    relevant_chunks, metadatas = retrieve_relevant_chunks(query)

    # Generate answer with context and citations
    answer, citations, highlights = generate_answer(query, relevant_chunks, metadatas)
    
    st.markdown("### Answer:")
    st.write(answer)
    
    st.markdown("### Source Citations:")
    for c in citations:
        st.write(c)
    
    st.markdown("### Supporting Passages:")
    for h in highlights:
        st.write(f"> {h}")
