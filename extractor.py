topic_extractor/extractor.py
!pip install python-docx
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from docx import Document
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class TopicExtractor:
    def __init__(self, filepath, num_topics):
        self.filepath = filepath
        self.num_topics = num_topics
        self.raw_text = ''
        self.cleaned_sentences = []
        self.topics = []

    def load_text(self):
        doc = Document(self.filepath)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        self.raw_text = re.sub(r'\s+', ' ', full_text)

    def preprocess(self):
        stop_words = set(stopwords.words('english'))
        sentences = re.split(r'[.!?]', self.raw_text)
        sentences = [s.strip() for s in sentences if len(s.split()) > 3]
        self.cleaned_sentences = []
        for sent in sentences:
            words = word_tokenize(sent.lower())
            words = [w for w in words if w.isalnum() and w not in stop_words]
            self.cleaned_sentences.append(" ".join(words))

    def vectorize(self):
        vectorizer = TfidfVectorizer()
        self.X = vectorizer.fit_transform(self.cleaned_sentences)

    def cluster_and_extract(self):
        km = KMeans(n_clusters=min(self.num_topics, len(self.cleaned_sentences)), random_state=42, n_init=10)
        km.fit(self.X)
        labels = km.labels_

        topic_map = {}
        for i, label in enumerate(labels):
            if label not in topic_map:
                topic_map[label] = []
            topic_map[label].append(self.cleaned_sentences[i])

        self.topics = []
        for cluster in topic_map.values():
            combined = " | ".join(sorted(set(" ".join(cluster).split()), key=len)[-3:])
            self.topics.append(combined.title())

    def get_topics(self):
        return self.topics
