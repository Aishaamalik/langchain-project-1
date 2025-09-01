import ollama
import re

def generate_answer(query, relevant_chunks, metadatas):
    # Assemble context from relevant chunks
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
    You are a helpful assistant. Use the following context to answer the question.

    Context:
    {context}

    Question:
    {query}

    Provide the answer with citations in the format [doc:filename.pdf p.X] and highlight supporting passages in quotes.
    """

    response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': prompt}])

    # Extract answer, citations, and highlights
    full_response = response['message']['content']

    # Parse citations using regex
    citation_pattern = r'\[doc:([^\s]+)\s+p\.(\d+)\]'
    citation_matches = re.findall(citation_pattern, full_response)

    # Format citations as list of strings and remove duplicates
    citations = list(set([f"[doc:{filename} p.{page}]" for filename, page in citation_matches]))

    # Parse supporting passages (assuming they are in quotes)
    highlight_pattern = r'"([^"]*)"'
    highlights = re.findall(highlight_pattern, full_response)

    # Filter highlights to remove short or irrelevant ones (e.g., document names)
    highlights = [h for h in highlights if len(h) > 10 and not h.endswith('.pdf') and not h.endswith('.txt') and not h.endswith('.docx')]

    # Remove citations from answer to get clean answer
    answer = re.sub(citation_pattern, '', full_response).strip()

    return answer, citations, highlights
