import os
import hashlib
import time
from embeddings import embed_and_store_documents

# Simple monitoring using file timestamps and checksums
file_checksums = {}

def compute_checksum(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

def monitor_index_changes():
    # Check files in data folder for changes
    data_folder = "./data"
    changed_docs = []
    for root, _, files in os.walk(data_folder):
        for file in files:
            if file.endswith((".pdf", ".txt", ".docx", ".doc", ".pptx")):
                path = os.path.join(root, file)
                checksum = compute_checksum(path)
                if file not in file_checksums or file_checksums[file] != checksum:
                    file_checksums[file] = checksum
                    changed_docs.append(path)
    if changed_docs:
        from utils import load_documents_from_paths
        from embeddings import embed_and_store_documents

        # Load and process changed documents from disk
        docs = load_documents_from_paths(changed_docs)
        # Embed and store updated documents
        embed_and_store_documents(docs)
