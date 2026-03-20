"""GMM Dynamic Top-K retriever for Korean EE knowledge graph RAG."""
import logging

import numpy as np

from ee_agent.rag.embedder import KoreanEmbedder
from ee_agent.rag.vector_store import FAISSVectorStore

logger = logging.getLogger(__name__)

try:
    from sklearn.mixture import GaussianMixture

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class GMMDynamicRetriever:
    """
    GMM-based Dynamic Top-K Retriever.

    Strategy:
    1. Embed query with KR-ELECTRA
    2. Retrieve candidate pool (top CANDIDATE_POOL)
    3. Fit 2-component GMM on candidate score distribution
    4. Return only documents in the high-relevance cluster

    This prevents noisy low-relevance documents from entering agent context.
    """

    MIN_K = 3
    MAX_K = 15
    CANDIDATE_POOL = 20
    GMM_COMPONENTS = 2

    def __init__(self, embedder: KoreanEmbedder, vector_store: FAISSVectorStore):
        self.embedder = embedder
        self.store = vector_store

    def retrieve(self, query: str, max_k: int | None = None) -> list[dict]:
        """
        Retrieve relevant documents using GMM Dynamic Top-K.
        Returns list of {"metadata": dict, "score": float}.
        """
        if max_k is None:
            max_k = self.MAX_K

        if self.store.size() == 0:
            return []

        query_embedding = self.embedder.embed(query)
        pool_size = min(self.CANDIDATE_POOL, self.store.size())
        candidates = self.store.search(query_embedding, k=pool_size)

        if not candidates:
            return []

        scores = np.array([c["score"] for c in candidates])

        if SKLEARN_AVAILABLE and len(scores) >= self.GMM_COMPONENTS * 3:
            k = self._gmm_select_k(scores)
        else:
            threshold = float(scores.mean())
            k = max(self.MIN_K, int(np.sum(scores >= threshold)))

        k = min(max(k, self.MIN_K), max_k)
        return candidates[:k]

    def _gmm_select_k(self, scores: np.ndarray) -> int:
        """
        Fit 2-component GMM on score distribution.
        Returns the count of documents in the high-relevance cluster.
        """
        try:
            gmm = GaussianMixture(n_components=self.GMM_COMPONENTS, random_state=42)
            gmm.fit(scores.reshape(-1, 1))
            labels = gmm.predict(scores.reshape(-1, 1))
            means = gmm.means_.flatten()
            high_cluster = int(np.argmax(means))
            k = int(np.sum(labels == high_cluster))
            return max(self.MIN_K, min(k, self.MAX_K))
        except Exception as e:
            logger.warning(f"GMM fitting failed: {e}. Using MIN_K={self.MIN_K}.")
            return self.MIN_K

    def add_concept(self, name: str, definition: str, subject: str) -> None:
        """Add a concept to the retriever knowledge base."""
        text = f"{name}: {definition}"
        embedding = self.embedder.embed(text)
        self.store.add(
            embedding,
            {"type": "concept", "name": name, "definition": definition, "subject": subject},
        )

    def add_formula(self, name: str, latex: str, description: str) -> None:
        """Add a formula to the knowledge base."""
        text = f"{name} {description}"
        embedding = self.embedder.embed(text)
        self.store.add(
            embedding,
            {"type": "formula", "name": name, "latex": latex, "description": description},
        )

    def add_regulation(self, article: str, content: str, keywords: list[str]) -> None:
        """Add a regulation to the knowledge base."""
        text = f"{article} {content}"
        embedding = self.embedder.embed(text)
        self.store.add(
            embedding,
            {"type": "regulation", "article": article, "content": content, "keywords": keywords},
        )

    def retrieve_by_type(self, query: str, doc_type: str, k: int = 5) -> list[dict]:
        """Retrieve relevant documents filtered by type."""
        results = self.retrieve(query, max_k=k * 3)
        filtered = [r for r in results if r["metadata"].get("type") == doc_type]
        return filtered[:k]

    def retrieve_formulas(self, query: str, k: int = 5) -> list[dict]:
        return self.retrieve_by_type(query, "formula", k)

    def retrieve_concepts(self, query: str, k: int = 5) -> list[dict]:
        return self.retrieve_by_type(query, "concept", k)

    def retrieve_regulations(self, query: str, k: int = 5) -> list[dict]:
        return self.retrieve_by_type(query, "regulation", k)
