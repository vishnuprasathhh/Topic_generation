# Topic_Generation

This code is a modular topic extraction system built for analyzing `.docx` lecture files — specifically tailored for philosophical/psychological course material like *Samkhya philosophy*. It uses TF-IDF vectorization + KMeans clustering to extract clear, unique, and human-readable topic titles.



# Key Features

- Accepts `.docx` educational files as input
- User can define how many topics they want (10, 50, 100, etc.)
- No API required — works fully offline
- Built with proper Python class (`TopicExtractor`) and modular design
- Clusters semantically related ideas and filters duplicates
- Outputs clean, complete, title-style topics



 #Project Structure

Topic_Generation/
├── topic_extractor/
│ ├── init.py
│ ├── extractor.py  contains TopicExtractor class
│ └── utils.py  helper functions
├── main.py # handles command-line execution
├── README.md # you're reading it now
└── sample_input.docx # (optional test input)


 How It Works

1. Extracts text from `.docx` using `python-docx`
2. Cleans and tokenizes text using `nltk`
3. Builds a **TF-IDF matrix** of n-gram phrases
4. Applies **KMeans clustering** to group semantically similar phrases
5. Picks the most central phrase from each cluster as a topic
6. Deduplicates and outputs human-readable, non-overlapping topics


 Example Usage

Enter the path to your DOCX file: /path/to/lecture.docx
How many topics do you want to extract? 50
