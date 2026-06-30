#!/usr/bin/env python3
"""
Build a lightweight local vector store from RAG markdown documents.

Uses scikit-learn TfidfVectorizer (no external downloads needed) to embed
documents, and persists the TF-IDF matrix + document store to disk via
Python's pickle.

Run once after updating rag_docs/.
"""

import pickle
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def load_documents(docs_dir: Path) -> list[dict]:
    """Load all .md files and split into sections by ## headers."""
    documents = []
    for md_file in sorted(docs_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        # Split by ## headers into chunks
        sections = re.split(r"\n(?=## )", text)
        for section in sections:
            section = section.strip()
            if not section:
                continue
            title_match = re.match(r"^#+\s*(.+)", section)
            title = title_match.group(1) if title_match else md_file.stem
            documents.append({
                "source": md_file.name,
                "title": title,
                "content": section,
            })
    return documents


def build_index(docs_dir: Path = None, persist_dir: Path = None):
    """Build TF-IDF index and persist to disk."""
    if docs_dir is None:
        docs_dir = get_project_root() / "backend" / "rag" / "rag_docs"
    if persist_dir is None:
        persist_dir = get_project_root() / "data" / "vector_store"

    persist_dir.mkdir(parents=True, exist_ok=True)

    # Load documents
    docs = load_documents(docs_dir)
    contents = [d["content"] for d in docs]
    print(f"Loaded {len(docs)} chunks from {len(set(d['source'] for d in docs))} documents")

    # Build TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=2000,
        ngram_range=(1, 2),
        analyzer="char_wb",  # character-level ngrams work well for Chinese
    )
    tfidf_matrix = vectorizer.fit_transform(contents)
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

    # Persist
    index_data = {
        "documents": docs,
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix,
    }
    index_path = persist_dir / "rag_index.pkl"
    with open(index_path, "wb") as f:
        pickle.dump(index_data, f)

    print(f"✅ Index saved to {index_path} ({index_path.stat().st_size / 1024:.1f} KB)")
    return index_data


if __name__ == "__main__":
    build_index()
