import chromadb
import ollama
import hashlib

# Initialize ChromaDB client with new API
client = chromadb.PersistentClient(path="./data/chroma")
collection = client.get_or_create_collection(name="pdf_docs")

def embed_text(text):
    # Use Ollama's embedding function directly
    response = ollama.embed(model='llama2', input=text)
    return response.embeddings[0]


def embed_and_store_documents(documents):
    for doc in documents:
        text = doc["page_content"]
        metadata = doc["metadata"]
        checksum = hashlib.md5(text.encode("utf-8")).hexdigest()
        
        # Check if already indexed
        existing = collection.get(where={"checksum": checksum})
        if existing and len(existing["ids"]) > 0:
            continue
        
        embedding = embed_text(text)
        collection.add(
            ids=[checksum],  # Use checksum as unique ID
            documents=[text],
            metadatas=[{**metadata, "checksum": checksum}],
            embeddings=[embedding]
        )

def retrieve_relevant_chunks(query, top_k=5):
    query_embedding = embed_text(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0]
