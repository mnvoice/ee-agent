"""Unit tests for RAG layer — no model downloads or FAISS required."""
import numpy as np
import pytest

from ee_agent.rag.embedder import KoreanEmbedder
from ee_agent.rag.vector_store import FAISSVectorStore
from ee_agent.rag.retriever import GMMDynamicRetriever


# ── KoreanEmbedder ───────────────────────────────────────────────────────────

class TestKoreanEmbedder:
    def test_embed_returns_768_dim(self):
        embedder = KoreanEmbedder()
        vec = embedder.embed("옴의 법칙: V = IR")
        assert vec.shape == (768,)

    def test_embed_returns_float32(self):
        embedder = KoreanEmbedder()
        vec = embedder.embed("전류 측정")
        assert vec.dtype == np.float32

    def test_embed_is_normalized(self):
        embedder = KoreanEmbedder()
        vec = embedder.embed("변압기 권수비")
        norm = np.linalg.norm(vec)
        assert abs(norm - 1.0) < 1e-5

    def test_embed_batch_correct_shape(self):
        embedder = KoreanEmbedder()
        texts = ["옴의 법칙", "키르히호프 법칙", "패러데이 법칙"]
        result = embedder.embed_batch(texts)
        assert result.shape == (3, 768)

    def test_embed_batch_single(self):
        embedder = KoreanEmbedder()
        result = embedder.embed_batch(["단일 텍스트"])
        assert result.shape == (1, 768)

    def test_fallback_is_deterministic(self):
        embedder = KoreanEmbedder()
        v1 = embedder._fallback_embed("전기기사 시험")
        v2 = embedder._fallback_embed("전기기사 시험")
        np.testing.assert_array_equal(v1, v2)

    def test_different_texts_give_different_embeddings(self):
        embedder = KoreanEmbedder()
        v1 = embedder._fallback_embed("옴의 법칙")
        v2 = embedder._fallback_embed("변압기 권수비")
        assert not np.allclose(v1, v2)

    def test_dim_property(self):
        embedder = KoreanEmbedder()
        assert embedder.dim == 768


# ── FAISSVectorStore ─────────────────────────────────────────────────────────

class TestFAISSVectorStore:
    def _make_embedding(self, seed: int = 42) -> np.ndarray:
        rng = np.random.RandomState(seed)
        vec = rng.randn(768).astype(np.float32)
        return vec / np.linalg.norm(vec)

    def test_initial_size_is_zero(self):
        store = FAISSVectorStore(dim=768)
        assert store.size() == 0

    def test_add_increases_size(self):
        store = FAISSVectorStore(dim=768)
        store.add(self._make_embedding(1), {"name": "옴의 법칙"})
        assert store.size() == 1

    def test_add_returns_correct_id(self):
        store = FAISSVectorStore(dim=768)
        idx0 = store.add(self._make_embedding(1), {"name": "A"})
        idx1 = store.add(self._make_embedding(2), {"name": "B"})
        assert idx0 == 0
        assert idx1 == 1

    def test_search_empty_returns_empty_list(self):
        store = FAISSVectorStore(dim=768)
        query = self._make_embedding(99)
        results = store.search(query, k=5)
        assert results == []

    def test_search_returns_metadata(self):
        store = FAISSVectorStore(dim=768)
        emb = self._make_embedding(1)
        store.add(emb, {"name": "옴의 법칙", "type": "concept"})
        results = store.search(emb, k=1)
        assert len(results) == 1
        assert results[0]["metadata"]["name"] == "옴의 법칙"

    def test_search_limits_results_by_k(self):
        store = FAISSVectorStore(dim=768)
        for i in range(10):
            store.add(self._make_embedding(i), {"id": i})
        query = self._make_embedding(0)
        results = store.search(query, k=3)
        assert len(results) <= 3

    def test_search_k_capped_at_store_size(self):
        store = FAISSVectorStore(dim=768)
        store.add(self._make_embedding(1), {"id": 0})
        results = store.search(self._make_embedding(1), k=100)
        assert len(results) == 1

    def test_add_batch_increases_size(self):
        store = FAISSVectorStore(dim=768)
        embeddings = np.array([self._make_embedding(i) for i in range(5)])
        metadatas = [{"id": i} for i in range(5)]
        ids = store.add_batch(embeddings, metadatas)
        assert store.size() == 5
        assert ids == [0, 1, 2, 3, 4]

    def test_search_score_is_float(self):
        store = FAISSVectorStore(dim=768)
        emb = self._make_embedding(1)
        store.add(emb, {"name": "test"})
        results = store.search(emb, k=1)
        assert isinstance(results[0]["score"], float)

    def test_save_and_load(self, tmp_path):
        store = FAISSVectorStore(dim=768)
        emb = self._make_embedding(42)
        store.add(emb, {"name": "persistence test"})
        path = str(tmp_path / "test_store")
        store.save(path)

        store2 = FAISSVectorStore(dim=768)
        store2.load(path)
        assert store2.size() == 1
        assert store2._metadata[0]["name"] == "persistence test"


# ── GMMDynamicRetriever ──────────────────────────────────────────────────────

class TestGMMDynamicRetriever:
    def _make_retriever(self) -> tuple[GMMDynamicRetriever, KoreanEmbedder, FAISSVectorStore]:
        embedder = KoreanEmbedder()
        store = FAISSVectorStore(dim=768)
        retriever = GMMDynamicRetriever(embedder=embedder, vector_store=store)
        return retriever, embedder, store

    def test_retrieve_empty_store(self):
        retriever, _, _ = self._make_retriever()
        results = retriever.retrieve("옴의 법칙")
        assert results == []

    def test_add_concept_increases_store_size(self):
        retriever, _, store = self._make_retriever()
        retriever.add_concept("옴의 법칙", "V = IR", "전기이론")
        assert store.size() == 1

    def test_add_formula_increases_store_size(self):
        retriever, _, store = self._make_retriever()
        retriever.add_formula("옴의 법칙", "V = IR", "전압, 전류, 저항 관계")
        assert store.size() == 1

    def test_add_regulation_increases_store_size(self):
        retriever, _, store = self._make_retriever()
        retriever.add_regulation("전기설비기술기준 제3조", "접지 규정", ["접지", "안전"])
        assert store.size() == 1

    def test_retrieve_returns_results_after_add(self):
        retriever, _, _ = self._make_retriever()
        retriever.add_concept("옴의 법칙", "전압과 전류의 비례 관계", "전기이론")
        results = retriever.retrieve("저항과 전류")
        assert len(results) >= 1

    def test_retrieve_respects_min_k(self):
        retriever, _, _ = self._make_retriever()
        for i in range(10):
            retriever.add_concept(f"개념{i}", f"정의{i}", "전기이론")
        results = retriever.retrieve("전기 개념")
        assert len(results) >= GMMDynamicRetriever.MIN_K

    def test_retrieve_does_not_exceed_max_k(self):
        retriever, _, _ = self._make_retriever()
        for i in range(30):
            retriever.add_concept(f"개념{i}", f"정의 {i}", "전기이론")
        results = retriever.retrieve("전기 법칙", max_k=GMMDynamicRetriever.MAX_K)
        assert len(results) <= GMMDynamicRetriever.MAX_K

    def test_retrieve_concepts_filters_type(self):
        retriever, _, _ = self._make_retriever()
        retriever.add_concept("옴의 법칙", "V = IR", "전기이론")
        retriever.add_formula("전력공식", "P = VI", "유효전력")
        results = retriever.retrieve_concepts("전압 전류")
        for r in results:
            assert r["metadata"]["type"] == "concept"

    def test_retrieve_formulas_filters_type(self):
        retriever, _, _ = self._make_retriever()
        retriever.add_concept("옴의 법칙", "V = IR", "전기이론")
        retriever.add_formula("전력공식", "P = VI", "유효전력")
        results = retriever.retrieve_formulas("전력 계산")
        for r in results:
            assert r["metadata"]["type"] == "formula"

    def test_retrieve_regulations_filters_type(self):
        retriever, _, _ = self._make_retriever()
        retriever.add_concept("개념", "정의", "전기이론")
        retriever.add_regulation("전기설비기술기준 제3조", "접지 규정", ["접지"])
        results = retriever.retrieve_regulations("접지 규정")
        for r in results:
            assert r["metadata"]["type"] == "regulation"

    def test_gmm_select_k_respects_min_k(self):
        retriever, _, _ = self._make_retriever()
        scores = np.array([0.9, 0.85, 0.3, 0.2, 0.1, 0.05])
        k = retriever._gmm_select_k(scores)
        assert k >= GMMDynamicRetriever.MIN_K

    def test_gmm_select_k_respects_max_k(self):
        retriever, _, _ = self._make_retriever()
        scores = np.linspace(0.1, 0.9, 50)
        k = retriever._gmm_select_k(scores)
        assert k <= GMMDynamicRetriever.MAX_K
