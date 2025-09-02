import json
import os
import uuid
from datetime import datetime

CHAT_DIR = "./data/chats"

def ensure_chat_dir():
    if not os.path.exists(CHAT_DIR):
        os.makedirs(CHAT_DIR)

def create_new_chat():
    ensure_chat_dir()
    chat_id = str(uuid.uuid4())
    chat_data = {
        "id": chat_id,
        "title": "New Chat",
        "created_at": datetime.now().isoformat(),
        "messages": [],
        "uploaded_files": []
    }
    save_chat(chat_data)
    return chat_data

def save_chat(chat_data):
    ensure_chat_dir()
    with open(os.path.join(CHAT_DIR, f"{chat_data['id']}.json"), "w") as f:
        json.dump(chat_data, f, indent=2)

def load_chat(chat_id):
    try:
        with open(os.path.join(CHAT_DIR, f"{chat_id}.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def list_chats():
    ensure_chat_dir()
    chats = []
    for file in os.listdir(CHAT_DIR):
        if file.endswith(".json"):
            chat_id = file[:-5]
            chat = load_chat(chat_id)
            if chat:
                chats.append(chat)
    return sorted(chats, key=lambda x: x["created_at"], reverse=True)

def add_message_to_chat(chat_id, role, content, citations=None, highlights=None):
    chat = load_chat(chat_id)
    if chat:
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        if citations:
            message["citations"] = citations
        if highlights:
            message["highlights"] = highlights
        chat["messages"].append(message)
        save_chat(chat)

def add_uploaded_files_to_chat(chat_id, files):
    chat = load_chat(chat_id)
    if chat:
        for file in files:
            chat["uploaded_files"].append({
                "name": file.name,
                "type": file.type,
                "uploaded_at": datetime.now().isoformat()
            })
        save_chat(chat)
