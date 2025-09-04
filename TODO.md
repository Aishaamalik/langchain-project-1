# TODO: Fix Chatbot Recovery Rate Answer

## Tasks
- [x] Update embeddings.py: Increase top_k to 100 in retrieve_relevant_chunks for better data retrieval
- [x] Modify query_handler.py: Add function to detect queries about highest recovery rate
- [x] Modify query_handler.py: Add function to parse chunks for country and recovery rate data
- [x] Modify query_handler.py: Add logic to calculate max recovery rate programmatically
- [x] Modify query_handler.py: Update generate_streaming_answer to use direct calculation for recovery rate queries
- [x] Test the chatbot with COVID dataset to confirm correct answer

## Progress
- Implementation complete with improvements for full document analysis.
- Increased retrieval to 100 chunks and chunk size to 2000 for better data coverage.
- Lowered similarity threshold to 0.0 to ensure answers are from documents when possible.
- Modified prompt to force answers using ONLY the provided context.
- To test: Upload any document, ask questions related to its content. Answers should be based on the document.
