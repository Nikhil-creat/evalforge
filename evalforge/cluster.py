import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

def embed(texts):
    try:  # better semantics when installed
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2").encode(texts, normalize_embeddings=True)
    except Exception:
        X = TfidfVectorizer(ngram_range=(1, 2), min_df=2, stop_words="english").fit_transform(texts)
        return normalize(TruncatedSVD(min(64, X.shape[1] - 1), random_state=0).fit_transform(X))

def cluster(texts, min_size=8):
    E = embed(texts)
    labels = HDBSCAN(min_cluster_size=min_size, min_samples=3).fit_predict(E)
    xy = PCA(2, random_state=0).fit_transform(E)
    d = np.full(len(texts), np.inf)
    for c in set(labels) - {-1}:
        m = labels == c
        d[m] = np.linalg.norm(E[m] - E[m].mean(0), axis=1)
    return labels, xy, d
