import streamlit as st
from utils import load_and_process_documents
from embeddings import embed_and_store_documents, retrieve_relevant_chunks
from query_handler import generate_answer
from index_monitor import monitor_index_changes

st.set_page_config(page_title="Private PDF/Docs Q&A (RAG)", layout="wide")

st.title("Private PDF/Docs Question Answering System")

# Initialize session state for query history
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

# Sidebar for query history
with st.sidebar:
    st.header("Query History")
    if st.session_state.query_history:
        for i, q in enumerate(st.session_state.query_history):
            st.write(f"{i+1}. {q}")
    else:
        st.write("No queries yet.")
    
    if st.button("Clear History"):
        st.session_state.query_history = []
        st.rerun()

# File uploader with drag and drop
uploaded_files = st.file_uploader(
    "Upload PDF or supported documents", 
    type=["pdf", "txt", "docx", "doc", "pptx"], 
    accept_multiple_files=True
)

if uploaded_files:
    try:
        # Process and index documents with progress bar
        progress_bar = st.progress(0)
        st.info("Processing documents...")
        docs = load_and_process_documents(uploaded_files)
        progress_bar.progress(50)
        embed_and_store_documents(docs)
        progress_bar.progress(100)
        st.success("Documents indexed successfully!")
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")

# Query input
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("Enter your question:")
with col2:
    if st.button("Clear Query"):
        query = ""

if query:
    try:
        # Add to history
        if query not in st.session_state.query_history:
            st.session_state.query_history.append(query)
        
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
    except Exception as e:
        st.error(f"Error processing query: {str(e)}")
