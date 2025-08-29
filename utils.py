from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os

def load_and_process_documents(uploaded_files):
    documents = []
    for file in uploaded_files:
        if file.type == "application/pdf":
            # Create a temporary file to save the uploaded PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name
            
            try:
                # Use PyPDFLoader with the temporary file path
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
            finally:
                # Clean up the temporary file
                os.unlink(temp_file_path)
        else:
            # Add support for other formats if needed
            content = file.read().decode("utf-8")
            docs = [{"page_content": content, "metadata": {"source": file.name}}]
        
        # Chunk documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        for doc in docs:
            chunks = text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                documents.append({
                    "page_content": chunk,
                    "metadata": {
                        "source": file.name,
                        "page": i + 1
                    }
                })
    return documents
