import ollama

def generate_answer(query, relevant_chunks):
    # Assemble context from relevant chunks
    context = "\n\n".join(relevant_chunks)
    
    prompt = f"""
    You are a helpful assistant. Use the following context to answer the question.
    
    Context:
    {context}
    
    Question:
    {query}
    
    Provide the answer with citations in the format [doc:filename.pdf p.X] and highlight supporting passages.
    """
    
    response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': prompt}])
    
    # Extract answer, citations, and highlights (simple parsing or regex can be used)
    answer = response['message']['content']
    
    # For demo, assume citations and highlights are embedded in answer text
    citations = []  # Extract citations from answer if needed
    highlights = [] # Extract highlighted passages if needed
    
    return answer, citations, highlights
