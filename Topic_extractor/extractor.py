import re
import numpy as np
from docx import Document
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

BUILTIN_STOPWORDS = set("""
a about above after again against all am an and any are aren't as at be because been before being below between both 
but by can can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further 
had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's 
i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on 
once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some 
such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've 
this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when 
when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've 
your yours yourself yourselves
""".split())

class TopicExtractor:
    def __init__(self, filepath: str, num_topics: int):
        self.filepath = filepath
        self.num_topics = num_topics

    def load_paragraphs(self) -> List[str]:
        document = Document(self.filepath)
        return [p.text.strip() for p in document.paragraphs if len(p.text.strip()) > 30]

    def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z\s]", "", text)
        tokens = [word for word in text.split() if word not in BUILTIN_STOPWORDS]
        return " ".join(tokens)

    def preprocess_all(self, paragraphs: List[str]) -> List[str]:
        return [self.preprocess_text(p) for p in paragraphs]

    def vectorize_and_cluster(self, texts: List[str]):
        vectorizer = TfidfVectorizer(max_df=0.85, min_df=1, ngram_range=(1, 3))
        tfidf_matrix = vectorizer.fit_transform(texts)
        num_clusters = min(self.num_topics, len(texts))
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        kmeans.fit(tfidf_matrix)
        return kmeans, tfidf_matrix

    def extract_topics(self, raw_paragraphs: List[str], labels: np.ndarray, centers: np.ndarray, matrix: np.ndarray) -> List[str]:
        topics = []
        for cluster_id in range(len(centers)):
            cluster_indices = np.where(labels == cluster_id)[0]
            if len(cluster_indices) == 0:
                continue
            best_idx = cluster_indices[0]
            topic_title = raw_paragraphs[best_idx].split('.')[0].strip().title()
            if topic_title not in topics:
                topics.append(topic_title)
            if len(topics) >= self.num_topics:
                break
        return topics

    def run_pipeline(self) -> List[str]:
        raw_paragraphs = self.load_paragraphs()
        processed_texts = self.preprocess_all(raw_paragraphs)
        kmeans, tfidf_matrix = self.vectorize_and_cluster(processed_texts)
        return self.extract_topics(raw_paragraphs, kmeans.labels_, kmeans.cluster_centers_, tfidf_matrix)
