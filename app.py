import streamlit as st
from utils import load_and_process_documents
from embeddings import embed_and_store_documents, retrieve_relevant_chunks
from query_handler import generate_answer, generate_streaming_answer
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

if 'show_file_uploader' not in st.session_state:
    st.session_state.show_file_uploader = False

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

    # CSS for fixed sidebar width and hidden scrollbar
    st.markdown("""
        <style>
        .stSidebar, .sidebar, [data-testid="stSidebar"] {
            width: 250px !important;
            min-width: 250px !important;
            max-width: 250px !important;
            overflow: auto !important;
        }
        .stSidebar::-webkit-scrollbar, .sidebar::-webkit-scrollbar, [data-testid="stSidebar"]::-webkit-scrollbar {
            display: none !important;
        }
        .stSidebar, .sidebar, [data-testid="stSidebar"] {
            -ms-overflow-style: none !important;
            scrollbar-width: none !important;
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
            # Display formatted content gracefully like ChatGPT
            # Removed import of markdown module to avoid ModuleNotFoundError
            # import streamlit.components.v1 as components

            # Display markdown content directly
            formatted_content = msg['content']
            st.markdown(formatted_content, unsafe_allow_html=True)

            # Remove display of citations and highlights as per user request
            # if 'citations' in msg and msg['citations']:
            #     st.markdown("**Source Citations:**")
            #     for c in msg['citations']:
            #         st.markdown(c)
            # if 'highlights' in msg and msg['highlights']:
            #     st.markdown("**Supporting Passages:**")
            #     for h in msg['highlights']:
            #         st.markdown(f"> {h}")

# File uploader popup triggered by plus icon
if st.session_state.show_file_uploader:
    uploaded_files = st.file_uploader(
        "📎 Upload documents to chat",
        type=None,  # Accept any file type
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
            st.session_state.show_file_uploader = False
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error processing documents: {str(e)}")

# Chat input with plus icon button on the right
col1, col2 = st.columns([20, 1], gap="small")
with col1:
    if prompt := st.chat_input("💬 Ask a question..."):
        # Add user message
        add_message_to_chat(st.session_state.current_chat_id, "user", prompt)
        
        # Process query
        try:
            monitor_index_changes()
            try:
                relevant_chunks, metadatas, distances = retrieve_relevant_chunks(prompt)
            except Exception:
                relevant_chunks, metadatas, distances = [], [], []

            # Determine mode: general or document based on similarity
            if not relevant_chunks or not distances:
                mode = 'general'
                relevant_chunks, metadatas = [], []
            else:
                similarities = [1 - d for d in distances]
                max_sim = max(similarities) if similarities else 0
                mode = 'general' if max_sim < 0.5 else 'document'

            # Use streaming answer generator
            answer_generator = generate_streaming_answer(prompt, relevant_chunks, metadatas, mode)
            
            # Display streaming response token by token
            with st.chat_message("assistant"):
                assistant_message_placeholder = st.empty()
                full_answer = ""
                for token in answer_generator:
                    full_answer += token
                    assistant_message_placeholder.markdown(full_answer)
                    # Optional: add a small delay for smoother streaming effect
                    # time.sleep(0.05)
            
            # After streaming complete, parse citations and highlights
            import re
            citation_pattern = r'\[doc:([^\s]+)\s+p\.(\d+)\]'
            # Remove citations and highlights completely as per user request
            # citation_matches = re.findall(citation_pattern, full_answer)
            # citations = list(set([f"[doc:{filename} p.{page}]" for filename, page in citation_matches]))
            
            # highlight_pattern = r'"([^"]*)"'
            # highlights = re.findall(highlight_pattern, full_answer)
            # highlights = [h for h in highlights if len(h) > 10 and not h.endswith('.pdf') and not h.endswith('.txt') and not h.endswith('.docx')]
            
            # Remove citations from answer
            answer_clean = re.sub(citation_pattern, '', full_answer).strip()
            
            # Add assistant message to chat without citations and highlights
            add_message_to_chat(st.session_state.current_chat_id, "assistant", answer_clean)
            
            st.rerun()
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            add_message_to_chat(st.session_state.current_chat_id, "assistant", error_msg)
            st.rerun()
with col2:
    if st.button("☰", help="Add files"):
        st.session_state.show_file_uploader = not st.session_state.show_file_uploader
        st.rerun()
