"""
RAG Retriever — load TF-IDF index and retrieve relevant documents.
"""

import pickle
from pathlib import Path

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


class RAGRetriever:
    """TF-IDF based retriever — no external downloads needed."""

    def __init__(self, persist_dir: str = None):
        if persist_dir is None:
            persist_dir = str(get_project_root() / "data" / "vector_store")

        index_path = Path(persist_dir) / "rag_index.pkl"
        if not index_path.exists():
            raise FileNotFoundError(
                f"RAG index not found at {index_path}. "
                f"Run 'python backend/rag/build_index.py' first."
            )

        with open(index_path, "rb") as f:
            data = pickle.load(f)

        self.documents = data["documents"]
        self.vectorizer = data["vectorizer"]
        self.tfidf_matrix = data["tfidf_matrix"]

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """Return top-k relevant document chunks."""
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = np.argsort(sims)[::-1][:top_k]

        chunks = []
        for idx in top_indices:
            if sims[idx] > 0:
                doc = self.documents[idx]
                chunks.append({
                    "content": doc["content"],
                    "source": doc["source"],
                    "title": doc["title"],
                    "score": float(sims[idx]),
                })
        return chunks

    def count(self) -> int:
        return len(self.documents)


# Singleton
_retriever: RAGRetriever | None = None


def get_retriever() -> RAGRetriever:
    global _retriever
    if _retriever is None:
        _retriever = RAGRetriever()
    return _retriever
