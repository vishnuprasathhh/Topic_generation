# Topic_generation
This code is a model-style topic extractor for educational documents.

- Reads a `.docx` file with paragraphs or lecture material
- Cleans and preprocesses the text
- Uses TF-IDF vectorization + KMeans clustering
- Extracts clean, title-style topics from representative paragraphs
- Outputs unique, non-redundant educational topics

- Fully offline (no API or NLTK)
- Modular Python codebase
- Handles user-defined topic counts**
- Ready for scaling to any .docx-based educational document

- `scikit-learn` for TF-IDF and clustering
- `python-docx` for parsing `.docx`
- `numpy`, `re` for utilities

