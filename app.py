import streamlit as st
from utils import load_and_process_documents
from embeddings import embed_and_store_documents, retrieve_relevant_chunks
from query_handler import generate_answer
from index_monitor import monitor_index_changes
from chat_manager import create_new_chat, load_chat, list_chats, add_message_to_chat, add_uploaded_files_to_chat, delete_chat, archive_chat, rename_chat

st.set_page_config(page_title="Private PDF/Docs Q&A (RAG)", page_icon="🤖", layout="wide")

# Initialize session state
if 'current_chat_id' not in st.session_state:
    new_chat = create_new_chat()
    st.session_state.current_chat_id = new_chat['id']
    st.session_state.chats = list_chats()

if 'chats' not in st.session_state:
    st.session_state.chats = list_chats()

# Sidebar for chat management
with st.sidebar:
    st.header("💬 Chats")

    # CSS for uniform button width in sidebar
    st.markdown("""
        <style>
        div.stButton > button {
            width: 200px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: left;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("➕ New Chat"):
        new_chat = create_new_chat()
        st.session_state.current_chat_id = new_chat['id']
        st.session_state.chats = list_chats()
        st.rerun()

    st.divider()

    for chat in st.session_state.chats:
        col1, col2 = st.columns([9, 1])
        with col1:
            if st.button(chat['title'], key=f"select_{chat['id']}", help=chat['title']):
                st.session_state.current_chat_id = chat['id']
                st.rerun()
        with col2:
            with st.popover("⋮"):
                # Rename
                new_name = st.text_input("New name", value=chat['title'], key=f"rename_input_{chat['id']}")
                if st.button("Save Rename", key=f"save_rename_{chat['id']}"):
                    rename_chat(chat['id'], new_name)
                    st.session_state.chats = list_chats()
                    st.rerun()
                # Delete
                if st.button("Delete", key=f"delete_{chat['id']}"):
                    if st.session_state.current_chat_id == chat['id']:
                        other_chats = [c for c in st.session_state.chats if c['id'] != chat['id']]
                        if other_chats:
                            st.session_state.current_chat_id = other_chats[0]['id']
                        else:
                            new_chat = create_new_chat()
                            st.session_state.current_chat_id = new_chat['id']
                            st.session_state.chats = list_chats()
                    delete_chat(chat['id'])
                    st.session_state.chats = list_chats()
                    st.rerun()
                # Archive
                if st.button("Archive", key=f"archive_{chat['id']}"):
                    if st.session_state.current_chat_id == chat['id']:
                        other_chats = [c for c in st.session_state.chats if c['id'] != chat['id']]
                        if other_chats:
                            st.session_state.current_chat_id = other_chats[0]['id']
                        else:
                            new_chat = create_new_chat()
                            st.session_state.current_chat_id = new_chat['id']
                            st.session_state.chats = list_chats()
                    archive_chat(chat['id'])
                    st.session_state.chats = list_chats()
                    st.rerun()

# Main chat interface
st.markdown("""
<div style="text-align: center;">
<h1 id="typewriter">🧠 DocuMind AI</h1>
</div>

<style>
#typewriter {
  overflow: hidden;
  border-right: .15em solid #007bff;
  white-space: nowrap;
  margin: 0 auto;
  letter-spacing: .15em;
  animation: typing 2s steps(15, end), blink-caret .75s step-end infinite;
}

@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}

@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: #007bff }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 10px;">
<p style="font-size: 18px; color: #666;">Intelligent Document Assistant | Private & Secure</p>
</div>
""", unsafe_allow_html=True)

# Load current chat
current_chat = load_chat(st.session_state.current_chat_id)

# Display chat messages
chat_container = st.container()
with chat_container:
    for msg in current_chat['messages']:
        with st.chat_message(msg['role']):
            st.write(msg['content'])
            if 'citations' in msg and msg['citations']:
                st.markdown("**Source Citations:**")
                for c in msg['citations']:
                    st.write(c)
            if 'highlights' in msg and msg['highlights']:
                st.markdown("**Supporting Passages:**")
                for h in msg['highlights']:
                    st.write(f"> {h}")

# File uploader in chat
uploaded_files = st.file_uploader(
    "📎 Upload documents to chat", 
    type=["pdf", "txt", "docx", "doc", "pptx"], 
    accept_multiple_files=True,
    key="file_uploader"
)

if uploaded_files:
    try:
        st.info("🔄 Processing documents...")
        docs = load_and_process_documents(uploaded_files)
        embed_and_store_documents(docs)
        add_uploaded_files_to_chat(st.session_state.current_chat_id, uploaded_files)
        st.success("✅ Documents indexed and added to chat!")
    except Exception as e:
        st.error(f"❌ Error processing documents: {str(e)}")

# Chat input
if prompt := st.chat_input("💬 Ask a question..."):
    # Add user message
    add_message_to_chat(st.session_state.current_chat_id, "user", prompt)
    
    # Process query
    try:
        monitor_index_changes()
        relevant_chunks, metadatas = retrieve_relevant_chunks(prompt)
        answer, citations, highlights = generate_answer(prompt, relevant_chunks, metadatas)
        
        # Add assistant message
        add_message_to_chat(st.session_state.current_chat_id, "assistant", answer, citations, highlights)
        
        st.rerun()
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        add_message_to_chat(st.session_state.current_chat_id, "assistant", error_msg)
        st.rerun()
