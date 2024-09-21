import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None

    def load_portfolio(self):
        if self.tfidf_matrix is None:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.data["Techstack"])

    def query_links(self, skills):
        if not skills:
            return []
        if isinstance(skills, str):
            skills = [skills]
        
        query_vec = self.vectorizer.transform([' '.join(skills)])
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        related_docs_indices = cosine_similarities.argsort()[::-1][:3]  # Get top 3 matches
        
        return [self.data.iloc[i]["Links"] for i in related_docs_indices]
