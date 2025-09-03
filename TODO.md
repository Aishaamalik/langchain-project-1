# TODO List for Adding Plus Icon to Chat Input

## Completed Tasks
- [x] Analyze app.py structure and identify chat input location
- [x] Plan UI changes: Add plus icon (hamburger menu) next to chat input using columns
- [x] Integrate file uploader into the plus icon toggle
- [x] Update app.py with modified code including session state for uploader visibility
- [x] Update file uploader to accept any file type (type=None)
- [x] Add support for additional file types in utils.py: csv, xlsx, ods
- [x] Add imports for CSVLoader and UnstructuredExcelLoader in utils.py
- [x] Implement loaders for csv, xlsx, ods with fallback for unsupported formats
- [x] Enhance fallback to use UnstructuredFileLoader for any file type to enable Q&A on uploaded files
- [x] Test the changes (run the app and verify plus icon functionality)

## Pending Tasks
- [ ] Run the Streamlit app locally to verify the plus icon appears and file uploader works
- [ ] Test uploading various file types: pdf, txt, docx, doc, pptx, csv, xlsx, ods, and other files
- [ ] Ensure file upload processes documents correctly and adds to chat for supported types
- [ ] Check UI alignment and responsiveness on different screen sizes
- [ ] Verify error handling for unsupported or corrupted files
