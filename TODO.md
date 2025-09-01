# TODO List for Fixing Source Citations and Supporting Passages

- [x] Modify embeddings.py: Update retrieve_relevant_chunks to return both documents and metadatas
- [x] Update app.py: Pass metadatas to generate_answer function
- [x] Modify query_handler.py: Update generate_answer to parse response for citations and highlights

# TODO List for Project Improvements and New Features

- [x] Improve index_monitor.py: Implement automatic re-embedding of changed documents by loading and processing changed files
- [x] Enhance app.py: Add UI improvements like upload progress bar, query history, clear button, and better error messages
- [ ] Update utils.py: Add support for more document types (e.g., .doc, .pptx) and richer metadata extraction (e.g., author, creation date)
- [ ] Enhance query_handler.py: Add support for follow-up questions and multi-turn conversations by maintaining conversation history
- [ ] Add logging: Implement logging across modules (embeddings.py, query_handler.py, app.py) for better debugging and monitoring
- [ ] Add error handling: Improve error handling in all modules for robustness (e.g., handle Ollama connection errors, file processing errors)
- [ ] Add tests: Create unit tests for core functions in embeddings.py, query_handler.py, and utils.py
- [ ] Add configuration: Create a config.py file for configurable parameters like chunk size, top_k, model name, etc.
- [ ] Add analytics dashboard: Implement a simple dashboard in app.py to show usage stats (e.g., number of documents, queries answered)
- [ ] Add user authentication: Implement basic user authentication or session management for privacy
- [ ] Add encryption: Add optional encryption for stored embeddings and documents for enhanced privacy
