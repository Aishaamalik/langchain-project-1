from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredPowerPointLoader, CSVLoader, UnstructuredExcelLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os

def load_documents_from_paths(file_paths):
    documents = []
    for path in file_paths:
        if path.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs = loader.load()
        elif path.endswith((".docx", ".doc")):
            loader = UnstructuredWordDocumentLoader(path)
            docs = loader.load()
        elif path.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(path)
            docs = loader.load()
        elif path.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            docs = [{"page_content": content, "metadata": {"source": os.path.basename(path)}}]
        else:
            # Skip unsupported formats
            continue
        
        # Chunk documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
        for doc in docs:
            chunks = text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                metadata = doc.metadata.copy()
                metadata.update({
                    "source": os.path.basename(path),
                    "page": i + 1
                })
                documents.append({
                    "page_content": chunk,
                    "metadata": metadata
                })
    return documents

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
        elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            # Word documents
            suffix = ".docx" if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" else ".doc"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name
            
            try:
                loader = UnstructuredWordDocumentLoader(temp_file_path)
                docs = loader.load()
            finally:
                os.unlink(temp_file_path)
        elif file.type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            # PowerPoint
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            try:
                loader = UnstructuredPowerPointLoader(temp_file_path)
                docs = loader.load()
            finally:
                os.unlink(temp_file_path)
        elif file.type == "text/csv":
            # CSV files
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            try:
                loader = CSVLoader(file_path=temp_file_path)
                docs = loader.load()
            finally:
                os.unlink(temp_file_path)
        elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            # Excel files (.xlsx)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            try:
                loader = UnstructuredExcelLoader(temp_file_path)
                docs = loader.load()
            finally:
                os.unlink(temp_file_path)
        elif file.type == "application/vnd.oasis.opendocument.spreadsheet":
            # OpenDocument Spreadsheet (.ods)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ods") as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            try:
                loader = UnstructuredExcelLoader(temp_file_path)  # Assuming it can handle .ods
                docs = loader.load()
            except:
                # Fallback to text if loader fails
                content = file.read().decode("utf-8", errors="ignore")
                docs = [{"page_content": content, "metadata": {"source": file.name}}]
            finally:
                os.unlink(temp_file_path)
        else:
            # Fallback for any file type using UnstructuredFileLoader
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            try:
                loader = UnstructuredFileLoader(temp_file_path)
                docs = loader.load()
            except Exception:
                # If UnstructuredFileLoader fails, try to decode as text
                try:
                    with open(temp_file_path, "rb") as f:
                        content = f.read().decode("utf-8")
                    docs = [{"page_content": content, "metadata": {"source": file.name}}]
                except UnicodeDecodeError:
                    # Skip files that can't be processed
                    docs = []
            finally:
                os.unlink(temp_file_path)
        
        # Chunk documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
        for doc in docs:
            chunks = text_splitter.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                metadata = doc.metadata.copy() if hasattr(doc, 'metadata') else {}
                metadata.update({
                    "source": file.name,
                    "page": i + 1
                })
                documents.append({
                    "page_content": chunk,
                    "metadata": metadata
                })
    return documents
