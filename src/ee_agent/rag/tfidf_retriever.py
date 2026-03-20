"""TF-IDF based retriever for Korean EE knowledge base.

Replaces neural embedding retriever when sentence-transformers is unavailable.
Works well for technical Korean text with specific terminology.
"""
import json
import logging
import re
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class TFIDFKnowledgeRetriever:
    """
    TF-IDF retriever for Korean EE knowledge base.

    Stores formulas, concepts, and regulations from the summary PDF.
    Retrieves by keyword similarity — effective for technical terminology.
    """

    def __init__(self):
        self._docs: list[dict] = []   # {"text": str, "metadata": dict}
        self._vectorizer: TfidfVectorizer | None = None
        self._matrix = None           # sparse TF-IDF matrix

    def _rebuild_index(self) -> None:
        """Rebuild TF-IDF index after adding documents."""
        if not self._docs:
            return
        texts = [d["text"] for d in self._docs]
        self._vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
            max_features=20000,
            sublinear_tf=True,
        )
        self._matrix = self._vectorizer.fit_transform(texts)
        logger.debug(f"TF-IDF index rebuilt: {len(self._docs)} docs, shape={self._matrix.shape}")

    def add_formula(self, name: str, latex: str, description: str) -> None:
        text = f"{name} {description} {latex}"
        self._docs.append({"text": text, "metadata": {
            "type": "formula", "name": name, "latex": latex, "description": description
        }})
        self._matrix = None  # invalidate index

    def add_concept(self, name: str, definition: str, subject: str) -> None:
        text = f"{name} {definition}"
        self._docs.append({"text": text, "metadata": {
            "type": "concept", "name": name, "definition": definition, "subject": subject
        }})
        self._matrix = None

    def add_regulation(self, article: str, content: str, keywords: list[str]) -> None:
        text = f"{article} {content} {' '.join(keywords)}"
        self._docs.append({"text": text, "metadata": {
            "type": "regulation", "article": article, "content": content, "keywords": keywords
        }})
        self._matrix = None

    def retrieve(self, query: str, max_k: int = 5) -> list[dict]:
        if not self._docs:
            return []
        if self._matrix is None:
            self._rebuild_index()
        q_vec = self._vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self._matrix).flatten()
        top_idx = scores.argsort()[::-1][:max_k]
        return [
            {"metadata": self._docs[i]["metadata"], "score": float(scores[i])}
            for i in top_idx if scores[i] > 0
        ]

    def retrieve_by_type(self, query: str, doc_type: str, k: int = 3) -> list[dict]:
        results = self.retrieve(query, max_k=k * 5)
        filtered = [r for r in results if r["metadata"].get("type") == doc_type]
        return filtered[:k]

    def retrieve_formulas(self, query: str, k: int = 3) -> list[dict]:
        return self.retrieve_by_type(query, "formula", k)

    def retrieve_concepts(self, query: str, k: int = 3) -> list[dict]:
        return self.retrieve_by_type(query, "concept", k)

    def retrieve_regulations(self, query: str, k: int = 3) -> list[dict]:
        return self.retrieve_by_type(query, "regulation", k)

    def size(self) -> int:
        return len(self._docs)

    CHUNK_SIZE = 500  # max entries per file

    def save(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        total = len(self._docs)
        if total <= self.CHUNK_SIZE:
            with open(path + ".json", "w", encoding="utf-8") as f:
                json.dump(self._docs, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {total} entries to {path}.json")
            return
        # Split into numbered chunks
        chunks = [self._docs[i:i + self.CHUNK_SIZE] for i in range(0, total, self.CHUNK_SIZE)]
        for idx, chunk in enumerate(chunks, start=1):
            chunk_path = f"{path}_{idx}.json"
            with open(chunk_path, "w", encoding="utf-8") as f:
                json.dump(chunk, f, ensure_ascii=False, indent=2)
        # Remove old single file if exists
        single = Path(path + ".json")
        if single.exists():
            single.unlink()
        logger.info(f"Saved {total} entries across {len(chunks)} files ({path}_1.json ~ {path}_{len(chunks)}.json)")

    def load(self, path: str) -> None:
        # Try chunked files first (knowledge_store_1.json, _2.json, ...)
        chunk_files = sorted(Path(path).parent.glob(Path(path).name + "_[0-9]*.json"))
        if chunk_files:
            self._docs = []
            for cf in chunk_files:
                with open(cf, encoding="utf-8") as f:
                    self._docs.extend(json.load(f))
            self._matrix = None
            logger.info(f"Loaded {len(self._docs)} entries from {len(chunk_files)} chunk files")
            return
        # Fallback: single file
        json_path = path + ".json"
        if not Path(json_path).exists():
            logger.warning(f"Knowledge base not found: {json_path}")
            return
        with open(json_path, encoding="utf-8") as f:
            self._docs = json.load(f)
        self._matrix = None
        logger.info(f"Loaded {len(self._docs)} entries from {json_path}")
