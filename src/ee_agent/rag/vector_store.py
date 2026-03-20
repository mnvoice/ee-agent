"""FAISS vector store for Korean EE knowledge retrieval."""
import logging
import pickle
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)

try:
    import faiss

    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not available. Using brute-force cosine similarity fallback.")


class FAISSVectorStore:
    """
    FAISS-based vector store for knowledge graph node embeddings.
    Stores Concept, Formula, Regulation embeddings for RAG retrieval.
    Uses Inner Product (cosine similarity with normalized vectors).
    """

    def __init__(self, dim: int = 768):
        self.dim = dim
        self._metadata: list[dict] = []
        self._embeddings: list[np.ndarray] = []  # fallback storage

        if FAISS_AVAILABLE:
            self._index = faiss.IndexFlatIP(dim)
        else:
            self._index = None

    def add(self, embedding: np.ndarray, metadata: dict) -> int:
        """Add a single vector with metadata. Returns assigned ID."""
        idx = len(self._metadata)
        self._metadata.append(metadata)
        if self._index is not None:
            vec = embedding.reshape(1, -1).astype(np.float32)
            self._index.add(vec)
        else:
            self._embeddings.append(embedding.astype(np.float32))
        return idx

    def add_batch(self, embeddings: np.ndarray, metadatas: list[dict]) -> list[int]:
        """Add multiple vectors. Returns list of assigned IDs."""
        start = len(self._metadata)
        self._metadata.extend(metadatas)
        if self._index is not None:
            self._index.add(embeddings.astype(np.float32))
        else:
            for emb in embeddings:
                self._embeddings.append(emb.astype(np.float32))
        return list(range(start, start + len(metadatas)))

    def search(self, query: np.ndarray, k: int = 5) -> list[dict]:
        """Search for k nearest neighbors. Returns list of {metadata, score}."""
        if len(self._metadata) == 0:
            return []

        k = min(k, len(self._metadata))

        if self._index is not None:
            vec = query.reshape(1, -1).astype(np.float32)
            scores, indices = self._index.search(vec, k)
            return [
                {"metadata": self._metadata[idx], "score": float(score)}
                for score, idx in zip(scores[0], indices[0])
                if 0 <= idx < len(self._metadata)
            ]

        # Brute-force cosine similarity fallback
        q = query.astype(np.float32)
        scored = []
        for i, emb in enumerate(self._embeddings):
            score = float(np.dot(q, emb))
            scored.append((score, i))
        scored.sort(reverse=True)
        return [
            {"metadata": self._metadata[i], "score": s}
            for s, i in scored[:k]
        ]

    def size(self) -> int:
        return len(self._metadata)

    def save(self, path: str) -> None:
        """Persist index and metadata to disk."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        if self._index is not None:
            faiss.write_index(self._index, str(path) + ".faiss")
        else:
            np.save(str(path) + ".npy", np.array(self._embeddings))
        with open(str(path) + ".meta.pkl", "wb") as f:
            pickle.dump(self._metadata, f)

    def load(self, path: str) -> None:
        """Load index and metadata from disk."""
        meta_path = str(path) + ".meta.pkl"
        if Path(meta_path).exists():
            with open(meta_path, "rb") as f:
                self._metadata = pickle.load(f)

        faiss_path = str(path) + ".faiss"
        if FAISS_AVAILABLE and Path(faiss_path).exists():
            self._index = faiss.read_index(faiss_path)
        else:
            npy_path = str(path) + ".npy"
            if Path(npy_path).exists():
                self._embeddings = list(np.load(npy_path))
