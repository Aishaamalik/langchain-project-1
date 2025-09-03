# TODO: Enhance Chatbot to Full Conversational Agent

## Tasks
- [x] Modify embeddings.py: Update retrieve_relevant_chunks to return distances for similarity check
- [x] Modify query_handler.py: Add support for general conversation mode in generate_streaming_answer
- [x] Modify app.py: Implement logic to detect general vs document queries using similarity scores and choose appropriate mode
- [x] Update prompts in query_handler.py to ensure responses are formatted in markdown
- [ ] Test the enhanced chatbot functionality

## Progress
- Modified embeddings.py to return distances.
- Modified query_handler.py for general mode and markdown formatting.
- Modified app.py to detect mode based on similarity.
